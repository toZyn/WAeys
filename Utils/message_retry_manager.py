"""Port of src/Utils/message-retry-manager.ts — retry receipt handling."""

from __future__ import annotations

import enum
import time

from .lru_cache import LRUCache

# Number of sent messages to cache in memory for handling retry receipts
RECENT_MESSAGES_SIZE = 512

MESSAGE_KEY_SEPARATOR = '\u0000'

# Timeout for session recreation - 1 hour
RECREATE_SESSION_TIMEOUT = 60 * 60 * 1000  # 1 hour in milliseconds
PHONE_REQUEST_DELAY = 3000


class RetryReason(enum.IntEnum):
    UnknownError = 0
    SignalErrorNoSession = 1
    SignalErrorInvalidKey = 2
    SignalErrorInvalidKeyId = 3
    # MAC verification failed - most common cause of decryption failures
    SignalErrorInvalidMessage = 4
    SignalErrorInvalidSignature = 5
    SignalErrorFutureMessage = 6
    # Explicit MAC failure - session is definitely out of sync
    SignalErrorBadMac = 7
    SignalErrorInvalidSession = 8
    SignalErrorInvalidMsgKey = 9
    BadBroadcastEphemeralSetting = 10
    UnknownCompanionNoPrekey = 11
    AdvFailure = 12
    StatusRevokeDelay = 13


# Error codes that indicate a MAC failure and require immediate session recreation
MAC_ERROR_CODES = {RetryReason.SignalErrorInvalidMessage, RetryReason.SignalErrorBadMac}


