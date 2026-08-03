"""Port of src/Signal/libsignal.ts (makeLibSignalRepository).

Wraps the ported libsignal session cipher / group sender-key protocol behind
the SignalRepository interface, using the SignalKeyStore for persistence and
a LIDMappingStore for PN<->LID resolution.
"""

from __future__ import annotations

import logging

from ..Utils.crypto import generate_signal_pub_key
from ..Utils.lru_cache import LRUCache
from ..WABinary.jid_utils import (
    WAJIDDomains,
    is_hosted_lid_user,
    is_hosted_pn_user,
    is_lid_user,
    is_pn_user,
    jid_decode,
    transfer_device,
)
from ..WAProto import WAProto as proto
from .Group import (
    GroupCipher,
    GroupSessionBuilder,
    SenderKeyDistributionMessage,
    SenderKeyName,
    SenderKeyRecord,
)
from .lid_mapping import LIDMappingStore
from .libsignal_errors import SessionError
from .libsignal_session_builder import SessionBuilder
from .libsignal_session_cipher import SessionCipher
from .libsignal_session_record import SessionRecord
from .protocol_address import ProtocolAddress
from .whisper_text_protocol import PreKeyWhisperMessage

logger = logging.getLogger(__name__)


def extract_identity_from_pkmsg(ciphertext: bytes):
    """Extract identity key from PreKeyWhisperMessage for identity change detection."""
    try:
        if not ciphertext or len(ciphertext) < 2:
            return None
        version = ciphertext[0]
        if (version & 0xF) != 3:
            return None
        pre_key_proto = PreKeyWhisperMessage.decode(bytes(ciphertext)[1:])
        identity_key = pre_key_proto.identityKey
        if identity_key is not None and len(identity_key) == 33:
            return bytes(identity_key)
        return None
    except Exception:
        return None


def jid_to_signal_protocol_address(jid: str) -> ProtocolAddress:
    decoded = jid_decode(jid)
    if decoded is None:
        raise ValueError(f'Unable to decode jid: "{jid}"')
    user = decoded.user
    device = decoded.device
    server = decoded.server
    domain_type = decoded.domainType

    if not user:
        raise ValueError(
            f'JID decoded but user is empty: "{jid}" -> user: "{user}", server: "{server}", device: {device}'
        )

    signal_user = f'{user}_{domain_type}' if domain_type != WAJIDDomains.WHATSAPP else user
    final_device = device or 0

    if device == 99 and server not in ('hosted', 'hosted.lid'):
        raise ValueError(
            f'Unexpected non-hosted device JID with device 99. This ID seems invalid. ID:{jid}'
        )

    return ProtocolAddress(signal_user, final_device)


def jid_to_signal_sender_key_name(group: str, user: str) -> SenderKeyName:
    return SenderKeyName(group, _sender_from_protocol_address(jid_to_signal_protocol_address(user)))


def _sender_from_protocol_address(addr: ProtocolAddress):
    from .Group.sender_key_name import Sender
    return Sender(addr.id, addr.device_id)


