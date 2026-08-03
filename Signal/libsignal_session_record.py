"""Port of libsignal's SessionRecord / SessionEntry (src/session_record.js).

The serialized form is a dict of base64 strings + numbers, matching what
Baileys stores in the 'session' SignalKeyStore bucket.
"""

from __future__ import annotations

import base64
import logging
import time
from typing import Optional

from .libsignal_constants import BaseKeyType

logger = logging.getLogger(__name__)

CLOSED_SESSIONS_MAX = 40
SESSION_RECORD_VERSION = 'v1'


def _b64(data: bytes) -> str:
    return base64.b64encode(bytes(data)).decode('ascii')


def _unb64(s: str) -> bytes:
    return base64.b64decode(s.encode('ascii'))


class SessionEntry:
    def __init__(self):
        self._chains = {}
        self.registrationId = None
        self.currentRatchet = None
        self.indexInfo = None
        self.pendingPreKey = None

    def __str__(self) -> str:
        base_key = None
        if self.indexInfo and self.indexInfo.get('baseKey'):
            base_key = _b64(self.indexInfo['baseKey'])
        return f'<SessionEntry [baseKey={base_key}]>'

    def add_chain(self, key: bytes, value: dict) -> None:
        if not isinstance(key, bytes):
            raise TypeError('Buffer required')
        chain_id = _b64(key)
        if chain_id in self._chains:
            raise ValueError('Overwrite attempt')
        self._chains[chain_id] = value

    def get_chain(self, key: bytes):
        if not isinstance(key, bytes):
            raise TypeError('Buffer required')
        return self._chains.get(_b64(key))

    def delete_chain(self, key: bytes) -> None:
        if not isinstance(key, bytes):
            raise TypeError('Buffer required')
        chain_id = _b64(key)
        if chain_id not in self._chains:
            raise KeyError('Not Found')
        del self._chains[chain_id]

    def chains(self):
        for chain_id, value in self._chains.items():
            yield _unb64(chain_id), value

    def serialize(self) -> dict:
        data = {
            'registrationId': self.registrationId,
            'currentRatchet': {
                'ephemeralKeyPair': {
                    'pubKey': _b64(self.currentRatchet['ephemeralKeyPair']['pubKey']),
                    'privKey': _b64(self.currentRatchet['ephemeralKeyPair']['privKey']),
                },
                'lastRemoteEphemeralKey': _b64(self.currentRatchet['lastRemoteEphemeralKey']),
                'previousCounter': self.currentRatchet['previousCounter'],
                'rootKey': _b64(self.currentRatchet['rootKey']),
            },
            'indexInfo': {
                'baseKey': _b64(self.indexInfo['baseKey']),
                'baseKeyType': self.indexInfo['baseKeyType'],
                'closed': self.indexInfo['closed'],
                'used': self.indexInfo['used'],
                'created': self.indexInfo['created'],
                'remoteIdentityKey': _b64(self.indexInfo['remoteIdentityKey']),
            },
            '_chains': self._serialize_chains(self._chains),
        }
        if self.pendingPreKey:
            pending = dict(self.pendingPreKey)
            pending['baseKey'] = _b64(self.pendingPreKey['baseKey'])
            data['pendingPreKey'] = pending
        return data

    @staticmethod
    def deserialize(data: dict) -> 'SessionEntry':
        obj = SessionEntry()
        obj.registrationId = data['registrationId']
        obj.currentRatchet = {
            'ephemeralKeyPair': {
                'pubKey': _unb64(data['currentRatchet']['ephemeralKeyPair']['pubKey']),
                'privKey': _unb64(data['currentRatchet']['ephemeralKeyPair']['privKey']),
            },
            'lastRemoteEphemeralKey': _unb64(data['currentRatchet']['lastRemoteEphemeralKey']),
            'previousCounter': data['currentRatchet']['previousCounter'],
            'rootKey': _unb64(data['currentRatchet']['rootKey']),
        }
        obj.indexInfo = {
            'baseKey': _unb64(data['indexInfo']['baseKey']),
            'baseKeyType': data['indexInfo']['baseKeyType'],
            'closed': data['indexInfo']['closed'],
            'used': data['indexInfo']['used'],
            'created': data['indexInfo']['created'],
            'remoteIdentityKey': _unb64(data['indexInfo']['remoteIdentityKey']),
        }
        obj._chains = SessionEntry._deserialize_chains(data['_chains'])
        if data.get('pendingPreKey'):
            pending = dict(data['pendingPreKey'])
            pending['baseKey'] = _unb64(data['pendingPreKey']['baseKey'])
            obj.pendingPreKey = pending
        return obj

    @staticmethod
    def _serialize_chains(chains: dict) -> dict:
        result = {}
        for chain_id, chain in chains.items():
            message_keys = {}
            for idx, key in chain['messageKeys'].items():
                message_keys[str(idx)] = _b64(key)
            chain_key = chain['chainKey']
            result[chain_id] = {
                'chainKey': {
                    'counter': chain_key['counter'],
                    'key': _b64(chain_key['key']) if chain_key.get('key') else None,
                },
                'chainType': chain['chainType'],
                'messageKeys': message_keys,
            }
        return result

    @staticmethod
    def _deserialize_chains(chains_data: dict) -> dict:
        result = {}
        for chain_id, chain in chains_data.items():
            message_keys = {}
            for idx, key in chain['messageKeys'].items():
                message_keys[int(idx)] = _unb64(key)
            chain_key = chain['chainKey']
            result[chain_id] = {
                'chainKey': {
                    'counter': chain_key['counter'],
                    'key': _unb64(chain_key['key']) if chain_key.get('key') else None,
                },
                'chainType': chain['chainType'],
                'messageKeys': message_keys,
            }
        return result


