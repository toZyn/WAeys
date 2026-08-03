"""Async mutex helpers mirroring src/Utils/make-mutex.ts.

Provides make_mutex() (a single-exclusion lock) and make_keyed_mutex()
(per-key exclusion with ref counting / cleanup), built on asyncio.Lock.
"""
import asyncio


def make_mutex():
    """Returns {mutex(fn)} executing fn exclusively (runExclusive)."""
    lock = asyncio.Lock()

    async def mutex(code):
        async with lock:
            if asyncio.iscoroutinefunction(code):
                return await code()
            return code()

    return {"mutex": mutex}


def make_keyed_mutex():
    """Returns {mutex(key, task)} serializing tasks per key."""
    map_ = {}

    async def mutex(key, task):
        entry = map_.get(key)
        if not entry:
            entry = {"lock": asyncio.Lock(), "refCount": 0}
            map_[key] = entry
        entry["refCount"] += 1
        try:
            async with entry["lock"]:
                if asyncio.iscoroutinefunction(task):
                    return await task()
                return task()
        finally:
            entry["refCount"] -= 1
            if entry["refCount"] == 0 and map_.get(key) is entry:
                del map_[key]

    return {"mutex": mutex}