class _SignalStorage:
    """The libsignal storage adapter (port of signalStorage())."""

    def __init__(self, auth: dict, lid_mapping: LIDMappingStore):
        self.auth = auth
        self.creds = auth['creds']
        self.keys = auth['keys']
        self.lid_mapping = lid_mapping

    async def _resolve_lid_signal_address(self, id: str) -> str:
        if '.' in id:
            parts = id.split('.')
            device_id = parts[0]
            device = parts[1] if len(parts) > 1 else '0'
            user_and_domain = device_id.split('_')
            user = user_and_domain[0]
            domain_type_raw = user_and_domain[1] if len(user_and_domain) > 1 else '0'
            domain_type = int(domain_type_raw or '0')

            if domain_type == WAJIDDomains.LID or domain_type == WAJIDDomains.HOSTED_LID:
                return id

            pn_jid = f'{user}{":" + device if device != "0" else ""}@{"hosted" if domain_type == WAJIDDomains.HOSTED else "s.whatsapp.net"}'

            lid_for_pn = await self.lid_mapping.get_lid_for_pn(pn_jid)
            if lid_for_pn:
                lid_addr = jid_to_signal_protocol_address(lid_for_pn)
                return str(lid_addr)

        return id

    async def load_session(self, id: str):
        try:
            wire_jid = await self._resolve_lid_signal_address(id)
            stored = await self.keys.get('session', [wire_jid])
            sess = stored.get(wire_jid)
            if sess:
                return SessionRecord.deserialize(sess)
        except Exception as e:
            logger.warning(f'Error loading session: {e}')
            return None
        return None

    async def store_session(self, id: str, session: SessionRecord) -> None:
        wire_jid = await self._resolve_lid_signal_address(id)
        await self.keys.set({'session': {wire_jid: session.serialize()}})

    async def is_trusted_identity(self, id: str, identity_key) -> bool:
        return True

    async def load_identity_key(self, id: str):
        wire_jid = await self._resolve_lid_signal_address(id)
        stored = await self.keys.get('identity-key', [wire_jid])
        return stored.get(wire_jid)

    async def save_identity(self, id: str, identity_key) -> bool:
        wire_jid = await self._resolve_lid_signal_address(id)
        stored = await self.keys.get('identity-key', [wire_jid])
        existing = stored.get(wire_jid)
        identity_key = bytes(identity_key)

        keys_match = existing is not None and len(existing) == len(identity_key) and all(
            a == b for a, b in zip(existing, identity_key)
        )

        if existing and not keys_match:
            await self.keys.set({
                'session': {wire_jid: None},
                'identity-key': {wire_jid: identity_key},
            })
            return True

        if existing is None:
            await self.keys.set({'identity-key': {wire_jid: identity_key}})
            return True

        return False

    async def load_pre_key(self, id):
        key_id = str(id)
        stored = await self.keys.get('pre-key', [key_id])
        key = stored.get(key_id)
        if key:
            return {
                'privKey': bytes(key['private']),
                'pubKey': bytes(key['public']),
            }
        return None

    async def remove_pre_key(self, id) -> None:
        await self.keys.set({'pre-key': {str(id): None}})

    async def load_signed_pre_key(self, id):
        key = self.creds['signedPreKey']
        return {
            'privKey': bytes(key['keyPair']['private']),
            'pubKey': bytes(key['keyPair']['public']),
        }

    async def load_sender_key(self, sender_key_name: SenderKeyName):
        key_id = str(sender_key_name)
        stored = await self.keys.get('sender-key', [key_id])
        key = stored.get(key_id)
        if key:
            return SenderKeyRecord.deserialize(bytes(key))
        return SenderKeyRecord()

    async def store_sender_key(self, sender_key_name: SenderKeyName, key: SenderKeyRecord) -> None:
        from ..Utils.generics import node_json_dumps
        key_id = str(sender_key_name)
        serialized = node_json_dumps(key.serialize())
        await self.keys.set({'sender-key': {key_id: serialized.encode('utf-8')}})

    def get_our_registration_id(self):
        return self.creds['registrationId']

    def get_our_identity(self):
        signed_identity_key = self.creds['signedIdentityKey']
        return {
            'privKey': bytes(signed_identity_key['private']),
            'pubKey': generate_signal_pub_key(bytes(signed_identity_key['public'])),
        }

    # ---- camelCase aliases for the libsignal core (faithful port) ----
    async def loadSession(self, id):
        return await self.load_session(id)

    async def storeSession(self, id, session):
        return await self.store_session(id, session)

    async def isTrustedIdentity(self, id, identity_key):
        return await self.is_trusted_identity(id, identity_key)

    async def loadIdentityKey(self, id):
        return await self.load_identity_key(id)

    async def saveIdentity(self, id, identity_key):
        return await self.save_identity(id, identity_key)

    async def loadPreKey(self, id):
        return await self.load_pre_key(id)

    async def removePreKey(self, id):
        return await self.remove_pre_key(id)

    async def loadSignedPreKey(self, id):
        return await self.load_signed_pre_key(id)

    async def loadSenderKey(self, sender_key_name):
        return await self.load_sender_key(sender_key_name)

    async def storeSenderKey(self, sender_key_name, key):
        return await self.store_sender_key(sender_key_name, key)

    async def getOurRegistrationId(self):
        return self.get_our_registration_id()

    async def getOurIdentity(self):
        return self.get_our_identity()


