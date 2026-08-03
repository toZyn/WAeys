"""Port of libsignal's SessionBuilder (src/session_builder.js)."""

from __future__ import annotations

import logging
import time

from .libsignal_constants import BaseKeyType, ChainType
from .libsignal_crypto import derive_secrets
from .libsignal_curve import calculate_agreement, generate_key_pair, verify_signature
from .libsignal_errors import PreKeyError, UntrustedIdentityKeyError
from .libsignal_queue_job import queue_job
from .libsignal_session_record import SessionRecord
from .protocol_address import ProtocolAddress

logger = logging.getLogger(__name__)


class SessionBuilder:
    def __init__(self, storage, protocol_address: ProtocolAddress):
        self.addr = protocol_address
        self.storage = storage

    async def init_outgoing(self, device: dict) -> None:
        fq_addr = self.addr.__str__()

        async def _do():
            if not await self.storage.isTrustedIdentity(self.addr.id, device['identityKey']):
                raise UntrustedIdentityKeyError(self.addr.id, device['identityKey'])
            verify_signature(
                device['identityKey'],
                device['signedPreKey']['publicKey'],
                device['signedPreKey']['signature'],
                True,
            )
            base_key = generate_key_pair()
            device_pre_key = device['preKey']['publicKey'] if device.get('preKey') else None
            session = await self.init_session(
                True,
                base_key,
                None,
                device['identityKey'],
                device_pre_key,
                device['signedPreKey']['publicKey'],
                device['registrationId'],
            )
            session.pendingPreKey = {
                'signedKeyId': device['signedPreKey']['keyId'],
                'baseKey': base_key['pubKey'],
            }
            if device.get('preKey'):
                session.pendingPreKey['preKeyId'] = device['preKey']['keyId']

            record = await self.storage.loadSession(fq_addr)
            if not record:
                record = SessionRecord()
            else:
                open_session = record.get_open_session()
                if open_session:
                    record.close_session(open_session)
            record.set_session(session)
            await self.storage.storeSession(fq_addr, record)

        return await queue_job(fq_addr, _do())

    async def init_incoming(self, record: SessionRecord, message) -> int | None:
        fq_addr = self.addr.__str__()
        if not await self.storage.isTrustedIdentity(fq_addr, message.identityKey):
            raise UntrustedIdentityKeyError(self.addr.id, message.identityKey)
        if record.get_session(message.baseKey):
            return None
        pre_key_pair = await self.storage.loadPreKey(message.preKeyId) if message.preKeyId else None
        if message.preKeyId and not pre_key_pair:
            raise PreKeyError('Invalid PreKey ID')
        signed_pre_key_pair = await self.storage.loadSignedPreKey(message.signedPreKeyId)
        if not signed_pre_key_pair:
            raise PreKeyError('Missing SignedPreKey')
        existing_open_session = record.get_open_session()
        if existing_open_session:
            logger.warning('Closing open session in favor of incoming prekey bundle')
            record.close_session(existing_open_session)
        record.set_session(await self.init_session(
            False,
            pre_key_pair,
            signed_pre_key_pair,
            message.identityKey,
            message.baseKey,
            None,
            message.registrationId,
        ))
        return message.preKeyId

    async def init_session(
        self,
        is_initiator: bool,
        our_ephemeral_key,
        our_signed_key,
        their_identity_pub_key,
        their_ephemeral_pub_key,
        their_signed_pub_key,
        registration_id,
    ):
        if is_initiator:
            if our_signed_key:
                raise ValueError('Invalid call to initSession')
            our_signed_key = our_ephemeral_key
        else:
            if their_signed_pub_key:
                raise ValueError('Invalid call to initSession')
            their_signed_pub_key = their_ephemeral_pub_key

        if not our_ephemeral_key or not their_ephemeral_pub_key:
            shared_secret = bytearray(32 * 4)
        else:
            shared_secret = bytearray(32 * 5)
        for i in range(32):
            shared_secret[i] = 0xFF

        our_identity_key = await self.storage.getOurIdentity()
        a1 = calculate_agreement(their_signed_pub_key, our_identity_key['privKey'])
        a2 = calculate_agreement(their_identity_pub_key, our_signed_key['privKey'])
        a3 = calculate_agreement(their_signed_pub_key, our_signed_key['privKey'])
        if is_initiator:
            shared_secret[32:64] = a1
            shared_secret[64:96] = a2
        else:
            shared_secret[64:96] = a1
            shared_secret[32:64] = a2
        shared_secret[96:128] = a3
        if our_ephemeral_key and their_ephemeral_pub_key:
            a4 = calculate_agreement(their_ephemeral_pub_key, our_ephemeral_key['privKey'])
            shared_secret[128:160] = a4

        master_key = derive_secrets(bytes(shared_secret), bytes(32), b'WhisperText')

        session = SessionRecord.create_entry()
        session.registrationId = registration_id
        session.currentRatchet = {
            'rootKey': master_key[0],
            'ephemeralKeyPair': generate_key_pair() if is_initiator else our_signed_key,
            'lastRemoteEphemeralKey': their_signed_pub_key,
            'previousCounter': 0,
        }
        session.indexInfo = {
            'created': int(time.time() * 1000),
            'used': int(time.time() * 1000),
            'remoteIdentityKey': their_identity_pub_key,
            'baseKey': our_ephemeral_key['pubKey'] if is_initiator else their_ephemeral_pub_key,
            'baseKeyType': BaseKeyType.OURS if is_initiator else BaseKeyType.THEIRS,
            'closed': -1,
        }
        if is_initiator:
            self.calculate_sending_ratchet(session, their_signed_pub_key)
        return session

    def calculate_sending_ratchet(self, session, remote_key: bytes) -> None:
        ratchet = session.currentRatchet
        shared_secret = calculate_agreement(remote_key, ratchet['ephemeralKeyPair']['privKey'])
        master_key = derive_secrets(shared_secret, ratchet['rootKey'], b'WhisperRatchet')
        session.add_chain(ratchet['ephemeralKeyPair']['pubKey'], {
            'messageKeys': {},
            'chainKey': {
                'counter': -1,
                'key': master_key[1],
            },
            'chainType': ChainType.SENDING,
        })
        ratchet['rootKey'] = master_key[0]
