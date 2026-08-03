"""Port of src/Signal/lid-mapping.ts (LIDMappingStore).

Maps phone-number JIDs to LID JIDs and back, with an in-memory TTL cache,
inflight-request coalescing and storage in the 'lid-mapping' key bucket.
"""

from __future__ import annotations

from typing import Optional

from ..Utils.lru_cache import LRUCache
from ..Utils.logger import logger
from ..WABinary.jid_utils import (
    WAJIDDomains,
    is_hosted_pn_user,
    is_hosted_lid_user,
    is_lid_user,
    is_pn_user,
    jid_decode,
    jid_normalized_user,
)


class LIDMappingStore:
    def __init__(self, keys, pn_to_lid_func=None):
        self.mapping_cache = LRUCache(
            ttl=3 * 24 * 60 * 60 * 1000,
            ttl_autopurge=True,
            update_age_on_get=True,
        )
        self.keys = keys
        self.pn_to_lid_func = pn_to_lid_func
        self.inflight_lid_lookups = {}
        self.inflight_pn_lookups = {}

    async def store_lidpn_mappings(self, pairs) -> None:
        if len(pairs) == 0:
            return

        validated_pairs = []
        for pair in pairs:
            lid = pair.get('lid')
            pn = pair.get('pn')
            if not ((is_lid_user(lid) and is_pn_user(pn)) or (is_pn_user(lid) and is_lid_user(pn))):
                logger.warn(f'Invalid LID-PN mapping: {lid}, {pn}')
                continue
            lid_decoded = jid_decode(lid)
            pn_decoded = jid_decode(pn)
            if not lid_decoded or not pn_decoded:
                continue
            validated_pairs.append({'pnUser': pn_decoded.user, 'lidUser': lid_decoded.user})

        if len(validated_pairs) == 0:
            return

        cache_miss_set = set()
        existing_mappings = {}

        for pair in validated_pairs:
            pn_user = pair['pnUser']
            cached = self.mapping_cache.get(f'pn:{pn_user}')
            if cached:
                existing_mappings[pn_user] = cached
            else:
                cache_miss_set.add(pn_user)

        if len(cache_miss_set) > 0:
            cache_misses = sorted(cache_miss_set)
            logger.debug(f'Batch fetching {len(cache_misses)} LID mappings from database')
            stored = await self.keys.get('lid-mapping', cache_misses)
            for pn_user in cache_misses:
                existing_lid_user = stored.get(pn_user)
                if existing_lid_user:
                    existing_mappings[pn_user] = existing_lid_user
                    self.mapping_cache.set(f'pn:{pn_user}', existing_lid_user)
                    self.mapping_cache.set(f'lid:{existing_lid_user}', pn_user)

        pair_map = {}
        for pair in validated_pairs:
            pn_user = pair['pnUser']
            lid_user = pair['lidUser']
            existing_lid_user = existing_mappings.get(pn_user)
            if existing_lid_user == lid_user:
                logger.debug({pn_user: pn_user, lid_user: lid_user}, 'LID mapping already exists, skipping')
                continue
            pair_map[pn_user] = lid_user

        if len(pair_map) == 0:
            return

        logger.debug({'pairMap': pair_map}, f"Storing {len(pair_map)} pn mappings")

        batch_data = {}
        for pn_user, lid_user in pair_map.items():
            batch_data[pn_user] = lid_user
            batch_data[f'{lid_user}_reverse'] = pn_user

        await self.keys.transaction(lambda: self.keys.set({'lid-mapping': batch_data}), 'lid-mapping')

        for pn_user, lid_user in pair_map.items():
            self.mapping_cache.set(f'pn:{pn_user}', lid_user)
            self.mapping_cache.set(f'lid:{lid_user}', pn_user)

    async def get_lid_for_pn(self, pn: str) -> Optional[str]:
        result = await self.get_lids_for_pns([pn])
        return result[0].get('lid') if result else None

    async def get_lids_for_pns(self, pns):
        if len(pns) == 0:
            return None
        sorted_pns = sorted(set(pns))
        cache_key = ','.join(sorted_pns)
        inflight = self.inflight_lid_lookups.get(cache_key)
        if inflight is not None:
            logger.debug(f'Coalescing getLIDsForPNs request for {len(sorted_pns)} PNs')
            return await inflight

        promise = self._get_lids_for_pns_impl(pns)
        self.inflight_lid_lookups[cache_key] = promise
        try:
            return await promise
        finally:
            self.inflight_lid_lookups.pop(cache_key, None)

    async def _get_lids_for_pns_impl(self, pns):
        usync_fetch = {}
        successful_pairs = {}
        pending = []

        def add_resolved_pair(pn, decoded, lid_user):
            normalized_lid_user = str(lid_user)
            if not normalized_lid_user:
                logger.warn(f'Invalid or empty LID user for PN {pn}: lidUser = "{lid_user}"')
                return False
            pn_device = decoded.device if decoded.device is not None else 0
            device_specific_lid = (
                f'{normalized_lid_user}' + (f':{pn_device}' if pn_device else '')
                + ('@hosted.lid' if decoded.server == 'hosted' else '@lid')
            )
            logger.debug(f'getLIDForPN: {pn} -> {device_specific_lid} (user mapping with device {pn_device})')
            successful_pairs[pn] = {'lid': device_specific_lid, 'pn': pn}
            return True

        for pn in pns:
            if not is_pn_user(pn) and not is_hosted_pn_user(pn):
                continue
            decoded = jid_decode(pn)
            if not decoded:
                continue
            pn_user = decoded.user
            cached = self.mapping_cache.get(f'pn:{pn_user}')
            if cached and isinstance(cached, str):
                if not add_resolved_pair(pn, decoded, cached):
                    logger.warn(f'Invalid entry for {pn} (pair not resolved)')
                continue
            pending.append({'pn': pn, 'pnUser': pn_user, 'decoded': decoded})

        if len(pending):
            pn_users = sorted(set(item['pnUser'] for item in pending))
            stored = await self.keys.get('lid-mapping', pn_users)
            for pn_user in pn_users:
                lid_user = stored.get(pn_user)
                if lid_user and isinstance(lid_user, str):
                    self.mapping_cache.set(f'pn:{pn_user}', lid_user)
                    self.mapping_cache.set(f'lid:{lid_user}', pn_user)

            for item in pending:
                pn = item['pn']
                pn_user = item['pnUser']
                decoded = item['decoded']
                cached = self.mapping_cache.get(f'pn:{pn_user}')
                if cached and isinstance(cached, str):
                    if not add_resolved_pair(pn, decoded, cached):
                        logger.warn(f'Invalid entry for {pn} (pair not resolved)')
                else:
                    logger.debug(f'No LID mapping found for PN user {pn_user}; batch getting from USync')
                    device = decoded.device or 0
                    normalized_pn = jid_normalized_user(pn)
                    if is_hosted_pn_user(normalized_pn):
                        normalized_pn = f'{pn_user}@s.whatsapp.net'
                    if normalized_pn not in usync_fetch:
                        usync_fetch[normalized_pn] = [device]
                    else:
                        usync_fetch[normalized_pn].append(device)

        if len(usync_fetch) > 0:
            result = await self.pn_to_lid_func(list(usync_fetch.keys())) if self.pn_to_lid_func else None
            if result and len(result) > 0:
                await self.store_lidpn_mappings(result)
                for pair in result:
                    pn_decoded = jid_decode(pair.get('pn'))
                    pn_user = pn_decoded.user if pn_decoded else None
                    if not pn_user:
                        continue
                    lid_user_decoded = jid_decode(pair.get('lid'))
                    lid_user = lid_user_decoded.user if lid_user_decoded else None
                    if not lid_user:
                        continue
                    for device in usync_fetch.get(pair.get('pn'), []):
                        device_specific_lid = (
                            f'{lid_user}' + (f':{device}' if device else '')
                            + ('@hosted.lid' if device == 99 else '@lid')
                        )
                        logger.debug(
                            f'getLIDForPN: USYNC success for {pair["pn"]} -> '
                            f'{device_specific_lid} (user mapping with device {device})'
                        )
                        device_specific_pn = (
                            f'{pn_user}' + (f':{device}' if device else '')
                            + ('@hosted' if device == 99 else '@s.whatsapp.net')
                        )
                        successful_pairs[device_specific_pn] = {
                            'lid': device_specific_lid,
                            'pn': device_specific_pn,
                        }
            else:
                logger.warn('USync fetch yielded no results for pending PNs')

        return list(successful_pairs.values()) if len(successful_pairs) > 0 else None

    async def get_pn_for_lid(self, lid: str) -> Optional[str]:
        result = await self.get_pns_for_lids([lid])
        return result[0].get('pn') if result else None

    async def get_pns_for_lids(self, lids):
        if len(lids) == 0:
            return None
        sorted_lids = sorted(set(lids))
        cache_key = ','.join(sorted_lids)
        inflight = self.inflight_pn_lookups.get(cache_key)
        if inflight is not None:
            logger.debug(f'Coalescing getPNsForLIDs request for {len(sorted_lids)} LIDs')
            return await inflight

        promise = self._get_pns_for_lids_impl(lids)
        self.inflight_pn_lookups[cache_key] = promise
        try:
            return await promise
        finally:
            self.inflight_pn_lookups.pop(cache_key, None)

    async def _get_pns_for_lids_impl(self, lids):
        successful_pairs = {}
        pending = []

        def add_resolved_pair(lid, decoded, pn_user):
            if not pn_user or not isinstance(pn_user, str):
                return False
            lid_device = decoded.device if decoded.device is not None else 0
            server = 'hosted' if decoded.domainType == WAJIDDomains.HOSTED_LID else 's.whatsapp.net'
            pn_jid = f'{pn_user}:{lid_device}@{server}'
            logger.debug(f'Found reverse mapping: {lid} -> {pn_jid}')
            successful_pairs[lid] = {'lid': lid, 'pn': pn_jid}
            return True

        for lid in lids:
            if not is_lid_user(lid):
                continue
            decoded = jid_decode(lid)
            if not decoded:
                continue
            lid_user = decoded.user
            cached = self.mapping_cache.get(f'lid:{lid_user}')
            if cached and isinstance(cached, str):
                add_resolved_pair(lid, decoded, cached)
                continue
            pending.append({'lid': lid, 'lidUser': lid_user, 'decoded': decoded})

        if len(pending):
            reverse_keys = sorted(set(f"{item['lidUser']}_reverse" for item in pending))
            stored = await self.keys.get('lid-mapping', reverse_keys)
            for item in pending:
                lid = item['lid']
                lid_user = item['lidUser']
                decoded = item['decoded']
                pn_user = self.mapping_cache.get(f'lid:{lid_user}')
                if not pn_user or not isinstance(pn_user, str):
                    pn_user = stored.get(f'{lid_user}_reverse')
                    if pn_user and isinstance(pn_user, str):
                        self.mapping_cache.set(f'lid:{lid_user}', pn_user)
                        self.mapping_cache.set(f'pn:{pn_user}', lid_user)
                if pn_user and isinstance(pn_user, str):
                    add_resolved_pair(lid, decoded, pn_user)
                else:
                    logger.debug(f'No reverse mapping found for LID user: {lid_user}')

        return list(successful_pairs.values()) if len(successful_pairs) else None

    def close(self) -> None:
        self.mapping_cache.clear()
