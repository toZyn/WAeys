"""Port of src/Utils/validate-connection.ts."""

from __future__ import annotations

import hashlib

from ..Defaults.index import (
    KEY_BUNDLE_TYPE,
    WA_ADV_ACCOUNT_SIG_PREFIX,
    WA_ADV_DEVICE_SIG_PREFIX,
    WA_ADV_HOSTED_ACCOUNT_SIG_PREFIX,
    WA_ADV_HOSTED_DEVICE_SIG_PREFIX,
)
from ..WAProto import WAProto as proto
from ..WABinary.generic_utils import get_binary_node_child
from ..WABinary.jid_utils import S_WHATSAPP_NET, jid_decode
from ..WABinary.types import BinaryNode
from .crypto import Curve, hmac_sign
from .generics import Boom, encode_big_endian
from .signal import create_signal_identity


def get_user_agent(config) -> dict:
    from ..WAProto import WAProto as _proto

    platform = (
        _proto.ClientPayload.UserAgent.Platform.ANDROID
        if 'android' in config['browser'][1].lower()
        else _proto.ClientPayload.UserAgent.Platform.WEB
    )
    return {
        'appVersion': {
            'primary': config['version'][0],
            'secondary': config['version'][1],
            'tertiary': config['version'][2],
        },
        'platform': platform,
        'releaseChannel': proto.ClientPayload.UserAgent.ReleaseChannel.RELEASE,
        'osVersion': '0.1',
        'device': 'Desktop',
        'osBuildNumber': '0.1',
        'localeLanguageIso6391': 'en',
        'mnc': '000',
        'mcc': '000',
        'localeCountryIso31661Alpha2': config.get('countryCode'),
    }


PLATFORM_MAP = {
    'Mac OS': proto.ClientPayload.WebInfo.WebSubPlatform.DARWIN,
    'Windows': proto.ClientPayload.WebInfo.WebSubPlatform.WIN32,
}


def get_web_info(config) -> dict:
    web_sub_platform = proto.ClientPayload.WebInfo.WebSubPlatform.WEB_BROWSER
    if (
        config.get('syncFullHistory')
        and config['browser'][0] in PLATFORM_MAP
        and config['browser'][1] == 'Desktop'
    ):
        web_sub_platform = PLATFORM_MAP[config['browser'][0]]
    return {'webSubPlatform': web_sub_platform}


def get_client_payload(config) -> dict:
    payload = {
        'connectType': proto.ClientPayload.ConnectType.WIFI_UNKNOWN,
        'connectReason': proto.ClientPayload.ConnectReason.USER_ACTIVATED,
        'userAgent': get_user_agent(config),
    }

    if 'android' not in config['browser'][1].lower():
        payload['webInfo'] = get_web_info(config)

    if config.get('pushName'):
        payload['pushName'] = config['pushName']

    return payload


def generate_login_node(user_jid: str, config) -> dict:
    decoded = jid_decode(user_jid)
    payload = {
        **get_client_payload(config),
        'passive': True,
        'pull': True,
        'username': int(decoded.user),
        'device': decoded.device,
        'lidDbMigrated': False,
    }
    return proto.ClientPayload.from_object(payload)


def _get_platform_type(platform: str) -> int:
    platform_type = platform.upper()
    if platform_type == 'ANDROID':
        return proto.DeviceProps.PlatformType.ANDROID_PHONE
    return getattr(proto.DeviceProps.PlatformType, platform_type, proto.DeviceProps.PlatformType.CHROME)


def generate_registration_node(creds: dict, config) -> dict:
    # the app version needs to be md5 hashed and passed in
    app_version_buf = hashlib.md5('.'.join(str(v) for v in config['version']).encode('utf-8')).digest()

    companion = {
        'os': config['browser'][0],
        'platformType': _get_platform_type(config['browser'][1]),
        'requireFullSync': config.get('syncFullHistory'),
        'historySyncConfig': {
            'storageQuotaMb': 10240,
            'inlineInitialPayloadInE2EeMsg': True,
            'supportCallLogHistory': False,
            'supportBotUserAgentChatHistory': True,
            'supportCagReactionsAndPolls': True,
            'supportBizHostedMsg': True,
            'supportRecentSyncChunkMessageCountTuning': True,
            'supportHostedGroupMsg': True,
            'supportFbidBotChatHistory': True,
            'supportMessageAssociation': True,
            'supportGroupHistory': False,
        },
        'version': {'primary': 10, 'secondary': 15, 'tertiary': 7},
    }

    companion_proto = proto.DeviceProps.encode(companion)

    register_payload = {
        **get_client_payload(config),
        'passive': False,
        'pull': False,
        'devicePairingData': {
            'buildHash': app_version_buf,
            'deviceProps': companion_proto,
            'eRegid': encode_big_endian(creds['registrationId']),
            'eKeytype': KEY_BUNDLE_TYPE,
            'eIdent': creds['signedIdentityKey']['public'],
            'eSkeyId': encode_big_endian(creds['signedPreKey']['keyId'], 3),
            'eSkeyVal': creds['signedPreKey']['keyPair']['public'],
            'eSkeySig': creds['signedPreKey']['signature'],
        },
    }

    return proto.ClientPayload.from_object(register_payload)


