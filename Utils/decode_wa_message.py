"""Port of src/Utils/decode-wa-message.ts — message stanza decoding/decryption."""

from __future__ import annotations

from ..WABinary.jid_utils import (
    are_jids_same_user,
    is_hosted_lid_user,
    is_hosted_pn_user,
    is_jid_broadcast,
    is_jid_group,
    is_jid_meta_ai,
    is_jid_newsletter,
    is_jid_status_broadcast,
    is_lid_user,
    is_pn_user,
)
from ..WAProto import WAProto as proto
from .generics import Boom, unpad_random_max16

NO_MESSAGE_FOUND_ERROR_TEXT = 'Message absent from node'
MISSING_KEYS_ERROR_TEXT = 'Key used already or never filled'
ACCOUNT_RESTRICTED_TEXT = 'Your account has been restricted'

# Retry configuration for failed decryption
DECRYPTION_RETRY_CONFIG = {
    'maxRetries': 3,
    'baseDelayMs': 100,
    'sessionRecordErrors': ['No session record', 'SessionError: No session record'],
}

# NACK reason codes we send to the server (client → server)
NACK_REASONS = {
    'SenderReachoutTimelocked': 463,
    'ParsingError': 487,
    'UnrecognizedStanza': 488,
    'UnrecognizedStanzaClass': 489,
    'UnrecognizedStanzaType': 490,
    'InvalidProtobuf': 491,
    'InvalidHostedCompanionStanza': 493,
    'MissingMessageSecret': 495,
    'SignalErrorOldCounter': 496,
    'MessageDeletedOnPeer': 499,
    'UnhandledError': 500,
    'UnsupportedAdminRevoke': 550,
    'UnsupportedLIDGroup': 551,
    'DBOperationFailed': 552,
}

# Server-side error codes returned in ack stanzas (server → client) that we
# currently have dedicated handlers for.
SERVER_ERROR_CODES = {
    'MessageAccountRestriction': '463',
    'SmaxInvalid': '479',
}


async def get_decryption_jid(sender: str, repository) -> str:
    if is_lid_user(sender) or is_hosted_lid_user(sender):
        return sender
    mapped = await repository['lidMapping'].get_lid_for_pn(sender)
    return mapped or sender


async def store_mapping_from_envelope(stanza, sender: str, repository, decryption_jid: str, logger) -> None:
    addressing_context = extract_addressing_context(stanza)
    sender_alt = addressing_context['senderAlt']

    if sender_alt and is_lid_user(sender_alt) and is_pn_user(sender) and decryption_jid == sender:
        try:
            await repository['lidMapping'].store_lidpn_mappings([{'lid': sender_alt, 'pn': sender}])
            await repository['migrateSession'](sender, sender_alt)
            logger.debug({'sender': sender, 'senderAlt': sender_alt}, 'Stored LID mapping from envelope')
        except Exception as error:
            logger.warn({'sender': sender, 'senderAlt': sender_alt, 'error': error}, 'Failed to store LID mapping')


def extract_addressing_context(stanza) -> dict:
    sender_alt = None
    recipient_alt = None

    attrs = stanza.attrs or {}
    sender = attrs.get('participant') or attrs.get('from')
    addressing_mode = attrs.get('addressing_mode') or ('lid' if (sender or '').endswith('lid') else 'pn')

    if addressing_mode == 'lid':
        sender_alt = attrs.get('participant_pn') or attrs.get('sender_pn') or attrs.get('peer_recipient_pn')
        recipient_alt = attrs.get('recipient_pn')
    else:
        sender_alt = attrs.get('participant_lid') or attrs.get('sender_lid') or attrs.get('peer_recipient_lid')
        recipient_alt = attrs.get('recipient_lid')

    return {'addressingMode': addressing_mode, 'senderAlt': sender_alt, 'recipientAlt': recipient_alt}


