"""Port of src/Utils/tc-token-utils.ts — trusted-contact token helpers."""

from __future__ import annotations

import json
import re
import time

from ..WABinary.generic_utils import get_binary_node_child, get_binary_node_children
from ..WABinary.jid_utils import (
    is_hosted_lid_user,
    is_hosted_pn_user,
    is_jid_meta_ai,
    is_lid_user,
    is_pn_user,
    jid_normalized_user,
)

# Same phone-number pattern as WABinary's is_jid_bot, applied against the user
# part so the check is invariant to @c.us <-> @s.whatsapp.net normalization.
BOT_PHONE_REGEX = re.compile(r'^1313555\d{4}$|^131655500\d{2}$')


def is_regular_user(jid) -> bool:
    """Mirror WA Web's Wid.isRegularUser() (user ^ !PSA ^ !Bot)."""
    if not jid:
        return False
    user = jid.split('@')[0] or ''
    if user == '0':
        return False  # PSA
    if BOT_PHONE_REGEX.match(user):
        return False  # Bot by phone pattern
    if is_jid_meta_ai(jid):
        return False  # MetaAI (@bot server)
    return bool(is_pn_user(jid) or is_lid_user(jid) or is_hosted_pn_user(jid) or is_hosted_lid_user(jid) or jid.endswith('@c.us'))


TC_TOKEN_BUCKET_DURATION = 604800  # 7 days
TC_TOKEN_NUM_BUCKETS = 4  # ~28-day rolling window

# Sentinel key under `tctoken` store holding a JSON array of tracked storage JIDs for cross-session pruning.
TC_TOKEN_INDEX_KEY = '__index'


async def read_tc_token_index(keys) -> list:
    """Read the persisted tctoken JID index and return its entries (never contains the sentinel key itself)."""
    data = await keys.get('tctoken', [TC_TOKEN_INDEX_KEY])
    entry = data.get(TC_TOKEN_INDEX_KEY)
    if not entry or not entry.get('token'):
        return []
    try:
        parsed = json.loads(bytes(entry['token']).decode('utf-8'))
        if not isinstance(parsed, list):
            return []
        return [j for j in parsed if isinstance(j, str) and len(j) > 0 and j != TC_TOKEN_INDEX_KEY]
    except Exception:
        return []


async def build_merged_tc_token_index_write(keys, added_jids) -> dict:
    """Build a SignalDataSet fragment that writes the merged index (persisted U added) under the sentinel key."""
    persisted = await read_tc_token_index(keys)
    merged = set(persisted)
    for jid in added_jids:
        if jid and jid != TC_TOKEN_INDEX_KEY:
            merged.add(jid)

    return {TC_TOKEN_INDEX_KEY: {'token': json.dumps(list(merged)).encode('utf-8')}}


def is_tc_token_expired(timestamp) -> bool:
    """WA Web has separate sender/receiver AB props for these but they're identical today."""
    if timestamp is None:
        return True
    try:
        ts = int(timestamp) if isinstance(timestamp, str) else timestamp
    except (TypeError, ValueError):
        return True
    now = int(time.time())
    current_bucket = now // TC_TOKEN_BUCKET_DURATION
    cutoff_bucket = current_bucket - (TC_TOKEN_NUM_BUCKETS - 1)
    cutoff_timestamp = cutoff_bucket * TC_TOKEN_BUCKET_DURATION
    return ts < cutoff_timestamp


def should_send_new_tc_token(sender_timestamp) -> bool:
    if sender_timestamp is None:
        return True
    now = int(time.time())
    current_bucket = now // TC_TOKEN_BUCKET_DURATION
    sender_bucket = int(sender_timestamp) // TC_TOKEN_BUCKET_DURATION
    return current_bucket > sender_bucket


async def resolve_tc_token_jid(jid: str, get_lid_for_pn) -> str:
    """Resolve JID to LID for tctoken storage (WA Web stores under LID)."""
    if is_lid_user(jid):
        return jid
    lid = await get_lid_for_pn(jid)
    return lid or jid


async def resolve_issuance_jid(jid: str, issue_to_lid: bool, get_lid_for_pn, get_pn_for_lid=None) -> str:
    """Resolve target JID for issuing privacy token based on AB prop 14303."""
    if issue_to_lid:
        if is_lid_user(jid):
            return jid
        lid = await get_lid_for_pn(jid)
        return lid or jid

    if not is_lid_user(jid):
        return jid
    if get_pn_for_lid is not None:
        pn = await get_pn_for_lid(jid)
        return pn or jid

    return jid


async def build_tc_token_from_jid(auth_state, jid, base_content=None, get_lid_for_pn=None):
    """Build a tctoken node for the given jid, if a valid stored token exists."""
    base_content = base_content or []
    try:
        storage_jid = await resolve_tc_token_jid(jid, get_lid_for_pn)
        tc_token_data = await auth_state['keys'].get('tctoken', [storage_jid])
        entry = (tc_token_data or {}).get(storage_jid) or {}
        tc_token_buffer = entry.get('token')
        timestamp = entry.get('timestamp')

        if not tc_token_buffer or timestamp is None or is_tc_token_expired(timestamp):
            if tc_token_buffer:
                # Preserve senderTimestamp so shouldSendNewTcToken() keeps its dedupe state
                # after we drop the unusable peer token.
                if entry.get('senderTimestamp') is not None:
                    cleared = {'token': b'', 'senderTimestamp': entry['senderTimestamp']}
                else:
                    cleared = None
                await auth_state['keys'].set({'tctoken': {storage_jid: cleared}})

            return base_content if len(base_content) > 0 else None

        from ..WABinary.types import BinaryNode

        base_content.append(BinaryNode(
            tag='tctoken',
            attrs={'t': str(timestamp)},
            content=tc_token_buffer,
        ))

        return base_content
    except Exception:
        return base_content if len(base_content) > 0 else None


async def store_tc_tokens_from_iq_result(result, fallback_jid, keys, get_lid_for_pn, on_new_jid_stored=None):
    tokens_node = get_binary_node_child(result, 'tokens')
    if not tokens_node:
        return

    token_nodes = get_binary_node_children(tokens_node, 'token')
    for token_node in token_nodes:
        if token_node.attrs.get('type') != 'trusted_contact' or not isinstance(token_node.content, bytes):
            continue

        # In notifications tokenNode.attrs.jid is your own device JID, not the sender's
        raw_jid = jid_normalized_user(fallback_jid or token_node.attrs.get('jid'))
        if not is_regular_user(raw_jid):
            continue
        storage_jid = await resolve_tc_token_jid(raw_jid, get_lid_for_pn)
        existing_tc_data = await keys.get('tctoken', [storage_jid])
        existing_entry = (existing_tc_data or {}).get(storage_jid) or {}

        try:
            existing_ts = int(existing_entry.get('timestamp') or 0) if existing_entry.get('timestamp') is not None else 0
        except (TypeError, ValueError):
            existing_ts = 0
        try:
            incoming_ts = int(token_node.attrs.get('t') or 0) if token_node.attrs.get('t') else 0
        except (TypeError, ValueError):
            incoming_ts = 0
        # timestamp-less tokens would be immediately expired
        if not incoming_ts:
            continue
        if existing_ts > 0 and existing_ts > incoming_ts:
            continue

        merged = dict(existing_entry)
        merged['token'] = bytes(token_node.content)
        merged['timestamp'] = token_node.attrs.get('t')

        await keys.set({'tctoken': {storage_jid: merged}})
        if on_new_jid_stored is not None:
            on_new_jid_stored(storage_jid)
