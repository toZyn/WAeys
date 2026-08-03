"""Generic binary node utilities (ported from src/WABinary/generic-utils.ts)."""

from __future__ import annotations

from typing import List, Optional

from .types import BinaryNode


def get_binary_node_children(node: Optional[BinaryNode], child_tag: str) -> List[BinaryNode]:
    if not node or not isinstance(node.content, list):
        return []
    return [child for child in node.content if isinstance(child, BinaryNode) and child.tag == child_tag]


def get_binary_node_child(node: Optional[BinaryNode], child_tag: str) -> Optional[BinaryNode]:
    children = get_binary_node_children(node, child_tag)
    return children[0] if children else None


def get_all_binary_node_children(node: BinaryNode) -> List[BinaryNode]:
    if isinstance(node.content, list):
        return node.content
    return []


def get_binary_node_child_buffer(node: Optional[BinaryNode], child_tag: str) -> Optional[bytes]:
    child = get_binary_node_child(node, child_tag)
    if child and isinstance(child.content, (bytes, bytearray)):
        return bytes(child.content)
    return None


def get_binary_node_child_string(node: Optional[BinaryNode], child_tag: str) -> Optional[str]:
    child = get_binary_node_child(node, child_tag)
    if child is None:
        return None
    if isinstance(child.content, (bytes, bytearray)):
        return bytes(child.content).decode('utf-8')
    if isinstance(child.content, str):
        return child.content
    return None


def get_binary_node_child_uint(node: BinaryNode, child_tag: str, length: int) -> Optional[int]:
    buff = get_binary_node_child_buffer(node, child_tag)
    if buff:
        return buffer_to_uint(buff, length)
    return None


class BoomError(Exception):
    """Python counterpart of @hapi/boom errors."""

    def __init__(self, message: str, status_code: int = 500, data=None):
        super().__init__(message)
        self.message = message
        self.statusCode = status_code
        self.output = {'statusCode': status_code, 'data': data}

    def __repr__(self):
        return f'BoomError({self.message!r}, statusCode={self.output["statusCode"]})'


def assert_node_error_free(node: BinaryNode):
    err_node = get_binary_node_child(node, 'error')
    if err_node:
        code = err_node.attrs.get('code')
        raise BoomError(err_node.attrs.get('text') or 'Unknown error',
                        status_code=int(code) if code and str(code).isdigit() else 500,
                        data=int(code) if code and str(code).isdigit() else None)


def reduce_binary_node_to_dictionary(node: BinaryNode, tag: str) -> dict:
    nodes = get_binary_node_children(node, tag)
    dict_ = {}
    for n in nodes:
        attrs = n.attrs
        if 'name' in attrs and isinstance(attrs.get('name'), str):
            dict_[attrs['name']] = attrs.get('value') or attrs.get('config_value')
        else:
            dict_[attrs.get('config_code')] = attrs.get('value') or attrs.get('config_value')
    return dict_


def buffer_to_uint(e: bytes, t: int) -> int:
    a = 0
    for i in range(t):
        a = 256 * a + e[i]
    return a


def binary_node_to_string(node, i: int = 0) -> str:
    tabs = '\t' * i
    if node is None:
        return ''
    if isinstance(node, str):
        return tabs + node
    if isinstance(node, (bytes, bytearray)):
        return tabs + bytes(node).hex()
    if isinstance(node, list):
        return '\n'.join([tabs + binary_node_to_string(x, i + 1) for x in node])

    children = binary_node_to_string(node.content, i + 1)
    attrs_str = ' '.join([f"{k}='{v}'" for k, v in (node.attrs or {}).items() if v is not None])
    tag = f'<{node.tag} {attrs_str}' if attrs_str else f'<{node.tag}'
    content = f'>\n{children}\n{tabs}</{node.tag}>' if children else '/>'
    return tag + content