def decode_message_node(stanza, me_id: str, me_lid: str) -> dict:
    attrs = stanza.attrs or {}

    msg_id = attrs.get('id')
    from_jid = attrs.get('from')
    participant = attrs.get('participant')
    recipient = attrs.get('recipient')

    if not msg_id:
        raise Boom('Invalid message stanza: missing id attribute', data=stanza)

    if not from_jid:
        raise Boom('Invalid message stanza: missing from attribute', data=stanza)

    addressing_context = extract_addressing_context(stanza)

    is_me = lambda jid: are_jids_same_user(jid, me_id)
    is_me_lid = lambda jid: are_jids_same_user(jid, me_lid)

    from_me = False
    chat_id = None
    author = None
    msg_type = None

    if is_pn_user(from_jid) or is_lid_user(from_jid) or is_hosted_lid_user(from_jid) or is_hosted_pn_user(from_jid):
        if recipient and not is_jid_meta_ai(recipient):
            if not is_me(from_jid) and not is_me_lid(from_jid):
                raise Boom('receipient present, but msg not from me', data=stanza)

            if is_me(from_jid) or is_me_lid(from_jid):
                from_me = True

            chat_id = recipient
        else:
            if is_me(from_jid) or is_me_lid(from_jid):
                from_me = True

            chat_id = from_jid

        msg_type = 'chat'
        author = from_jid
    elif is_jid_group(from_jid):
        if not participant:
            raise Boom('No participant in group message')

        if is_me(participant) or is_me_lid(participant):
            from_me = True

        msg_type = 'group'
        author = participant
        chat_id = from_jid
    elif is_jid_broadcast(from_jid):
        if not participant:
            raise Boom('No participant in group message')

        is_participant_me = is_me(participant)
        if is_jid_status_broadcast(from_jid):
            msg_type = 'direct_peer_status' if is_participant_me else 'other_status'
        else:
            msg_type = 'peer_broadcast' if is_participant_me else 'other_broadcast'

        from_me = is_participant_me
        chat_id = from_jid
        author = participant
    elif is_jid_newsletter(from_jid):
        msg_type = 'newsletter'
        chat_id = from_jid
        author = from_jid

        if is_me(from_jid) or is_me_lid(from_jid):
            from_me = True
    else:
        raise Boom('Unknown message type', data=stanza)

    pushname = attrs.get('notify')

    key = {
        'remoteJid': chat_id,
        'remoteJidAlt': addressing_context['senderAlt'] if not is_jid_group(chat_id) else None,
        'remoteJidUsername': (
            attrs.get('peer_recipient_username') or attrs.get('recipient_username')
            if not is_jid_group(chat_id)
            else None
        ),
        'fromMe': from_me,
        'id': msg_id,
        'participant': participant,
        'participantAlt': addressing_context['senderAlt'] if is_jid_group(chat_id) else None,
        'participantUsername': attrs.get('participant_username') if participant else None,
        'addressingMode': addressing_context['addressingMode'],
    }
    if msg_type == 'newsletter' and attrs.get('server_id'):
        key['server_id'] = attrs['server_id']

    full_message = {
        'key': key,
        'category': attrs.get('category'),
        'messageTimestamp': int(attrs['t']) if attrs.get('t') else None,
        'pushName': pushname,
        'broadcast': is_jid_broadcast(from_jid),
    }

    if key['fromMe']:
        full_message['status'] = proto.WebMessageInfo.Status.SERVER_ACK

    return {'fullMessage': full_message, 'author': author, 'sender': author if msg_type == 'chat' else chat_id}


