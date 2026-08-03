"""Port of src/Types/Auth.ts — auth creds, key pairs, SignalKeyStore.

Types are represented as Python dicts with the same keys as the TS shapes.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Union

from ..WAProto import WAProto as proto

KeyPair = Dict[str, bytes]  # {'public': bytes, 'private': bytes}

SignedKeyPair = Dict  # {keyPair, signature, keyId, timestampS?}

ProtocolAddressT = Dict[str, Union[str, int]]  # {name, deviceId}

SignalIdentity = Dict  # {identifier, identifierKey}

LIDMapping = Dict[str, str]  # {pn, lid}

LTHashState = Dict  # {version, hash, indexValueMap}

SignalCreds = Dict  # {signedIdentityKey, signedPreKey, registrationId}

AccountSettings = Dict  # {unarchiveChats, defaultDisappearingMode?}

AuthenticationCreds = Dict  # full creds dict (SignalCreds + noiseKey + ...)

# SignalDataTypeMap: type name -> stored value type
SignalDataTypeMap = {
    'pre-key': KeyPair,
    'session': bytes,
    'sender-key': bytes,
    'sender-key-memory': dict,
    'app-state-sync-key': object,
    'app-state-sync-version': LTHashState,
    'lid-mapping': str,
    'device-list': List[str],
    'tctoken': dict,
    'identity-key': bytes,
}

# SignalDataSet: {type: {id: value | None}}
SignalDataSet = Dict[str, Dict[str, Union[bytes, str, dict, List, None]]]

SignalKeyStore = Dict  # get(type, ids) / set(data) / clear?()

SignalKeyStoreWithTransaction = Dict  # + isInTransaction() / transaction(exec, key)

TransactionCapabilityOptions = Dict[str, int]

SignalAuthState = Dict  # {'creds': SignalCreds, 'keys': SignalKeyStore | WithTransaction}

AuthenticationState = Dict  # {'creds': AuthenticationCreds, 'keys': SignalKeyStore}


def make_auth_state(creds: dict, keys) -> dict:
    """Build an AuthenticationState dict from creds and a key store."""
    return {'creds': creds, 'keys': keys}
