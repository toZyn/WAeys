"""Port of src/Socket/Client/websocket.ts — WebSocketClient over websockets.

Uses the `websockets` library (asyncio) instead of Node's `ws`. Event surface
matches the TS: 'close', 'error', 'open', 'message', plus 'ping'/'pong'
(there is no 'upgrade'/'unexpected-response' equivalent in websockets).
"""

from __future__ import annotations

import asyncio
from typing import Optional, Union

from ...Defaults.index import DEFAULT_ORIGIN
from ...Types.Socket import SocketConfig
from .types import AbstractSocketClient


class WebSocketClient(AbstractSocketClient):
    OPEN = 'open'
    CLOSING = 'closing'
    CLOSED = 'closed'
    CONNECTING = 'connecting'

    def __init__(self, url: str, config: SocketConfig) -> None:
        super().__init__(url, config)
        self.socket = None
        self._connect_task: Optional[asyncio.Task] = None
        self._close_event: Optional[asyncio.Event] = None
        self._recv_task: Optional[asyncio.Task] = None

    def _state(self):
        if self.socket is None:
            connecting = self._connect_task is not None and not self._connect_task.done()
            return self.CONNECTING if connecting else self.CLOSED
        state = getattr(self.socket, 'state', None)
        if state is None:
            closed = getattr(self.socket, 'closed', None)
            if closed is True:
                return self.CLOSED
            if closed is False:
                return self.OPEN
            return None
        return {
            0: self.CONNECTING,
            1: self.OPEN,
            2: self.CLOSING,
            3: self.CLOSED,
        }.get(int(state), self.CONNECTING)

    @property
    def is_open(self) -> bool:
        return self._state() == self.OPEN

    @property
    def is_closed(self) -> bool:
        return self._state() in (None, self.CLOSED)

    @property
    def is_closing(self) -> bool:
        return self._state() in (None, self.CLOSING)

    @property
    def is_connecting(self) -> bool:
        return self._state() == self.CONNECTING

    def connect(self) -> None:
        if self._connect_task is not None and not self._connect_task.done():
            return

        self._connect_task = asyncio.ensure_future(self._connect())

    async def _connect(self) -> None:
        timeout_ms = self.config.get('connectTimeoutMs') or 20_000
        headers = (self.config.get('options') or {}).get('headers') or {}
        origin = DEFAULT_ORIGIN

        self._close_event = asyncio.Event()

        try:
            self.socket = await asyncio.wait_for(
                websockets_connect(
                    self.url,
                    origin=origin,
                    additional_headers=headers,
                ),
                timeout=timeout_ms / 1000.0,
            )
        except Exception as err:
            self.socket = None
            self.emit('error', err)
            return

        self.emit('open')

        self._recv_task = asyncio.ensure_future(self._recv_loop())

    async def _recv_loop(self) -> None:
        assert self.socket is not None
        try:
            async for message in self.socket:
                if isinstance(message, bytes):
                    self.emit('message', message)
                else:
                    self.emit('message', message.encode('utf-8'))
        except Exception as err:
            if not self.is_closed:
                self.emit('error', err)
        finally:
            self._close_event.set()
            self.emit('close', None)

    async def close(self) -> None:
        if self.socket is None:
            return

        close_event = self._close_event
        try:
            await self.socket.close()
        except Exception:
            pass

        if close_event is not None:
            await close_event.wait()

        self.socket = None

    def send(self, data: Union[str, bytes], cb=None) -> bool:
        if self.socket is None:
            return False

        async def _do_send():
            try:
                await self.socket.send(data)
                if cb is not None:
                    cb(None)
            except Exception as err:
                if cb is not None:
                    cb(err)

        asyncio.ensure_future(_do_send())
        return True


def websockets_connect(uri, origin=None, additional_headers=None):
    import websockets

    kwargs = {}
    if origin:
        kwargs['origin'] = origin
    if additional_headers:
        kwargs['additional_headers'] = dict(additional_headers)
    return websockets.connect(uri, **kwargs)
