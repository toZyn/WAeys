"""Port of libsignal's SenderKeyDistributionMessage (src/Signal/Group/sender-key-distribution-message.ts).

Wire format: [version byte] || SenderKeyDistributionMessage proto.
"""

from __future__ import annotations

from typing import Optional

from ...WAProto import WAProto as proto
from .ciphertext_message import CiphertextMessage


def _ints_to_byte_high_and_low(high_value: int, low_value: int) -> int:
    return (((high_value << 4) | low_value) & 0xFF) % 256


class SenderKeyDistributionMessage(CiphertextMessage):
    def __init__(
        self,
        id: Optional[int] = None,
        iteration: Optional[int] = None,
        chain_key: Optional[bytes] = None,
        signature_key: Optional[bytes] = None,
        serialized: Optional[bytes] = None,
    ):
        super().__init__()

        if serialized is not None:
            message = bytes(serialized)[1:]
            distribution_message = proto.SenderKeyDistributionMessage.decode(message)

            self._serialized = bytes(serialized)
            self._id = distribution_message.id
            self._iteration = distribution_message.iteration
            ck = distribution_message.chainKey
            self._chain_key = ck if isinstance(ck, bytes) else bytes(ck)
            sk = distribution_message.signingKey
            self._signature_key = sk if isinstance(sk, bytes) else bytes(sk)
        else:
            version = _ints_to_byte_high_and_low(self.CURRENT_VERSION, self.CURRENT_VERSION)
            self._id = id
            self._iteration = iteration
            self._chain_key = chain_key
            self._signature_key = signature_key

            message = proto.SenderKeyDistributionMessage.encode(proto.SenderKeyDistributionMessage(
                id=id,
                iteration=iteration,
                chainKey=chain_key,
                signingKey=signature_key,
            ))

            self._serialized = bytes([version]) + message

    def serialize(self) -> bytes:
        return self._serialized

    def get_type(self) -> int:
        return self.SENDERKEY_DISTRIBUTION_TYPE

    def get_iteration(self) -> int:
        return self._iteration

    def get_chain_key(self) -> bytes:
        return self._chain_key

    def get_signature_key(self) -> bytes:
        return self._signature_key

    def get_id(self) -> int:
        return self._id
