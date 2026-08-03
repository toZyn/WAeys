"""Port of src/Utils/auth-utils.ts — cacheable signal key store, transactions."""

from __future__ import annotations

import asyncio
import time

from ..Defaults.index import DEFAULT_CACHE_TTLS
from .crypto import Curve, signed_key_pair
from .generics import Boom, delay, generate_registration_id
from .pre_key_manager import PreKeyManager


def _get_unique_id(type_: str, id_: str) -> str:
    return f'{type_}.{id_}'


class SignalKeyStore:
    """SignalKeyStore wrapper.

    Exposes the store's async functions as attributes (``store.get``/``store.set``)
    and also supports subscript access (``store['get']``/``store['set']``) so both
    calling conventions used across the codebase work without dict built-in shadowing.
    """

    __slots__ = ('_methods',)

    def __init__(self, methods):
        self._methods = dict(methods)

    def __getattr__(self, name):
        methods = self._methods
        if name in methods:
            return methods[name]
        raise AttributeError(name)

    def __getitem__(self, key):
        methods = self._methods
        if key in methods:
            return methods[key]
        raise KeyError(key)

    def __contains__(self, key):
        return key in self._methods


def make_cacheable_signal_key_store(store, logger=None, cache=None):
    """Adds caching capability to a SignalKeyStore."""
    if cache is None:
        cache = {'_store': {}, '_expiry': {}}
    elif not isinstance(cache, dict):
        cache = {'_store': {}, '_expiry': {}}
    else:
        cache.setdefault('_store', {})
        cache.setdefault('_expiry', {})

    ttl = DEFAULT_CACHE_TTLS['SIGNAL_STORE']  # 5 minutes
    cache_mutex = asyncio.Lock()

    async def get(type_, ids):
        async with cache_mutex:
            now = time.time()
            data = {}
            ids_to_fetch = []
            for id_ in ids:
                uid = _get_unique_id(type_, id_)
                exp = cache['_expiry'].get(uid)
                if exp is not None and exp > now:
                    data[id_] = cache['_store'][uid]
                else:
                    ids_to_fetch.append(id_)
            if ids_to_fetch:
                if logger:
                    logger.trace({'items': len(ids_to_fetch)}, 'loading from store')
                fetched = await store['get'](type_, ids_to_fetch)
                for id_ in ids_to_fetch:
                    item = fetched.get(id_)
                    if item is not None:
                        data[id_] = item
                        cache['_store'][_get_unique_id(type_, id_)] = item
                        cache['_expiry'][_get_unique_id(type_, id_)] = now + ttl
            return data

    async def set(data):
        async with cache_mutex:
            keys = 0
            now = time.time()
            for type_ in data:
                for id_ in data[type_]:
                    cache['_store'][_get_unique_id(type_, id_)] = data[type_][id_]
                    cache['_expiry'][_get_unique_id(type_, id_)] = now + ttl
                    keys += 1
            if logger:
                logger.trace({'keys': keys}, 'updated cache')
            await store['set'](data)

    async def clear():
        cache['_store'].clear()
        cache['_expiry'].clear()
        try:
            clear_ = store['clear']
        except (KeyError, TypeError):
            clear_ = None
        if clear_:
            await clear_()

    return SignalKeyStore({'get': get, 'set': set, 'clear': clear})


def _run_queued(lock: asyncio.Lock, coro_factory):
    """Run a coroutine under a lock, returning a task."""

    async def _runner():
        async with lock:
            return await coro_factory()

    return asyncio.ensure_future(_runner())


class _TransactionContext:
    __slots__ = ('cache', 'mutations', 'db_queries')

    def __init__(self):
        self.cache = {}
        self.mutations = {}
        self.db_queries = 0


class _TransactionStorage:
    """AsyncLocalStorage-ish context holder (single context per task)."""

    def __init__(self):
        self._contexts = {}

    def get_store(self):
        try:
            task = asyncio.current_task()
        except RuntimeError:
            return None
        return self._contexts.get(task)

    def run(self, ctx, work):
        try:
            task = asyncio.current_task()
        except RuntimeError:
            return work()
        self._contexts[task] = ctx
        try:
            return work()
        finally:
            self._contexts.pop(task, None)


