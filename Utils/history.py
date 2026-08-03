"""Port of src/Utils/history.ts — history sync processing."""

from __future__ import annotations

import zlib

from ..WABinary.jid_utils import is_hosted_lid_user, is_hosted_pn_user, is_lid_user, is_pn_user
from ..WAProto import WAProto as proto
from .generics import to_number
from .messages import normalize_message_content
from .messages_media import download_content_from_message

WAMessageStubType = proto.WebMessageInfo.StubType


def _extract_pn_from_messages(messages: list):
    for msg_item in messages:
        message = msg_item.get('message') or {}
        # Only extract from outgoing messages (fromMe: true) in 1:1 chats
        # because userReceipt.userJid is the recipient's JID
        if not message.get('key', {}).get('fromMe') or not message.get('userReceipt'):
            continue

        user_receipts = message.get('userReceipt') or []
        if not user_receipts:
            continue
        user_jid = (user_receipts[0] or {}).get('userJid')
        if user_jid and (is_pn_user(user_jid) or is_hosted_pn_user(user_jid)):
            return user_jid

    return None


def _inflate(data: bytes) -> bytes:
    return zlib.decompress(data)


def process_history_message(item: dict, logger=None) -> dict:
    messages = []
    contacts = []
    chats = []
    lid_pn_mappings = []

    if logger is not None:
        logger.trace({'progress': item.get('progress')}, 'processing history of type ' + str(item.get('syncType')))

    # Extract LID-PN mappings for all sync types
    for m in item.get('phoneNumberToLidMappings') or []:
        if m.get('lidJid') and m.get('pnJid'):
            lid_pn_mappings.append({'lid': m['lidJid'], 'pn': m['pnJid']})

    sync_type = item.get('syncType')
    initial_types = {
        proto.HistorySync.HistorySyncType.INITIAL_BOOTSTRAP,
        proto.HistorySync.HistorySyncType.RECENT,
        proto.HistorySync.HistorySyncType.FULL,
        proto.HistorySync.HistorySyncType.ON_DEMAND,
    }
    if sync_type in initial_types:
        for chat in list(item.get('conversations') or []):
            contacts.append({
                'id': chat.get('id'),
                'name': chat.get('displayName') or chat.get('name') or chat.get('username') or None,
                'username': chat.get('username') or None,
                'lid': chat.get('lidJid') or chat.get('accountLid') or None,
                'phoneNumber': chat.get('pnJid') or None,
            })

            chat_id = chat.get('id')
            is_lid = is_lid_user(chat_id) or is_hosted_lid_user(chat_id)
            is_pn = is_pn_user(chat_id) or is_hosted_pn_user(chat_id)
            if is_lid and chat.get('pnJid'):
                lid_pn_mappings.append({'lid': chat_id, 'pn': chat['pnJid']})
            elif is_pn and chat.get('lidJid'):
                lid_pn_mappings.append({'lid': chat['lidJid'], 'pn': chat_id})
            elif is_lid and not chat.get('pnJid'):
                # Fallback: extract PN from userReceipt in messages when pnJid is missing
                pn_from_receipt = _extract_pn_from_messages(chat.get('messages') or [])
                if pn_from_receipt:
                    lid_pn_mappings.append({'lid': chat_id, 'pn': pn_from_receipt})

            msgs = chat.get('messages') or []
            chat.pop('messages', None)

            for msg_item in msgs:
                message = msg_item.get('message')
                if message is None:
                    continue
                messages.append(message)

                if not chat.get('messages'):
                    # keep only the most recent message in the chat array
                    chat['messages'] = [{'message': message}]

                if not message.get('key', {}).get('fromMe') and not chat.get('lastMessageRecvTimestamp'):
                    chat['lastMessageRecvTimestamp'] = to_number(message.get('messageTimestamp'))

                stub_type = message.get('messageStubType')
                stub_params = message.get('messageStubParameters') or []
                if (
                    (stub_type == WAMessageStubType.BIZ_PRIVACY_MODE_TO_BSP
                     or stub_type == WAMessageStubType.BIZ_PRIVACY_MODE_TO_FB)
                    and stub_params
                    and stub_params[0]
                ):
                    contacts.append({
                        'id': message.get('key', {}).get('participant') or message.get('key', {}).get('remoteJid'),
                        'verifiedName': stub_params[0],
                    })

            chats.append(chat)
    elif sync_type == proto.HistorySync.HistorySyncType.PUSH_NAME:
        for c in item.get('pushnames') or []:
            contacts.append({'id': c.get('id'), 'notify': c.get('pushname')})

    return {
        'chats': chats,
        'contacts': contacts,
        'messages': messages,
        'lidPnMappings': lid_pn_mappings,
        'pastParticipants': item.get('pastParticipants'),
        'syncType': sync_type,
        'progress': item.get('progress'),
    }


async def download_history(msg, options=None):
    """Download and inflate a HistorySync blob described by a HistorySyncNotification.

    Returns a decoded proto.HistorySync.
    """
    if hasattr(msg, 'mediaKey'):
        msg = {
            'mediaKey': msg.mediaKey,
            'directPath': msg.directPath,
            'url': msg.url,
        }
    stream = await download_content_from_message(msg, 'md-msg-hist', {'options': options})
    chunks = [chunk async for chunk in stream]
    buffer = b''.join(chunks)
    sync_data = proto.HistorySync.decode(_inflate(buffer))
    return _history_to_dict(sync_data)


def _history_to_dict(sync_data) -> dict:
    """Convert a decoded proto.HistorySync into a plain dict."""
    from .decode_wa_message import _message_to_dict

    return _message_to_dict(sync_data)


async def download_and_process_history_sync_notification(msg, options=None, logger=None):
    if msg.get('initialHistBootstrapInlinePayload'):
        history_msg = proto.HistorySync.decode(_inflate(bytes(msg['initialHistBootstrapInlinePayload'])))
    else:
        history_msg = await download_history(msg, options)

    return process_history_message(history_msg, logger)


def get_history_msg(message) -> dict:
    normalized_content = normalize_message_content(message) if message else None
    if not normalized_content:
        return None
    protocol_message = normalized_content.get('protocolMessage')
    if not protocol_message:
        return None
    return protocol_message.get('historySyncNotification')