def make_libsignal_repository(auth: dict, logger_=None, pn_to_lid_func=None):
    """Create a SignalRepository-backed signal implementation.

    auth: {'creds': {...}, 'keys': SignalKeyStore-ish} (SignalAuthState).
    """
    lid_mapping = LIDMappingStore(auth['keys'], pn_to_lid_func)
    storage = _SignalStorage(auth, lid_mapping)

    parsed_keys = auth['keys']
    migrated_session_cache = LRUCache(
        ttl=3 * 24 * 60 * 60 * 1000,
        ttl_autopurge=True,
        update_age_on_get=True,
    )

    async def ensure_sender_key_and_create_skdm(group: str, me_id: str):
        sender_name = jid_to_signal_sender_key_name(group, me_id)
        sender_name_str = str(sender_name)
        stored = await auth['keys'].get('sender-key', [sender_name_str])
        sender_key = stored.get(sender_name_str)
        if not sender_key:
            await storage.store_sender_key(sender_name, SenderKeyRecord())
        skdm = await GroupSessionBuilder(storage).create(sender_name)
        return {'senderName': sender_name, 'skdm': skdm}

    async def decrypt_group_message(opts):
        sender_name = jid_to_signal_sender_key_name(opts['group'], opts['authorJid'])
        cipher = GroupCipher(storage, sender_name)
        async with _transaction(parsed_keys, opts['group']):
            return await cipher.decrypt(opts['msg'])

    async def process_sender_key_distribution_message(opts):
        item = opts['item']
        author_jid = opts['authorJid']
        group_id = getattr(item, 'groupId', None)
        if not group_id:
            raise ValueError('Group ID is required for sender key distribution message')
        builder = GroupSessionBuilder(storage)
        sender_name = jid_to_signal_sender_key_name(group_id, author_jid)
        skdm_bytes = getattr(item, 'axolotlSenderKeyDistributionMessage', None)
        sender_msg = SenderKeyDistributionMessage(None, None, None, None, skdm_bytes)
        sender_name_str = str(sender_name)
        stored = await auth['keys'].get('sender-key', [sender_name_str])
        if not stored.get(sender_name_str):
            await storage.store_sender_key(sender_name, SenderKeyRecord())

        async with _transaction(parsed_keys, group_id):
            stored = await auth['keys'].get('sender-key', [sender_name_str])
            if not stored.get(sender_name_str):
                await storage.store_sender_key(sender_name, SenderKeyRecord())
            await builder.process(sender_name, sender_msg)

    async def decrypt_message(opts):
        jid = opts['jid']
        msg_type = opts['type']
        ciphertext = opts['ciphertext']
        addr = jid_to_signal_protocol_address(jid)
        session = SessionCipher(storage, addr)

        if msg_type == 'pkmsg':
            identity_key = extract_identity_from_pkmsg(ciphertext)
            if identity_key:
                addr_str = str(addr)
                identity_changed = await storage.save_identity(addr_str, identity_key)
                if identity_changed:
                    logger.info(f'identity key changed or new contact, session will be re-established: {jid}')

        async def do_decrypt():
            if msg_type == 'pkmsg':
                return await session.decrypt_pre_key_whisper_message(ciphertext)
            if msg_type == 'msg':
                return await session.decrypt_whisper_message(ciphertext)
            raise ValueError(f'Unknown message type: {msg_type}')

        async with _transaction(parsed_keys, jid):
            return await do_decrypt()

    async def encrypt_message(opts):
        jid = opts['jid']
        data = opts['data']
        addr = jid_to_signal_protocol_address(jid)
        cipher = SessionCipher(storage, addr)
        async with _transaction(parsed_keys, jid):
            result = await cipher.encrypt(data)
            sig_type = 'pkmsg' if result['type'] == 3 else 'msg'
            return {'type': sig_type, 'ciphertext': bytes(result['body'])}

    async def encrypt_group_message(opts):
        group = opts['group']
        me_id = opts['meId']
        data = opts['data']
        async with _transaction(parsed_keys, group):
            info = await ensure_sender_key_and_create_skdm(group, me_id)
            sender_name = info['senderName']
            skdm = info['skdm']
            ciphertext = await GroupCipher(storage, sender_name).encrypt(data)
            return {'ciphertext': ciphertext, 'senderKeyDistributionMessage': skdm.serialize()}

    async def get_sender_key_distribution_message(opts):
        group = opts['group']
        me_id = opts['meId']
        async with _transaction(parsed_keys, group):
            info = await ensure_sender_key_and_create_skdm(group, me_id)
            return info['skdm'].serialize()

    async def has_sender_key(opts):
        sender_name = str(jid_to_signal_sender_key_name(opts['group'], opts['meId']))
        stored = await auth['keys'].get('sender-key', [sender_name])
        return bool(stored.get(sender_name))

    async def get_session_info(jid):
        addr = str(jid_to_signal_protocol_address(jid))
        session = await storage.load_session(addr)
        if not session:
            return None
        open_session = session.get_open_session()
        if open_session is None:
            return None
        base_key = open_session.indexInfo.get('baseKey')
        registration_id = open_session.registrationId
        if not base_key or not isinstance(registration_id, int):
            return None
        return {'baseKey': bytes(base_key), 'registrationId': registration_id}

    async def inject_e2e_session(opts):
        jid = opts['jid']
        session = opts['session']
        builder = SessionBuilder(storage, jid_to_signal_protocol_address(jid))
        async with _transaction(parsed_keys, jid):
            await builder.init_outgoing({
                'identityKey': bytes(session['identityKey']),
                'signedPreKey': {
                    'publicKey': bytes(session['signedPreKey']['publicKey']),
                    'signature': bytes(session['signedPreKey']['signature']),
                    'keyId': session['signedPreKey']['keyId'],
                },
                'preKey': {
                    'publicKey': bytes(session['preKey']['publicKey']),
                    'keyId': session['preKey']['keyId'],
                } if session.get('preKey') else None,
                'registrationId': session['registrationId'],
            })

    async def validate_session(jid):
        try:
            addr = jid_to_signal_protocol_address(jid)
            session = await storage.load_session(str(addr))
            if not session:
                return {'exists': False, 'reason': 'no session'}
            if not session.have_open_session():
                return {'exists': False, 'reason': 'no open session'}
            return {'exists': True}
        except Exception:
            return {'exists': False, 'reason': 'validation error'}

    async def delete_session(jids):
        if not jids:
            return
        session_updates = {}
        for jid in jids:
            addr = jid_to_signal_protocol_address(jid)
            session_updates[str(addr)] = None
        async with _transaction(parsed_keys, f'delete-{len(jids)}-sessions'):
            await auth['keys'].set({'session': session_updates})

    async def migrate_session(from_jid: str, to_jid: str):
        if not from_jid or (not is_lid_user(to_jid) and not is_hosted_lid_user(to_jid)):
            return {'migrated': 0, 'skipped': 0, 'total': 0}
        if not is_pn_user(from_jid) and not is_hosted_pn_user(from_jid):
            return {'migrated': 0, 'skipped': 0, 'total': 1}

        decoded_from = jid_decode(from_jid)
        user = decoded_from.user if decoded_from else None

        stored = await parsed_keys.get('device-list', [user])
        user_devices = stored.get(user)
        if not user_devices:
            return {'migrated': 0, 'skipped': 0, 'total': 0}

        decoded_from = jid_decode(from_jid)
        from_device = decoded_from.device if decoded_from else None
        from_device_str = str(from_device) if from_device is not None else '0'
        if from_device_str not in user_devices:
            user_devices = list(user_devices) + [from_device_str]

        uncached_devices = [d for d in user_devices if not migrated_session_cache.has(f'{user}.{d}')]
        device_session_keys = [f'{user}.{d}' for d in uncached_devices]
        existing_sessions = await parsed_keys.get('session', device_session_keys)

        device_jids = []
        for session_key, session_data in existing_sessions.items():
            if session_data:
                parts = session_key.split('.')
                if len(parts) < 2:
                    continue
                device_num_raw = parts[1]
                try:
                    device_num = int(device_num_raw)
                except ValueError:
                    continue
                if device_num == 0:
                    jid = f'{user}@s.whatsapp.net'
                elif device_num == 99:
                    jid = f'{user}:99@hosted'
                else:
                    jid = f'{user}:{device_num}@s.whatsapp.net'
                device_jids.append(jid)

        async with _transaction(
            parsed_keys,
            f'migrate-{len(device_jids)}-sessions-{jid_decode(to_jid).user if jid_decode(to_jid) else ""}',
        ):
            migration_ops = []
            for jid in device_jids:
                lid_with_device = transfer_device(jid, to_jid)
                from_decoded = jid_decode(jid)
                to_decoded = jid_decode(lid_with_device)
                if not from_decoded or not to_decoded:
                    continue
                migration_ops.append({
                    'fromJid': jid,
                    'toJid': lid_with_device,
                    'pnUser': from_decoded.user,
                    'lidUser': to_decoded.user,
                    'deviceId': from_decoded.device or 0,
                    'fromAddr': jid_to_signal_protocol_address(jid),
                    'toAddr': jid_to_signal_protocol_address(lid_with_device),
                })

            total_ops = len(migration_ops)
            migrated_count = 0

            pn_addr_strings = list(set(op['fromAddr'].__str__() for op in migration_ops))
            pn_sessions = await parsed_keys.get('session', pn_addr_strings)

            session_updates = {}
            for op in migration_ops:
                pn_addr_str = op['fromAddr'].__str__()
                lid_addr_str = op['toAddr'].__str__()
                pn_session = pn_sessions.get(pn_addr_str)
                if pn_session:
                    from_session = SessionRecord.deserialize(pn_session)
                    if from_session.have_open_session():
                        session_updates[lid_addr_str] = from_session.serialize()
                        session_updates[pn_addr_str] = None
                        migrated_count += 1

            if len(session_updates) > 0:
                await parsed_keys.set({'session': session_updates})
                for op in migration_ops:
                    if session_updates.get(op['toAddr'].__str__()):
                        device_key = f"{op['pnUser']}.{op['deviceId']}"
                        migrated_session_cache.set(device_key, True)

            skipped_count = total_ops - migrated_count
            return {'migrated': migrated_count, 'skipped': skipped_count, 'total': total_ops}

    repository = {
        'decryptGroupMessage': decrypt_group_message,
        'processSenderKeyDistributionMessage': process_sender_key_distribution_message,
        'decryptMessage': decrypt_message,
        'encryptMessage': encrypt_message,
        'encryptGroupMessage': encrypt_group_message,
        'getSenderKeyDistributionMessage': get_sender_key_distribution_message,
        'hasSenderKey': has_sender_key,
        'getSessionInfo': get_session_info,
        'injectE2ESession': inject_e2e_session,
        'validateSession': validate_session,
        'deleteSession': delete_session,
        'jidToSignalProtocolAddress': lambda jid: str(jid_to_signal_protocol_address(jid)),
        'migrateSession': migrate_session,
        'lidMapping': lid_mapping,
        'close': lambda: (lid_mapping.close(), migrated_session_cache.clear()),
    }

    return repository


class _Transaction:
    """Context manager wrapping keys.transaction() for stores that support it."""

    def __init__(self, keys, key):
        self.keys = keys
        self.key = key
        self.cm = None

    async def __aenter__(self):
        if hasattr(self.keys, 'transaction'):
            self.cm = self.keys.transaction(self.key)
            return await self.cm.__aenter__()
        return self.keys

    async def __aexit__(self, exc_type, exc, tb):
        if self.cm is not None:
            return await self.cm.__aexit__(exc_type, exc, tb)
        return False


def _transaction(keys, key):
    return _Transaction(keys, key)
