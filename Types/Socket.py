"""Port of src/Types/Socket.ts — SocketConfig and cache store types."""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Tuple, Union

WAVersion = Tuple[int, int, int]
WABrowserDescription = Tuple[str, str, str]

CacheStore = Dict  # get/set/del/flushAll/close?

PossiblyExtendedCacheStore = Dict  # + mget/mset/mdel

PatchedMessageWithRecipientJID = Dict  # proto.IMessage & {recipientJid?}

SocketConfig = Dict  # full config dict, see TS for the field list

UserFacingSocketConfig = Dict  # Partial<SocketConfig> & {auth}

BrowsersMap = Dict  # ubuntu/macOS/baileys/windows/android/appropriate -> (name, version, short)
