"""Port of libsignal's SenderKeyRecord (src/Signal/Group/sender-key-record.ts)."""

from __future__ import annotations

import json
from typing import Optional

from ...Utils.generics import BufferJSON
from .sender_key_state import SenderKeyState

MAX_STATES = 5


class SenderKeyRecord:
    def __init__(self, serialized: Optional[list] = None):
        self._sender_key_states: list[SenderKeyState] = []
        if serialized is not None:
            for structure in serialized:
                self._sender_key_states.append(
                    SenderKeyState(sender_key_state_structure=structure)
                )

    def is_empty(self) -> bool:
        return len(self._sender_key_states) == 0

    def get_sender_key_state(self, key_id: Optional[int] = None) -> Optional[SenderKeyState]:
        if key_id is None and len(self._sender_key_states):
            return self._sender_key_states[-1]

        for state in self._sender_key_states:
            if state.get_key_id() == key_id:
                return state
        return None

    def add_sender_key_state(self, id: int, iteration: int, chain_key: bytes, signature_key: bytes) -> None:
        self._sender_key_states.append(SenderKeyState(id, iteration, chain_key, None, signature_key))
        if len(self._sender_key_states) > MAX_STATES:
            self._sender_key_states.pop(0)

    def set_sender_key_state(self, id: int, iteration: int, chain_key: bytes, key_pair: dict) -> None:
        self._sender_key_states.clear()
        self._sender_key_states.append(SenderKeyState(id, iteration, chain_key, key_pair))

    def serialize(self) -> list:
        return [state.get_structure() for state in self._sender_key_states]

    @staticmethod
    def deserialize(data: bytes) -> 'SenderKeyRecord':
        parsed = json.loads(bytes(data).decode('utf-8'), object_hook=BufferJSON.reviver)
        return SenderKeyRecord(parsed)
