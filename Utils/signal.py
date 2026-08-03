"""Port of src/Utils/signal.ts — signal key/node helpers."""

from __future__ import annotations

from ..Defaults.index import KEY_BUNDLE_TYPE
from ..WABinary.generic_utils import (
    assert_node_error_free,
    get_binary_node_child,
    get_binary_node_child_buffer,
    get_binary_node_children,
    get_binary_node_child_uint,
)
from ..WABinary.jid_utils import S_WHATSAPP_NET, WAJIDDomains, get_server_from_domain_type, jid_decode
from ..WABinary.types import BinaryNode
from .crypto import Curve, generate_signal_pub_key
from .generics import encode_big_endian


def chunk(array, size):
    return [array[i:i + size] for i in range(0, len(array), size)]


def create_signal_identity(wid: str, account_signature_key: bytes) -> dict:
    return {
        'identifier': {'name': wid, 'deviceId': 0},
        'identifierKey': generate_signal_pub_key(account_signature_key),
    }


async def get_pre_keys(store: dict, min_id: int, limit: int):
    id_list = [str(i) for i in range(min_id, limit)]
    return await store['get']('pre-key', id_list)


def generate_or_get_pre_keys(creds: dict, range_: int):
    available = creds['nextPreKeyId'] - creds['firstUnuploadedPreKeyId']
    remaining = range_ - available
    last_pre_key_id = creds['nextPreKeyId'] + remaining - 1
    new_pre_keys = {}
    if remaining > 0:
        for i in range(creds['nextPreKeyId'], last_pre_key_id + 1):
            new_pre_keys[i] = Curve.generate_key_pair()
    return {
        'newPreKeys': new_pre_keys,
        'lastPreKeyId': last_pre_key_id,
        'preKeysRange': [creds['firstUnuploadedPreKeyId'], range_],
    }


def xmpp_signed_pre_key(key: dict) -> BinaryNode:
    return BinaryNode(
        tag='skey',
        attrs={},
        content=[
            BinaryNode(tag='id', attrs={}, content=encode_big_endian(key['keyId'], 3)),
            BinaryNode(tag='value', attrs={}, content=key['keyPair']['public']),
            BinaryNode(tag='signature', attrs={}, content=key['signature']),
        ],
    )


def xmpp_pre_key(pair: dict, key_id: int) -> BinaryNode:
    return BinaryNode(
        tag='key',
        attrs={},
        content=[
            BinaryNode(tag='id', attrs={}, content=encode_big_endian(key_id, 3)),
            BinaryNode(tag='value', attrs={}, content=pair['public']),
        ],
    )


def _is_valid_uint(n):
    return isinstance(n, int) and not isinstance(n, bool)


def extract_e2e_session_from_retry_receipt(receipt):
    keys_node = get_binary_node_child(receipt, 'keys')
    if not keys_node:
        return None

    type_buf = get_binary_node_child_buffer(keys_node, 'type')
    if not type_buf or len(type_buf) != 1 or type_buf[0] != KEY_BUNDLE_TYPE[0]:
        return None

    identity = get_binary_node_child_buffer(keys_node, 'identity')
    skey = get_binary_node_child(keys_node, 'skey')
    if not identity or len(identity) != 32 or not skey:
        return None

    registration_id = get_binary_node_child_uint(receipt, 'registration', 4)
    if not _is_valid_uint(registration_id):
        return None

    signed_pub_key = get_binary_node_child_buffer(skey, 'value')
    signed_sig = get_binary_node_child_buffer(skey, 'signature')
    signed_key_id = get_binary_node_child_uint(skey, 'id', 3)
    if not signed_pub_key or len(signed_pub_key) != 32 or not signed_sig or not _is_valid_uint(signed_key_id):
        return None

    pre_key_node = get_binary_node_child(keys_node, 'key')
    pre_key = None
    if pre_key_node:
        pre_key_pub = get_binary_node_child_buffer(pre_key_node, 'value')
        pre_key_id = get_binary_node_child_uint(pre_key_node, 'id', 3)
        if not pre_key_pub or len(pre_key_pub) != 32 or not _is_valid_uint(pre_key_id):
            return None
        pre_key = {'keyId': pre_key_id, 'publicKey': generate_signal_pub_key(pre_key_pub)}

    return {
        'registrationId': registration_id,
        'identityKey': generate_signal_pub_key(identity),
        'signedPreKey': {
            'keyId': signed_key_id,
            'publicKey': generate_signal_pub_key(signed_pub_key),
            'signature': signed_sig,
        },
        'preKey': pre_key,
    }