class MessageRetryManager:
    def __init__(self, logger, max_msg_retry_count: int):
        self.logger = logger
        self.max_msg_retry_count = max_msg_retry_count
        self.message_key_index = {}
        self.pending_phone_requests = {}
        self.statistics = {
            'totalRetries': 0,
            'successfulRetries': 0,
            'failedRetries': 0,
            'mediaRetries': 0,
            'sessionRecreations': 0,
            'phoneRequests': 0,
        }

        def on_dispose(_value, key):
            separator_index = key.rfind(MESSAGE_KEY_SEPARATOR)
            if separator_index > -1:
                message_id = key[separator_index + len(MESSAGE_KEY_SEPARATOR):]
                self.message_key_index.pop(message_id, None)

        self.recent_messages_map = LRUCache(
            ttl=5 * 60 * 1000,
            ttl_autopurge=True,
            max=RECENT_MESSAGES_SIZE,
            dispose=on_dispose,
        )
        self.session_recreate_history = LRUCache(
            ttl=RECREATE_SESSION_TIMEOUT * 2,
            ttl_autopurge=True,
        )
        self.retry_counters = LRUCache(
            ttl=15 * 60 * 1000,
            ttl_autopurge=True,
            update_age_on_get=True,
        )
        self.base_keys = LRUCache(
            ttl=15 * 60 * 1000,
            ttl_autopurge=True,
            max=1024,
        )

    def add_recent_message(self, to: str, id: str, message) -> None:
        key_str = self._key_to_string({'to': to, 'id': id})

        self.recent_messages_map.set(key_str, {'message': message, 'timestamp': int(time.time() * 1000)})
        self.message_key_index[id] = key_str

        self.logger.debug(f'Added message to retry cache: {to}/{id}')

    def get_recent_message(self, to: str, id: str):
        key_str = self._key_to_string({'to': to, 'id': id})
        return self.recent_messages_map.get(key_str)

    def should_recreate_session(self, jid: str, has_session: bool, error_code=None) -> dict:
        # If we don't have a session, always recreate
        if not has_session:
            self.session_recreate_history.set(jid, int(time.time() * 1000))
            self.statistics['sessionRecreations'] += 1
            return {'reason': "we don't have a Signal session with them", 'recreate': True}

        # IMMEDIATE recreation for MAC errors - session is definitely out of sync
        if error_code is not None and error_code in MAC_ERROR_CODES:
            self.session_recreate_history.set(jid, int(time.time() * 1000))
            self.statistics['sessionRecreations'] += 1
            self.logger.warn(
                {'jid': jid, 'errorCode': RetryReason(error_code).name},
                'MAC error detected, forcing immediate session recreation',
            )
            return {
                'reason': f'MAC error (code {error_code}: {RetryReason(error_code).name}), immediate session recreation',
                'recreate': True,
            }

        now = int(time.time() * 1000)
        prev_time = self.session_recreate_history.get(jid)

        # If no previous recreation or it's been more than an hour
        if not prev_time or now - prev_time > RECREATE_SESSION_TIMEOUT:
            self.session_recreate_history.set(jid, now)
            self.statistics['sessionRecreations'] += 1
            return {'reason': 'retry count > 1 and over an hour since last recreation', 'recreate': True}

        return {'reason': '', 'recreate': False}

    def parse_retry_error_code(self, error_attr):
        if error_attr is None or error_attr == '':
            return None

        try:
            code = int(error_attr, 10)
        except ValueError:
            return None

        # Validate it's a known RetryReason
        if RetryReason.UnknownError <= code <= RetryReason.StatusRevokeDelay:
            return code

        return RetryReason.UnknownError

    def is_mac_error(self, error_code) -> bool:
        return error_code is not None and error_code in MAC_ERROR_CODES

    def increment_retry_count(self, message_id: str) -> int:
        self.retry_counters.set(message_id, (self.retry_counters.get(message_id) or 0) + 1)
        self.statistics['totalRetries'] += 1
        return self.retry_counters.get(message_id) or 0

    def get_retry_count(self, message_id: str) -> int:
        return self.retry_counters.get(message_id) or 0

    def has_exceeded_max_retries(self, message_id: str) -> bool:
        return self.get_retry_count(message_id) >= self.max_msg_retry_count

    def mark_retry_success(self, message_id: str) -> None:
        self.statistics['successfulRetries'] += 1
        self.retry_counters.delete(message_id)
        self.cancel_pending_phone_request(message_id)
        self._remove_recent_message(message_id)

    def mark_retry_failed(self, message_id: str) -> None:
        self.statistics['failedRetries'] += 1
        self.retry_counters.delete(message_id)
        self.cancel_pending_phone_request(message_id)
        self._remove_recent_message(message_id)

    def schedule_phone_request(self, message_id: str, callback, delay: int = PHONE_REQUEST_DELAY):
        # Cancel any existing request for this message
        self.cancel_pending_phone_request(message_id)

        import asyncio

        handle = asyncio.get_event_loop().call_later(delay / 1000.0, lambda: self._run_phone_request(message_id, callback))

        self.pending_phone_requests[message_id] = handle
        self.logger.debug(f'Scheduled phone request for message {message_id} with {delay}ms delay')

    def _run_phone_request(self, message_id: str, callback):
        self.pending_phone_requests.pop(message_id, None)
        self.statistics['phoneRequests'] += 1
        callback()

    def cancel_pending_phone_request(self, message_id: str) -> None:
        handle = self.pending_phone_requests.pop(message_id, None)
        if handle is not None:
            handle.cancel()
            self.logger.debug(f'Cancelled pending phone request for message {message_id}')

    def clear(self) -> None:
        self.recent_messages_map.clear()
        self.message_key_index.clear()
        self.session_recreate_history.clear()
        self.retry_counters.clear()
        self.base_keys.clear()
        for message_id in list(self.pending_phone_requests.keys()):
            self.cancel_pending_phone_request(message_id)

        self.statistics = {
            'totalRetries': 0,
            'successfulRetries': 0,
            'failedRetries': 0,
            'mediaRetries': 0,
            'sessionRecreations': 0,
            'phoneRequests': 0,
        }

    def save_base_key(self, addr: str, msg_id: str, base_key: bytes) -> None:
        self.base_keys.set(f'{addr}:{msg_id}', base_key)

    def has_same_base_key(self, addr: str, msg_id: str, base_key: bytes) -> bool:
        stored = self.base_keys.get(f'{addr}:{msg_id}')
        if not stored or len(stored) != len(base_key):
            return False

        for i in range(len(stored)):
            if stored[i] != base_key[i]:
                return False

        return True

    def delete_base_key(self, addr: str, msg_id: str) -> None:
        self.base_keys.delete(f'{addr}:{msg_id}')

    def _key_to_string(self, key: dict) -> str:
        return f'{key["to"]}{MESSAGE_KEY_SEPARATOR}{key["id"]}'

    def _remove_recent_message(self, message_id: str) -> None:
        key_str = self.message_key_index.get(message_id)
        if not key_str:
            return

        self.recent_messages_map.delete(key_str)
        self.message_key_index.pop(message_id, None)
