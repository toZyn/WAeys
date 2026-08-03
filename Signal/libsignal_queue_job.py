"""Port of libsignal's queue_job.js.

Serializes async operations per bucket key (an asyncio.Lock per bucket).
"""

from __future__ import annotations

import asyncio
from typing import Awaitable, TypeVar

T = TypeVar('T')

_locks = {}
_locks_guard = asyncio.Lock()


async def queue_job(bucket: str, awaitable: Awaitable[T]) -> T:
    async with _locks_guard:
        lock = _locks.setdefault(bucket, asyncio.Lock())
    async with lock:
        return await awaitable
