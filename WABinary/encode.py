"""Binary node encoder (ported from src/WABinary/encode.ts)."""

from __future__ import annotations

from typing import List, Optional

from . import constants
from .jid_utils import jid_decode


def encode_binary_node(node, opts=None, buffer: Optional[list] = None) -> bytes:
    if opts is None:
        opts = constants
    if buffer is None:
        buffer = [0]
    _encode_binary_node_inner(node, opts, buffer)
    return bytes(buffer)


def _encode_binary_node_inner(node, opts, buffer: list):
    TAGS = opts.TAGS
    TOKEN_MAP = opts.TOKEN_MAP

    def push_byte(value: int):
        buffer.append(value & 0xFF)

    def push_int(value: int, n: int, little_endian: bool = False):
        for i in range(n):
            cur_shift = i if little_endian else n - 1 - i
            buffer.append((value >> (cur_shift * 8)) & 0xFF)

    def push_bytes(bytes_list):
        for b in bytes_list:
            buffer.append(b)

    def push_int16(value: int):
        push_bytes([(value >> 8) & 0xFF, value & 0xFF])

    def push_int20(value: int):
        push_bytes([(value >> 16) & 0x0F, (value >> 8) & 0xFF, value & 0xFF])

    def write_byte_length(length: int):
        if length >= 4294967296:
            raise ValueError('string too large to encode: ' + str(length))
        if length >= 1 << 20:
            push_byte(TAGS['BINARY_32'])
            push_int(length, 4)
        elif length >= 256:
            push_byte(TAGS['BINARY_20'])
            push_int20(length)
        else:
            push_byte(TAGS['BINARY_8'])
            push_byte(length)

    def write_string_raw(s: str):
        data = s.encode('utf-8')
        write_byte_length(len(data))
        push_bytes(data)

    def write_jid(decoded):
        domain_type = decoded.domainType or 0
        device = decoded.device
        user = decoded.user
        if device is not None:
            push_byte(TAGS['AD_JID'])
            push_byte(domain_type)
            push_byte(device)
            write_string(user)
        else:
            push_byte(TAGS['JID_PAIR'])
            if len(user):
                write_string(user)
            else:
                push_byte(TAGS['LIST_EMPTY'])
            write_string(decoded.server)

    def pack_nibble(char: str) -> int:
        if char == '-':
            return 10
        if char == '.':
            return 11
        if char == '\0':
            return 15
        if '0' <= char <= '9':
            return ord(char) - ord('0')
        raise ValueError(f'invalid byte for nibble "{char}"')

    def pack_hex(char: str) -> int:
        if '0' <= char <= '9':
            return ord(char) - ord('0')
        if 'A' <= char <= 'F':
            return 10 + ord(char) - ord('A')
        if 'a' <= char <= 'f':
            return 10 + ord(char) - ord('a')
        if char == '\0':
            return 15
        raise ValueError(f'Invalid hex char "{char}"')

    def write_packed_bytes(s: str, type_: str):
        if len(s) > TAGS['PACKED_MAX']:
            raise ValueError('Too many bytes to pack')
        push_byte(TAGS['NIBBLE_8'] if type_ == 'nibble' else TAGS['HEX_8'])
        rounded_length = (len(s) + 1) // 2
        if len(s) % 2 != 0:
            rounded_length |= 128
        push_byte(rounded_length)
        pack_function = pack_nibble if type_ == 'nibble' else pack_hex

        def pack_byte_pair(v1: str, v2: str) -> int:
            return (pack_function(v1) << 4) | pack_function(v2)

        str_length_half = len(s) // 2
        for i in range(str_length_half):
            push_byte(pack_byte_pair(s[2 * i], s[2 * i + 1]))
        if len(s) % 2 != 0:
            push_byte(pack_byte_pair(s[-1], '\x00'))

    def is_nibble(s: Optional[str]) -> bool:
        if not s or len(s) > TAGS['PACKED_MAX']:
            return False
        for char in s:
            if not ('0' <= char <= '9') and char != '-' and char != '.':
                return False
        return True

    def is_hex(s: Optional[str]) -> bool:
        if not s or len(s) > TAGS['PACKED_MAX']:
            return False
        for char in s:
            if not ('0' <= char <= '9') and not ('A' <= char <= 'F'):
                return False
        return True

    def write_string(s: Optional[str]):
        if s is None:
            push_byte(TAGS['LIST_EMPTY'])
            return
        if s == '':
            write_string_raw(s)
            return

        token_index = TOKEN_MAP.get(s)
        if token_index is not None:
            dict_idx = token_index.get('dict')
            if isinstance(dict_idx, int):
                push_byte(TAGS['DICTIONARY_0'] + dict_idx)
            push_byte(token_index['index'])
        elif is_nibble(s):
            write_packed_bytes(s, 'nibble')
        elif is_hex(s):
            write_packed_bytes(s, 'hex')
        else:
            decoded_jid = jid_decode(s)
            if decoded_jid:
                write_jid(decoded_jid)
            else:
                write_string_raw(s)

    def write_list_start(list_size: int):
        if list_size == 0:
            push_byte(TAGS['LIST_EMPTY'])
        elif list_size < 256:
            push_bytes([TAGS['LIST_8'], list_size])
        else:
            push_byte(TAGS['LIST_16'])
            push_int16(list_size)

    if not node.tag:
        raise ValueError('Invalid node: tag cannot be undefined')

    attrs = node.attrs or {}
    valid_attributes = [k for k in attrs.keys() if attrs[k] is not None]

    content = node.content
    content_count = 1 if content is not None else 0
    write_list_start(2 * len(valid_attributes) + 1 + content_count)
    write_string(node.tag)

    for key in valid_attributes:
        if isinstance(attrs[key], str):
            write_string(key)
            write_string(attrs[key])

    if isinstance(content, str):
        write_string(content)
    elif isinstance(content, (bytes, bytearray)):
        write_byte_length(len(content))
        push_bytes(content)
    elif isinstance(content, list):
        valid_content = [
            item for item in content
            if item and (getattr(item, 'tag', None) or isinstance(item, (bytes, bytearray)) or isinstance(item, str))
        ]
        write_list_start(len(valid_content))
        for item in valid_content:
            if isinstance(item, (bytes, bytearray)):
                write_byte_length(len(item))
                push_bytes(item)
            elif isinstance(item, str):
                write_string(item)
            else:
                _encode_binary_node_inner(item, opts, buffer)
    elif content is None:
        pass
    else:
        raise ValueError(f'invalid children for header "{node.tag}": {content}')

    return buffer
