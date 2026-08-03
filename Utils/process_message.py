"""Port of src/Utils/process-message.ts — message processing helpers."""

from __future__ import annotations

from ..WABinary.jid_utils import (
    are_jids_same_user,
    is_hosted_lid_user,
    is_hosted_pn_user,
    is_jid_broadcast,
    is_jid_status_broadcast,
    jid_decode,
    jid_encode,
    jid_normalized_user,
)
from .generics import Boom
from .messages import get_content_type, normalize_message_content

REAL_MSG_STUB_TYPES = {
    'CIPHERTEXT',
    'REVOKE',
    'GROUP_MEMBERSHIP_JOIN',
    'GROUP_MEMBERSHIP_LEAVE',
    'GROUP_MEMBERSHIP_INVITE',
    'GROUP_MEMBERSHIP_REQUEST_JOIN',
    'GROUP_MEMBERSHIP_REQUEST_REJECT',
    'GROUP_MEMBERSHIP_REQUEST_LEAVE',
    'CHANGE_EPHEMERAL_SETTING',
    'E2E_IDENTITY_CHANGED',
    'GROUP_PARENT_CHANGED',
    'GROUP_PARENT_REMOVED',
    'NEW_DEVICE_INITIAL',
}

REAL_MSG_REQ_ME_STUB_TYPES = {
    'GROUP_MEMBERSHIP_JOIN',
    'GROUP_MEMBERSHIP_LEAVE',
    'GROUP_MEMBERSHIP_INVITE',
    'GROUP_MEMBERSHIP_REQUEST_JOIN',
    'GROUP_MEMBERSHIP_REQUEST_REJECT',
    'GROUP_MEMBERSHIP_REQUEST_LEAVE',
    'CHANGE_EPHEMERAL_SETTING',
    'E2E_IDENTITY_CHANGED',
    'GROUP_PARENT_CHANGED',
    'GROUP_PARENT_REMOVED',
}


def clean_message(message: dict, me_id: str, me_lid: str) -> None:
    key = message.get('key') or {}
    remote_jid = key.get('remoteJid')
    if remote_jid:
        if is_hosted_pn_user(remote_jid) or is_hosted_lid_user(remote_jid):
            decoded = jid_decode(remote_jid)
            server = 's.whatsapp.net' if is_hosted_pn_user(remote_jid) else 'lid'
            key['remoteJid'] = jid_encode(decoded.user if decoded else None, server)
        else:
            key['remoteJid'] = jid_normalized_user(remote_jid)

    participant = key.get('participant')
    if participant:
        if is_hosted_pn_user(participant) or is_hosted_lid_user(participant):
            decoded = jid_decode(participant)
            server = 's.whatsapp.net' if is_hosted_pn_user(participant) else 'lid'
            key['participant'] = jid_encode(decoded.user if decoded else None, server)
        else:
            key['participant'] = jid_normalized_user(participant)

    content = normalize_message_content(message.get('message'))
    if content and content.get('reactionMessage'):
        normalise_key(content['reactionMessage'].get('key'), message, me_id, me_lid)
    if content and content.get('pollUpdateMessage'):
        normalise_key(content['pollUpdateMessage'].get('pollCreationMessageKey'), message, me_id, me_lid)


def normalise_key(msg_key: dict, message: dict, me_id: str, me_lid: str) -> None:
    if not message.get('key', {}).get('fromMe'):
        from_me = msg_key.get('fromMe')
        msg_key['fromMe'] = (
            (not from_me)
            and (
                are_jids_same_user(msg_key.get('participant') or msg_key.get('remoteJid'), me_id)
                or are_jids_same_user(msg_key.get('participant') or msg_key.get('remoteJid'), me_lid)
            )
        ) if not from_me else False
        msg_key['remoteJid'] = message.get('key', {}).get('remoteJid')
        if not msg_key.get('participant'):
            msg_key['participant'] = message.get('key', {}).get('participant')


def is_real_message(message: dict) -> bool:
    normalized_content = normalize_message_content(message.get('message'))
    has_some_content = get_content_type(normalized_content) is not None
    stub_type = message.get('messageStubType')
    return (
        (
            normalized_content is not None
            or stub_type in REAL_MSG_STUB_TYPES
            or stub_type in REAL_MSG_REQ_ME_STUB_TYPES
        )
        and has_some_content
        and not (normalized_content or {}).get('protocolMessage')
        and not (normalized_content or {}).get('reactionMessage')
        and not (normalized_content or {}).get('pollUpdateMessage')
    )


def should_increment_chat_unread(message: dict) -> bool:
    key = message.get('key') or {}
    return not key.get('fromMe') and not message.get('messageStubType')


def get_chat_id(msg_key: dict) -> str:
    remote_jid = msg_key.get('remoteJid')
    participant = msg_key.get('participant')
    from_me = msg_key.get('fromMe')
    if not remote_jid:
        raise Boom(
            'Cannot derive chat id: message key is missing remoteJid',
            data={'remoteJid': remote_jid, 'participant': participant, 'fromMe': from_me},
        )
    if is_jid_broadcast(remote_jid) and not is_jid_status_broadcast(remote_jid) and not from_me:
        return participant or remote_jid
    return remote_jid
