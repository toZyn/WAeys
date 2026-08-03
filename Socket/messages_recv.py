"""Port of src/Socket/messages-recv.ts — inbound message/socket event handling.

Composes on top of ``make_messages_socket`` and wires the ``CB:message``,
``CB:call``, ``CB:receipt`` and ``CB:notification`` stanza handlers plus the
``call``/``connection.update`` event listeners.
"""

from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime, timezone

from ..Defaults.index import (
    DEFAULT_CACHE_TTLS,
    KEY_BUNDLE_TYPE,
    MIN_PREKEY_COUNT,
    PLACEHOLDER_MAX_AGE_SECONDS,
    STATUS_EXPIRY_SECONDS,
)
from ..Types.Message import MessageReceiptType, WAMessageStatus, WAMessageStubType
from ..Types.State import ReachoutTimelockEnforcementType
from ..Utils.crypto import (
    Curve,
    aes_decrypt_ctr,
    aes_encrypt_gcm,
    derive_pairing_code_key,
    hkdf,
)
from ..Utils.decode_wa_message import (
    ACCOUNT_RESTRICTED_TEXT,
    MISSING_KEYS_ERROR_TEXT,
    NACK_REASONS,
    NO_MESSAGE_FOUND_ERROR_TEXT,
    SERVER_ERROR_CODES,
    decode_message_node,
    decrypt_message_node,
    extract_addressing_context,
)
from ..Utils.generics import (
    Boom,
    delay,
    encode_big_endian,
    get_call_status_from_node,
    get_status_from_receipt_type,
    to_number,
    unix_timestamp_seconds,
)
from ..Utils.history import get_history_msg
from ..Utils.identity_change_handler import handle_identity_change
from ..Utils.lru_cache import LRUCache
from ..Utils.make_mutex import make_mutex
from ..Utils.messages_media import decode_media_retry_node
from ..Utils.offline_node_processor import make_offline_node_processor
from ..Utils.process_message import clean_message
from ..Utils.signal import (
    extract_e2e_session_from_retry_receipt,
    get_next_pre_keys,
    xmpp_pre_key,
    xmpp_signed_pre_key,
)
from ..Utils.validate_connection import encode_signed_device_identity
from ..Utils.stanza_ack import build_ack_stanza
from ..Utils.tc_token_utils import (
    TC_TOKEN_INDEX_KEY,
    build_merged_tc_token_index_write,
    is_tc_token_expired,
    read_tc_token_index,
    resolve_issuance_jid,
    resolve_tc_token_jid,
    store_tc_tokens_from_iq_result,
)
from ..WABinary.generic_utils import (
    binary_node_to_string,
    get_all_binary_node_children,
    get_binary_node_child,
    get_binary_node_child_buffer,
    get_binary_node_child_string,
    get_binary_node_child_uint,
    get_binary_node_children,
)
from ..WABinary.jid_utils import (
    S_WHATSAPP_NET,
    are_jids_same_user,
    is_jid_group,
    is_jid_newsletter,
    is_jid_status_broadcast,
    is_lid_user,
    is_pn_user,
    jid_decode,
    jid_encode,
    jid_normalized_user,
)
from ..WABinary.types import BinaryNode
from ..WAProto import WAProto as proto
from .messages_send import make_messages_socket

ENFORCEMENT_TYPE_VALUES = {e.value for e in ReachoutTimelockEnforcementType}


def extract_group_metadata(result: BinaryNode) -> dict:
    """Port of src/Socket/groups.ts extractGroupMetadata."""
    from ..WABinary.generic_utils import get_binary_node_child, get_binary_node_children, get_binary_node_child_string

    group = get_binary_node_child(result, 'group')
    if not group:
        error_node = get_binary_node_child(result, 'error')
        if error_node:
            code = int((error_node.attrs or {}).get('code') or 500)
            text = (error_node.attrs or {}).get('text') or 'group metadata query failed'
            raise Boom(text, status_code=code, data=error_node)

        raise Boom('Invalid group metadata response: missing <group> node', data=result)

    if not (group.attrs or {}).get('id'):
        raise Boom('Invalid group metadata response: missing group id', data=group)

    desc_child = get_binary_node_child(group, 'description')
    desc = None
    desc_id = None
    desc_owner = None
    desc_owner_pn = None
    desc_owner_username = None
    desc_time = None
    if desc_child:
        desc = get_binary_node_child_string(desc_child, 'body')
        desc_owner = jid_normalized_user((desc_child.attrs or {}).get('participant')) if (desc_child.attrs or {}).get('participant') else None
        desc_owner_pn = jid_normalized_user((desc_child.attrs or {}).get('participant_pn')) if (desc_child.attrs or {}).get('participant_pn') else None
        desc_owner_username = (desc_child.attrs or {}).get('participant_username') or None
        desc_time = _safe_int((desc_child.attrs or {}).get('t'))
        desc_id = (desc_child.attrs or {}).get('id')

    group_id = (group.attrs or {}).get('id')
    if '@' not in group_id:
        group_id = jid_encode(group_id, 'g.us')
    eph = get_binary_node_child(group, 'ephemeral')
    eph = (eph.attrs or {}).get('expiration') if eph else None
    member_add_mode = get_binary_node_child_string(group, 'member_add_mode') == 'all_member_add'

    def _safe_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    metadata = {
        'id': group_id,
        'notify': (group.attrs or {}).get('notify'),
        'addressingMode': 'lid' if (group.attrs or {}).get('addressing_mode') == 'lid' else 'pn',
        'subject': (group.attrs or {}).get('subject'),
        'subjectOwner': (group.attrs or {}).get('s_o'),
        'subjectOwnerPn': (group.attrs or {}).get('s_o_pn'),
        'subjectOwnerUsername': (group.attrs or {}).get('s_o_username'),
        'subjectTime': _safe_int((group.attrs or {}).get('s_t')),
        'size': _safe_int((group.attrs or {}).get('size')) if (group.attrs or {}).get('size') else len(get_binary_node_children(group, 'participant')),
        'creation': _safe_int((group.attrs or {}).get('creation')),
        'owner': jid_normalized_user((group.attrs or {}).get('creator')) if (group.attrs or {}).get('creator') else None,
        'ownerPn': jid_normalized_user((group.attrs or {}).get('creator_pn')) if (group.attrs or {}).get('creator_pn') else None,
        'ownerUsername': (group.attrs or {}).get('creator_username') or None,
        'owner_country_code': (group.attrs or {}).get('creator_country_code'),
        'desc': desc,
        'descId': desc_id,
        'descOwner': desc_owner,
        'descOwnerPn': desc_owner_pn,
        'descOwnerUsername': desc_owner_username,
        'descTime': desc_time,
        'linkedParent': (get_binary_node_child(group, 'linked_parent').attrs or {}).get('jid') if get_binary_node_child(group, 'linked_parent') else None,
        'restrict': bool(get_binary_node_child(group, 'locked')),
        'announce': bool(get_binary_node_child(group, 'announcement')),
        'isCommunity': bool(get_binary_node_child(group, 'parent')),
        'isCommunityAnnounce': bool(get_binary_node_child(group, 'default_sub_group')),
        'joinApprovalMode': bool(get_binary_node_child(group, 'membership_approval_mode')),
        'memberAddMode': member_add_mode,
        'participants': [],
        'ephemeralDuration': int(eph) if eph is not None else None,
    }

    participants = []
    for participant in get_binary_node_children(group, 'participant'):
        attrs = participant.attrs or {}
        participants.append({
            'id': attrs.get('jid'),
            'phoneNumber': attrs.get('phone_number') if (is_lid_user(attrs.get('jid')) and is_pn_user(attrs.get('phone_number'))) else None,
            'lid': attrs.get('lid') if (is_pn_user(attrs.get('jid')) and is_lid_user(attrs.get('lid'))) else None,
            'username': attrs.get('participant_username') or attrs.get('username') or None,
            'admin': attrs.get('type') or None,
        })
    metadata['participants'] = participants

    return metadata


async def _noop():
    return None


def _is_valid_enforcement_type(value):
    return isinstance(value, str) and value in ENFORCEMENT_TYPE_VALUES