def configure_successful_pairing(stanza, creds: dict) -> dict:
    msg_id = stanza.attrs.get('id')

    pair_success_node = get_binary_node_child(stanza, 'pair-success')

    device_identity_node = get_binary_node_child(pair_success_node, 'device-identity')
    platform_node = get_binary_node_child(pair_success_node, 'platform')
    device_node = get_binary_node_child(pair_success_node, 'device')
    business_node = get_binary_node_child(pair_success_node, 'biz')

    if not device_identity_node or not device_node:
        raise Boom('Missing device-identity or device in pair success node', data=stanza)

    biz_name = (business_node.attrs or {}).get('name') if business_node else None
    jid = (device_node.attrs or {}).get('jid')
    lid = (device_node.attrs or {}).get('lid')

    hmac_msg = proto.ADVSignedDeviceIdentityHMAC.decode(device_identity_node.content)

    details = hmac_msg.details
    hmac = hmac_msg.hmac
    account_type = hmac_msg.accountType

    hmac_prefix = b''
    if account_type is not None and account_type == proto.ADVEncryptionType.HOSTED:
        hmac_prefix = WA_ADV_HOSTED_ACCOUNT_SIG_PREFIX

    import base64

    adv_sign = hmac_sign(
        bytes(hmac_prefix) + bytes(details),
        base64.b64decode(_to_b64(creds['advSecretKey'])),
    )
    if bytes(hmac) != bytes(adv_sign):
        raise Boom('Invalid account signature')

    account = proto.ADVSignedDeviceIdentity.decode(details)
    account_signature_key = account.accountSignatureKey
    account_signature = account.accountSignature
    device_details = account.details

    device_identity = proto.ADVDeviceIdentity.decode(device_details)

    account_signature_prefix = (
        WA_ADV_HOSTED_ACCOUNT_SIG_PREFIX
        if device_identity.deviceType == proto.ADVEncryptionType.HOSTED
        else WA_ADV_ACCOUNT_SIG_PREFIX
    )
    account_msg = bytes(account_signature_prefix) + bytes(device_details) + creds['signedIdentityKey']['public']
    if not Curve.verify(bytes(account_signature_key), account_msg, bytes(account_signature)):
        raise Boom('Failed to verify account signature')

    device_msg = (
        bytes(WA_ADV_DEVICE_SIG_PREFIX)
        + bytes(device_details)
        + creds['signedIdentityKey']['public']
        + bytes(account_signature_key)
    )
    if hasattr(account, 'deviceSignature'):
        account.deviceSignature = Curve.sign(creds['signedIdentityKey']['private'], device_msg)
    else:
        account['deviceSignature'] = Curve.sign(creds['signedIdentityKey']['private'], device_msg)

    identity = create_signal_identity(lid, bytes(account_signature_key))
    account_enc = encode_signed_device_identity(account, False)

    reply = BinaryNode(
        tag='iq',
        attrs={'to': S_WHATSAPP_NET, 'type': 'result', 'id': msg_id},
        content=[
            BinaryNode(
                tag='pair-device-sign',
                attrs={},
                content=[
                    BinaryNode(
                        tag='device-identity',
                        attrs={'key-index': str(device_identity.keyIndex)},
                        content=account_enc,
                    )
                ],
            )
        ],
    )

    auth_update = {
        'account': account,
        'me': {'id': jid, 'name': biz_name, 'lid': lid},
        'signalIdentities': (creds.get('signalIdentities') or []) + [identity],
        'platform': (platform_node.attrs or {}).get('name') if platform_node else None,
    }

    return {'creds': auth_update, 'reply': reply}


def _to_b64(value) -> str:
    """advSecretKey is stored base64; ensure we pass a proper b64 string."""
    if isinstance(value, bytes):
        import base64

        return base64.b64encode(value).decode('ascii')
    return value


def encode_signed_device_identity(account, include_signature_key: bool) -> bytes:
    account = dict(getattr(account, '__dict__', account) or {})
    if not include_signature_key or not (account.get('accountSignatureKey') or b''):
        account['accountSignatureKey'] = None
    return proto.ADVSignedDeviceIdentity.encode(account)
