"""Port of libsignal's GroupSessionBuilder (src/Signal/Group/group-session-builder.ts)."""

from __future__ import annotations

from ...Utils.crypto import Curve
from . import keyhelper
from .sender_key_distribution_message import SenderKeyDistributionMessage
from .sender_key_name import SenderKeyName
from .sender_key_record import SenderKeyRecord


class GroupSessionBuilder:
    def __init__(self, sender_key_store):
        self._sender_key_store = sender_key_store

    async def process(self, sender_key_name: SenderKeyName, sender_key_distribution_message: SenderKeyDistributionMessage) -> None:
        sender_key_record = await self._sender_key_store.load_sender_key(sender_key_name)
        sender_key_record.add_sender_key_state(
            sender_key_distribution_message.get_id(),
            sender_key_distribution_message.get_iteration(),
            sender_key_distribution_message.get_chain_key(),
            sender_key_distribution_message.get_signature_key(),
        )
        await self._sender_key_store.store_sender_key(sender_key_name, sender_key_record)

    async def create(self, sender_key_name: SenderKeyName) -> SenderKeyDistributionMessage:
        sender_key_record = await self._sender_key_store.load_sender_key(sender_key_name)

        if sender_key_record.is_empty():
            key_id = keyhelper.generate_sender_key_id()
            sender_key = keyhelper.generate_sender_key()
            signing_key = keyhelper.generate_sender_signing_key()

            sender_key_record.set_sender_key_state(key_id, 0, sender_key, signing_key)
            await self._sender_key_store.store_sender_key(sender_key_name, sender_key_record)

        state = sender_key_record.get_sender_key_state()
        if state is None:
            raise ValueError('No session state available')

        return SenderKeyDistributionMessage(
            state.get_key_id(),
            state.get_sender_chain_key().get_iteration(),
            state.get_sender_chain_key().get_seed(),
            state.get_signing_key_public(),
        )