def make_messages_recv_socket(sock: dict, config: dict) -> dict:
    logger = config.get('logger')
    retry_request_delay_ms = config.get('retryRequestDelayMs')
    max_msg_retry_count = config.get('maxMsgRetryCount')
    get_message = config.get('getMessage')
    should_ignore_jid = config.get('shouldIgnoreJid') or (lambda jid: False)
    enable_auto_session_recreation = config.get('enableAutoSessionRecreation')

    messages_sock = make_messages_socket(sock, config)
    user_devices_cache = messages_sock['userDevicesCache']
    devices_mutex = messages_sock['devicesMutex']
    ev = messages_sock['ev']
    auth_state = messages_sock['authState']
    ws = messages_sock['ws']
    message_mutex = messages_sock['messageMutex']
    notification_mutex = messages_sock.get('notificationMutex') or make_mutex()
    receipt_mutex = messages_sock.get('receiptMutex') or make_mutex()
    signal_repository = messages_sock['signalRepository']
    query = messages_sock['query']
    upsert_message = messages_sock['upsertMessage']
    resync_app_state = messages_sock.get('resyncAppState') or (lambda names, _force: asyncio.ensure_future(_noop()))
    on_unexpected_error = messages_sock.get('onUnexpectedError') or (lambda err, identifier: None)
    assert_sessions = messages_sock['assertSessions']
    send_node = messages_sock['sendNode']
    relay_message = messages_sock['relayMessage']
    send_receipt = messages_sock['sendReceipt']
    upload_pre_keys = messages_sock.get('uploadPreKeys') or (lambda: None)
    send_peer_data_operation_message = messages_sock['sendPeerDataOperationMessage']
    message_retry_manager = messages_sock['messageRetryManager']
    register_socket_end_handler = messages_sock['registerSocketEndHandler']
    issue_privacy_tokens = messages_sock['issuePrivacyTokens']
    fetch_account_reachout_timelock = messages_sock.get('fetchAccountReachoutTimelock') or (lambda: asyncio.ensure_future(_noop()))
    placeholder_resend_cache = messages_sock.get('placeholderResendCache') or LRUCache(ttl=2 * 60 * 60 * 1000)

    try:
        get_lid_for_pn = signal_repository['lidMapping'].get_lid_for_pn
    except (KeyError, TypeError):
        get_lid_for_pn = None

    # this mutex ensures that each retryRequest will wait for the previous one to finish
    retry_mutex = make_mutex()

    msg_retry_cache = config.get('msgRetryCounterCache') or LRUCache(
        ttl=DEFAULT_CACHE_TTLS['MSG_RETRY'] * 1000
    )
    call_offer_cache = config.get('callOfferCache') or LRUCache(ttl=DEFAULT_CACHE_TTLS['CALL_OFFER'] * 1000)

    # Debounce identity-change session refreshes per JID to avoid bursts
    identity_assert_debounce = LRUCache(ttl=5000)

    send_active_receipts = False

    async def fetch_message_history(count, oldest_msg_key, oldest_msg_timestamp):
        if not (auth_state['creds'].get('me') or {}).get('id'):
            raise Boom('Not authenticated')

        pdo_message = {
            'historySyncOnDemandRequest': {
                'chatJid': oldest_msg_key.get('remoteJid'),
                'oldestMsgFromMe': oldest_msg_key.get('fromMe'),
                'oldestMsgId': oldest_msg_key.get('id'),
                'oldestMsgTimestampMs': oldest_msg_timestamp,
                'onDemandMsgCount': count,
            },
            'peerDataOperationRequestType': proto.Message.PeerDataOperationRequestType.HISTORY_SYNC_ON_DEMAND,
        }

        return await send_peer_data_operation_message(pdo_message)

    async def request_placeholder_resend(message_key, msg_data=None):
        if not (auth_state['creds'].get('me') or {}).get('id'):
            raise Boom('Not authenticated')

        if placeholder_resend_cache.get(message_key.get('id')):
            if logger is not None:
                logger.debug({'messageKey': message_key}, 'already requested resend')
            return None
        else:
            placeholder_resend_cache.set(message_key['id'], msg_data or True)

        await delay(2000)

        if not placeholder_resend_cache.get(message_key.get('id')):
            if logger is not None:
                logger.debug({'messageKey': message_key}, 'message received while resend requested')
            return 'RESOLVED'

        pdo_message = {
            'placeholderMessageResendRequest': [{'messageKey': message_key}],
            'peerDataOperationRequestType': proto.Message.PeerDataOperationRequestType.PLACEHOLDER_MESSAGE_RESEND,
        }

        async def _timeout_cleanup():
            await asyncio.sleep(8)
            if placeholder_resend_cache.get(message_key.get('id')):
                if logger is not None:
                    logger.debug({'messageKey': message_key}, 'PDO message without response after 8 seconds. Phone possibly offline')
                placeholder_resend_cache.delete(message_key.get('id'))

        asyncio.ensure_future(_timeout_cleanup())

        return await send_peer_data_operation_message(pdo_message)

    async def handle_mex_notification(node):
        update_node = get_binary_node_child(node, 'update')

        if update_node:
            op_name = (update_node.attrs or {}).get('op_name')
            if not op_name:
                if logger is not None:
                    logger.warn({'node': binary_node_to_string(node)}, 'mex notification missing op_name, fallback to legacy')
                await handle_legacy_mex_newsletter_notification(node)
                return

            mex_response = None
            try:
                mex_response = json.loads(bytes(update_node.content).decode('utf-8'))
            except Exception as error:
                if logger is not None:
                    logger.error({'err': error, 'opName': op_name}, 'failed to parse mex notification JSON')
                return

            if mex_response.get('errors'):
                if logger is not None:
                    logger.warn({'errors': mex_response['errors'], 'opName': op_name}, 'mex notification has GQL errors')
                return

            data = mex_response.get('data')
            if not data:
                if logger is not None:
                    logger.warn({'opName': op_name}, 'mex notification has null data')
                return

            if logger is not None:
                logger.debug({'opName': op_name}, 'processing mex notification')

            switch = {
                'NotificationUserReachoutTimelockUpdate': lambda: handle_reachout_timelock_notification(data),
                'MessageCappingInfoNotification': lambda: handle_message_capping_notification(data),
            }
            if op_name in switch:
                switch[op_name]()
            else:
                await handle_legacy_mex_newsletter_notification(node)
            return

        await handle_legacy_mex_newsletter_notification(node)

    def handle_reachout_timelock_notification(data):
        payload = data.get('xwa2_notify_account_reachout_timelock')
        if payload is None:
            if logger is not None:
                logger.warn('reachout timelock notification missing payload')
            return

        if not payload.get('is_active'):
            if logger is not None:
                logger.info('reachout timelock restriction lifted')
            ev.emit('connection.update', {
                'reachoutTimeLock': {
                    'isActive': False,
                    'enforcementType': ReachoutTimelockEnforcementType.DEFAULT.value,
                }
            })
            return

        time_enforcement_ends_ts = payload.get('time_enforcement_ends')
        if time_enforcement_ends_ts:
            time_enforcement_ends = datetime.fromtimestamp(int(time_enforcement_ends_ts), tz=timezone.utc)
        else:
            time_enforcement_ends = datetime.now(timezone.utc).timestamp() + 60

        enforcement_type = (
            payload.get('enforcement_type')
            if _is_valid_enforcement_type(payload.get('enforcement_type'))
            else ReachoutTimelockEnforcementType.DEFAULT.value
        )

        if logger is not None:
            logger.info({'enforcementType': enforcement_type, 'timeEnforcementEnds': time_enforcement_ends}, 'reachout timelock restriction set')

        ev.emit('connection.update', {
            'reachoutTimeLock': {
                'isActive': True,
                'timeEnforcementEnds': time_enforcement_ends,
                'enforcementType': enforcement_type,
            }
        })

    def handle_message_capping_notification(data):
        payload = data.get('xwa2_notify_new_chat_messages_capping_info_update')
        if payload is None:
            if logger is not None:
                logger.warn('message capping notification missing payload')
            return

        if logger is not None:
            logger.info({'payload': payload}, 'received message capping update')
        ev.emit('message-capping.update', payload)

    async def handle_legacy_mex_newsletter_notification(node):
        mex_node = get_binary_node_child(node, 'mex')
        update_node = None
        if not (mex_node and mex_node.content):
            update_node = get_binary_node_child(node, 'update') or (get_all_binary_node_children(node)[0] if get_all_binary_node_children(node) else None)
        payload_node = mex_node if (mex_node and mex_node.content) else update_node
        if payload_node is None or payload_node.content is None:
            if logger is not None:
                logger.warn({'node': binary_node_to_string(node)}, 'invalid mex newsletter notification')
            return

        data = None
        try:
            payload_content = payload_node.content
            if isinstance(payload_content, list):
                if logger is not None:
                    logger.warn({'payloadNode': payload_node}, 'invalid mex newsletter notification payload format')
                return
            content_buf = payload_content.encode('latin-1') if isinstance(payload_content, str) else bytes(payload_content)
            data = json.loads(content_buf.decode('utf-8'))
        except Exception as error:
            if logger is not None:
                logger.error({'err': error, 'node': binary_node_to_string(node)}, 'failed to parse mex newsletter notification')
            return

        operation = (data or {}).get('operation') or (payload_node.attrs or {}).get('op_name')
        updates = (data or {}).get('updates')
        if not updates:
            linked_profiles = ((data or {}).get('data') or {}).get('xwa2_notify_linked_profiles')
            if linked_profiles:
                updates = [linked_profiles]

        if not updates or not operation:
            if logger is not None:
                logger.warn({'data': data}, 'invalid mex newsletter notification content')
            return

        if logger is not None:
            logger.info({'operation': operation, 'updates': updates}, 'got mex newsletter notification')

        if operation == 'NotificationNewsletterUpdate':
            for update in updates:
                if update.get('jid') and update.get('settings') and len(update.get('settings', {})) > 0:
                    ev.emit('newsletter-settings.update', {
                        'id': update['jid'],
                        'update': update['settings'],
                    })
        elif operation == 'NotificationNewsletterAdminPromote':
            for update in updates:
                if update.get('jid') and update.get('user'):
                    ev.emit('newsletter-participants.update', {
                        'id': update['jid'],
                        'author': (node.attrs or {}).get('from'),
                        'user': update['user'],
                        'new_role': 'ADMIN',
                        'action': 'promote',
                    })
        elif operation == 'NotificationLinkedProfilesUpdates':
            mappings = []
            for update in updates:
                lid = update.get('jid')
                added_profiles = update.get('added_profiles') if isinstance(update.get('added_profiles'), list) else []
                for profile in added_profiles:
                    pn = profile if isinstance(profile, str) else (profile.get('pn') if isinstance(profile, dict) else None) or (
                        profile.get('jid') if isinstance(profile, dict) else None
                    )
                    if lid and pn:
                        mapping = {'lid': lid, 'pn': pn}
                        ev.emit('lid-mapping.update', mapping)
                        mappings.append(mapping)

            await signal_repository['lidMapping'].store_lidpn_mappings(mappings)
        else:
            if logger is not None:
                logger.info({'operation': operation, 'data': data}, 'unhandled mex newsletter notification')

    # Handles newsletter notifications
    async def handle_newsletter_notification(node):
        from_jid = (node.attrs or {}).get('from')
        children = get_all_binary_node_children(node)
        author = (node.attrs or {}).get('participant')

        for child in children:
            if logger is not None:
                logger.debug({'from': from_jid, 'child': child}, 'got newsletter notification')

            if child.tag == 'reaction':
                reaction_update = {
                    'id': from_jid,
                    'server_id': (child.attrs or {}).get('message_id'),
                    'reaction': {
                        'code': get_binary_node_child_string(child, 'reaction'),
                        'count': 1,
                    },
                }
                ev.emit('newsletter.reaction', reaction_update)
            elif child.tag == 'view':
                view_update = {
                    'id': from_jid,
                    'server_id': (child.attrs or {}).get('message_id'),
                    'count': int(child.content or b'0') if child.content else 0,
                }
                ev.emit('newsletter.view', view_update)
            elif child.tag == 'participant':
                participant_update = {
                    'id': from_jid,
                    'author': author,
                    'user': (child.attrs or {}).get('jid'),
                    'action': (child.attrs or {}).get('action'),
                    'new_role': (child.attrs or {}).get('role'),
                }
                ev.emit('newsletter-participants.update', participant_update)
            elif child.tag == 'update':
                settings_node = get_binary_node_child(child, 'settings')
                if settings_node:
                    update = {}
                    name_node = get_binary_node_child(settings_node, 'name')
                    if name_node and name_node.content:
                        update['name'] = bytes(name_node.content).decode('utf-8', errors='replace')

                    description_node = get_binary_node_child(settings_node, 'description')
                    if description_node and description_node.content:
                        update['description'] = bytes(description_node.content).decode('utf-8', errors='replace')

                    ev.emit('newsletter-settings.update', {
                        'id': from_jid,
                        'update': update,
                    })
            elif child.tag == 'message':
                plaintext_node = get_binary_node_child(child, 'plaintext')
                if plaintext_node and plaintext_node.content:
                    try:
                        content_buf = plaintext_node.content.encode('latin-1') if isinstance(plaintext_node.content, str) else bytes(plaintext_node.content)
                        message_proto = proto.Message.decode(content_buf)
                        full_message = proto.WebMessageInfo.from_object({
                            'key': {
                                'remoteJid': from_jid,
                                'id': (child.attrs or {}).get('message_id') or (child.attrs or {}).get('server_id'),
                                'fromMe': False,
                            },
                            'message': message_proto,
                            'messageTimestamp': int((child.attrs or {}).get('t') or 0),
                        })
                        await upsert_message(full_message, 'append')
                        if logger is not None:
                            logger.debug('Processed plaintext newsletter message')
                    except Exception as error:
                        if logger is not None:
                            logger.error({'error': error}, 'Failed to decode plaintext newsletter message')
            else:
                if logger is not None:
                    logger.warn({'node': node, 'child': child}, 'Unknown newsletter notification child')

    async def send_message_ack(node, error_code=None):
        stanza = build_ack_stanza(node, error_code, (auth_state['creds'].get('me') or {}).get('id'))
        if logger is not None:
            logger.debug({'recv': {'tag': node.tag, 'attrs': node.attrs}, 'sent': stanza.attrs}, 'sent ack')
        await send_node(stanza)

    async def reject_call(call_id, call_from):
        stanza = BinaryNode(
            tag='call',
            attrs={
                'from': (auth_state['creds'].get('me') or {}).get('id'),
                'to': call_from,
            },
            content=[
                BinaryNode(
                    tag='reject',
                    attrs={
                        'call-id': call_id,
                        'call-creator': call_from,
                        'count': '0',
                    },
                )
            ],
        )
        await query(stanza)

    async def send_retry_request(node, force_include_keys=False):
        decoded = decode_message_node(node, (auth_state['creds'].get('me') or {}).get('id'), (auth_state['creds'].get('me') or {}).get('lid') or '')
        full_message = decoded['fullMessage']
        msg_key = full_message['key']
        msg_id = msg_key.get('id')

        if message_retry_manager:
            if message_retry_manager.has_exceeded_max_retries(msg_id):
                if logger is not None:
                    logger.debug({'msgId': msg_id}, 'reached retry limit with new retry manager, clearing')
                message_retry_manager.mark_retry_failed(msg_id)
                return

            retry_count = message_retry_manager.increment_retry_count(msg_id)

            key = f'{msg_id}:{msg_key.get("participant")}'
            msg_retry_cache.set(key, retry_count)
        else:
            key = f'{msg_id}:{msg_key.get("participant")}'
            retry_count = msg_retry_cache.get(key) or 0
            if retry_count >= max_msg_retry_count:
                if logger is not None:
                    logger.debug({'retryCount': retry_count, 'msgId': msg_id}, 'reached retry limit, clearing')
                msg_retry_cache.delete(key)
                return

            retry_count += 1
            msg_retry_cache.set(key, retry_count)

        key = f'{msg_id}:{msg_key.get("participant")}'
        retry_count = msg_retry_cache.get(key) or 1

        creds = auth_state['creds']
        account = creds.get('account')
        signed_pre_key = creds.get('signedPreKey')
        identity_key = creds.get('signedIdentityKey')
        from_jid = (node.attrs or {}).get('from')

        # Check if we should recreate the session
        should_recreate_session = False
        recreate_reason = ''

        if enable_auto_session_recreation and message_retry_manager and retry_count > 1:
            try:
                session_id = signal_repository['jidToSignalProtocolAddress'](from_jid)
                has_session = await signal_repository['validateSession'](from_jid)
                result = message_retry_manager.should_recreate_session(from_jid, has_session.get('exists'))
                should_recreate_session = result['recreate']
                recreate_reason = result['reason']

                if should_recreate_session:
                    if logger is not None:
                        logger.debug({'fromJid': from_jid, 'retryCount': retry_count, 'reason': recreate_reason}, 'recreating session for retry')
                    await auth_state['keys'].set({'session': {session_id: None}})
                    force_include_keys = True
            except Exception as error:
                if logger is not None:
                    logger.warn({'error': error, 'fromJid': from_jid}, 'failed to check session recreation')

        if retry_count <= 2:
            if message_retry_manager:
                async def _phone_request():
                    try:
                        request_id = await request_placeholder_resend(msg_key)
                        if logger is not None:
                            logger.debug(f'sendRetryRequest: requested placeholder resend ({request_id}) for message {msg_id} (scheduled)')
                    except Exception as error:
                        if logger is not None:
                            logger.warn({'error': error, 'msgId': msg_id}, 'failed to send scheduled phone request')

                message_retry_manager.schedule_phone_request(msg_id, _phone_request)
            else:
                request_id = await request_placeholder_resend(msg_key)
                if logger is not None:
                    logger.debug(f'sendRetryRequest: requested placeholder resend for message {request_id}')

        device_identity = encode_signed_device_identity(account, True)

        async def _send_receipt():
            receipt = BinaryNode(
                tag='receipt',
                attrs={
                    'id': msg_id,
                    'type': 'retry',
                    'to': (node.attrs or {}).get('from'),
                },
                content=[
                    BinaryNode(
                        tag='retry',
                        attrs={
                            'count': str(retry_count),
                            'id': (node.attrs or {}).get('id'),
                            't': (node.attrs or {}).get('t'),
                            'v': '1',
                            'error': '0',
                        },
                    ),
                    BinaryNode(
                        tag='registration',
                        attrs={},
                        content=encode_big_endian(auth_state['creds'].get('registrationId')),
                    ),
                ],
            )

            if (node.attrs or {}).get('recipient'):
                receipt.attrs['recipient'] = (node.attrs or {}).get('recipient')

            if (node.attrs or {}).get('participant'):
                receipt.attrs['participant'] = (node.attrs or {}).get('participant')

            if retry_count > 1 or force_include_keys or should_recreate_session:
                update, pre_keys = await get_next_pre_keys(auth_state, 1)

                key_ids = list(pre_keys.keys())
                key_id = key_ids[0]
                key = pre_keys[key_id]

                receipt.content.append(
                    BinaryNode(
                        tag='keys',
                        attrs={},
                        content=[
                            BinaryNode(tag='type', attrs={}, content=bytes(KEY_BUNDLE_TYPE)),
                            BinaryNode(tag='identity', attrs={}, content=identity_key.get('public')),
                            xmpp_pre_key(key, int(key_id)),
                            xmpp_signed_pre_key(signed_pre_key),
                            BinaryNode(tag='device-identity', attrs={}, content=device_identity),
                        ],
                    )
                )

                ev.emit('creds.update', update)

            await send_node(receipt)

            if logger is not None:
                logger.info({'msgAttrs': node.attrs, 'retryCount': retry_count}, 'sent retry receipt')

        await auth_state['keys'].transaction(_send_receipt, (auth_state['creds'].get('me') or {}).get('id') or 'sendRetryRequest')

    # Mirrors WAWeb/Handle/PreKeyLow.js: skip a re-issued notification with the same stanza id.
    in_flight_pre_key_low = set()

    def reissue_tc_token_after_identity_change(from_jid):
        async def _run():
            normalized_jid = jid_normalized_user(from_jid)
            tc_jid = await resolve_tc_token_jid(normalized_jid, get_lid_for_pn)
            tc_token_data = await auth_state['keys'].get('tctoken', [tc_jid])
            sender_ts = None
            if tc_token_data and tc_token_data.get(tc_jid):
                sender_ts = tc_token_data[tc_jid].get('senderTimestamp')

            if sender_ts is None or is_tc_token_expired(sender_ts):
                return

            if logger is not None:
                logger.debug({'jid': normalized_jid, 'senderTimestamp': sender_ts}, 'identity changed, re-issuing tctoken')
            get_pn_for_lid = signal_repository['lidMapping'].get_pn_for_lid
            issue_jid = await resolve_issuance_jid(
                normalized_jid,
                messages_sock.get('serverProps', {}).get('lidTrustedTokenIssueToLid'),
                get_lid_for_pn,
                get_pn_for_lid,
            )
            result = await issue_privacy_tokens([issue_jid], sender_ts)
            await store_tc_tokens_from_iq_result({
                'result': result,
                'fallbackJid': tc_jid,
                'keys': auth_state['keys'],
                'getLIDForPN': get_lid_for_pn,
                'onNewJidStored': track_tc_token_jid,
            })

        asyncio.ensure_future(_run()).add_done_callback(
            lambda fut: (
                None
                if not fut.exception()
                else (logger.debug({'jid': from_jid, 'err': getattr(fut.exception(), 'message', fut.exception())}, 'failed to re-issue tctoken after identity change') if logger is not None else None)
            )
        )

    async def handle_encrypt_notification(node):
        from_jid = (node.attrs or {}).get('from')
        if from_jid == S_WHATSAPP_NET:
            stanza_id = (node.attrs or {}).get('id')
            if stanza_id and stanza_id in in_flight_pre_key_low:
                return

            count_child = get_binary_node_child(node, 'count')
            count = int((count_child.attrs or {}).get('value'))
            should_upload_more_pre_keys = count < MIN_PREKEY_COUNT

            if logger is not None:
                logger.debug({'count': count, 'shouldUploadMorePreKeys': should_upload_more_pre_keys}, 'recv pre-key count')
            if should_upload_more_pre_keys:
                if stanza_id:
                    in_flight_pre_key_low.add(stanza_id)
                try:
                    await upload_pre_keys()
                finally:
                    if stanza_id:
                        in_flight_pre_key_low.discard(stanza_id)
        else:
            result = await handle_identity_change(node, {
                'meId': (auth_state['creds'].get('me') or {}).get('id'),
                'meLid': (auth_state['creds'].get('me') or {}).get('lid'),
                'validateSession': signal_repository['validateSession'],
                'assertSessions': assert_sessions,
                'debounceCache': identity_assert_debounce,
                'logger': logger,
                'onBeforeSessionRefresh': reissue_tc_token_after_identity_change,
            })

            if result.get('action') == 'no_identity_node':
                if logger is not None:
                    logger.info({'node': node}, 'unknown encrypt notification')

    def handle_group_notification(full_node, child, msg):
        # TODO: Support PN/LID (Here is only LID now)

        acting_participant_lid = (full_node.attrs or {}).get('participant')
        acting_participant_pn = (full_node.attrs or {}).get('participant_pn')
        acting_participant_username = (full_node.attrs or {}).get('participant_username')

        child_participant = get_binary_node_child(child, 'participant')
        affected_participant_lid = (child_participant.attrs or {}).get('jid') if child_participant else (acting_participant_lid or '')
        affected_participant_pn = (child_participant.attrs or {}).get('phone_number') if child_participant else (acting_participant_pn or '')

        child_tag = child.tag
        if child_tag == 'create':
            metadata = extract_group_metadata(child)

            msg['messageStubType'] = WAMessageStubType.GROUP_CREATE
            msg['messageStubParameters'] = [metadata['subject']]
            msg['key'] = {'participant': metadata.get('owner'), 'participantAlt': metadata.get('ownerPn')}

            ev.emit('chats.upsert', [
                {
                    'id': metadata['id'],
                    'name': metadata['subject'],
                    'conversationTimestamp': metadata['creation'],
                }
            ])
            ev.emit('groups.upsert', [
                {
                    **metadata,
                    'author': acting_participant_lid,
                    'authorPn': acting_participant_pn,
                    'authorUsername': acting_participant_username,
                }
            ])
        elif child_tag in ('ephemeral', 'not_ephemeral'):
            msg['message'] = {
                'protocolMessage': {
                    'type': proto.Message.ProtocolMessage.Type.EPHEMERAL_SETTING,
                    'ephemeralExpiration': int((child.attrs or {}).get('expiration') or 0),
                }
            }
        elif child_tag == 'modify':
            old_number = [p.attrs.get('jid') for p in get_binary_node_children(child, 'participant')]
            msg['messageStubParameters'] = old_number or []
            msg['messageStubType'] = WAMessageStubType.GROUP_PARTICIPANT_CHANGE_NUMBER
        elif child_tag in ('promote', 'demote', 'remove', 'add', 'leave'):
            stub_type = f'GROUP_PARTICIPANT_{child_tag.upper()}'
            msg['messageStubType'] = getattr(WAMessageStubType, stub_type)

            participants = []
            for participant in get_binary_node_children(child, 'participant'):
                attrs = participant.attrs or {}
                participants.append({
                    'id': attrs.get('jid'),
                    'phoneNumber': attrs.get('phone_number') if (is_lid_user(attrs.get('jid')) and is_pn_user(attrs.get('phone_number'))) else None,
                    'lid': attrs.get('lid') if (is_pn_user(attrs.get('jid')) and is_lid_user(attrs.get('lid'))) else None,
                    'username': attrs.get('participant_username') or attrs.get('username') or None,
                    'admin': attrs.get('type') or None,
                })

            if (
                len(participants) == 1
                and (
                    are_jids_same_user(participants[0]['id'], acting_participant_lid)
                    or are_jids_same_user(participants[0]['id'], acting_participant_pn)
                )
                and child_tag == 'remove'
            ):
                msg['messageStubType'] = WAMessageStubType.GROUP_PARTICIPANT_LEAVE

            msg['messageStubParameters'] = [json.dumps(a) for a in participants]
        elif child_tag == 'subject':
            msg['messageStubType'] = WAMessageStubType.GROUP_CHANGE_SUBJECT
            msg['messageStubParameters'] = [(child.attrs or {}).get('subject')]
        elif child_tag == 'description':
            body_node = get_binary_node_child(child, 'body')
            description = bytes(body_node.content).decode('utf-8', errors='replace') if (body_node and body_node.content) else None
            msg['messageStubType'] = WAMessageStubType.GROUP_CHANGE_DESCRIPTION
            msg['messageStubParameters'] = [description] if description else None
        elif child_tag in ('announcement', 'not_announcement'):
            msg['messageStubType'] = WAMessageStubType.GROUP_CHANGE_ANNOUNCE
            msg['messageStubParameters'] = ['on' if child_tag == 'announcement' else 'off']
        elif child_tag in ('locked', 'unlocked'):
            msg['messageStubType'] = WAMessageStubType.GROUP_CHANGE_RESTRICT
            msg['messageStubParameters'] = ['on' if child_tag == 'locked' else 'off']
        elif child_tag == 'invite':
            msg['messageStubType'] = WAMessageStubType.GROUP_CHANGE_INVITE_LINK
            msg['messageStubParameters'] = [(child.attrs or {}).get('code')]
        elif child_tag == 'member_add_mode':
            add_mode = child.content
            if add_mode:
                msg['messageStubType'] = WAMessageStubType.GROUP_MEMBER_ADD_MODE
                msg['messageStubParameters'] = [bytes(add_mode).decode('utf-8', errors='replace')]
        elif child_tag == 'membership_approval_mode':
            approval_mode = get_binary_node_child(child, 'group_join')
            if approval_mode:
                msg['messageStubType'] = WAMessageStubType.GROUP_MEMBERSHIP_JOIN_APPROVAL_MODE
                msg['messageStubParameters'] = [(approval_mode.attrs or {}).get('state')]
        elif child_tag == 'created_membership_requests':
            msg['messageStubType'] = WAMessageStubType.GROUP_MEMBERSHIP_JOIN_APPROVAL_REQUEST_NON_ADMIN_ADD
            msg['messageStubParameters'] = [
                json.dumps({'lid': affected_participant_lid, 'pn': affected_participant_pn}),
                'created',
                (child.attrs or {}).get('request_method'),
            ]
        elif child_tag == 'revoked_membership_requests':
            is_denied = are_jids_same_user(affected_participant_lid, acting_participant_lid)
            # TODO: LIDMAPPING SUPPORT
            msg['messageStubType'] = WAMessageStubType.GROUP_MEMBERSHIP_JOIN_APPROVAL_REQUEST_NON_ADMIN_ADD
            msg['messageStubParameters'] = [
                json.dumps({'lid': affected_participant_lid, 'pn': affected_participant_pn}),
                'revoked' if is_denied else 'rejected',
            ]

    async def handle_devices_notification(node):
        children = get_all_binary_node_children(node)
        child = children[0] if children else None
        from_jid = jid_normalized_user((node.attrs or {}).get('from'))

        if not child:
            if logger is not None:
                logger.debug({'from': from_jid}, 'devices notification missing child, skipping')
            return

        tag = child.tag
        device_hash = (child.attrs or {}).get('device_hash')
        devices = get_binary_node_children(child, 'device')

        me_id = (auth_state['creds'].get('me') or {}).get('id')
        me_lid = (auth_state['creds'].get('me') or {}).get('lid')
        if are_jids_same_user(from_jid, me_id) or (me_lid and are_jids_same_user(from_jid, me_lid)):
            device_jids = [(d.attrs or {}).get('jid') for d in devices]
            if logger is not None:
                logger.info({'deviceJids': device_jids}, 'got my own devices')

        if not devices:
            if logger is not None:
                logger.debug({'from': from_jid, 'tag': tag}, 'no devices in notification, skipping')
            return

        decoded = []
        for d in devices:
            jid = (d.attrs or {}).get('jid')
            if not jid:
                continue
            parts = jid_decode(jid)
            if not parts:
                if logger is not None:
                    logger.debug({'jid': jid}, 'failed to decode device jid, skipping')
                continue

            decoded.append({'jid': jid, 'user': parts.user, 'server': parts.server, 'device': parts.device})

        if not decoded:
            return

        async def _mutex_work():
            by_user = {}
            for d in decoded:
                by_user.setdefault(d['user'], []).append(d)

            for user, entries in by_user.items():
                if tag == 'update':
                    if logger is not None:
                        logger.debug({'user': user}, f"{user}'s device list updated, dropping cached devices")
                    user_devices_cache.delete(user)
                    continue

                if tag == 'remove':
                    await signal_repository['deleteSession']([e['jid'] for e in entries])

                existing_cache = user_devices_cache.get(user) or []
                if not existing_cache:
                    if logger is not None:
                        logger.debug({'user': user, 'tag': tag}, 'device list not cached, deferring to USync refresh')
                    continue

                affected = {e.get('device') for e in entries}
                if tag == 'add':
                    if logger is not None:
                        logger.info({'deviceHash': device_hash, 'count': len(entries)}, 'devices added')
                    updated_devices = [
                        *[d for d in existing_cache if d.get('device') not in affected],
                        *[{'user': e['user'], 'server': e['server'], 'device': e.get('device')} for e in entries],
                    ]
                elif tag == 'remove':
                    if logger is not None:
                        logger.info({'deviceHash': device_hash, 'count': len(entries)}, 'devices removed')
                    updated_devices = [d for d in existing_cache if d.get('device') not in affected]
                else:
                    if logger is not None:
                        logger.debug({'tag': tag}, 'Unknown device list change tag')
                    continue

                if len(updated_devices) == 0:
                    user_devices_cache.delete(user)
                else:
                    user_devices_cache.set(user, updated_devices)

        await devices_mutex['mutex'](_mutex_work)

    async def process_notification(node):
        result = {}
        children = get_all_binary_node_children(node)
        child = children[0] if children else None
        node_type = (node.attrs or {}).get('type')
        from_jid = jid_normalized_user((node.attrs or {}).get('from'))

        if node_type == 'newsletter':
            await handle_newsletter_notification(node)
        elif node_type == 'mex':
            await handle_mex_notification(node)
        elif node_type == 'w:gp2':
            # TODO: HANDLE PARTICIPANT_PN
            handle_group_notification(node, child, result)
        elif node_type == 'mediaretry':
            event = decode_media_retry_node(node)
            ev.emit('messages.media-update', [event])
        elif node_type == 'encrypt':
            await handle_encrypt_notification(node)
        elif node_type == 'devices':
            try:
                await handle_devices_notification(node)
            except Exception as error:
                if logger is not None:
                    logger.error({'error': error, 'node': node}, 'failed to handle devices notification')
        elif node_type == 'server_sync':
            update = get_binary_node_child(node, 'collection')
            if update:
                name = (update.attrs or {}).get('name')
                await resync_app_state([name], False)
        elif node_type == 'picture':
            set_picture = get_binary_node_child(node, 'set')
            del_picture = get_binary_node_child(node, 'delete')

            # TODO: WAJIDHASH stuff proper support inhouse
            ev.emit('contacts.update', [
                {
                    'id': jid_normalized_user((node.attrs or {}).get('from')) or ((set_picture or del_picture).attrs or {}).get('hash') or '',
                    'imgUrl': 'changed' if set_picture else 'removed',
                }
            ])

            if is_jid_group(from_jid):
                picture_node = set_picture or del_picture
                result['messageStubType'] = WAMessageStubType.GROUP_CHANGE_ICON

                if set_picture:
                    result['messageStubParameters'] = [(set_picture.attrs or {}).get('id')]

                result['participant'] = (picture_node.attrs or {}).get('author') if picture_node else None
                result['key'] = {
                    **(result.get('key') or {}),
                    'participant': (set_picture.attrs or {}).get('author') if set_picture else None,
                }
        elif node_type == 'account_sync':
            if child.tag == 'disappearing_mode':
                new_duration = int((child.attrs or {}).get('duration'))
                timestamp = int((child.attrs or {}).get('t'))

                if logger is not None:
                    logger.info({'newDuration': new_duration}, 'updated account disappearing mode')

                ev.emit('creds.update', {
                    'accountSettings': {
                        **auth_state['creds'].get('accountSettings', {}),
                        'defaultDisappearingMode': {
                            'ephemeralExpiration': new_duration,
                            'ephemeralSettingTimestamp': timestamp,
                        },
                    }
                })
            elif child.tag == 'blocklist':
                blocklists = get_binary_node_children(child, 'item')

                for item in blocklists:
                    attrs = item.attrs or {}
                    blocklist = [attrs.get('jid')]
                    block_type = 'add' if attrs.get('action') == 'block' else 'remove'
                    ev.emit('blocklist.update', {'blocklist': blocklist, 'type': block_type})
        elif node_type == 'link_code_companion_reg':
            link_code_companion_reg = get_binary_node_child(node, 'link_code_companion_reg')
            ref = to_required_buffer(get_binary_node_child_buffer(link_code_companion_reg, 'link_code_pairing_ref'))
            primary_identity_public_key = to_required_buffer(
                get_binary_node_child_buffer(link_code_companion_reg, 'primary_identity_pub')
            )
            primary_ephemeral_public_key_wrapped = to_required_buffer(
                get_binary_node_child_buffer(link_code_companion_reg, 'link_code_pairing_wrapped_primary_ephemeral_pub')
            )
            code_pairing_public_key = decipher_link_public_key(primary_ephemeral_public_key_wrapped)
            companion_shared_key = Curve.shared_key(
                auth_state['creds'].get('pairingEphemeralKeyPair').get('private'),
                code_pairing_public_key,
            )
            random_bytes = os.urandom(32)
            link_code_salt = os.urandom(32)
            link_code_pairing_expanded = hkdf(
                companion_shared_key,
                32,
                info='link_code_pairing_key_bundle_encryption_key'.encode('utf-8'),
                salt=link_code_salt,
            )
            encrypt_payload = (
                bytes(auth_state['creds'].get('signedIdentityKey').get('public'))
                + bytes(primary_identity_public_key)
                + random_bytes
            )
            encrypt_iv = os.urandom(12)
            encrypted = aes_encrypt_gcm(encrypt_payload, link_code_pairing_expanded, encrypt_iv, b'')
            encrypted_payload = link_code_salt + encrypt_iv + encrypted
            identity_shared_key = Curve.shared_key(
                auth_state['creds'].get('signedIdentityKey').get('private'),
                primary_identity_public_key,
            )
            identity_payload = companion_shared_key + identity_shared_key + random_bytes
            adv_secret_key = hkdf(identity_payload, 32, info=b'adv_secret')
            auth_state['creds']['advSecretKey'] = adv_secret_key.hex()
            await query({
                'tag': 'iq',
                'attrs': {
                    'to': S_WHATSAPP_NET,
                    'type': 'set',
                    'id': messages_sock['generateMessageTag'](),
                    'xmlns': 'md',
                },
                'content': [
                    {
                        'tag': 'link_code_companion_reg',
                        'attrs': {
                            'jid': (auth_state['creds'].get('me') or {}).get('id'),
                            'stage': 'companion_finish',
                        },
                        'content': [
                            {
                                'tag': 'link_code_pairing_wrapped_key_bundle',
                                'attrs': {},
                                'content': encrypted_payload,
                            },
                            {
                                'tag': 'companion_identity_public',
                                'attrs': {},
                                'content': auth_state['creds'].get('signedIdentityKey').get('public'),
                            },
                            {
                                'tag': 'link_code_pairing_ref',
                                'attrs': {},
                                'content': ref,
                            },
                        ],
                    }
                ],
            })
            auth_state['creds']['registered'] = True
            ev.emit('creds.update', auth_state['creds'])
        elif node_type == 'privacy_token':
            await handle_privacy_token_notification(node)

        if len(result):
            return result
        return None

    # In-memory cache of storage JIDs with stored tctokens, seeded from the persisted index.
    tc_token_known_jids = set()

    async def _load_tc_token_index():
        try:
            jids = await read_tc_token_index(auth_state['keys'])
            for jid in jids:
                tc_token_known_jids.add(jid)
            if logger is not None:
                logger.debug({'count': len(tc_token_known_jids)}, 'loaded tctoken index')
        except Exception as err:
            if logger is not None:
                logger.warn({'err': getattr(err, 'message', err)}, 'failed to load tctoken index')

    tc_token_index_loaded = asyncio.ensure_future(_load_tc_token_index())

    tc_token_index_timer = None

    async def flush_tc_token_index():
        nonlocal tc_token_index_timer
        if tc_token_index_timer is not None:
            tc_token_index_timer.cancel()
            tc_token_index_timer = None

        # Merge with whatever is already persisted so we don't clobber writes from other paths
        write = await build_merged_tc_token_index_write(auth_state['keys'], tc_token_known_jids)
        return await auth_state['keys'].set({'tctoken': write})

    def schedule_tc_token_index_save():
        nonlocal tc_token_index_timer
        if tc_token_index_timer is not None:
            tc_token_index_timer.cancel()

        async def _flush():
            try:
                await flush_tc_token_index()
            except Exception as err:
                if logger is not None:
                    logger.warn({'err': getattr(err, 'message', err)}, 'failed to save tctoken index')

        loop = asyncio.get_event_loop()
        tc_token_index_timer = loop.call_later(5, lambda: asyncio.ensure_future(_flush()))

    def track_tc_token_jid(jid):
        if jid and jid != TC_TOKEN_INDEX_KEY and jid not in tc_token_known_jids:
            tc_token_known_jids.add(jid)
            schedule_tc_token_index_save()

    async def handle_privacy_token_notification(node):
        tokens_node = get_binary_node_child(node, 'tokens')
        if not tokens_node:
            return

        from_jid = jid_normalized_user((node.attrs or {}).get('from'))

        # WA Web uses: senderLid ?? toLid(from) for the storage key
        sender_lid = (node.attrs or {}).get('sender_lid')
        if sender_lid and is_lid_user(jid_normalized_user(sender_lid)):
            sender_lid = jid_normalized_user(sender_lid)
        else:
            sender_lid = None
        fallback_jid = sender_lid or await resolve_tc_token_jid(from_jid, get_lid_for_pn)

        if logger is not None:
            logger.debug({'from': from_jid, 'storageJid': fallback_jid}, 'processing privacy token notification')

        await store_tc_tokens_from_iq_result({
            'result': node,
            'fallbackJid': fallback_jid,
            'keys': auth_state['keys'],
            'getLIDForPN': get_lid_for_pn,
            'onNewJidStored': track_tc_token_jid,
        })

    async def decipher_link_public_key(data):
        buffer = to_required_buffer(data)
        salt = buffer[:32]
        secret_key = await derive_pairing_code_key(auth_state['creds'].get('pairingCode'), salt)
        iv = buffer[32:48]
        payload = buffer[48:80]
        return aes_decrypt_ctr(payload, secret_key, iv)

    def to_required_buffer(data):
        if data is None:
            raise Boom('Invalid buffer', status_code=400)
        return bytes(data)

    async def will_send_message_again(id, participant):
        key = f'{id}:{participant}'
        retry_count = msg_retry_cache.get(key) or 0
        return retry_count < max_msg_retry_count

    async def update_send_message_again_count(id, participant):
        key = f'{id}:{participant}'
        new_value = (msg_retry_cache.get(key) or 0) + 1
        msg_retry_cache.set(key, new_value)

    async def send_messages_again(key, ids, retry_node, receipt_node):
        remote_jid = key.get('remoteJid')
        participant = key.get('participant') or remote_jid

        retry_count = int((retry_node.attrs or {}).get('count') or 1)
        msg_id = ids[0]

        # Try to get messages from cache first, then fallback to getMessage
        msgs = []
        for id in ids:
            msg = None

            # Try to get from retry cache first if enabled
            if message_retry_manager:
                cached_msg = message_retry_manager.get_recent_message(remote_jid, id)
                if cached_msg:
                    msg = cached_msg.get('message')
                    if logger is not None:
                        logger.debug({'jid': remote_jid, 'id': id}, 'found message in retry cache')

                    # Mark retry as successful since we found the message
                    message_retry_manager.mark_retry_success(id)

            # Fallback to getMessage if not found in cache
            if not msg:
                msg = await get_message({**key, 'id': id})
                if msg:
                    if logger is not None:
                        logger.debug({'jid': remote_jid, 'id': id}, 'found message via getMessage')
                    if message_retry_manager:
                        message_retry_manager.mark_retry_success(id)

            msgs.append(msg)

        # if it's the primary jid sending the request just re-send the message to everyone
        decoded = jid_decode(participant)
        send_to_all = not (decoded.device) if decoded else True

        session_id = signal_repository['jidToSignalProtocolAddress'](participant)
        injected_from_bundle = False

        bundle = extract_e2e_session_from_retry_receipt(receipt_node)
        if bundle:
            try:
                await signal_repository['injectE2ESession']({'jid': participant, 'session': bundle})
                injected_from_bundle = True
                if logger is not None:
                    logger.debug({'participant': participant, 'retryCount': retry_count}, 'injected session from retry receipt key bundle')
            except Exception as error:
                if logger is not None:
                    logger.warn({'error': error, 'participant': participant}, 'failed to inject session from retry receipt')

        if not injected_from_bundle:
            received_reg_id = get_binary_node_child_uint(receipt_node, 'registration', 4)
            if isinstance(received_reg_id, int):
                info = await signal_repository['getSessionInfo'](participant)
                if info and info.get('registrationId') != 0 and info.get('registrationId') != received_reg_id:
                    if logger is not None:
                        logger.info(
                            {'participant': participant, 'stored': info.get('registrationId'), 'received': received_reg_id},
                            'reg id mismatch on retry without bundle, deleting session',
                        )
                    await auth_state['keys'].set({'session': {session_id: None}})

        base_key_check_retry = 2
        if msg_id and message_retry_manager:
            info = await signal_repository['getSessionInfo'](participant)
            if info:
                if retry_count == base_key_check_retry:
                    message_retry_manager.save_base_key(session_id, msg_id, info.get('baseKey'))
                elif retry_count > base_key_check_retry:
                    if message_retry_manager.has_same_base_key(session_id, msg_id, info.get('baseKey')):
                        if logger is not None:
                            logger.warn({'participant': participant, 'retryCount': retry_count}, 'base key collision on retry, forcing fresh session')
                        await auth_state['keys'].set({'session': {session_id: None}})

                    message_retry_manager.delete_base_key(session_id, msg_id)

        should_recreate_session = False
        recreate_reason = ''

        if enable_auto_session_recreation and message_retry_manager and retry_count > 1 and not injected_from_bundle:
            try:
                has_session = await signal_repository['validateSession'](participant)
                result = message_retry_manager.should_recreate_session(participant, has_session.get('exists'))
                should_recreate_session = result['recreate']
                recreate_reason = result['reason']

                if should_recreate_session:
                    if logger is not None:
                        logger.debug({'participant': participant, 'retryCount': retry_count, 'reason': recreate_reason}, 'recreating session for outgoing retry')
                    await auth_state['keys'].set({'session': {session_id: None}})
            except Exception as error:
                if logger is not None:
                    logger.warn({'error': error, 'participant': participant}, 'failed to check session recreation for outgoing retry')

        if not injected_from_bundle:
            await assert_sessions([participant], True)

        if is_jid_group(remote_jid):
            await auth_state['keys'].set({'sender-key-memory': {remote_jid: None}})

        if logger is not None:
            logger.debug(
                {'participant': participant, 'sendToAll': send_to_all, 'shouldRecreateSession': should_recreate_session, 'recreateReason': recreate_reason, 'injectedFromBundle': injected_from_bundle},
                'prepared session for retry resend',
            )

        for i, msg in enumerate(msgs):
            if not ids[i]:
                continue

            if msg and (await will_send_message_again(ids[i], participant)):
                await update_send_message_again_count(ids[i], participant)
                msg_relay_opts = {'messageId': ids[i]}

                if send_to_all:
                    msg_relay_opts['useUserDevicesCache'] = False
                else:
                    msg_relay_opts['participant'] = {
                        'jid': participant,
                        'count': int((retry_node.attrs or {}).get('count')),
                    }

                await relay_message(key.get('remoteJid'), msg, msg_relay_opts)
            else:
                if logger is not None:
                    logger.debug({'jid': key.get('remoteJid'), 'id': ids[i]}, 'recv retry request, but message not available')

    async def handle_receipt(node):
        attrs = node.attrs or {}
        content = node.content
        is_lid = (attrs.get('from') or '').find('lid') > -1
        me_id = (auth_state['creds'].get('me') or {}).get('id')
        me_lid = (auth_state['creds'].get('me') or {}).get('lid')
        is_node_from_me = are_jids_same_user(
            attrs.get('participant') or attrs.get('from'),
            me_lid if is_lid else me_id,
        )
        remote_jid = (attrs.get('from') if (not is_node_from_me or is_jid_group(attrs.get('from'))) else attrs.get('recipient'))
        from_me = not attrs.get('recipient') or ((attrs.get('type') in ('retry', 'sender')) and is_node_from_me)

        key = {
            'remoteJid': remote_jid,
            'id': '',
            'fromMe': from_me,
            'participant': attrs.get('participant'),
        }

        ids = [attrs.get('id')]
        if isinstance(content, list):
            if content and content[0] is not None:
                items = get_binary_node_children(content[0], 'item')
                ids.extend([(i.attrs or {}).get('id') for i in items])

        try:
            async def _mutex_work():
                status = get_status_from_receipt_type(attrs.get('type'))
                if (
                    status is not None
                    # basically, we only want to know when a message from us has been delivered to/read by the other person
                    and (status >= proto.WebMessageInfo.Status.SERVER_ACK or not is_node_from_me)
                ):
                    if is_jid_group(remote_jid) or is_jid_status_broadcast(remote_jid):
                        if attrs.get('participant'):
                            update_key = 'receiptTimestamp' if status == proto.WebMessageInfo.Status.DELIVERY_ACK else 'readTimestamp'
                            ev.emit(
                                'message-receipt.update',
                                [
                                    {
                                        'key': {**key, 'id': id},
                                        'receipt': {
                                            'userJid': jid_normalized_user(attrs.get('participant')),
                                            update_key: int(attrs.get('t')),
                                        },
                                    }
                                    for id in ids
                                ],
                            )
                    else:
                        ev.emit(
                            'messages.update',
                            [
                                {
                                    'key': {**key, 'id': id},
                                    'update': {'status': status, 'messageTimestamp': to_number(int(attrs.get('t') or 0))},
                                }
                                for id in ids
                            ],
                        )

                if attrs.get('type') == 'retry':
                    # correctly set who is asking for the retry
                    key['participant'] = key.get('participant') or attrs.get('from')
                    retry_node = get_binary_node_child(node, 'retry')
                    if ids[0] and key.get('participant') and (await will_send_message_again(ids[0], key['participant'])):
                        if key.get('fromMe'):
                            try:
                                await update_send_message_again_count(ids[0], key['participant'])
                                if logger is not None:
                                    logger.debug({'attrs': attrs, 'key': key}, 'recv retry request')
                                await send_messages_again(key, ids, retry_node, node)
                            except Exception as error:
                                if logger is not None:
                                    logger.error(
                                        {'key': key, 'ids': ids, 'trace': getattr(error, '__traceback__', None)},
                                        'error in sending message again',
                                    )
                        else:
                            if logger is not None:
                                logger.info({'attrs': attrs, 'key': key}, 'recv retry for not fromMe message')
                    else:
                        if logger is not None:
                            logger.info({'attrs': attrs, 'key': key}, 'will not send message again, as sent too many times')

            await receipt_mutex['mutex'](_mutex_work)
        finally:
            try:
                await send_message_ack(node)
            except Exception as ack_err:
                if logger is not None:
                    logger.error({'ackErr': ack_err}, 'failed to ack receipt')

    async def handle_notification(node):
        remote_jid = (node.attrs or {}).get('from')

        try:
            async def _mutex_work():
                msg = await process_notification(node)
                if msg:
                    me_id = (auth_state['creds'].get('me') or {}).get('id')
                    from_me = are_jids_same_user((node.attrs or {}).get('participant') or remote_jid, me_id)
                    addressing = extract_addressing_context(node)
                    msg['key'] = {
                        'remoteJid': remote_jid,
                        'fromMe': from_me,
                        'participant': (node.attrs or {}).get('participant'),
                        'participantAlt': addressing['senderAlt'],
                        'participantUsername': (node.attrs or {}).get('participant_username'),
                        'addressingMode': addressing['addressingMode'],
                        'id': (node.attrs or {}).get('id'),
                        **(msg.get('key') or {}),
                    }
                    msg.setdefault('participant', (node.attrs or {}).get('participant'))
                    msg['messageTimestamp'] = int((node.attrs or {}).get('t'))

                    full_msg = proto.WebMessageInfo.from_object(msg)
                    await upsert_message(full_msg, 'append')

            await notification_mutex['mutex'](_mutex_work)
        finally:
            try:
                await send_message_ack(node)
            except Exception as ack_err:
                if logger is not None:
                    logger.error({'ackErr': ack_err}, 'failed to ack notification')

    async def handle_message(node):
        enc_node = get_binary_node_child(node, 'enc')
        # TODO: temporary fix for crashes and issues resulting of failed msmsg decryption
        if enc_node and (enc_node.attrs or {}).get('type') == 'msmsg':
            if logger is not None:
                logger.debug({'key': (node.attrs or {}).get('key')}, 'ignored msmsg')
            await send_message_ack(node, NACK_REASONS['MissingMessageSecret'])
            return

        acked = False

        try:
            decrypted = decrypt_message_node(
                node,
                (auth_state['creds'].get('me') or {}).get('id'),
                (auth_state['creds'].get('me') or {}).get('lid') or '',
                signal_repository,
                logger,
            )
            msg = decrypted['fullMessage']
            category = decrypted['category']
            author = decrypted['author']
            decrypt = decrypted['decrypt']

            alt = msg.get('key', {}).get('participantAlt') or msg.get('key', {}).get('remoteJidAlt')
            # store new mappings we didn't have before
            if alt:
                alt_server = None
                decoded_alt = jid_decode(alt)
                if decoded_alt:
                    alt_server = decoded_alt.server
                primary_jid = msg.get('key', {}).get('participant') or msg.get('key', {}).get('remoteJid')
                if alt_server == 'lid':
                    if not (await signal_repository['lidMapping'].get_pn_for_lid(alt)):
                        await signal_repository['lidMapping'].store_lidpn_mappings([{'lid': alt, 'pn': primary_jid}])
                        await signal_repository['migrateSession'](primary_jid, alt)
                else:
                    await signal_repository['lidMapping'].store_lidpn_mappings([{'lid': primary_jid, 'pn': alt}])
                    await signal_repository['migrateSession'](alt, primary_jid)

            async def _mutex_work():
                nonlocal acked
                await decrypt()

                if (
                    msg.get('key', {}).get('remoteJid')
                    and msg.get('key', {}).get('id')
                    and msg.get('message')
                    and message_retry_manager
                ):
                    message_retry_manager.add_recent_message(msg['key']['remoteJid'], msg['key']['id'], msg['message'])

                # message failed to decrypt
                if msg.get('messageStubType') == proto.WebMessageInfo.StubType.CIPHERTEXT and msg.get('category') != 'peer':
                    stub_params = msg.get('messageStubParameters') or []
                    if stub_params and stub_params[0] == MISSING_KEYS_ERROR_TEXT:
                        acked = True
                        await send_message_ack(node, NACK_REASONS['ParsingError'])
                        return

                    if stub_params and stub_params[0] == NO_MESSAGE_FOUND_ERROR_TEXT:
                        # Message arrived without encryption (e.g. CTWA ads messages).
                        unavailable_node = get_binary_node_child(node, 'unavailable')
                        unavailable_type = (unavailable_node.attrs or {}).get('type') if unavailable_node else None
                        if unavailable_type in (
                            'bot_unavailable_fanout',
                            'hosted_unavailable_fanout',
                            'view_once_unavailable_fanout',
                        ):
                            if logger is not None:
                                logger.debug(
                                    {'msgId': msg.get('key', {}).get('id'), 'unavailableType': unavailable_type},
                                    'skipping placeholder resend for excluded unavailable type',
                                )
                            acked = True
                            await send_message_ack(node)
                            return

                        message_age = unix_timestamp_seconds() - to_number(msg.get('messageTimestamp'))
                        if message_age > PLACEHOLDER_MAX_AGE_SECONDS:
                            if logger is not None:
                                logger.debug({'msgId': msg.get('key', {}).get('id'), 'messageAge': message_age}, 'skipping placeholder resend for old message')
                            acked = True
                            await send_message_ack(node)
                            return

                        # Request the real content from the phone via placeholder resend PDO.
                        clean_key = {
                            'remoteJid': msg.get('key', {}).get('remoteJid'),
                            'fromMe': msg.get('key', {}).get('fromMe'),
                            'id': msg.get('key', {}).get('id'),
                            'participant': msg.get('key', {}).get('participant'),
                        }
                        msg_data = {
                            'key': msg.get('key'),
                            'messageTimestamp': msg.get('messageTimestamp'),
                            'pushName': msg.get('pushName'),
                            'participant': msg.get('participant'),
                            'verifiedBizName': msg.get('verifiedBizName'),
                        }

                        async def _on_request_done():
                            request_id = await request_placeholder_resend(clean_key, msg_data)
                            if request_id and request_id != 'RESOLVED':
                                if logger is not None:
                                    logger.debug({'msgId': msg.get('key', {}).get('id'), 'requestId': request_id}, 'requested placeholder resend for unavailable message')
                                ev.emit('messages.update', [
                                    {
                                        'key': msg.get('key'),
                                        'update': {'messageStubParameters': [NO_MESSAGE_FOUND_ERROR_TEXT, request_id]},
                                    }
                                ])

                        asyncio.ensure_future(_on_request_done()).add_done_callback(
                            lambda fut: (
                                None
                                if not fut.exception()
                                else (
                                    logger.warn({'err': fut.exception(), 'msgId': msg.get('key', {}).get('id')}, 'failed to request placeholder resend for unavailable message')
                                    if logger is not None
                                    else None
                                )
                            )
                        )
                        acked = True
                        await send_message_ack(node)
                        # Don't return — fall through to upsertMessage so the stub is emitted
                    else:
                        # Skip retry for expired status messages (>24h old)
                        if is_jid_status_broadcast(msg.get('key', {}).get('remoteJid')):
                            message_age = unix_timestamp_seconds() - to_number(msg.get('messageTimestamp'))
                            if message_age > STATUS_EXPIRY_SECONDS:
                                if logger is not None:
                                    logger.debug(
                                        {'msgId': msg.get('key', {}).get('id'), 'messageAge': message_age, 'remoteJid': msg.get('key', {}).get('remoteJid')},
                                        'skipping retry for expired status message',
                                    )
                                acked = True
                                await send_message_ack(node)
                                return

                        if logger is not None:
                            logger.debug('[handleMessage] Attempting retry request for failed decryption')

                        # WAWeb only retry-receipts here; server emits PreKeyLow if prekeys run low.
                        async def _retry_work():
                            nonlocal acked
                            try:
                                if not ws.is_open:
                                    if logger is not None:
                                        logger.debug({'node': node}, 'Connection closed, skipping retry')
                                    return

                                enc_node = get_binary_node_child(node, 'enc')
                                await send_retry_request(node, not enc_node)
                                if retry_request_delay_ms:
                                    await delay(retry_request_delay_ms)
                            except Exception as err:
                                if logger is not None:
                                    logger.error({'err': err}, 'Failed to send retry')

                            acked = True
                            await send_message_ack(node, NACK_REASONS['UnhandledError'])

                        await retry_mutex['mutex'](_retry_work)
                else:
                    if message_retry_manager and msg.get('key', {}).get('id'):
                        message_retry_manager.cancel_pending_phone_request(msg['key']['id'])

                    is_newsletter = is_jid_newsletter(msg.get('key', {}).get('remoteJid'))
                    if not is_newsletter:
                        # no type in the receipt => message delivered
                        type_ = None
                        participant = msg.get('key', {}).get('participant')
                        if category == 'peer':
                            # special peer message
                            type_ = 'peer_msg'
                        elif msg.get('key', {}).get('fromMe'):
                            # message was sent by us from a different device
                            type_ = 'sender'
                            # need to specially handle this case
                            if is_lid_user(msg.get('key', {}).get('remoteJid')) or is_lid_user(msg.get('key', {}).get('remoteJidAlt')):
                                participant = author  # TODO: investigate sending receipts to LIDs and not PNs
                        elif not send_active_receipts:
                            type_ = 'inactive'

                        acked = True
                        await send_receipt(msg['key']['remoteJid'], participant, [msg['key']['id']], type_)

                        # send ack for history message
                        is_any_history_msg = get_history_msg(msg.get('message'))
                        if is_any_history_msg:
                            jid = jid_normalized_user(msg['key']['remoteJid'])
                            await send_receipt(jid, None, [msg['key']['id']], 'hist_sync')  # TODO: investigate
                    else:
                        acked = True
                        await send_message_ack(node)
                        if logger is not None:
                            logger.debug({'key': msg.get('key')}, 'processed newsletter message without receipts')

                clean_message(msg, (auth_state['creds'].get('me') or {}).get('id'), (auth_state['creds'].get('me') or {}).get('lid'))

                await upsert_message(msg, 'append' if (node.attrs or {}).get('offline') else 'notify')

            await message_mutex['mutex'](_mutex_work)
        except Exception as error:
            if logger is not None:
                logger.error({'error': error, 'node': binary_node_to_string(node)}, 'error in handling message')
            if not acked:
                try:
                    await send_message_ack(node, NACK_REASONS['UnhandledError'])
                except Exception as ack_err:
                    if logger is not None:
                        logger.error({'ackErr': ack_err}, 'failed to ack message after error')

    async def handle_call(node):
        try:
            attrs = node.attrs or {}
            children = get_all_binary_node_children(node)
            info_child = children[0] if children else None

            if not info_child:
                raise Boom('Missing call info in call node')

            status = get_call_status_from_node(info_child)

            call_id = (info_child.attrs or {}).get('call-id')
            from_jid = (info_child.attrs or {}).get('from') or (info_child.attrs or {}).get('call-creator')

            call = {
                'chatId': attrs.get('from'),
                'from': from_jid,
                'callerPn': (info_child.attrs or {}).get('caller_pn'),
                'id': call_id,
                'date': datetime.fromtimestamp(int(attrs.get('t') or 0), tz=timezone.utc),
                'offline': bool(attrs.get('offline')),
                'status': status,
            }

            if status == 'relaylatency':
                latency_value = (info_child.attrs or {}).get('latency') or (info_child.attrs or {}).get('latency_ms') or (info_child.attrs or {}).get('latency-ms')
                latency_ms = float(latency_value) if latency_value else None
                if latency_ms is not None:
                    call['latencyMs'] = latency_ms

            if status == 'offer':
                call['isVideo'] = bool(get_binary_node_child(info_child, 'video'))
                call['isGroup'] = (info_child.attrs or {}).get('type') == 'group' or bool((info_child.attrs or {}).get('group-jid'))
                call['groupJid'] = (info_child.attrs or {}).get('group-jid')
                call_offer_cache.set(call['id'], call)

            existing_call = call_offer_cache.get(call['id'])

            # use existing call info to populate this event
            if existing_call:
                call['isVideo'] = existing_call.get('isVideo')
                call['isGroup'] = existing_call.get('isGroup')
                call['callerPn'] = call.get('callerPn') or existing_call.get('callerPn')

            # delete data once call has ended
            if status in ('reject', 'accept', 'timeout', 'terminate'):
                call_offer_cache.delete(call['id'])

            ev.emit('call', [call])
        except Exception as error:
            if logger is not None:
                logger.error({'error': error, 'node': binary_node_to_string(node)}, 'error in handling call')
        finally:
            try:
                await send_message_ack(node)
            except Exception as ack_err:
                if logger is not None:
                    logger.error({'ackErr': ack_err}, 'failed to ack call')

    async def handle_bad_ack(node):
        attrs = node.attrs or {}
        key = {'remoteJid': attrs.get('from'), 'fromMe': True, 'id': attrs.get('id')}

        # WARNING: REFRAIN FROM ENABLING THIS FOR NOW. IT WILL CAUSE A LOOP
        # if(attrs.phash) { ... }

        # error in acknowledgement, device could not display the message
        if attrs.get('error'):
            is_reachout_timelocked = attrs.get('error') == str(NACK_REASONS['SenderReachoutTimelocked'])

            if attrs.get('error') == SERVER_ERROR_CODES['MessageAccountRestriction']:
                # 463 = 1:1 message missing privacy token (tctoken). Usually means the account is restricted.
                if logger is not None:
                    logger.warn(
                        {'msgId': attrs.get('id'), 'from': attrs.get('from')},
                        'error 463: account restricted or missing tctoken for contact',
                    )

                ack_from = attrs.get('from')
                if ack_from and ack_from not in in_flight463_recoveries:
                    in_flight463_recoveries.add(ack_from)

                    async def _recover():
                        try:
                            get_pn_for_lid = signal_repository['lidMapping'].get_pn_for_lid
                            tc_storage_jid = await resolve_tc_token_jid(ack_from, get_lid_for_pn)
                            issue_jid = await resolve_issuance_jid(
                                ack_from,
                                messages_sock.get('serverProps', {}).get('lidTrustedTokenIssueToLid'),
                                get_lid_for_pn,
                                get_pn_for_lid,
                            )
                            result = await issue_privacy_tokens([issue_jid], unix_timestamp_seconds())
                            await store_tc_tokens_from_iq_result({
                                'result': result,
                                'fallbackJid': tc_storage_jid,
                                'keys': auth_state['keys'],
                                'getLIDForPN': get_lid_for_pn,
                                'onNewJidStored': track_tc_token_jid,
                            })
                            if logger is not None:
                                logger.debug({'from': ack_from}, 'completed 463 token recovery issuance')
                        except Exception as err:
                            if logger is not None:
                                logger.debug({'from': ack_from, 'err': getattr(err, 'message', err)}, 'failed 463 token recovery issuance')
                        finally:
                            in_flight463_recoveries.discard(ack_from)

                    asyncio.ensure_future(_recover())
            elif attrs.get('error') == SERVER_ERROR_CODES['SmaxInvalid']:
                if logger is not None:
                    logger.warn(
                        {'msgId': attrs.get('id'), 'from': attrs.get('from')},
                        'smax-invalid (479): stanza rejected by server — likely stale device session or malformed addressing',
                    )
            elif is_reachout_timelocked:
                # user is temporarily restricted, fetch current restriction details
                try:
                    await fetch_account_reachout_timelock()
                except Exception as err:
                    if logger is not None:
                        logger.warn({'err': err}, 'failed to fetch reachout timelock')
                if logger is not None:
                    logger.warn({'attrs': attrs}, 'received error in ack')
            else:
                if logger is not None:
                    logger.warn({'attrs': attrs}, 'received error in ack')

            ev.emit('messages.update', [
                {
                    'key': key,
                    'update': {
                        'status': WAMessageStatus.ERROR,
                        'messageStubParameters': [attrs.get('error'), ACCOUNT_RESTRICTED_TEXT] if is_reachout_timelocked else [attrs.get('error')],
                    },
                }
            ])

    # processes a node with the given function and buffers events
    async def process_node_with_buffer(node, identifier, exec_fn):
        ev.buffer()
        try:
            await exec_fn(node)
        except Exception as err:
            on_unexpected_error(err, identifier)
        finally:
            ev.flush()

    offline_node_processor = make_offline_node_processor(
        {
            'message': handle_message,
            'call': handle_call,
            'receipt': handle_receipt,
            'notification': handle_notification,
        },
        {
            'isWsOpen': lambda: ws.is_open,
            'onUnexpectedError': on_unexpected_error,
            'yieldToEventLoop': lambda: asyncio.sleep(0),
        },
    )

    async def process_node(type_, node, identifier, exec_):
        # Fast path: ack and drop ignored JIDs before entering the buffer/queue
        from_jid = (node.attrs or {}).get('from')
        ignore_jid = from_jid
        if type_ == 'receipt' and from_jid:
            attrs = node.attrs or {}
            is_lid = (attrs.get('from') or '').find('lid') > -1
            me_id = (auth_state['creds'].get('me') or {}).get('id')
            me_lid = (auth_state['creds'].get('me') or {}).get('lid')
            is_node_from_me = are_jids_same_user(
                attrs.get('participant') or attrs.get('from'),
                me_lid if is_lid else me_id,
            )
            ignore_jid = (attrs.get('from') if (not is_node_from_me or is_jid_group(attrs.get('from'))) else attrs.get('recipient'))

        if ignore_jid and ignore_jid != S_WHATSAPP_NET and should_ignore_jid(ignore_jid):
            await send_message_ack(node, NACK_REASONS['UnhandledError'] if type_ == 'message' else None)
            return

        is_offline = bool((node.attrs or {}).get('offline'))

        if is_offline:
            offline_node_processor['enqueue'](type_, node)
        else:
            await process_node_with_buffer(node, identifier, exec_)

    async def _on_message(node):
        await process_node('message', node, 'processing message', handle_message)

    async def _on_call(node):
        await process_node('call', node, 'handling call', handle_call)

    async def _on_receipt(node):
        await process_node('receipt', node, 'handling receipt', handle_receipt)

    async def _on_notification(node):
        await process_node('notification', node, 'handling notification', handle_notification)

    ws.on('CB:message', lambda node: asyncio.ensure_future(_on_message(node)))
    ws.on('CB:call', lambda node: asyncio.ensure_future(_on_call(node)))
    ws.on('CB:receipt', lambda node: asyncio.ensure_future(_on_receipt(node)))
    ws.on('CB:notification', lambda node: asyncio.ensure_future(_on_notification(node)))
    ws.on('CB:ack,class:message', lambda node: asyncio.ensure_future(_on_bad_ack(node)))

    async def _on_bad_ack(node):
        try:
            await handle_bad_ack(node)
        except Exception as error:
            on_unexpected_error(error, 'handling bad ack')

    async def _on_call_event(calls):
        call = calls[0] if calls else None
        if not call:
            return

        # missed call + group call notification message generation
        if call.get('status') == 'timeout' or (call.get('status') == 'offer' and call.get('isGroup')):
            msg = {
                'key': {
                    'remoteJid': call.get('chatId'),
                    'id': call.get('id'),
                    'fromMe': False,
                },
                'messageTimestamp': unix_timestamp_seconds(call.get('date')),
            }
            if call.get('status') == 'timeout':
                if call.get('isGroup'):
                    msg['messageStubType'] = WAMessageStubType.CALL_MISSED_GROUP_VIDEO if call.get('isVideo') else WAMessageStubType.CALL_MISSED_GROUP_VOICE
                else:
                    msg['messageStubType'] = WAMessageStubType.CALL_MISSED_VIDEO if call.get('isVideo') else WAMessageStubType.CALL_MISSED_VOICE
            else:
                msg['message'] = {'call': {'callKey': bytes(call.get('id'), 'utf-8')}}

            proto_msg = proto.WebMessageInfo.from_object(msg)
            await upsert_message(proto_msg, 'append' if call.get('offline') else 'notify')

    ev.on('call', lambda calls: asyncio.ensure_future(_on_call_event(calls)))

    # timestamp of last tctoken prune run — throttles to once per 24h
    last_tc_token_prune_ts = 0
    # dedupe in-flight 463 recovery token issuance by target JID
    in_flight463_recoveries = set()

    def _on_connection_update(update):
        nonlocal send_active_receipts, last_tc_token_prune_ts, tc_token_index_timer
        if 'isOnline' in update:
            send_active_receipts = update['isOnline']
            if logger is not None:
                logger.trace(f'sendActiveReceipts set to "{send_active_receipts}"')

        # Flush pending tctoken index save on disconnect to avoid writing after close
        if update.get('connection') == 'close' and tc_token_index_timer is not None:
            tc_token_index_timer.cancel()
            tc_token_index_timer = None
            # Best-effort flush — may fail if store is already closed
            try:
                asyncio.ensure_future(flush_tc_token_index())
            except Exception:
                pass

        # Prune expired tctokens when coming online, at most once per 24 hours
        if update.get('isOnline'):
            now = datetime.now(timezone.utc).timestamp() * 1000
            day_ms = 24 * 60 * 60 * 1000
            if now - last_tc_token_prune_ts >= day_ms:
                last_tc_token_prune_ts = now
                asyncio.ensure_future(prune_expired_tc_tokens())

    ev.on('connection.update', _on_connection_update)

    def _on_socket_end(error):
        nonlocal send_active_receipts
        if not config.get('msgRetryCounterCache') and hasattr(msg_retry_cache, 'clear'):
            msg_retry_cache.clear()

        if not config.get('callOfferCache') and hasattr(call_offer_cache, 'clear'):
            call_offer_cache.clear()

        identity_assert_debounce.clear()
        send_active_receipts = False

    register_socket_end_handler(_on_socket_end)

    async def prune_expired_tc_tokens():
        try:
            await tc_token_index_loaded

            # Union with the persisted index picks up JIDs added by other layers
            persisted = await read_tc_token_index(auth_state['keys'])
            all_jids = set(tc_token_known_jids)
            for jid in persisted:
                all_jids.add(jid)
            if not all_jids:
                return

            jids = list(all_jids)
            all_tokens = await auth_state['keys'].get('tctoken', jids)

            writes = {}
            survivors = set()
            mutated = 0

            for jid in jids:
                entry = all_tokens.get(jid)
                if not entry:
                    mutated += 1
                    continue

                has_peer_token = bool(entry.get('token'))
                peer_token_expired = has_peer_token and is_tc_token_expired(entry.get('timestamp'))
                has_sender_ts = entry.get('senderTimestamp') is not None
                sender_ts_expired = has_sender_ts and is_tc_token_expired(entry.get('senderTimestamp'))
                keep_peer_token = has_peer_token and not peer_token_expired
                keep_sender_ts = has_sender_ts and not sender_ts_expired

                if not keep_peer_token and not keep_sender_ts:
                    writes[jid] = None
                    mutated += 1
                elif peer_token_expired and keep_sender_ts:
                    writes[jid] = {'token': b'', 'senderTimestamp': entry.get('senderTimestamp')}
                    survivors.add(jid)
                    mutated += 1
                else:
                    survivors.add(jid)

            if mutated == 0:
                return

            await auth_state['keys'].set({
                'tctoken': {
                    **writes,
                    TC_TOKEN_INDEX_KEY: {
                        'token': json.dumps(list(survivors)).encode('utf-8'),
                    },
                }
            })

            tc_token_known_jids.clear()
            for jid in survivors:
                tc_token_known_jids.add(jid)

            if logger is not None:
                logger.debug({'mutated': mutated, 'remaining': len(survivors)}, 'pruned expired tctokens')
        except Exception as err:
            if logger is not None:
                logger.warn({'err': getattr(err, 'message', err)}, 'failed to prune expired tctokens')

    result = dict(messages_sock)
    result.update({
        'sendMessageAck': send_message_ack,
        'sendRetryRequest': send_retry_request,
        'rejectCall': reject_call,
        'fetchMessageHistory': fetch_message_history,
        'requestPlaceholderResend': request_placeholder_resend,
        'messageRetryManager': message_retry_manager,
        'handleMessage': handle_message,
        'handleCall': handle_call,
        'handleReceipt': handle_receipt,
        'handleNotification': handle_notification,
    })
    return result
