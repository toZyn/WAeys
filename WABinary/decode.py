"""Binary node decoder (ported from src/WABinary/decode.ts)."""

from __future__ import annotations

import zlib
from typing import List, Optional, Tuple

from . import constants
from .jid_utils import jid_encode, WAJIDDomains
from .types import BinaryNode


def decompressing_if_required(buffer: bytes) -> bytes:
    if 2 & buffer[0]:
        buffer = zlib.decompress(buffer[1:])
    else:
        buffer = buffer[1:]
    return buffer


def decode_decompressed_binary_node(buffer: bytes, opts=None, index_ref: Optional[list] = None) -> BinaryNode:
    if opts is None:
        opts = constants
    DOUBLE_BYTE_TOKENS = opts.DOUBLE_BYTE_TOKENS
    SINGLE_BYTE_TOKENS = opts.SINGLE_BYTE_TOKENS
    TAGS = opts.TAGS

    if index_ref is None:
        index_ref = [0]

    def check_eos(length: int):
        if index_ref[0] + length > len(buffer):
            raise ValueError('end of stream')

    def next():
        value = buffer[index_ref[0]]
        index_ref[0] += 1
        return value

    def read_byte() -> int:
        check_eos(1)
        return next()

    def read_bytes(n: int) -> bytes:
        check_eos(n)
        value = buffer[index_ref[0]:index_ref[0] + n]
        index_ref[0] += n
        return value

    def read_string_from_chars(length: int) -> str:
        return read_bytes(length).decode('utf-8')

    def read_int(n: int, little_endian: bool = False) -> int:
        check_eos(n)
        val = 0
        for i in range(n):
            shift = i if little_endian else n - 1 - i
            val |= next() << (shift * 8)
        return val

    def read_int20() -> int:
        check_eos(3)
        return ((next() & 15) << 16) + (next() << 8) + next()

    def unpack_hex(value: int) -> int:
        if 0 <= value < 16:
            return ord('0') + value if value < 10 else ord('A') + value - 10
        raise ValueError('invalid hex: ' + str(value))

    def unpack_nibble(value: int) -> int:
        if 0 <= value <= 9:
            return ord('0') + value
        if value == 10:
            return ord('-')
        if value == 11:
            return ord('.')
        if value == 15:
            return 0
        raise ValueError('invalid nibble: ' + str(value))

    def unpack_byte(tag: int, value: int) -> int:
        if tag == TAGS['NIBBLE_8']:
            return unpack_nibble(value)
        if tag == TAGS['HEX_8']:
            return unpack_hex(value)
        raise ValueError('unknown tag: ' + str(tag))

    def read_packed8(tag: int) -> str:
        start_byte = read_byte()
        value = ''
        for _ in range(start_byte & 127):
            cur_byte = read_byte()
            value += chr(unpack_byte(tag, (cur_byte & 0xF0) >> 4))
            value += chr(unpack_byte(tag, cur_byte & 0x0F))
        if start_byte >> 7 != 0:
            value = value[:-1]
        return value

    def is_list_tag(tag: int) -> bool:
        return tag == TAGS['LIST_EMPTY'] or tag == TAGS['LIST_8'] or tag == TAGS['LIST_16']

    def read_list_size(tag: int) -> int:
        if tag == TAGS['LIST_EMPTY']:
            return 0
        if tag == TAGS['LIST_8']:
            return read_byte()
        if tag == TAGS['LIST_16']:
            return read_int(2)
        raise ValueError('invalid tag for list size: ' + str(tag))

    def read_jid_pair() -> str:
        i = read_string(read_byte())
        j = read_string(read_byte())
        if j:
            return (i or '') + '@' + j
        raise ValueError(f'invalid jid pair: {i}, {j}')

    def read_ad_jid() -> str:
        raw_domain_type = read_byte()
        domain_type = raw_domain_type
        device = read_byte()
        user = read_string(read_byte())

        server = 's.whatsapp.net'
        if domain_type == WAJIDDomains.LID:
            server = 'lid'
        elif domain_type == WAJIDDomains.HOSTED:
            server = 'hosted'
        elif domain_type == WAJIDDomains.HOSTED_LID:
            server = 'hosted.lid'

        return jid_encode(user, server, device)

    def read_fb_jid() -> str:
        user = read_string(read_byte())
        device = read_int(2)
        server = read_string(read_byte())
        return f'{user}:{device}@{server}'

    def read_interop_jid() -> str:
        user = read_string(read_byte())
        device = read_int(2)
        integrator = read_int(2)
        server = 'interop'
        before_server = index_ref[0]
        try:
            server = read_string(read_byte())
        except Exception:
            index_ref[0] = before_server
        return f'{integrator}-{user}:{device}@{server}'

    def get_token_double(index1: int, index2: int) -> str:
        dict_ = DOUBLE_BYTE_TOKENS[index1] if index1 < len(DOUBLE_BYTE_TOKENS) else None
        if dict_ is None:
            raise ValueError(f'Invalid double token dict ({index1})')
        if index2 >= len(dict_):
            raise ValueError(f'Invalid double token ({index2})')
        return dict_[index2]

    def read_string(tag: int) -> str:
        if 1 <= tag < len(SINGLE_BYTE_TOKENS):
            return SINGLE_BYTE_TOKENS[tag] or ''
        if tag == TAGS['DICTIONARY_0']:
            return get_token_double(0, read_byte())
        if tag == TAGS['DICTIONARY_1']:
            return get_token_double(1, read_byte())
        if tag == TAGS['DICTIONARY_2']:
            return get_token_double(2, read_byte())
        if tag == TAGS['DICTIONARY_3']:
            return get_token_double(3, read_byte())
        if tag == TAGS['LIST_EMPTY']:
            return ''
        if tag == TAGS['BINARY_8']:
            return read_string_from_chars(read_byte())
        if tag == TAGS['BINARY_20']:
            return read_string_from_chars(read_int20())
        if tag == TAGS['BINARY_32']:
            return read_string_from_chars(read_int(4))
        if tag == TAGS['JID_PAIR']:
            return read_jid_pair()
        if tag == TAGS['FB_JID']:
            return read_fb_jid()
        if tag == TAGS['INTEROP_JID']:
            return read_interop_jid()
        if tag == TAGS['AD_JID']:
            return read_ad_jid()
        if tag == TAGS['HEX_8'] or tag == TAGS['NIBBLE_8']:
            return read_packed8(tag)
        raise ValueError('invalid string with tag: ' + str(tag))

    def read_list(tag: int) -> List[BinaryNode]:
        items: List[BinaryNode] = []
        size = read_list_size(tag)
        for _ in range(size):
            items.append(decode_decompressed_binary_node(buffer, opts, index_ref))
        return items

    list_size = read_list_size(read_byte())
    header = read_string(read_byte())
    if not list_size or not len(header):
        raise ValueError('invalid node')

    attrs = {}
    data = None

    # read the attributes in
    attributes_length = (list_size - 1) >> 1
    for _ in range(attributes_length):
        key = read_string(read_byte())
        value = read_string(read_byte())
        attrs[key] = value

    if list_size % 2 == 0:
        tag = read_byte()
        if is_list_tag(tag):
            data = read_list(tag)
        else:
            if tag == TAGS['BINARY_8']:
                data = read_bytes(read_byte())
            elif tag == TAGS['BINARY_20']:
                data = read_bytes(read_int20())
            elif tag == TAGS['BINARY_32']:
                data = read_bytes(read_int(4))
            else:
                data = read_string(tag)

    return BinaryNode(tag=header, attrs=attrs, content=data)


def decode_binary_node(buff: bytes) -> BinaryNode:
    decomp_buff = decompressing_if_required(buff)
    return decode_decompressed_binary_node(decomp_buff, constants)