def decrypt_message_node(stanza, me_id: str, me_lid: str, repository, logger):
    result = decode_message_node(stanza, me_id, me_lid)
    full_message = result['fullMessage']
    author = result['author']
    sender = result['sender']

    async def decrypt():
        decryptables = 0
        if isinstance(stanza.content, list):
            for child in stanza.content:
                tag = child.tag
                attrs = child.attrs or {}
                content = child.content

                if tag == 'verified_name' and isinstance(content, bytes):
                    cert = proto.VerifiedNameCertificate.decode(content)
                    details = cert.details
                    if isinstance(details, bytes):
                        details = proto.VerifiedNameCertificate.Details.decode(details)
                    full_message['verifiedBizName'] = details.verifiedName

                if tag == 'unavailable' and attrs.get('type') == 'view_once':
                    full_message['key']['isViewOnce'] = True

                if attrs.get('count') and tag == 'enc':
                    full_message['retryCount'] = int(attrs['count'])

                if tag != 'enc' and tag != 'plaintext':
                    continue

                if not isinstance(content, bytes):
                    continue

                decryptables += 1

                decryption_jid = await get_decryption_jid(author, repository)

                if tag != 'plaintext':
                    await store_mapping_from_envelope(stanza, author, repository, decryption_jid, logger)

                try:
                    e2e_type = 'plaintext' if tag == 'plaintext' else attrs.get('type')

                    if e2e_type == 'skmsg':
                        msg_buffer = await repository['decryptGroupMessage']({
                            'group': sender,
                            'authorJid': author,
                            'msg': content,
                        })
                    elif e2e_type == 'pkmsg' or e2e_type == 'msg':
                        msg_buffer = await repository['decryptMessage']({
                            'jid': decryption_jid,
                            'type': e2e_type,
                            'ciphertext': content,
                        })
                    elif e2e_type == 'plaintext':
                        msg_buffer = content
                    else:
                        raise Exception(f'Unknown e2e type: {e2e_type}')

                    msg = proto.Message.decode(unpad_random_max16(msg_buffer) if e2e_type != 'plaintext' else msg_buffer)
                    msg = msg.deviceSentMessage.message if getattr(msg, 'deviceSentMessage', None) else msg
                    if getattr(msg, 'senderKeyDistributionMessage', None):
                        try:
                            await repository['processSenderKeyDistributionMessage']({
                                'authorJid': author,
                                'item': msg.senderKeyDistributionMessage,
                            })
                        except Exception as err:
                            logger.error({'key': full_message['key'], 'err': err}, 'failed to process sender key distribution message')

                    if full_message.get('message'):
                        full_message['message'].update(_message_to_dict(msg))
                    else:
                        full_message['message'] = _message_to_dict(msg)
                except Exception as err:
                    error_context = {
                        'key': full_message['key'],
                        'err': err,
                        'messageType': 'plaintext' if tag == 'plaintext' else attrs.get('type'),
                        'sender': sender,
                        'author': author,
                        'isSessionRecordError': is_session_record_error(err),
                    }

                    logger.error(error_context, 'failed to decrypt message')

                    full_message['messageStubType'] = proto.WebMessageInfo.StubType.CIPHERTEXT
                    full_message['messageStubParameters'] = [str(getattr(err, 'message', None) or err)]

        if not decryptables and not full_message.get('key', {}).get('isViewOnce'):
            full_message['messageStubType'] = proto.WebMessageInfo.StubType.CIPHERTEXT
            full_message['messageStubParameters'] = [NO_MESSAGE_FOUND_ERROR_TEXT]

    return {
        'fullMessage': full_message,
        'category': stanza.attrs.get('category') if stanza.attrs else None,
        'author': author,
        'decrypt': decrypt,
    }


def _message_to_dict(msg) -> dict:
    """Convert a decoded proto Message into a plain dict of set fields.

    The port represents message content as nested dicts (see normalize_message_content),
    so sub-messages are converted recursively.
    """
    if isinstance(msg, dict):
        return msg
    out = {}
    for name in getattr(msg, 'FIELDS', {}):
        value = getattr(msg, name, None)
        if value is not None:
            out[name] = _proto_value_to_dict(value)
    return out


def _proto_value_to_dict(value):
    from ..WAProto.runtime import Message as _ProtoBase

    if isinstance(value, _ProtoBase):
        return _message_to_dict(value)
    if isinstance(value, list):
        return [_proto_value_to_dict(v) for v in value]
    if isinstance(value, dict):
        return {k: _proto_value_to_dict(v) for k, v in value.items()}
    if isinstance(value, int) and hasattr(value, 'name') and type(value).__name__.endswith('Enum'):
        return int(value)
    return value


def is_session_record_error(error) -> bool:
    error_message = getattr(error, 'message', None) or str(error) or ''
    return any(pattern in error_message for pattern in DECRYPTION_RETRY_CONFIG['sessionRecordErrors'])
