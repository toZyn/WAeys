"""libsignal crypto helpers (port of libsignal/src/crypto.js).

The standalone `hkdf` in Utils.crypto performs the same derivation as
libsignal's `deriveSecrets` (RFC 5869, salt 32 bytes, info prefixed chunk).
"""
from __future__ import annotations

import hashlib
import hmac as _hmac

from ..Utils.crypto import aes_cbc_decrypt, aes_cbc_encrypt, hkdf


def derive_secrets(input_bytes: bytes, salt: bytes, info: bytes, chunks: int = 3) -> list:
    """RFC 5869 HKDF returning the first `chunks` 32-byte outputs."""
    if len(salt) != 32:
        raise ValueError('Got salt of incorrect length')
    if chunks < 1 or chunks > 3:
        raise AssertionError
    derived = hkdf(input_bytes, 32 * chunks, info, salt)
    return [derived[i * 32:(i + 1) * 32] for i in range(chunks)]


def encrypt(key: bytes, data: bytes, iv: bytes) -> bytes:
    return aes_cbc_encrypt(data, key, iv)


def decrypt(key: bytes, data: bytes, iv: bytes) -> bytes:
    return aes_cbc_decrypt(data, key, iv)


def calculate_mac(key: bytes, data: bytes) -> bytes:
    return _hmac.new(key, data, hashlib.sha256).digest()


def hash(data: bytes) -> bytes:
    return hashlib.sha512(data).digest()


def verify_mac(data: bytes, key: bytes, mac: bytes, length: int) -> None:
    calculated = calculate_mac(key, data)[:length]
    if len(mac) != length or len(calculated) != length:
        raise ValueError('Bad MAC length')
    if not _hmac.compare_digest(bytes(mac), calculated):
        raise ValueError('Bad MAC')
