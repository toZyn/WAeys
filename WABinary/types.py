"""Binary node types (ported from src/WABinary/types.ts)."""

from __future__ import annotations

from typing import Dict, List, Optional, Union

# BinaryNode content can be: list of nodes, a string, or raw bytes
BinaryNodeContent = Optional[Union['BinaryNode', List['BinaryNode'], str, bytes]]


class BinaryNode:
    """the binary node WA uses internally for communication"""

    __slots__ = ('tag', 'attrs', 'content')

    def __init__(self, tag: str, attrs: Optional[Dict[str, str]] = None, content: BinaryNodeContent = None):
        self.tag = tag
        self.attrs: Dict[str, str] = attrs or {}
        self.content: BinaryNodeContent = content

    def __repr__(self) -> str:
        return f'<BinaryNode {self.tag} attrs={self.attrs} content={self.content!r}>'


BinaryNodeAttributes = Dict[str, str]
BinaryNodeData = BinaryNodeContent
