"""Port of libsignal's SessionCipher (src/session_cipher.js).

Implements the Signal double-ratchet: X3DH-style session setup, symmetric
ratchet on each chain, HKDF key derivation and message MACs.

Storage is an object with async methods:
  loadSession(addr) -> SessionRecord | None
  storeSession(addr, record)
  isTrustedIdentity(id, identityKey) -> bool
  getOurIdentity() -> {privKey, pubKey}
  getOurRegistrationId() -> int
  loadPreKey(id) -> {privKey, pubKey} | None
  loadSignedPreKey(id) -> {privKey, pubKey} | None
  removePreKey(id)
"""

from __future__ import annotations

import logging
import time

from .libsignal_constants import ChainType
from .libsignal_crypto import calculate_mac, decrypt, derive_secrets, encrypt, verify_mac
from .libsignal_curve import calculate_agreement, generate_key_pair
from .libsignal_errors import MessageCounterError, PreKeyError, SessionError, UntrustedIdentityKeyError
from .libsignal_queue_job import queue_job
from .libsignal_session_record import SessionEntry, SessionRecord
from .libsignal_session_builder import SessionBuilder
from .protocol_address import ProtocolAddress
from .whisper_text_protocol import PreKeyWhisperMessage, WhisperMessage

logger = logging.getLogger(__name__)

VERSION = 3


def _encode_tuple_byte(number1: int, number2: int) -> int:
    if number1 > 15 or number2 > 15:
        raise TypeError('Numbers must be 4 bits or less')
    return (number1 << 4) | number2


def _decode_tuple_byte(byte: int):
    return [byte >> 4, byte & 0xf]


