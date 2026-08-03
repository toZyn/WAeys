"""Port of libsignal's ProtocolAddress (src/protocol_address.js)."""

from __future__ import annotations


class ProtocolAddress:
    def __init__(self, id: str, device_id: int):
        if not isinstance(id, str):
            raise TypeError('id required for addr')
        if '.' in id:
            raise TypeError('encoded addr detected')
        self.id = id
        if not isinstance(device_id, int):
            raise TypeError('number required for deviceId')
        self.device_id = device_id

    @staticmethod
    def from_encoded(encoded_address: str) -> 'ProtocolAddress':
        import re
        if not isinstance(encoded_address, str) or not re.match(r'.*\.\d+', encoded_address):
            raise ValueError('Invalid address encoding')
        parts = encoded_address.split('.')
        return ProtocolAddress(parts[0], int(parts[1]))

    def __str__(self) -> str:
        return f'{self.id}.{self.device_id}'

    def is_same(self, other) -> bool:
        if not isinstance(other, ProtocolAddress):
            return False
        return other.id == self.id and other.device_id == self.device_id
