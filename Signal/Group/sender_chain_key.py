"""Port of libsignal's SenderChainKey (src/Signal/Group/sender-chain-key.ts)."""

from __future__ import annotations

from ...Utils.crypto import hmac_sign
from .sender_message_key import SenderMessageKey

MESSAGE_KEY_SEED = b'\x01'
CHAIN_KEY_SEED = b'\x02'


class SenderChainKey:
    def __init__(self, iteration: int, chain_key: bytes):
        self._iteration = iteration
        self._chain_key = bytes(chain_key)

    def get_iteration(self) -> int:
        return self._iteration

    def get_sender_message_key(self) -> SenderMessageKey:
        return SenderMessageKey(self._iteration, self._get_derivative(MESSAGE_KEY_SEED, self._chain_key))

    def get_next(self) -> 'SenderChainKey':
        return SenderChainKey(self._iteration + 1, self._get_derivative(CHAIN_KEY_SEED, self._chain_key))

    def get_seed(self) -> bytes:
        return self._chain_key

    @staticmethod
    def _get_derivative(seed: bytes, key: bytes) -> bytes:
        return hmac_sign(seed, key)