class SessionCipher:
    def __init__(self, storage, protocol_address: ProtocolAddress):
        if not isinstance(protocol_address, ProtocolAddress):
            raise TypeError('protocolAddress must be a ProtocolAddress')
        self.addr = protocol_address
        self.storage = storage

    async def get_record(self):
        record = await self.storage.loadSession(self.addr.__str__())
        if record is not None and not isinstance(record, SessionRecord):
            raise TypeError('SessionRecord type expected from loadSession')
        return record

    async def store_record(self, record: SessionRecord) -> None:
        record.remove_old_sessions()
        await self.storage.storeSession(self.addr.__str__(), record)

    async def queue_job(self, awaitable):
        return await queue_job(self.addr.__str__(), awaitable)

    async def encrypt(self, data: bytes) -> dict:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f'Expected Buffer instead of: {type(data).__name__}')
        data = bytes(data)
        our_identity_key = await self.storage.getOurIdentity()

        async def _do():
            record = await self.get_record()
            if not record:
                raise SessionError('No sessions')
            session = record.get_open_session()
            if not session:
                raise SessionError('No open session')
            remote_identity_key = session.indexInfo['remoteIdentityKey']
            if not await self.storage.isTrustedIdentity(self.addr.id, remote_identity_key):
                raise UntrustedIdentityKeyError(self.addr.id, remote_identity_key)

            chain = session.get_chain(session.currentRatchet['ephemeralKeyPair']['pubKey'])
            if chain['chainType'] == ChainType.RECEIVING:
                raise ValueError('Tried to encrypt on a receiving chain')
            self.fill_message_keys(chain, chain['chainKey']['counter'] + 1)
            keys = derive_secrets(
                chain['messageKeys'][chain['chainKey']['counter']],
                bytes(32),
                b'WhisperMessageKeys',
            )
            del chain['messageKeys'][chain['chainKey']['counter']]

            msg = WhisperMessage(
                ephemeralKey=session.currentRatchet['ephemeralKeyPair']['pubKey'],
                counter=chain['chainKey']['counter'],
                previousCounter=session.currentRatchet['previousCounter'],
                ciphertext=encrypt(keys[0], data, keys[2][:16]),
            )
            msg_buf = WhisperMessage.encode(msg)

            mac_input = bytearray(len(msg_buf) + (33 * 2) + 1)
            mac_input[0:33] = our_identity_key['pubKey']
            mac_input[33:66] = session.indexInfo['remoteIdentityKey']
            mac_input[66] = _encode_tuple_byte(VERSION, VERSION)
            mac_input[67:] = msg_buf
            mac = calculate_mac(keys[1], bytes(mac_input))

            result = bytearray(len(msg_buf) + 9)
            result[0] = _encode_tuple_byte(VERSION, VERSION)
            result[1:1 + len(msg_buf)] = msg_buf
            result[1 + len(msg_buf):] = mac[:8]
            await self.store_record(record)

            if session.pendingPreKey:
                msg_type = 3
                pre_key_msg = PreKeyWhisperMessage(
                    identityKey=our_identity_key['pubKey'],
                    registrationId=await self.storage.getOurRegistrationId(),
                    baseKey=session.pendingPreKey['baseKey'],
                    signedPreKeyId=session.pendingPreKey['signedKeyId'],
                    message=bytes(result),
                )
                if session.pendingPreKey.get('preKeyId'):
                    pre_key_msg.preKeyId = session.pendingPreKey['preKeyId']
                body = bytes([_encode_tuple_byte(VERSION, VERSION)]) + PreKeyWhisperMessage.encode(pre_key_msg)
            else:
                msg_type = 1
                body = bytes(result)
            return {
                'type': msg_type,
                'body': body,
                'registrationId': session.registrationId,
            }

        return await self.queue_job(_do())

    async def decrypt_with_sessions(self, data: bytes, sessions):
        if not sessions:
            raise SessionError('No sessions available')
        errs = []
        for session in sessions:
            try:
                plaintext = await self.do_decrypt_whisper_message(data, session)
                session.indexInfo['used'] = int(time.time() * 1000)
                return {'session': session, 'plaintext': plaintext}
            except Exception as e:
                errs.append(e)
        logger.error('Failed to decrypt message with any known session...')
        for e in errs:
            logger.error('Session error: %s', e)
        raise SessionError('No matching sessions found for message')

    async def decrypt_whisper_message(self, data: bytes) -> bytes:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f'Expected Buffer instead of: {type(data).__name__}')
        data = bytes(data)

        async def _do():
            record = await self.get_record()
            if not record:
                raise SessionError('No session record')
            result = await self.decrypt_with_sessions(data, record.get_sessions())
            remote_identity_key = result['session'].indexInfo['remoteIdentityKey']
            if not await self.storage.isTrustedIdentity(self.addr.id, remote_identity_key):
                raise UntrustedIdentityKeyError(self.addr.id, remote_identity_key)
            if record.is_closed(result['session']):
                logger.warning('Decrypted message with closed session.')
            await self.store_record(record)
            return result['plaintext']

        return await self.queue_job(_do())

    async def decrypt_pre_key_whisper_message(self, data: bytes) -> bytes:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f'Expected Buffer instead of: {type(data).__name__}')
        data = bytes(data)
        versions = _decode_tuple_byte(data[0])
        if versions[1] > 3 or versions[0] < 3:
            raise ValueError('Incompatible version number on PreKeyWhisperMessage')

        async def _do():
            record = await self.get_record()
            pre_key_proto = PreKeyWhisperMessage.decode(data[1:])
            if not record:
                if pre_key_proto.registrationId is None:
                    raise ValueError('No registrationId')
                record = SessionRecord()
            builder = SessionBuilder(self.storage, self.addr)
            pre_key_id = await builder.init_incoming(record, pre_key_proto)
            session = record.get_session(pre_key_proto.baseKey)
            plaintext = await self.do_decrypt_whisper_message(pre_key_proto.message, session)
            await self.store_record(record)
            if pre_key_id:
                await self.storage.removePreKey(pre_key_id)
            return plaintext

        return await self.queue_job(_do())

    async def do_decrypt_whisper_message(self, message_buffer: bytes, session: SessionEntry) -> bytes:
        if not isinstance(message_buffer, (bytes, bytearray)):
            raise TypeError(f'Expected Buffer instead of: {type(message_buffer).__name__}')
        message_buffer = bytes(message_buffer)
        if not session:
            raise TypeError('session required')
        versions = _decode_tuple_byte(message_buffer[0])
        if versions[1] > 3 or versions[0] < 3:
            raise ValueError('Incompatible version number on WhisperMessage')
        message_proto = message_buffer[1:-8]
        message = WhisperMessage.decode(message_proto)
        self.maybe_step_ratchet(session, message.ephemeralKey, message.previousCounter)
        chain = session.get_chain(message.ephemeralKey)
        if chain['chainType'] == ChainType.SENDING:
            raise ValueError('Tried to decrypt on a sending chain')
        self.fill_message_keys(chain, message.counter)
        if message.counter not in chain['messageKeys']:
            raise MessageCounterError('Key used already or never filled')
        message_key = chain['messageKeys'][message.counter]
        del chain['messageKeys'][message.counter]
        keys = derive_secrets(message_key, bytes(32), b'WhisperMessageKeys')

        our_identity_key = await self.storage.getOurIdentity()
        mac_input = bytearray(len(message_proto) + (33 * 2) + 1)
        mac_input[0:33] = session.indexInfo['remoteIdentityKey']
        mac_input[33:66] = our_identity_key['pubKey']
        mac_input[66] = _encode_tuple_byte(VERSION, VERSION)
        mac_input[67:] = message_proto
        verify_mac(bytes(mac_input), keys[1], message_buffer[-8:], 8)

        plaintext = decrypt(keys[0], message.ciphertext, keys[2][:16])
        session.pendingPreKey = None
        return plaintext

    def fill_message_keys(self, chain: dict, counter: int) -> None:
        if chain['chainKey']['counter'] >= counter:
            return
        if counter - chain['chainKey']['counter'] > 2000:
            raise SessionError('Over 2000 messages into the future!')
        if chain['chainKey'].get('key') is None:
            raise SessionError('Chain closed')
        key = chain['chainKey']['key']
        chain['messageKeys'][chain['chainKey']['counter'] + 1] = calculate_mac(key, bytes([1]))
        chain['chainKey']['key'] = calculate_mac(key, bytes([2]))
        chain['chainKey']['counter'] += 1
        self.fill_message_keys(chain, counter)

    def maybe_step_ratchet(self, session: SessionEntry, remote_key: bytes, previous_counter: int) -> None:
        if session.get_chain(remote_key):
            return
        ratchet = session.currentRatchet
        previous_ratchet = session.get_chain(ratchet['lastRemoteEphemeralKey'])
        if previous_ratchet:
            self.fill_message_keys(previous_ratchet, previous_counter)
            previous_ratchet['chainKey'].pop('key', None)
        self.calculate_ratchet(session, remote_key, False)
        prev_counter = session.get_chain(ratchet['ephemeralKeyPair']['pubKey'])
        if prev_counter:
            ratchet['previousCounter'] = prev_counter['chainKey']['counter']
            session.delete_chain(ratchet['ephemeralKeyPair']['pubKey'])
        ratchet['ephemeralKeyPair'] = generate_key_pair()
        self.calculate_ratchet(session, remote_key, True)
        ratchet['lastRemoteEphemeralKey'] = remote_key

    def calculate_ratchet(self, session: SessionEntry, remote_key: bytes, sending: bool) -> None:
        ratchet = session.currentRatchet
        shared_secret = calculate_agreement(remote_key, ratchet['ephemeralKeyPair']['privKey'])
        master_key = derive_secrets(shared_secret, ratchet['rootKey'], b'WhisperRatchet', 2)
        chain_key = ratchet['ephemeralKeyPair']['pubKey'] if sending else remote_key
        session.add_chain(chain_key, {
            'messageKeys': {},
            'chainKey': {
                'counter': -1,
                'key': master_key[1],
            },
            'chainType': ChainType.SENDING if sending else ChainType.RECEIVING,
        })
        ratchet['rootKey'] = master_key[0]

    async def has_open_session(self) -> bool:
        async def _do():
            record = await self.get_record()
            if not record:
                return False
            return record.have_open_session()

        return await self.queue_job(_do())

    async def close_open_session(self) -> None:
        async def _do():
            record = await self.get_record()
            if record:
                open_session = record.get_open_session()
                if open_session:
                    record.close_session(open_session)
                    await self.store_record(record)

        return await self.queue_job(_do())
