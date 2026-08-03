"""Port of src/Utils/reporting-utils.ts — reporting token helpers."""

from __future__ import annotations

import hmac
import hashlib

from ..WABinary.types import BinaryNode
from .crypto import hkdf

ENC_SECRET_REPORT_TOKEN = 'Report Token'

WIRE = {
    'VARINT': 0,
    'FIXED64': 1,
    'BYTES': 2,
    'FIXED32': 5,
}


def should_include_reporting_token(message) -> bool:
    if hasattr(message, 'reactionMessage'):
        return not message.reactionMessage and not getattr(message, 'encReactionMessage', None) \
            and not getattr(message, 'encEventResponseMessage', None) and not getattr(message, 'pollUpdateMessage', None)
    message = message or {}
    return (
        not message.get('reactionMessage')
        and not message.get('encReactionMessage')
        and not message.get('encEventResponseMessage')
        and not message.get('pollUpdateMessage')
    )


def _generate_msg_secret_key(
    modification_type: str,
    orig_msg_id: str,
    orig_msg_sender: str,
    modification_sender: str,
    orig_msg_secret: bytes,
) -> bytes:
    use_case_secret = (
        orig_msg_id.encode('utf-8')
        + orig_msg_sender.encode('utf-8')
        + modification_sender.encode('utf-8')
        + modification_type.encode('utf-8')
    )
    return hkdf(bytes(orig_msg_secret), 32, info=use_case_secret.decode('latin1'))


def _decode_varint(buffer: bytes, offset: int) -> dict:
    value = 0
    bytes_ = 0
    shift = 0

    while offset + bytes_ < len(buffer):
        current = buffer[offset + bytes_]
        value |= (current & 0x7F) << shift
        bytes_ += 1

        if (current & 0x80) == 0:
            return {'value': value, 'bytes': bytes_, 'ok': True}

        shift += 7

        if shift > 35:
            return {'value': 0, 'bytes': 0, 'ok': False}

    return {'value': 0, 'bytes': 0, 'ok': False}


def _encode_varint(value: int) -> bytes:
    parts = []
    remaining = value & 0xFFFFFFFF

    while remaining > 0x7F:
        parts.append((remaining & 0x7F) | 0x80)
        remaining >>= 7

    parts.append(remaining)
    return bytes(parts)


def _compile_reporting_fields(fields: list) -> dict:
    out = {}
    for f in fields:
        out[f['f']] = {
            'm': f.get('m'),
            'children': _compile_reporting_fields(f['s']) if f.get('s') else None,
        }
    return out


_reporting_fields = [
    {'f': 1},
    {'f': 3, 's': [{'f': 2}, {'f': 3}, {'f': 8}, {'f': 11}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}, {'f': 25}]},
    {'f': 4, 's': [{'f': 1}, {'f': 16}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}]},
    {'f': 5, 's': [{'f': 3}, {'f': 4}, {'f': 5}, {'f': 16}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}]},
    {'f': 6, 's': [{'f': 1}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}, {'f': 30}]},
    {'f': 7, 's': [{'f': 2}, {'f': 7}, {'f': 10}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}, {'f': 20}]},
    {'f': 8, 's': [{'f': 2}, {'f': 7}, {'f': 9}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}, {'f': 21}]},
    {'f': 9, 's': [{'f': 2}, {'f': 6}, {'f': 7}, {'f': 13}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}, {'f': 20}]},
    {'f': 12, 's': [{'f': 1}, {'f': 2}, {'f': 14, 'm': True}, {'f': 15}]},
    {'f': 18, 's': [{'f': 6}, {'f': 16}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}]},
    {'f': 26, 's': [{'f': 4}, {'f': 5}, {'f': 8}, {'f': 13}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}]},
    {'f': 28, 's': [{'f': 1}, {'f': 2}, {'f': 4}, {'f': 5}, {'f': 6}, {'f': 7, 's': [{'f': 21}, {'f': 22}]}]},
    {'f': 37, 's': [{'f': 1, 'm': True}]},
    {
        'f': 49,
        's': [
            {'f': 2},
            {'f': 3, 's': [{'f': 1}, {'f': 2}]},
            {'f': 5, 's': [{'f': 21}, {'f': 22}]},
            {'f': 8, 's': [{'f': 1}, {'f': 2}]},
        ],
    },
    {'f': 53, 's': [{'f': 1, 'm': True}]},
    {'f': 55, 's': [{'f': 1, 'm': True}]},
    {'f': 58, 's': [{'f': 1, 'm': True}]},
    {'f': 59, 's': [{'f': 1, 'm': True}]},
    {
        'f': 60,
        's': [
            {'f': 2},
            {'f': 3, 's': [{'f': 1}, {'f': 2}]},
            {'f': 5, 's': [{'f': 21}, {'f': 22}]},
            {'f': 8, 's': [{'f': 1}, {'f': 2}]},
        ],
    },
    {
        'f': 64,
        's': [
            {'f': 2},
            {'f': 3, 's': [{'f': 1}, {'f': 2}]},
            {'f': 5, 's': [{'f': 21}, {'f': 22}]},
            {'f': 8, 's': [{'f': 1}, {'f': 2}]},
        ],
    },
    {'f': 66, 's': [{'f': 2}, {'f': 6}, {'f': 7}, {'f': 13}, {'f': 17, 's': [{'f': 21}, {'f': 22}]}, {'f': 20}]},
    {'f': 74, 's': [{'f': 1, 'm': True}]},
    {'f': 87, 's': [{'f': 1, 'm': True}]},
    {'f': 88, 's': [{'f': 1}, {'f': 2, 's': [{'f': 1}]}, {'f': 3, 's': [{'f': 21}, {'f': 22}]}]},
    {'f': 92, 's': [{'f': 1, 'm': True}]},
    {'f': 93, 's': [{'f': 1, 'm': True}]},
    {'f': 94, 's': [{'f': 1, 'm': True}]},
]

