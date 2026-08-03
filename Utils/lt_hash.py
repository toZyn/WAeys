"""LT Hash — summation-based integrity hash mirroring whatsgp-rust-bridge's
LTHashAntiTampering (originally src/Utils/lt-hash.ts).

Wire-accurate port of wacore-appstate's lthash.rs:
  - each operand's contribution is HKDF-SHA256(salt=None, info="WhatsApp Patch Integrity", len=128)
  - the 128-byte accumulator is treated as 64 little-endian u16 lanes
  - operations are pointwise wrapping (mod 2^16) add / subtract
  - subtractThenAdd first subtracts every sub operand, then adds every add operand
"""
import struct

from .crypto import hkdf

WAPATCH_INTEGRITY_INFO = b"WhatsApp Patch Integrity"
HKDF_SIZE = 128


def _hkdf_expand(item: bytes) -> bytes:
    return hkdf(item, num_bytes=HKDF_SIZE, info=WAPATCH_INTEGRITY_INFO, salt=b"")


def _pointwise(base: bytearray, operand: bytes, subtract: bool) -> None:
    assert len(base) == len(operand)
    assert len(base) % 2 == 0
    for off in range(0, len(base), 2):
        x = struct.unpack_from("<H", base, off)[0]
        y = struct.unpack_from("<H", operand, off)[0]
        r = (x - y) & 0xFFFF if subtract else (x + y) & 0xFFFF
        struct.pack_into("<H", base, off, r)


class LTHash:
    def __init__(self, hkdf_info: bytes = WAPATCH_INTEGRITY_INFO, hkdf_size: int = HKDF_SIZE):
        self.hkdf_info = hkdf_info
        self.hkdf_size = hkdf_size

    def _operand(self, item: bytes) -> bytes:
        if self.hkdf_info == WAPATCH_INTEGRITY_INFO and self.hkdf_size == HKDF_SIZE:
            return _hkdf_expand(item)
        return hkdf(item, num_bytes=self.hkdf_size, info=self.hkdf_info, salt=b"")

    def _multiple_op(self, base: bytearray, input_items: list, subtract: bool) -> None:
        for item in input_items:
            derived = self._operand(item)
            _pointwise(base, derived, subtract)

    def subtract_then_add(self, base: bytes, subtract: list, add: list) -> bytes:
        output = bytearray(base)
        self.subtract_then_add_in_place(output, subtract, add)
        return bytes(output)

    def subtract_then_add_in_place(self, base: bytearray, subtract: list, add: list) -> None:
        self._multiple_op(base, subtract, True)
        self._multiple_op(base, add, False)


WAPATCH_INTEGRITY = LTHash()


class LTHashAntiTampering:
    """Facade matching the wasm_bindgen API used by Baileys' lt-hash.ts."""

    def __init__(self):
        self.inner = WAPATCH_INTEGRITY

    def subtractThenAdd(self, base: bytes, subtract: list, add: list) -> bytes:
        return self.inner.subtract_then_add(base, subtract, add)


LT_HASH_ANTI_TAMPERING = LTHashAntiTampering()
