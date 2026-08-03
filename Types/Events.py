"""Port of src/Types/Events.ts — Baileys event map and event emitter.

Python port: the event map keys are strings, payloads are dicts.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Set, Union

from ..WAProto import WAProto as proto

BaileysEventMap = Dict  # event name -> payload dict

BufferedEventData = Dict  # {historySets, chatUpserts, ...}

BaileysEvent = str


class BaileysEventEmitter:
    """Small typed-ish event emitter mirroring BaileysEventEmitter from TS."""

    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable]] = {}

    def on(self, event: str, listener: Callable) -> None:
        self._listeners.setdefault(event, []).append(listener)

    def off(self, event: str, listener: Callable) -> None:
        lst = self._listeners.get(event)
        if lst is not None:
            try:
                lst.remove(listener)
            except ValueError:
                pass

    def removeAllListeners(self, event: str) -> None:
        self._listeners.pop(event, None)

    def emit(self, event: str, arg) -> bool:
        lst = self._listeners.get(event)
        if not lst:
            return False
        for listener in list(lst):
            listener(arg)
        return True
