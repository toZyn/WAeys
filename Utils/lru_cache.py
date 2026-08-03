"""A small TTL LRU cache (stand-in for the `lru-cache` npm package)."""

from __future__ import annotations

import time
from collections import OrderedDict


class LRUCache:
    def __init__(
        self,
        ttl: int = 0,
        ttl_autopurge: bool = False,
        update_age_on_get: bool = False,
        max: int = 0,
        dispose=None,
    ):
        self.ttl = ttl
        self.ttl_autopurge = ttl_autopurge
        self.update_age_on_get = update_age_on_get
        self.max = max
        self.dispose = dispose
        self._data = OrderedDict()  # key -> (value, expires_at)
        self._last_purge = 0.0

    def _purge_expired(self) -> None:
        now = time.time() * 1000
        expired = [k for k, (v, exp) in self._data.items() if exp is not None and exp <= now]
        for k in expired:
            self._dispose(k, self._data[k][0])
            del self._data[k]

    def _evict_if_needed(self) -> None:
        if self.max and len(self._data) > self.max:
            while len(self._data) > self.max:
                k, (v, exp) = self._data.popitem(last=False)
                self._dispose(k, v)

    def _dispose(self, key, value) -> None:
        if self.dispose is not None:
            self.dispose(value, key)

    def get(self, key, default=None):
        if not self._data:
            return default
        if self.ttl_autopurge:
            self._purge_expired()
        else:
            item = self._data.get(key)
            if item is not None:
                value, expires_at = item
                if expires_at is not None and expires_at <= time.time() * 1000:
                    self._dispose(key, value)
                    del self._data[key]
                    return default
        if key not in self._data:
            return default
        value, expires_at = self._data[key]
        if self.update_age_on_get:
            self._data.move_to_end(key)
        return value

    def set(self, key, value, ttl=None) -> None:
        now = time.time() * 1000
        ttl_ms = self.ttl if ttl is None else ttl
        expires_at = now + ttl_ms if ttl_ms else None
        if key in self._data:
            self._data[key] = (value, expires_at)
            self._data.move_to_end(key)
        else:
            self._data[key] = (value, expires_at)
            self._data.move_to_end(key)
            self._evict_if_needed()

    def has(self, key) -> bool:
        return self.get(key) is not None

    def delete(self, key) -> None:
        if key in self._data:
            value, expires_at = self._data.pop(key)
            self._dispose(key, value)

    def clear(self) -> None:
        keys = list(self._data.keys())
        self._data.clear()
        for k in keys:
            self._dispose(k, None)

    def __contains__(self, key):
        return self.get(key) is not None

    def __len__(self) -> int:
        return len(self._data)
