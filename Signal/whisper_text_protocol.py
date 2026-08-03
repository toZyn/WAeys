"""WhisperText protocol protobufs (port of libsignal's src/WhisperTextProtocol.js).

These two messages are internal to libsignal and are NOT part of WAProto.
"""
from __future__ import annotations

from ..WAProto.runtime import FieldDescriptor, Message

class WhisperMessage(Message):
    FIELDS = {
        'ephemeralKey': FieldDescriptor('ephemeralKey', 1, 'bytes', repeated=False, packed=False),
        'counter': FieldDescriptor('counter', 2, 'uint32', repeated=False, packed=False),
        'previousCounter': FieldDescriptor('previousCounter', 3, 'uint32', repeated=False, packed=False),
        'ciphertext': FieldDescriptor('ciphertext', 4, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PreKeyWhisperMessage(Message):
    FIELDS = {
        'preKeyId': FieldDescriptor('preKeyId', 1, 'uint32', repeated=False, packed=False),
        'baseKey': FieldDescriptor('baseKey', 2, 'bytes', repeated=False, packed=False),
        'identityKey': FieldDescriptor('identityKey', 3, 'bytes', repeated=False, packed=False),
        'message': FieldDescriptor('message', 4, 'bytes', repeated=False, packed=False),
        'registrationId': FieldDescriptor('registrationId', 5, 'uint32', repeated=False, packed=False),
        'signedPreKeyId': FieldDescriptor('signedPreKeyId', 6, 'uint32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
