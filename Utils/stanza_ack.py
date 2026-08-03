"""Port of src/Utils/stanza-ack.ts — ACK stanza builder."""

from __future__ import annotations

from ..WABinary.types import BinaryNode


def build_ack_stanza(node: BinaryNode, error_code: int = None, me_id: str = None) -> BinaryNode:
    """Builds an ACK stanza for a received node. Pure function -- no I/O.

    Mirrors WhatsApp Web's ACK construction:
    - WAWebHandleMsgSendAck.sendAck / sendNack
    - WAWebCreateNackFromStanza.createNackFromStanza
    """
    attrs = node.attrs or {}
    stanza_attrs = {
        'id': attrs['id'],
        'to': attrs['from'],
        'class': node.tag,
    }

    if error_code:
        stanza_attrs['error'] = str(error_code)

    if attrs.get('participant'):
        stanza_attrs['participant'] = attrs['participant']

    if attrs.get('recipient'):
        stanza_attrs['recipient'] = attrs['recipient']

    # WA Web always includes type when present: `n.type || DROP_ATTR`
    if attrs.get('type'):
        stanza_attrs['type'] = attrs['type']

    # WA Web WAWebHandleMsgSendAck.sendAck/sendNack always include `from` for message-class ACKs
    if node.tag == 'message' and me_id:
        stanza_attrs['from'] = me_id

    return BinaryNode(tag='ack', attrs=stanza_attrs)