def _extract_key(key):
    if not key:
        return None
    return {
        'keyId': get_binary_node_child_uint(key, 'id', 3),
        'publicKey': generate_signal_pub_key(get_binary_node_child_buffer(key, 'value')),
        'signature': get_binary_node_child_buffer(key, 'signature'),
    }


async def parse_and_inject_e2e_sessions(node, repository) -> None:
    list_node = get_binary_node_child(node, 'list')
    nodes = get_binary_node_children(list_node, 'user') if list_node else []
    for n in nodes:
        assert_node_error_free(n)

    chunk_size = 100
    for nodes_chunk in chunk(nodes, chunk_size):
        for n in nodes_chunk:
            signed_key = get_binary_node_child(n, 'skey')
            key = get_binary_node_child(n, 'key')
            identity = get_binary_node_child_buffer(n, 'identity')
            jid = n.attrs.get('jid')
            registration_id = get_binary_node_child_uint(n, 'registration', 4)
            await repository.inject_e2e_session({
                'jid': jid,
                'session': {
                    'registrationId': registration_id,
                    'identityKey': generate_signal_pub_key(identity),
                    'signedPreKey': _extract_key(signed_key),
                    'preKey': _extract_key(key),
                },
            })


def extract_device_jids(result: list, my_jid: str, my_lid: str, exclude_zero_devices: bool) -> list:
    decoded_my = jid_decode(my_jid)
    my_user = decoded_my.user
    my_device = decoded_my.device

    extracted = []
    for user_result in result:
        devices = user_result.get('devices')
        user_id = user_result.get('id')
        decoded = jid_decode(user_id)
        if not decoded:
            continue
        user, server = decoded.user, decoded.server
        domain_type = decoded.domainType
        device_list = (devices or {}).get('deviceList')
        if not isinstance(device_list, list):
            continue
        for device_info in device_list:
            device = device_info.get('id')
            key_index = device_info.get('keyIndex')
            is_hosted = device_info.get('isHosted')
            if (
                (not exclude_zero_devices or device != 0)
                and ((my_user != user and my_lid != user) or my_device != device)
                and (device == 0 or bool(key_index))
            ):
                if is_hosted:
                    domain_type = WAJIDDomains.HOSTED_LID if domain_type == WAJIDDomains.LID else WAJIDDomains.HOSTED
                extracted.append({
                    'user': user,
                    'device': device,
                    'domainType': domain_type,
                    'server': get_server_from_domain_type(server, domain_type),
                })
    return extracted


async def get_next_pre_keys(state: dict, count: int):
    creds = state['creds']
    keys = state['keys']
    result = generate_or_get_pre_keys(creds, count)
    new_pre_keys = result['newPreKeys']
    last_pre_key_id = result['lastPreKeyId']
    pre_keys_range = result['preKeysRange']

    update = {
        'nextPreKeyId': max(last_pre_key_id + 1, creds['nextPreKeyId']),
        'firstUnuploadedPreKeyId': max(creds['firstUnuploadedPreKeyId'], last_pre_key_id + 1),
    }

    await keys['set']({'pre-key': new_pre_keys})

    pre_keys = await get_pre_keys(keys, pre_keys_range[0], pre_keys_range[0] + pre_keys_range[1])

    return {'update': update, 'preKeys': pre_keys}


async def get_next_pre_keys_node(state: dict, count: int):
    creds = state['creds']
    result = await get_next_pre_keys(state, count)
    update = result['update']
    pre_keys = result['preKeys']

    node = BinaryNode(
        tag='iq',
        attrs={'xmlns': 'encrypt', 'type': 'set', 'to': S_WHATSAPP_NET},
        content=[
            BinaryNode(tag='registration', attrs={}, content=encode_big_endian(creds['registrationId'])),
            BinaryNode(tag='type', attrs={}, content=KEY_BUNDLE_TYPE),
            BinaryNode(tag='identity', attrs={}, content=creds['signedIdentityKey']['public']),
            BinaryNode(
                tag='list',
                attrs={},
                content=[xmpp_pre_key(pre_keys[int(k)], int(k)) for k in pre_keys],
            ),
            xmpp_signed_pre_key(creds['signedPreKey']),
        ],
    )

    return {'update': update, 'node': node}
