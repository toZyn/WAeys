"""Port of src/Utils/pre-key-manager.ts — PreKeyManager."""

from __future__ import annotations

import asyncio


class PreKeyManager:
    """Manages pre-key operations with proper concurrency control."""

    def __init__(self, store: dict, logger=None):
        self.store = store
        self.logger = logger
        self.queues = {}

    def _get_queue(self, key_type: str) -> asyncio.Lock:
        if key_type not in self.queues:
            self.queues[key_type] = asyncio.Lock()
        return self.queues[key_type]

    async def process_operations(self, data, key_type, transaction_cache, mutations, is_in_transaction):
        key_data = data.get(key_type)
        if not key_data:
            return

        async with self._get_queue(key_type):
            transaction_cache[key_type] = transaction_cache.get(key_type) or {}
            mutations[key_type] = mutations.get(key_type) or {}

            deletions = []
            updates = {}
            for key_id, value in key_data.items():
                if value is None:
                    deletions.append(key_id)
                else:
                    updates[key_id] = value

            if updates:
                transaction_cache[key_type].update(updates)
                mutations[key_type].update(updates)

            if deletions:
                await self._process_deletions(key_type, deletions, transaction_cache, mutations, is_in_transaction)

    async def _process_deletions(self, key_type, ids, transaction_cache, mutations, is_in_transaction):
        if is_in_transaction:
            for key_id in ids:
                if transaction_cache[key_type].get(key_id):
                    transaction_cache[key_type][key_id] = None
                    mutations[key_type][key_id] = None
                else:
                    if self.logger:
                        self.logger.warn(f'Skipping deletion of non-existent {key_type} in transaction: {key_id}')
        else:
            existing_keys = await self.store['get'](key_type, ids)
            for key_id in ids:
                if existing_keys.get(key_id):
                    transaction_cache[key_type][key_id] = None
                    mutations[key_type][key_id] = None
                else:
                    if self.logger:
                        self.logger.warn(f'Skipping deletion of non-existent {key_type}: {key_id}')

    async def validate_deletions(self, data, key_type):
        key_data = data.get(key_type)
        if not key_data:
            return

        async with self._get_queue(key_type):
            deletion_ids = [key_id for key_id, value in key_data.items() if value is None]
            if not deletion_ids:
                return

            existing_keys = await self.store['get'](key_type, deletion_ids)
            for key_id in deletion_ids:
                if not existing_keys.get(key_id):
                    if self.logger:
                        self.logger.warn(f'Skipping deletion of non-existent {key_type}: {key_id}')
                    del data[key_type][key_id]
