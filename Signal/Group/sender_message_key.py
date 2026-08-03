"""Port of libsignal's SenderMessageKey (src/Signal/Group/sender-message-key.ts)."""

from __future__ import annotations

from ...Utils.crypto import hkdf

WHISPER_GROUP_INFO = b'WhisperGroup'


class SenderMessageKey:
    def __init__(self, iteration: int, seed: bytes):
        derivative = hkdf(seed, 96, WHISPER_GROUP_INFO, bytes(32))
        d0 = derivative[0:32]
        d1 = derivative[32:64]
        keys = bytearray(32)
        keys[0:16] = d0[16:32]
        keys[16:32] = d1[0:16]

        self._iteration = iteration
        self._iv = d0[0:16]
        self._cipher_key = bytes(keys)
        self._seed = bytes(seed)

    def get_iteration(self) -> int:
        return self._iteration

    def get_iv(self) -> bytes:
        return self._iv

    def get_cipher_key(self) -> bytes:
        return self._cipher_key

    def get_seed(self) -> bytes:
        return self._seed
