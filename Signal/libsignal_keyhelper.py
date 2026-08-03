"""Port of libsignal's keyhelper.js."""

from __future__ import annotations

import secrets

from .libsignal_curve import calculate_signature, generate_key_pair


def is_non_negative_integer(n) -> bool:
    return isinstance(n, int) and not isinstance(n, bool) and n >= 0


def generate_identity_key_pair() -> dict:
    return generate_key_pair()


def generate_registration_id() -> int:
    return int.from_bytes(secrets.token_bytes(2), 'little') & 0x3fff


def generate_signed_pre_key(identity_key_pair: dict, signed_key_id: int) -> dict:
    if not isinstance(identity_key_pair.get('privKey'), bytes) or len(identity_key_pair['privKey']) != 32:
        raise TypeError('Invalid argument for identityKeyPair')
    if not isinstance(identity_key_pair.get('pubKey'), bytes) or len(identity_key_pair['pubKey']) != 33:
        raise TypeError('Invalid argument for identityKeyPair')
    if not is_non_negative_integer(signed_key_id):
        raise TypeError('Invalid argument for signedKeyId: ' + str(signed_key_id))
    key_pair = generate_key_pair()
    signature = calculate_signature(identity_key_pair['privKey'], key_pair['pubKey'])
    return {
        'keyId': signed_key_id,
        'keyPair': key_pair,
        'signature': signature,
    }


def generate_pre_key(key_id: int) -> dict:
    if not is_non_negative_integer(key_id):
        raise TypeError('Invalid argument for keyId: ' + str(key_id))
    key_pair = generate_key_pair()
    return {
        'keyId': key_id,
        'keyPair': key_pair,
    }