class SessionRecord:
    def __init__(self):
        self.sessions = {}
        self.version = SESSION_RECORD_VERSION

    @staticmethod
    def create_entry() -> SessionEntry:
        return SessionEntry()

    @staticmethod
    def migrate(data: dict) -> None:
        sessions = data['_sessions']
        registration_id = data.get('registrationId')
        if registration_id is not None:
            for key in sessions:
                if 'registrationId' not in sessions[key] or sessions[key]['registrationId'] is None:
                    sessions[key]['registrationId'] = registration_id
        else:
            for key in sessions:
                if sessions[key]['indexInfo']['closed'] == -1:
                    logger.error(
                        'V1 session storage migration error: registrationId %s for open session version %s',
                        registration_id, data.get('version'))

    @staticmethod
    def deserialize(data) -> 'SessionRecord':
        if data.get('version') != SESSION_RECORD_VERSION:
            SessionRecord.migrate(data)
        obj = SessionRecord()
        for key, entry in (data.get('_sessions') or {}).items():
            obj.sessions[key] = SessionEntry.deserialize(entry)
        return obj

    def serialize(self) -> dict:
        sessions = {}
        for key, entry in self.sessions.items():
            sessions[key] = entry.serialize()
        return {
            '_sessions': sessions,
            'version': self.version,
        }

    def have_open_session(self) -> bool:
        open_session = self.get_open_session()
        return bool(open_session and isinstance(open_session.registrationId, int))

    def get_session(self, key: bytes) -> Optional[SessionEntry]:
        if not isinstance(key, bytes):
            raise TypeError('Buffer required')
        session = self.sessions.get(_b64(key))
        if session and session.indexInfo['baseKeyType'] == BaseKeyType.OURS:
            raise ValueError('Tried to lookup a session using our basekey')
        return session

    def get_open_session(self) -> Optional[SessionEntry]:
        for session in self.sessions.values():
            if not self.is_closed(session):
                return session
        return None

    def set_session(self, session: SessionEntry) -> None:
        self.sessions[_b64(session.indexInfo['baseKey'])] = session

    def get_sessions(self):
        return sorted(
            self.sessions.values(),
            key=lambda s: s.indexInfo.get('used') or 0,
            reverse=True,
        )

    def close_session(self, session: SessionEntry) -> None:
        if self.is_closed(session):
            logger.warning('Session already closed: %s', session)
            return
        logger.info('Closing session: %s', session)
        session.indexInfo['closed'] = int(time.time() * 1000)

    def open_session(self, session: SessionEntry) -> None:
        if not self.is_closed(session):
            logger.warning('Session already open')
        logger.info('Opening session: %s', session)
        session.indexInfo['closed'] = -1

    def is_closed(self, session: SessionEntry) -> bool:
        return session.indexInfo['closed'] != -1

    def remove_old_sessions(self) -> None:
        while len(self.sessions) > CLOSED_SESSIONS_MAX:
            oldest_key = None
            oldest_session = None
            for key, session in self.sessions.items():
                if session.indexInfo['closed'] != -1 and (
                    oldest_session is None
                    or session.indexInfo['closed'] < oldest_session.indexInfo['closed']
                ):
                    oldest_key = key
                    oldest_session = session
            if oldest_key:
                logger.info('Removing old closed session: %s', oldest_session)
                del self.sessions[oldest_key]
            else:
                raise ValueError('Corrupt sessions object')

    def delete_all_sessions(self) -> None:
        self.sessions.clear()
