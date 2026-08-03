"""Port of libsignal's keyhelper (src/Signal/Group/keyhelper.ts)."""

from __future__ import annotations

import secrets
from typing import Optional

from ..libsignal_curve import generate_key_pair as curve_generate_key_pair


def generate_sender_key() -> bytes:
    return secrets.token_bytes(32)


def generate_sender_key_id() -> int:
    return secrets.randbelow(2147483647)


def generate_sender_signing_key(key: Optional[dict] = None) -> dict:
    if key is None:
        key = curve_generate_key_pair()
    return {
        'public': bytes(key['pubKey']),
        'private': bytes(key['privKey']),
    }
