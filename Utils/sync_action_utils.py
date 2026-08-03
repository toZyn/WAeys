"""Port of src/Utils/sync-action-utils.ts — sync action event helpers."""

from __future__ import annotations

from ..WABinary.jid_utils import is_lid_user, is_pn_user


def process_contact_action(action: dict, id: str, logger=None) -> list:
    """Process contactAction and return events to emit. Pure function - no side effects."""
    results = []

    if not id:
        if logger is not None:
            logger.warn(
                {
                    'hasFullName': bool(action.get('fullName')),
                    'hasLidJid': bool(action.get('lidJid')),
                    'hasPnJid': bool(action.get('pnJid')),
                },
                'contactAction sync: missing id in index',
            )
        return results

    lid_jid = action.get('lidJid')
    id_is_pn = is_pn_user(id)
    # PN is in index[1], not in contactAction.pnJid which is usually null
    phone_number = id if id_is_pn else action.get('pnJid') or None

    # Always emit contacts.upsert
    results.append({
        'event': 'contacts.upsert',
        'data': [
            {
                'id': id,
                'name': action.get('fullName') or action.get('firstName') or action.get('username') or None,
                'username': action.get('username') or None,
                'lid': lid_jid or None,
                'phoneNumber': phone_number,
            }
        ],
    })

    # Emit lid-mapping.update if we have valid LID-PN pair
    if lid_jid and is_lid_user(lid_jid) and id_is_pn:
        results.append({
            'event': 'lid-mapping.update',
            'data': {'lid': lid_jid, 'pn': id},
        })

    return results


def emit_sync_action_results(ev, results: list) -> None:
    for result in results:
        if result['event'] == 'contacts.upsert':
            ev.emit('contacts.upsert', result['data'])
        else:
            ev.emit('lid-mapping.update', result['data'])