_compiled_reporting_fields = _compile_reporting_fields(_reporting_fields)
_EMPTY_MAP = {}


def _extract_reporting_token_content(data: bytes, cfg: dict):
    out = []
    i = 0

    while i < len(data):
        tag = _decode_varint(data, i)
        if not tag['ok']:
            return None

        field_num = tag['value'] >> 3
        wire_type = tag['value'] & 0x7

        field_start = i
        i += tag['bytes']

        field_cfg = cfg.get(field_num)

        if wire_type == WIRE['VARINT']:
            v = _decode_varint(data, i)
            if not v['ok']:
                return None
            end = i + v['bytes']
            if not field_cfg:
                i = end
                continue
            if end > len(data):
                return None
            out.append({'num': field_num, 'bytes': data[field_start:end]})
            i = end
            continue

        if wire_type == WIRE['FIXED64']:
            end = i + 8
            if not field_cfg:
                if end > len(data):
                    return None
                i = end
                continue
            if end > len(data):
                return None
            out.append({'num': field_num, 'bytes': data[field_start:end]})
            i = end
            continue

        if wire_type == WIRE['FIXED32']:
            end = i + 4
            if not field_cfg:
                if end > len(data):
                    return None
                i = end
                continue
            if end > len(data):
                return None
            out.append({'num': field_num, 'bytes': data[field_start:end]})
            i = end
            continue

        if wire_type == WIRE['BYTES']:
            length = _decode_varint(data, i)
            if not length['ok']:
                return None
            val_start = i + length['bytes']
            val_end = val_start + length['value']
            if val_end > len(data):
                return None

            if not field_cfg:
                i = val_end
                continue

            if field_cfg.get('m') or field_cfg.get('children'):
                sub = _extract_reporting_token_content(
                    data[val_start:val_end], field_cfg.get('children') or _EMPTY_MAP
                )
                if sub is None:
                    return None
                if len(sub) > 0:
                    new_tag = _encode_varint(tag['value'])
                    new_len = _encode_varint(len(sub))
                    out.append({'num': field_num, 'bytes': new_tag + new_len + sub})
                i = val_end
                continue

            out.append({'num': field_num, 'bytes': data[field_start:val_end]})
            i = val_end
            continue

        return None

    if len(out) == 0:
        return b''

    out.sort(key=lambda x: x['num'])
    return b''.join(x['bytes'] for x in out)


async def get_message_reporting_token(msg_protobuf: bytes, message: dict, key: dict):
    msg_secret = None
    if message.get('messageContextInfo'):
        msg_secret = message['messageContextInfo'].get('messageSecret')
    if not msg_secret or not key.get('id'):
        return None

    from_jid = key['remoteJid'] if key.get('fromMe') else key.get('participant') or key['remoteJid']
    to_jid = key.get('participant') or key['remoteJid'] if key.get('fromMe') else key['remoteJid']

    reporting_secret = _generate_msg_secret_key(ENC_SECRET_REPORT_TOKEN, key['id'], from_jid, to_jid, msg_secret)

    content = _extract_reporting_token_content(bytes(msg_protobuf), _compiled_reporting_fields)
    if not content or len(content) == 0:
        return None

    reporting_token = hmac.new(reporting_secret, content, hashlib.sha256).digest()[:16]

    return BinaryNode(
        tag='reporting',
        attrs={},
        content=[
            BinaryNode(
                tag='reporting_token',
                attrs={'v': '2'},
                content=reporting_token,
            )
        ],
    )
