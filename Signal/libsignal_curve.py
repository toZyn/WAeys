"""libsignal curve primitives (port of libsignal/src/curve.js).

Key differences from our Utils/crypto Curve:
- pubKey is returned WITH the 0x05 version byte prefix (33 bytes)
- signatures use the curve25519-donna scheme (sign with clamped scalar directly)
"""

from __future__ import annotations

from ..Utils.crypto import (
    KEY_BUNDLE_TYPE,
    curve25519_donna_sign,
    curve25519_donna_verify,
    x25519_generate_key_pair,
    x25519_public_key,
    x25519_shared_key,
)


def _scrub_pub_key_format(pub_key: bytes) -> bytes:
    if not isinstance(pub_key, (bytes, bytearray)):
        raise TypeError('Invalid public key type')
    pub_key = bytes(pub_key)
    if (len(pub_key) != 33 or pub_key[0] != 5) and len(pub_key) != 32:
        raise ValueError('Invalid public key')
    if len(pub_key) == 33:
        return pub_key[1:]
    return pub_key


def _validate_priv_key(priv_key) -> None:
    if priv_key is None:
        raise ValueError('Undefined private key')
    if not isinstance(priv_key, (bytes, bytearray)):
        raise TypeError(f'Invalid private key type: {type(priv_key).__name__}')
    if len(priv_key) != 32:
        raise ValueError(f'Incorrect private key length: {len(priv_key)}')


def get_public_from_private_key(priv_key: bytes) -> bytes:
    """Derive the 33-byte (0x05-prefixed) public key from a private key."""
    _validate_priv_key(priv_key)
    return KEY_BUNDLE_TYPE + x25519_public_key(priv_key)


def generate_key_pair() -> dict:
    """Returns {'pubKey': 33-byte (0x05-prefixed), 'privKey': 32-byte}."""
    priv, pub = x25519_generate_key_pair()
    return {
        'privKey': priv,
        'pubKey': KEY_BUNDLE_TYPE + pub,
    }


def calculate_agreement(pub_key: bytes, priv_key: bytes) -> bytes:
    pub_key = _scrub_pub_key_format(pub_key)
    _validate_priv_key(priv_key)
    if len(pub_key) != 32:
        raise ValueError('Invalid public key')
    return x25519_shared_key(bytes(priv_key), pub_key)


def calculate_signature(priv_key: bytes, message: bytes) -> bytes:
    _validate_priv_key(priv_key)
    if not message:
        raise ValueError('Invalid message')
    return curve25519_donna_sign(bytes(priv_key), bytes(message))


def verify_signature(pub_key: bytes, msg: bytes, sig: bytes, is_init: bool = False) -> bool:
    pub_key = _scrub_pub_key_format(pub_key)
    if len(pub_key) != 32:
        raise ValueError('Invalid public key')
    if not msg:
        raise ValueError('Invalid message')
    if not sig or len(sig) != 64:
        raise ValueError('Invalid signature')
    return True if is_init else curve25519_donna_verify(pub_key, bytes(msg), bytes(sig))
