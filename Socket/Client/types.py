"""Port of src/Socket/Client/types.ts — AbstractSocketClient base class."""

from __future__ import annotations

import asyncio
from typing import Callable, Dict, List, Optional, Union

from ...Types.Socket import SocketConfig


class AbstractSocketClient:
    """EventEmitter-compatible base for the socket client.

    Port of the TS `AbstractSocketClient extends EventEmitter`. Provides a
    minimal emitter interface (on/off/once/emit/removeAllListeners) and the
    abstract connect/close/send surface. WS-level events ('open', 'message',
    'close', 'error', ...) plus dynamic routing events ('TAG:...', 'CB:...')
    are emitted through this emitter by the socket layer.
    """

    def __init__(self, url: str, config: SocketConfig) -> None:
        self.url = url
        self.config = config
        self._listeners: Dict[str, List[Callable]] = {}

    def set_max_listeners(self, _n: int) -> None:
        pass

    def on(self, event: str, listener: Callable) -> None:
        self._listeners.setdefault(event, []).append(listener)

    def once(self, event: str, listener: Callable) -> None:
        def wrapper(*args, **kwargs):
            self.off(event, wrapper)
            return listener(*args, **kwargs)

        self.on(event, wrapper)

    def off(self, event: str, listener: Callable) -> None:
        lst = self._listeners.get(event)
        if lst is not None:
            try:
                lst.remove(listener)
            except ValueError:
                pass

    def remove_all_listeners(self, event: Optional[str] = None) -> None:
        if event is None:
            self._listeners.clear()
        else:
            self._listeners.pop(event, None)

    def emit(self, event: str, *args) -> bool:
        lst = self._listeners.get(event)
        if not lst:
            return False
        for listener in list(lst):
            listener(*args)
        return True

    # -- abstract interface (implemented by concrete clients) --

    @property
    def is_open(self) -> bool:
        raise NotImplementedError

    @property
    def is_closed(self) -> bool:
        raise NotImplementedError

    @property
    def is_closing(self) -> bool:
        raise NotImplementedError

    @property
    def is_connecting(self) -> bool:
        raise NotImplementedError

    def connect(self) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    def send(self, data: Union[str, bytes], cb: Optional[Callable] = None) -> bool:
        raise NotImplementedError
