"""Port of src/Types/Signal.ts — SignalRepository interface + E2E types.

Python port uses plain dicts/typed aliases matching the TS shapes.
"""
from __future__ import annotations

from typing import Callable, Dict, List, Optional, Union

from ..Signal.protocol_address import ProtocolAddress as _ProtocolAddress

# DecryptGroupSignalOpts
DecryptGroupSignalOpts = Dict[str, Union[str, bytes]]

# ProcessSenderKeyDistributionMessageOpts
ProcessSenderKeyDistributionMessageOpts = Dict[str, Union[dict, str]]

# DecryptSignalProtoOpts
DecryptSignalProtoOpts = Dict[str, Union[str, bytes]]

# EncryptMessageOpts
EncryptMessageOpts = Dict[str, Union[str, bytes]]

# EncryptGroupMessageOpts
EncryptGroupMessageOpts = Dict[str, Union[str, bytes]]

# GetSenderKeyDistributionMessageOpts
GetSenderKeyDistributionMessageOpts = Dict[str, str]

PreKey = Dict[str, Union[int, bytes]]
SignedPreKey = Dict[str, Union[int, bytes]]
E2ESession = Dict[str, Union[int, bytes, SignedPreKey, PreKey, None]]
E2ESessionOpts = Dict[str, Union[str, E2ESession]]


class SignalRepository:
    """Interface mirroring src/Types/Signal.ts SignalRepository.

    Implemented by make_libsignal_repository (dict of coroutines) — this class
    documents the contract.
    """

    async def decryptGroupMessage(self, opts: DecryptGroupSignalOpts) -> bytes: ...
    async def processSenderKeyDistributionMessage(self, opts: ProcessSenderKeyDistributionMessageOpts) -> None: ...
    async def decryptMessage(self, opts: DecryptSignalProtoOpts) -> bytes: ...
    async def encryptMessage(self, opts: EncryptMessageOpts) -> Dict[str, Union[str, bytes]]: ...
    async def encryptGroupMessage(self, opts: EncryptGroupMessageOpts) -> Dict[str, bytes]: ...
    async def getSenderKeyDistributionMessage(self, opts: GetSenderKeyDistributionMessageOpts) -> bytes: ...
    async def hasSenderKey(self, opts: GetSenderKeyDistributionMessageOpts) -> bool: ...
    async def getSessionInfo(self, jid: str) -> Optional[Dict[str, Union[bytes, int]]]: ...
    async def injectE2ESession(self, opts: E2ESessionOpts) -> None: ...
    async def validateSession(self, jid: str) -> Dict[str, Union[bool, str]]: ...
    def jidToSignalProtocolAddress(self, jid: str) -> str: ...
    async def migrateSession(self, fromJid: str, toJid: str) -> Dict[str, int]: ...
    async def deleteSession(self, jids: List[str]) -> None: ...


# SignalRepositoryWithLIDStore adds `lidMapping` and optional `close()`