def add_transaction_capability(state, logger, options):
    """Adds DB-like transaction capability to the SignalKeyStore."""
    max_commit_retries = options.get('maxCommitRetries', 5)
    delay_between_tries_ms = options.get('delayBetweenTriesMs', 100)

    tx_storage = _TransactionStorage()
    key_queues = {}
    tx_mutexes = {}
    tx_mutex_ref_counts = {}

    pre_key_manager = PreKeyManager(state, logger)

    def get_queue(key):
        if key not in key_queues:
            key_queues[key] = asyncio.Lock()
        return key_queues[key]

    def get_tx_mutex(key):
        if key not in tx_mutexes:
            tx_mutexes[key] = asyncio.Lock()
            tx_mutex_ref_counts[key] = 0
        return tx_mutexes[key]

    def acquire_tx_mutex_ref(key):
        tx_mutex_ref_counts[key] = tx_mutex_ref_counts.get(key, 0) + 1

    def release_tx_mutex_ref(key):
        count = tx_mutex_ref_counts.get(key, 1) - 1
        tx_mutex_ref_counts[key] = count
        if count <= 0:
            tx_mutexes.pop(key, None)
            tx_mutex_ref_counts.pop(key, None)

    def is_in_transaction():
        return tx_storage.get_store() is not None

    async def commit_with_retry(mutations):
        if not mutations:
            logger.trace('no mutations in transaction')
            return
        logger.trace('committing transaction')
        for attempt in range(max_commit_retries):
            try:
                await state['set'](mutations)
                logger.trace({'mutationCount': len(mutations)}, 'committed transaction')
                return
            except Exception as error:
                retries_left = max_commit_retries - attempt - 1
                logger.warn(f'failed to commit mutations, retries left={retries_left}')
                if retries_left == 0:
                    raise error
                await delay(delay_between_tries_ms)

    async def get(type_, ids):
        ctx = tx_storage.get_store()
        if not ctx:
            return await state['get'](type_, ids)

        cached = ctx.cache.get(type_) or {}
        missing = [id_ for id_ in ids if id_ not in cached]

        if missing:
            ctx.db_queries += 1
            logger.trace({'type': type_, 'count': len(missing)}, 'fetching missing keys in transaction')
            async with get_tx_mutex(type_):
                fetched = await state['get'](type_, missing)
            ctx.cache[type_] = ctx.cache.get(type_) or {}
            ctx.cache[type_].update(fetched)

        result = {}
        for id_ in ids:
            value = ctx.cache[type_].get(id_) if type_ in ctx.cache else None
            if value is not None:
                result[id_] = value
        return result

    async def set(data):
        ctx = tx_storage.get_store()
        if not ctx:
            types = list(data.keys())
            for type_ in types:
                if type_ == 'pre-key':
                    await pre_key_manager.validate_deletions(data, type_)

            tasks = []
            for type_ in types:
                async def _write(type_=type_):
                    async with get_queue(type_):
                        await state['set']({type_: data[type_]})
                tasks.append(asyncio.ensure_future(_write()))
            await asyncio.gather(*tasks)
            return

        logger.trace({'types': list(data.keys())}, 'caching in transaction')
        for key in data:
            ctx.cache[key] = ctx.cache.get(key) or {}
            ctx.mutations[key] = ctx.mutations.get(key) or {}
            if key == 'pre-key':
                await pre_key_manager.process_operations(data, key, ctx.cache, ctx.mutations, True)
            else:
                ctx.cache[key].update(data[key])
                ctx.mutations[key].update(data[key])

    async def transaction(work, key):
        existing = tx_storage.get_store()
        if existing:
            logger.trace('reusing existing transaction context')
            return await work()

        mutex = get_tx_mutex(key)
        acquire_tx_mutex_ref(key)
        try:
            async with mutex:
                ctx = _TransactionContext()
                logger.trace('entering transaction')
                try:
                    result = tx_storage.run(ctx, work)
                    if asyncio.iscoroutine(result):
                        result = await result
                    await commit_with_retry(ctx.mutations)
                    logger.trace({'dbQueries': ctx.db_queries}, 'transaction completed')
                    return result
                except Exception as error:
                    logger.error({'error': error}, 'transaction failed, rolling back')
                    raise
        finally:
            release_tx_mutex_ref(key)

    return SignalKeyStore({
        'get': get,
        'set': set,
        'isInTransaction': is_in_transaction,
        'is_in_transaction': is_in_transaction,
        'transaction': transaction,
    })


def assert_me_id(creds: dict) -> str:
    id_ = (creds.get('me') or {}).get('id')
    if not id_:
        raise Boom('Cannot proceed: socket is not authenticated yet (creds.me.id is missing)', 401)
    return id_


def init_auth_creds() -> dict:
    identity_key = Curve.generate_key_pair()
    return {
        'noiseKey': Curve.generate_key_pair(),
        'pairingEphemeralKeyPair': Curve.generate_key_pair(),
        'signedIdentityKey': identity_key,
        'signedPreKey': signed_key_pair(identity_key, 1),
        'registrationId': generate_registration_id(),
        'advSecretKey': __import__('base64').b64encode(__import__('os').urandom(32)).decode('ascii'),
        'processedHistoryMessages': [],
        'nextPreKeyId': 1,
        'firstUnuploadedPreKeyId': 1,
        'accountSyncCounter': 0,
        'accountSettings': {'unarchiveChats': False},
        'registered': False,
        'pairingCode': None,
        'lastPropHash': None,
        'routingInfo': None,
        'additionalData': None,
    }


def make_memory_key_store():
    """In-memory SignalKeyStore: {get, set, clear} as used by the auth state."""

    store = {}

    async def get(type_, ids):
        data = store.get(type_) or {}
        return {i: data[i] for i in ids if i in data}

    async def set(data):
        for type_, entries in data.items():
            bucket = store.setdefault(type_, {})
            for id_, value in entries.items():
                if value is None:
                    bucket.pop(id_, None)
                else:
                    bucket[id_] = value

    async def clear():
        store.clear()

    return SignalKeyStore({'get': get, 'set': set, 'clear': clear})
