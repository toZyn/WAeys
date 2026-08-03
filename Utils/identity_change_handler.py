"""Port of src/Utils/identity-change-handler.ts — E2E identity change handling."""

from __future__ import annotations

from ..WABinary.generic_utils import get_binary_node_child
from ..WABinary.jid_utils import are_jids_same_user, jid_decode
from .generics import is_string_null_or_empty


async def handle_identity_change(node, ctx: dict) -> dict:
    from_jid = (node.attrs or {}).get('from')
    if not from_jid:
        return {'action': 'invalid_notification'}

    identity_node = get_binary_node_child(node, 'identity')
    if not identity_node:
        return {'action': 'no_identity_node'}

    ctx['logger'].info({'jid': from_jid}, 'identity changed')

    decoded = jid_decode(from_jid)
    if decoded and decoded.device and decoded.device != 0:
        ctx['logger'].debug({'jid': from_jid, 'device': decoded.device}, 'ignoring identity change from companion device')
        return {'action': 'skipped_companion_device', 'device': decoded.device}

    is_self_primary = ctx['meId'] and (
        are_jids_same_user(from_jid, ctx['meId'])
        or (ctx['meLid'] and are_jids_same_user(from_jid, ctx['meLid']))
    )
    if is_self_primary:
        ctx['logger'].info({'jid': from_jid}, 'self primary identity changed')
        return {'action': 'skipped_self_primary'}

    if ctx['debounceCache'].get(from_jid):
        ctx['logger'].debug({'jid': from_jid}, 'skipping identity assert (debounced)')
        return {'action': 'debounced'}

    ctx['debounceCache'].set(from_jid, True)

    is_offline_notification = not is_string_null_or_empty((node.attrs or {}).get('offline'))
    has_existing_session = await ctx['validateSession'](from_jid)

    if not has_existing_session.get('exists'):
        ctx['logger'].debug({'jid': from_jid}, 'no old session, skipping session refresh')
        return {'action': 'skipped_no_session'}

    ctx['logger'].debug({'jid': from_jid}, 'old session exists, will refresh session')

    if is_offline_notification:
        ctx['logger'].debug({'jid': from_jid}, 'skipping session refresh during offline processing')
        return {'action': 'skipped_offline'}

    on_before = ctx.get('onBeforeSessionRefresh')
    if on_before is not None:
        on_before(from_jid)

    try:
        await ctx['assertSessions']([from_jid], True)
        return {'action': 'session_refreshed'}
    except Exception as error:
        ctx['logger'].warn({'error': error, 'jid': from_jid}, 'failed to assert sessions after identity change')
        return {'action': 'session_refresh_failed', 'error': error}
