"""Port of src/WAM/encode.ts — encodeWAM."""

from __future__ import annotations

import struct

from .constants import (
    FLAG_BYTE,
    FLAG_EVENT,
    FLAG_EXTENDED,
    FLAG_FIELD,
    FLAG_GLOBAL,
    WEB_EVENTS,
    WEB_GLOBALS,
)


def _get_header_bit_length(key: int) -> int:
    return 2 if key < 256 else 3


def encode_wam(binary_info) -> bytes:
    binary_info.buffer = []

    _encode_wam_header(binary_info)
    _encode_events(binary_info)

    total_size = sum(len(a) for a in binary_info.buffer)
    out = bytearray(total_size)
    offset = 0
    for chunk in binary_info.buffer:
        out[offset:offset + len(chunk)] = chunk
        offset += len(chunk)

    return bytes(out)


def _encode_wam_header(binary_info):
    header = bytearray(8)
    header[0:3] = b'WAM'
    header[3] = binary_info.protocolVersion
    header[4] = 1  # random flag
    struct.pack_into('>H', header, 5, binary_info.sequence)
    header[7] = 0  # regular channel
    binary_info.buffer.append(bytes(header))


def _encode_global_attributes(binary_info, globals_):
    for key, value in globals_.items():
        gid = next((g['id'] for g in WEB_GLOBALS if g.get('name') == key), None)
        if gid is None:
            continue
        if isinstance(value, bool):
            value = 1 if value else 0
        binary_info.buffer.append(_serialize_data(gid, value, FLAG_GLOBAL))


def _encode_events(binary_info):
    for event_obj in binary_info.events:
        name = next(iter(event_obj))
        props, globals_ = event_obj[name]['props'], event_obj[name].get('globals', {})
        _encode_global_attributes(binary_info, globals_)

        event = next((e for e in WEB_EVENTS if e.get('name') == name), None)
        if event is None:
            continue

        props_items = list(props.items())

        extended = any(value is not None for _, value in props_items)

        event_flag = FLAG_EVENT if extended else FLAG_EVENT | FLAG_EXTENDED
        binary_info.buffer.append(_serialize_data(event['id'], -event['weight'], event_flag))

        for i, (key, value) in enumerate(props_items):
            prop_def = event.get('props', {}).get(key)
            if prop_def is None:
                continue
            prop_id = prop_def[0]
            extended = i < len(props_items) - 1
            if isinstance(value, bool):
                value = 1 if value else 0
            field_flag = FLAG_EVENT if extended else FLAG_FIELD | FLAG_EXTENDED
            binary_info.buffer.append(_serialize_data(prop_id, value, field_flag))


def _serialize_data(key: int, value, flag: int) -> bytes:
    buffer_length = _get_header_bit_length(key)

    if value is None:
        if flag == FLAG_GLOBAL:
            out = bytearray(buffer_length)
            _serialize_header(out, 0, key, flag)
            return bytes(out)
    elif isinstance(value, int) and not isinstance(value, bool):
        if value in (0, 1):
            out = bytearray(buffer_length)
            _serialize_header(out, 0, key, flag | ((value + 1) << 4))
            return bytes(out)
        elif -128 <= value < 128:
            out = bytearray(buffer_length + 1)
            offset = _serialize_header(out, 0, key, flag | (3 << 4))
            struct.pack_into('<b', out, offset, value)
            return bytes(out)
        elif -32768 <= value < 32768:
            out = bytearray(buffer_length + 2)
            offset = _serialize_header(out, 0, key, flag | (4 << 4))
            struct.pack_into('<h', out, offset, value)
            return bytes(out)
        elif -2147483648 <= value < 2147483648:
            out = bytearray(buffer_length + 4)
            offset = _serialize_header(out, 0, key, flag | (5 << 4))
            struct.pack_into('<i', out, offset, value)
            return bytes(out)
        else:
            out = bytearray(buffer_length + 8)
            offset = _serialize_header(out, 0, key, flag | (7 << 4))
            struct.pack_into('<d', out, offset, float(value))
            return bytes(out)
    elif isinstance(value, float):
        out = bytearray(buffer_length + 8)
        offset = _serialize_header(out, 0, key, flag | (7 << 4))
        struct.pack_into('<d', out, offset, value)
        return bytes(out)
    elif isinstance(value, str):
        utf8_bytes = len(value.encode('utf-8'))
        if utf8_bytes < 256:
            out = bytearray(buffer_length + 1 + utf8_bytes)
            offset = _serialize_header(out, 0, key, flag | (8 << 4))
            out[offset] = utf8_bytes
            offset += 1
        elif utf8_bytes < 65536:
            out = bytearray(buffer_length + 2 + utf8_bytes)
            offset = _serialize_header(out, 0, key, flag | (9 << 4))
            struct.pack_into('<H', out, offset, utf8_bytes)
            offset += 2
        else:
            out = bytearray(buffer_length + 4 + utf8_bytes)
            offset = _serialize_header(out, 0, key, flag | (10 << 4))
            struct.pack_into('<I', out, offset, utf8_bytes)
            offset += 4
        out[offset:offset + utf8_bytes] = value.encode('utf-8')
        return bytes(out)

    raise ValueError(f'missing value: {value!r}')


def _serialize_header(buffer: bytearray, offset: int, key: int, flag: int) -> int:
    if key < 256:
        buffer[offset] = flag
        offset += 1
        buffer[offset] = key
        offset += 1
    else:
        buffer[offset] = flag | FLAG_BYTE
        offset += 1
        struct.pack_into('<H', buffer, offset, key)
        offset += 2
    return offset
