"""Port of libsignal's errors.js and small constant modules."""

from __future__ import annotations


class SignalError(Exception):
    pass


class UntrustedIdentityKeyError(SignalError):
    def __init__(self, addr, identity_key):
        super().__init__()
        self.addr = addr
        self.identity_key = identity_key


class SessionError(SignalError):
    pass


class MessageCounterError(SessionError):
    pass


class PreKeyError(SessionError):
    pass
