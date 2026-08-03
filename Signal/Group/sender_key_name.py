"""Port of libsignal's SenderKeyName (src/Signal/Group/sender-key-name.ts)."""

from __future__ import annotations


def _is_null(s: str | None) -> bool:
    return s is None or s == ''


def _int_value(num: int) -> int:
    max_value = 0x7FFFFFFF
    min_value = -0x80000000
    if num > max_value or num < min_value:
        return num & 0xFFFFFFFF
    return num


def _hash_code(str_key: str) -> int:
    h = 0
    if not _is_null(str_key):
        for ch in str_key:
            h = h * 31 + ord(ch)
            h = _int_value(h)
    return h


class Sender:
    def __init__(self, id: str, device_id: int):
        self.id = id
        self.device_id = device_id

    def __str__(self):
        return f'{self.id}.{self.device_id}'


class SenderKeyName:
    def __init__(self, group_id: str, sender: Sender):
        self._group_id = group_id
        self._sender = sender

    def get_group_id(self) -> str:
        return self._group_id

    def get_sender(self) -> Sender:
        return self._sender

    def serialize(self) -> str:
        return f'{self._group_id}::{self._sender.id}::{self._sender.device_id}'

    def __str__(self):
        return self.serialize()

    def equals(self, other: 'SenderKeyName | None') -> bool:
        if other is None:
            return False
        return self._group_id == other._group_id and str(self._sender) == str(other._sender)

    def __eq__(self, other):
        return self.equals(other)

    def __hash__(self):
        return _hash_code(self._group_id) ^ _hash_code(str(self._sender))
