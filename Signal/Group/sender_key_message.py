"""Port of libsignal's SenderKeyMessage (src/Signal/Group/sender-key-message.ts).

Wire format: [version byte] || SenderKeyMessage proto || 64-byte ed25519(donna) signature.
"""

from __future__ import annotations

from typing import Optional

from ...Utils.crypto import curve25519_donna_sign, curve25519_donna_verify
from ...WAProto import WAProto as proto
from .ciphertext_message import CiphertextMessage

SIGNATURE_LENGTH = 64


class SenderKeyMessage(CiphertextMessage):
    def __init__(
        self,
        key_id: Optional[int] = None,
        iteration: Optional[int] = None,
        ciphertext: Optional[bytes] = None,
        signature_key: Optional[bytes] = None,
        serialized: Optional[bytes] = None,
    ):
        super().__init__()

        if serialized is not None:
            version = serialized[0]
            message = serialized[1:len(serialized) - SIGNATURE_LENGTH]
            signature = serialized[-SIGNATURE_LENGTH:]
            sender_key_message = proto.SenderKeyMessage.decode(message)

            self._serialized = bytes(serialized)
            self._message_version = (version & 0xFF) >> 4
            self._key_id = sender_key_message.id
            self._iteration = sender_key_message.iteration
            ct = sender_key_message.ciphertext
            self._ciphertext = ct if isinstance(ct, bytes) else bytes(ct)
            self._signature = signature
        else:
            version = (((self.CURRENT_VERSION << 4) | self.CURRENT_VERSION) & 0xFF) % 256
            ciphertext_buffer = bytes(ciphertext or b'')
            message = proto.SenderKeyMessage.encode(proto.SenderKeyMessage(
                id=key_id,
                iteration=iteration,
                ciphertext=ciphertext_buffer,
            ))
            signature = curve25519_donna_sign(signature_key or b'', bytes([version]) + message)

            self._serialized = bytes([version]) + message + signature
            self._message_version = self.CURRENT_VERSION
            self._key_id = key_id
            self._iteration = iteration
            self._ciphertext = ciphertext_buffer
            self._signature = signature

    def get_key_id(self) -> int:
        return self._key_id

    def get_iteration(self) -> int:
        return self._iteration

    def get_cipher_text(self) -> bytes:
        return self._ciphertext

    def verify_signature(self, signature_key: bytes) -> None:
        part1 = self._serialized[:len(self._serialized) - SIGNATURE_LENGTH]
        part2 = self._serialized[-SIGNATURE_LENGTH:]
        if not curve25519_donna_verify(signature_key, part1, part2):
            raise ValueError('Invalid signature!')

    def serialize(self) -> bytes:
        return self._serialized

    def get_type(self) -> int:
        return 4
