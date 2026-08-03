"""Port of libsignal's SenderKeyState (src/Signal/Group/sender-key-state.ts)."""

from __future__ import annotations

from typing import Optional

from .sender_chain_key import SenderChainKey
from .sender_message_key import SenderMessageKey

MAX_MESSAGE_KEYS = 2000


class SenderKeyState:
    def __init__(
        self,
        id: Optional[int] = None,
        iteration: Optional[int] = None,
        chain_key: Optional[bytes] = None,
        signature_key_pair: Optional[dict] = None,
        signature_key_public: Optional[bytes] = None,
        signature_key_private: Optional[bytes] = None,
        sender_key_state_structure: Optional[dict] = None,
    ):
        if sender_key_state_structure is not None:
            structure = dict(sender_key_state_structure)
            message_keys = structure.get('senderMessageKeys')
            structure['senderMessageKeys'] = list(message_keys) if isinstance(message_keys, list) else []
            self._structure = structure
        else:
            if signature_key_pair is not None:
                signature_key_public = signature_key_pair['public']
                signature_key_private = signature_key_pair['private']

            self._structure = {
                'senderKeyId': id or 0,
                'senderChainKey': {
                    'iteration': iteration or 0,
                    'seed': bytes(chain_key or b''),
                },
                'senderSigningKey': {
                    'public': bytes(signature_key_public or b''),
                    'private': bytes(signature_key_private or b''),
                },
                'senderMessageKeys': [],
            }

    def get_key_id(self) -> int:
        return self._structure['senderKeyId']

    def get_sender_chain_key(self) -> SenderChainKey:
        return SenderChainKey(
            self._structure['senderChainKey']['iteration'],
            self._structure['senderChainKey']['seed'],
        )

    def set_sender_chain_key(self, chain_key: SenderChainKey) -> None:
        self._structure['senderChainKey'] = {
            'iteration': chain_key.get_iteration(),
            'seed': chain_key.get_seed(),
        }

    def get_signing_key_public(self) -> bytes:
        public_key = bytes(self._structure['senderSigningKey']['public'])

        if len(public_key) == 32:
            fixed = bytearray(33)
            fixed[0] = 0x05
            fixed[1:] = public_key
            return bytes(fixed)

        return public_key

    def get_signing_key_private(self) -> bytes:
        return bytes(self._structure['senderSigningKey']['private'] or b'')

    def has_sender_message_key(self, iteration: int) -> bool:
        return any(key['iteration'] == iteration for key in self._structure['senderMessageKeys'])

    def add_sender_message_key(self, sender_message_key: SenderMessageKey) -> None:
        self._structure['senderMessageKeys'].append({
            'iteration': sender_message_key.get_iteration(),
            'seed': sender_message_key.get_seed(),
        })

        if len(self._structure['senderMessageKeys']) > MAX_MESSAGE_KEYS:
            self._structure['senderMessageKeys'].pop(0)

    def remove_sender_message_key(self, iteration: int) -> Optional[SenderMessageKey]:
        keys = self._structure['senderMessageKeys']
        for i, key in enumerate(keys):
            if key['iteration'] == iteration:
                removed = keys.pop(i)
                return SenderMessageKey(removed['iteration'], removed['seed'])
        return None

    def get_structure(self) -> dict:
        return self._structure
