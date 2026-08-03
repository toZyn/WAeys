"""Port of libsignal's GroupCipher (src/Signal/Group/group_cipher.ts)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ...Utils.crypto import aes_cbc_decrypt, aes_cbc_encrypt
from .sender_key_message import SenderKeyMessage
from .sender_key_name import SenderKeyName
from .sender_key_record import SenderKeyRecord

if TYPE_CHECKING:
    pass


class GroupCipher:
    def __init__(self, sender_key_store, sender_key_name: SenderKeyName):
        self._sender_key_store = sender_key_store
        self._sender_key_name = sender_key_name

    async def encrypt(self, padded_plaintext: bytes) -> bytes:
        record = await self._sender_key_store.load_sender_key(self._sender_key_name)
        if record is None:
            raise ValueError('No SenderKeyRecord found for encryption')

        sender_key_state = record.get_sender_key_state()
        if sender_key_state is None:
            raise ValueError('No session to encrypt message')

        iteration = sender_key_state.get_sender_chain_key().get_iteration()
        sender_key = self._get_sender_key(sender_key_state, 0 if iteration == 0 else iteration + 1)

        ciphertext = self._get_cipher_text(sender_key.get_iv(), sender_key.get_cipher_key(), padded_plaintext)

        sender_key_message = SenderKeyMessage(
            sender_key_state.get_key_id(),
            sender_key.get_iteration(),
            ciphertext,
            sender_key_state.get_signing_key_private(),
        )

        await self._sender_key_store.store_sender_key(self._sender_key_name, record)
        return sender_key_message.serialize()

    async def decrypt(self, sender_key_message_bytes: bytes) -> bytes:
        record = await self._sender_key_store.load_sender_key(self._sender_key_name)
        if record is None:
            raise ValueError('No SenderKeyRecord found for decryption')

        sender_key_message = SenderKeyMessage(None, None, None, None, sender_key_message_bytes)
        sender_key_state = record.get_sender_key_state(sender_key_message.get_key_id())
        if sender_key_state is None:
            raise ValueError('No session found to decrypt message')

        sender_key_message.verify_signature(sender_key_state.get_signing_key_public())
        sender_key = self._get_sender_key(sender_key_state, sender_key_message.get_iteration())

        plaintext = self._get_plain_text(
            sender_key.get_iv(),
            sender_key.get_cipher_key(),
            sender_key_message.get_cipher_text(),
        )

        await self._sender_key_store.store_sender_key(self._sender_key_name, record)
        return plaintext

    def _get_sender_key(self, sender_key_state, iteration: int):
        sender_chain_key = sender_key_state.get_sender_chain_key()
        if sender_chain_key.get_iteration() > iteration:
            if sender_key_state.has_sender_message_key(iteration):
                message_key = sender_key_state.remove_sender_message_key(iteration)
                if message_key is None:
                    raise ValueError('No sender message key found for iteration')
                return message_key

            raise ValueError(
                f'Received message with old counter: {sender_chain_key.get_iteration()}, {iteration}'
            )

        if iteration - sender_chain_key.get_iteration() > 2000:
            raise ValueError('Over 2000 messages into the future!')

        while sender_chain_key.get_iteration() < iteration:
            sender_key_state.add_sender_message_key(sender_chain_key.get_sender_message_key())
            sender_chain_key = sender_chain_key.get_next()

        sender_key_state.set_sender_chain_key(sender_chain_key.get_next())
        return sender_chain_key.get_sender_message_key()

    @staticmethod
    def _get_plain_text(iv: bytes, key: bytes, ciphertext: bytes) -> bytes:
        try:
            return aes_cbc_decrypt(ciphertext, key, iv)
        except Exception as e:
            raise ValueError('InvalidMessageException') from e

    @staticmethod
    def _get_cipher_text(iv: bytes, key: bytes, plaintext: bytes) -> bytes:
        try:
            return aes_cbc_encrypt(plaintext, key, iv)
        except Exception as e:
            raise ValueError('InvalidMessageException') from e
