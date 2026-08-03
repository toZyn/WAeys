"""Port of src/Socket/messages-send.ts — make_messages_socket (message relaying/sending layer).

Built as a layer over the base socket (`make_socket` in socket.py). Depends on the
following keys being present on the socket object (provided by chats/groups/newsletter
layers at integration time):

  - ev, authState, signalRepository, query, sendNode, executeUSyncQuery,
    registerSocketEndHandler, user, serverProps
  - messageMutex, upsertMessage, fetchPrivacySettings, groupMetadata,
    groupToggleEphemeral, profilePictureUrl, createCallLink

Returns an extended socket dict (dict spread of the input socket).
"""

from __future__ import annotations

import asyncio
import time
from datetime import datetime, timezone

from ..Defaults.index import DEFAULT_CACHE_TTLS, WA_DEFAULT_EPHEMERAL
from ..Utils.auth_utils import assert_me_id
from ..Utils.generics import (
    Boom,
    bind_wait_for_event,
    encode_newsletter_message,
    encode_wa_message,
    generate_message_id_v2,
    generate_participant_hash_v2,
    unix_timestamp_seconds,
)
from ..Utils.lru_cache import LRUCache
from ..Utils.make_mutex import make_keyed_mutex, make_mutex
from ..Utils.message_retry_manager import MessageRetryManager
from ..Utils.messages import (
    aggregate_message_keys_not_from_me,
    assert_media_content,
    generate_wa_message,
    normalize_message_content,
)
from ..Utils.messages_media import (
    DEF_MEDIA_HOST,
    decrypt_media_retry_data,
    get_status_code_for_media_retry,
    get_url_from_direct_path,
    get_wa_upload_to_server,
)
from ..Utils.reporting_utils import get_message_reporting_token, should_include_reporting_token
from ..Utils.signal import extract_device_jids, parse_and_inject_e2e_sessions
from ..Utils.tc_token_utils import (
    build_merged_tc_token_index_write,
    is_tc_token_expired,
    resolve_issuance_jid,
    resolve_tc_token_jid,
    should_send_new_tc_token,
    store_tc_tokens_from_iq_result,
)
from ..WAProto import WAProto as proto
from ..WABinary.jid_utils import (
    PSA_WID,
    S_WHATSAPP_NET,
    are_jids_same_user,
    is_hosted_lid_user,
    is_hosted_pn_user,
    is_jid_bot,
    is_jid_group,
    is_jid_meta_ai,
    is_lid_user,
    is_pn_user,
    jid_decode,
    jid_encode,
    jid_normalized_user,
)
from ..WAUSync.USyncQuery import USyncQuery
from ..WAUSync.USyncUser import USyncUser

STATUS_JID = 'status@broadcast'


def _get_media_type(message) -> str:
    if getattr(message, 'imageMessage', None):
        return 'image'
    if getattr(message, 'videoMessage', None):
        return 'gif' if getattr(message, 'videoMessage', None).gifPlayback else 'video'
    if getattr(message, 'audioMessage', None):
        return 'ptt' if getattr(message, 'audioMessage', None).ptt else 'audio'
    if getattr(message, 'contactMessage', None):
        return 'vcard'
    if getattr(message, 'documentMessage', None):
        return 'document'
    if getattr(message, 'contactsArrayMessage', None):
        return 'contact_array'
    if getattr(message, 'liveLocationMessage', None):
        return 'livelocation'
    if getattr(message, 'stickerMessage', None):
        return 'sticker'
    if getattr(message, 'listMessage', None):
        return 'list'
    if getattr(message, 'listResponseMessage', None):
        return 'list_response'
    if getattr(message, 'buttonsResponseMessage', None):
        return 'buttons_response'
    if getattr(message, 'orderMessage', None):
        return 'order'
    if getattr(message, 'productMessage', None):
        return 'product'
    if getattr(message, 'interactiveResponseMessage', None):
        return 'native_flow_response'
    if getattr(message, 'groupInviteMessage', None):
        return 'url'
    return ''


def _get_message_type(message) -> str:
    normalized = normalize_message_content(message)
    if not normalized:
        return 'text'

    if normalized.get('reactionMessage') is not None or normalized.get('encReactionMessage') is not None:
        return 'reaction'

    if (
        normalized.get('pollCreationMessage') is not None
        or normalized.get('pollCreationMessageV2') is not None
        or normalized.get('pollCreationMessageV3') is not None
        or normalized.get('pollUpdateMessage') is not None
    ):
        return 'poll'

    if normalized.get('eventMessage') is not None:
        return 'event'

    if _get_media_type(normalized) != '':
        return 'media'

    return 'text'


def make_messages_socket(sock: dict, config: dict) -> dict:
    logger = config.get('logger')
    link_preview_image_thumbnail_width = config.get('linkPreviewImageThumbnailWidth')
    generate_high_quality_link_preview = config.get('generateHighQualityLinkPreview')
    http_request_options = config.get('options')
    patch_message_before_sending = config.get('patchMessageBeforeSending')
    cached_group_metadata = config.get('cachedGroupMetadata')
    enable_recent_message_cache = config.get('enableRecentMessageCache')
    max_msg_retry_count = config.get('maxMsgRetryCount')

    ev = sock['ev']
    auth_state = sock['authState']
    signal_repository = sock['signalRepository']
    message_mutex = sock['messageMutex']
    upsert_message = sock['upsertMessage']
    query = sock['query']
    fetch_privacy_settings = sock['fetchPrivacySettings']
    send_node = sock['sendNode']
    group_metadata = sock['groupMetadata']
    group_toggle_ephemeral = sock['groupToggleEphemeral']
    register_socket_end_handler = sock['registerSocketEndHandler']

    get_lid_for_pn = signal_repository['lidMapping'].get_lid_for_pn

    in_flight_tc_token_issuance = set()

    user_devices_cache = config.get('userDevicesCache') or LRUCache(ttl=DEFAULT_CACHE_TTLS['USER_DEVICES'] * 1000)
    devices_mutex = make_mutex()

    message_retry_manager = MessageRetryManager(logger, max_msg_retry_count) if enable_recent_message_cache else None

    encryption_mutex = make_keyed_mutex()

    media_conn = None
    media_host = DEF_MEDIA_HOST

    async def refresh_media_conn(force_get=False):
        nonlocal media_conn, media_host
        media = await media_conn if media_conn else None
        if (
            not media
            or force_get
            or time.time() * 1000 - media['fetchDate'].timestamp() * 1000 > media['ttl'] * 1000
        ):
            async def _fetch():
                result = await query(
                    {
                        'tag': 'iq',
                        'attrs': {'type': 'set', 'xmlns': 'w:m', 'to': S_WHATSAPP_NET},
                        'content': [{'tag': 'media_conn', 'attrs': {}}],
                    }
                )

                def _child(node, tag):
                    content = node.get('content') or []
                    for child in content:
                        if getattr(child, 'tag', None) == tag or (isinstance(child, dict) and child.get('tag') == tag):
                            return child
                    return None

                media_conn_node = _child(result, 'media_conn')
                hosts = []
                content = media_conn_node.get('content') or []
                for child in content:
                    child_tag = getattr(child, 'tag', None) or (child.get('tag') if isinstance(child, dict) else None)
                    if child_tag == 'host':
                        attrs = getattr(child, 'attrs', None) or child.get('attrs', {})
                        hosts.append(
                            {
                                'hostname': attrs.get('hostname'),
                                'maxContentLengthBytes': int(attrs.get('maxContentLengthBytes', 0)),
                            }
                        )
                node = {
                    'hosts': hosts,
                    'auth': media_conn_node.get('attrs', {}).get('auth'),
                    'ttl': int(media_conn_node.get('attrs', {}).get('ttl', 0)),
                    'fetchDate': datetime.now(timezone.utc),
                }
                if logger is not None:
                    logger.debug('fetched media conn')
                if node['hosts']:
                    media_host = node['hosts'][0]['hostname']
                return node

            media_conn = asyncio.ensure_future(_fetch())

        return await media_conn

    async def send_receipt(jid, participant, message_ids, type_):
        if not message_ids:
            raise Boom('missing ids in receipt')

        node = {'tag': 'receipt', 'attrs': {'id': message_ids[0]}}
        is_read_receipt = type_ == 'read' or type_ == 'read-self'
        if is_read_receipt:
            node['attrs']['t'] = str(unix_timestamp_seconds())

        if type_ == 'sender' and (is_pn_user(jid) or is_lid_user(jid)):
            node['attrs']['recipient'] = jid
            node['attrs']['to'] = participant
        else:
            node['attrs']['to'] = jid
            if participant:
                node['attrs']['participant'] = participant

        if type_:
            node['attrs']['type'] = type_

        remaining_message_ids = message_ids[1:]
        if remaining_message_ids:
            node['content'] = [
                {
                    'tag': 'list',
                    'attrs': {},
                    'content': [{'tag': 'item', 'attrs': {'id': id_}} for id_ in remaining_message_ids],
                }
            ]

        if logger is not None:
            logger.debug({'attrs': node['attrs'], 'messageIds': message_ids}, 'sending receipt for messages')
        await send_node(node)

    async def send_receipts(keys, type_):
        recps = aggregate_message_keys_not_from_me(keys)
        for recp in recps:
            await send_receipt(recp['jid'], recp['participant'], recp['messageIds'], type_)

    async def read_messages(keys):
        privacy_settings = await fetch_privacy_settings()
        read_type = 'read' if privacy_settings.get('readreceipts') == 'all' else 'read-self'
        await send_receipts(keys, read_type)

    async def get_usync_devices(jids, use_cache, ignore_zero_devices):
        device_results = []

        if not use_cache and logger is not None:
            logger.debug('not using cache for devices')

        to_fetch = []
        jids_with_user = []
        for jid in jids:
            decoded = jid_decode(jid)
            user = getattr(decoded, 'user', None) if decoded else None
            device = getattr(decoded, 'device', None) if decoded else None
            is_explicit_device = isinstance(device, int) and device >= 0

            if is_explicit_device and user:
                device_results.append({'user': user, 'device': device, 'jid': jid})
                continue

            jid = jid_normalized_user(jid)
            jids_with_user.append({'jid': jid, 'user': user})

        mget_devices = None
        if use_cache:
            users_to_fetch = [j['user'] for j in jids_with_user if j['user']]
            if users_to_fetch:
                mget_devices = await _cache_mget(user_devices_cache, users_to_fetch)

        for entry in jids_with_user:
            jid = entry['jid']
            user = entry['user']
            if use_cache:
                devices = None
                if mget_devices:
                    devices = mget_devices.get(user)
                if devices is None:
                    devices = user_devices_cache.get(user)
                if devices:
                    devices_with_jid = [
                        {**d, 'jid': jid_encode(d['user'], d['server'], d.get('device'))} for d in devices
                    ]
                    device_results.extend(devices_with_jid)
                    if logger is not None:
                        logger.trace({'user': user}, 'using cache for devices')
                else:
                    to_fetch.append(jid)
            else:
                to_fetch.append(jid)

        if not to_fetch:
            return device_results

        requested_lid_users = set()
        for jid in to_fetch:
            if is_lid_user(jid) or is_hosted_lid_user(jid):
                user = jid_decode(jid).user if jid_decode(jid) else None
                if user:
                    requested_lid_users.add(user)

        usync_query = USyncQuery().with_context('message').with_device_protocol().with_lid_protocol()
        for jid in to_fetch:
            usync_query.with_user(USyncUser().with_id(jid))

        result = await sock['executeUSyncQuery'](usync_query)

        if result:
            lid_results = [a for a in result['list'] if a.get('lid')]
            if lid_results:
                if logger is not None:
                    logger.trace('Storing LID maps from device call')
                await signal_repository['lidMapping'].store_lidpn_mappings(
                    [{'lid': a['lid'], 'pn': a['id']} for a in lid_results]
                )
                try:
                    lids = [a['lid'] for a in lid_results]
                    if lids:
                        await assert_sessions(lids, True)
                except Exception as e:
                    if logger is not None:
                        logger.warn({'e': e, 'count': len(lid_results)}, 'failed to assert sessions for newly mapped LIDs')

            extracted = extract_device_jids(
                result['list'], auth_state['creds']['me']['id'], auth_state['creds']['me'].get('lid'), ignore_zero_devices
            )
            device_map = {}
            for item in extracted:
                device_map.setdefault(item['user'], []).append(item)

            for user, user_devices in device_map.items():
                is_lid_user_flag = user in requested_lid_users
                for item in user_devices:
                    final_jid = (
                        jid_encode(user, item['server'], item['device'])
                        if is_lid_user_flag
                        else jid_encode(item['user'], item['server'], item['device'])
                    )
                    device_results.append({**item, 'jid': final_jid})
                    if logger is not None:
                        logger.debug(
                            {'user': item['user'], 'device': item['device'], 'finalJid': final_jid, 'usedLid': is_lid_user_flag},
                            'Processed device with LID priority',
                        )

            async def _store_devices():
                for key, value in device_map.items():
                    if value:
                        user_devices_cache.set(key, value)

            await devices_mutex['mutex'](_store_devices)

            user_device_updates = {}
            for user_id, devices in device_map.items():
                if devices:
                    user_device_updates[user_id] = [str(d.get('device') or '0') for d in devices]

            if user_device_updates:
                try:
                    await auth_state['keys'].set({'device-list': user_device_updates})
                    if logger is not None:
                        logger.debug(
                            {'userCount': len(user_device_updates)}, 'stored user device lists for bulk migration'
                        )
                except Exception as error:
                    if logger is not None:
                        logger.warn({'error': error}, 'failed to store user device lists')

        return device_results

    async def _cache_mget(cache, keys):
        out = {}
        for k in keys:
            value = cache.get(k)
            if value is not None:
                out[k] = value
        return out

    def update_member_label(jid, member_label):
        return relay_message(
            jid,
            {
                'protocolMessage': {
                    'type': proto.Message.ProtocolMessage.Type.GROUP_MEMBER_LABEL_CHANGE,
                    'memberLabel': {
                        'label': (member_label or '')[:30],
                        'labelTimestamp': unix_timestamp_seconds(),
                    },
                }
            },
            {
                'additionalNodes': [
                    {
                        'tag': 'meta',
                        'attrs': {'tag_reason': 'user_update', 'appdata': 'member_tag'},
                        'content': None,
                    }
                ]
            },
        )

    async def assert_sessions(jids, force=False):
        did_fetch_new_session = False
        unique_jids = list(dict.fromkeys(jids))
        jids_requiring_fetch = []

        if logger is not None:
            logger.debug({'jids': jids}, 'assertSessions call with jids')

        for jid in unique_jids:
            if not force:
                session_validation = await signal_repository['validateSession'](jid)
                if session_validation.get('exists'):
                    continue
            jids_requiring_fetch.append(jid)

        if jids_requiring_fetch:
            wire_jids = []
            wire_jids.extend(j for j in jids_requiring_fetch if is_lid_user(j) or is_hosted_lid_user(j))
            pn_jids = [j for j in jids_requiring_fetch if is_pn_user(j) or is_hosted_pn_user(j)]
            if pn_jids:
                lids = await signal_repository['lidMapping'].get_lids_for_pns(pn_jids)
                wire_jids.extend(a['lid'] for a in (lids or []))
            wire_jids = list(dict.fromkeys(wire_jids))

            if logger is not None:
                logger.debug({'jidsRequiringFetch': jids_requiring_fetch, 'wireJids': wire_jids}, 'fetching sessions')
            result = await query(
                {
                    'tag': 'iq',
                    'attrs': {'xmlns': 'encrypt', 'type': 'get', 'to': S_WHATSAPP_NET},
                    'content': [
                        {
                            'tag': 'key',
                            'attrs': {},
                            'content': [
                                {'tag': 'user', 'attrs': {'jid': jid, **({'reason': 'identity'} if force else {})}}
                                for jid in wire_jids
                            ],
                        }
                    ],
                }
            )
            await parse_and_inject_e2e_sessions(result, signal_repository)
            did_fetch_new_session = True

        return did_fetch_new_session

    async def send_peer_data_operation_message(pdo_message):
        if not auth_state['creds']['me'].get('id'):
            raise Boom('Not authenticated')

        protocol_message = {
            'protocolMessage': {
                'peerDataOperationRequestMessage': pdo_message,
                'type': proto.Message.ProtocolMessage.Type.PEER_DATA_OPERATION_REQUEST_MESSAGE,
            }
        }

        me_jid = jid_normalized_user(auth_state['creds']['me']['id'])

        msg_id = await relay_message(
            me_jid,
            protocol_message,
            {
                'additionalAttributes': {'category': 'peer', 'push_priority': 'high_force'},
                'additionalNodes': [{'tag': 'meta', 'attrs': {'appdata': 'default'}}],
            },
        )

        return msg_id

    async def create_participant_nodes(recipient_jids, message, extra_attrs=None, dsm_message=None):
        if not recipient_jids:
            return {'nodes': [], 'shouldIncludeDeviceIdentity': False}

        patched = await patch_message_before_sending(message, recipient_jids)
        if isinstance(patched, list):
            patched_messages = patched
        else:
            patched_messages = [{'recipientJid': jid, 'message': patched} for jid in recipient_jids]

        should_include_device_identity = False
        me_id = auth_state['creds']['me']['id']
        me_lid = auth_state['creds']['me'].get('lid')
        me_lid_user = jid_decode(me_lid).user if me_lid and jid_decode(me_lid) else None

        async def encrypt_for_recipient(entry):
            nonlocal should_include_device_identity
            jid = entry['recipientJid']
            patched_message = entry['message']
            try:
                if not jid:
                    return None

                msg_to_encrypt = patched_message

                if dsm_message:
                    target_user = jid_decode(jid).user if jid_decode(jid) else None
                    own_pn_user = jid_decode(me_id).user if jid_decode(me_id) else None
                    own_lid_user = me_lid_user

                    is_own_user = target_user == own_pn_user or (own_lid_user and target_user == own_lid_user)
                    is_exact_sender_device = jid == me_id or (me_lid and jid == me_lid)

                    if is_own_user and not is_exact_sender_device:
                        msg_to_encrypt = dsm_message
                        if logger is not None:
                            logger.debug({'jid': jid, 'targetUser': target_user}, 'Using DSM for own device')

                bytes_ = encode_wa_message(msg_to_encrypt)

                async def _encrypt():
                    nonlocal should_include_device_identity
                    result = await signal_repository['encryptMessage']({'jid': jid, 'data': bytes_})
                    if result['type'] == 'pkmsg':
                        should_include_device_identity = True
                    return {
                        'tag': 'to',
                        'attrs': {'jid': jid},
                        'content': [
                            {
                                'tag': 'enc',
                                'attrs': {'v': '2', 'type': result['type'], **(extra_attrs or {})},
                                'content': result['ciphertext'],
                            }
                        ],
                    }

                return await encryption_mutex['mutex'](jid, _encrypt)
            except Exception as err:
                if logger is not None:
                    logger.error({'jid': jid, 'err': err}, 'Failed to encrypt for recipient')
                return None

        results = await asyncio.gather(*[encrypt_for_recipient(p) for p in patched_messages])
        nodes = [node for node in results if node is not None]

        if recipient_jids and not nodes:
            raise Boom('All encryptions failed', status_code=500)

        return {'nodes': nodes, 'shouldIncludeDeviceIdentity': should_include_device_identity}

    async def relay_message(jid, message, opts=None):
        opts = dict(opts or {})
        msg_id = opts.get('messageId')
        participant = opts.get('participant')
        additional_attributes = opts.get('additionalAttributes')
        additional_nodes = opts.get('additionalNodes')
        use_user_devices_cache = opts.get('useUserDevicesCache')
        use_cached_group_metadata = opts.get('useCachedGroupMetadata')
        status_jid_list = opts.get('statusJidList')

        me_id = assert_me_id(auth_state['creds'])
        me_lid = auth_state['creds']['me'].get('lid')
        is_retry_resend = bool(participant and participant.get('jid'))
        should_include_device_identity = is_retry_resend
        status_jid = STATUS_JID

        decoded = jid_decode(jid)
        user = decoded.user if decoded else None
        server = decoded.server if decoded else None
        is_group = server == 'g.us'
        is_status = jid == status_jid
        is_lid = server == 'lid'
        is_newsletter = server == 'newsletter'
        is_group_or_status = is_group or is_status
        final_jid = jid

        msg_id = msg_id or generate_message_id_v2(me_id)
        use_user_devices_cache = use_user_devices_cache is not False
        use_cached_group_metadata = use_cached_group_metadata is not False and not is_status

        participants = []
        destination_jid = status_jid if is_status else final_jid
        binary_node_content = []
        devices = []
        reporting_message = None

        me_msg = {
            'deviceSentMessage': {'destinationJid': destination_jid, 'message': message},
            'messageContextInfo': getattr(message, 'messageContextInfo', None),
        }

        extra_attrs = {}

        if participant:
            if not is_group and not is_status:
                additional_attributes = {**(additional_attributes or {}), 'device_fanout': 'false'}

            p_decoded = jid_decode(participant['jid'])
            devices.append(
                {
                    'user': p_decoded.user if p_decoded else None,
                    'device': p_decoded.device if p_decoded else None,
                    'jid': participant['jid'],
                }
            )

        async def _run():
            nonlocal should_include_device_identity, reporting_message, additional_attributes, extra_attrs, participants, devices, binary_node_content
            media_type = _get_media_type(message)
            if media_type:
                extra_attrs['mediatype'] = media_type

            if is_newsletter:
                patched = await patch_message_before_sending(message, []) if patch_message_before_sending else message
                bytes_ = encode_newsletter_message(patched)
                binary_node_content.append({'tag': 'plaintext', 'attrs': {}, 'content': bytes_})
                stanza = {
                    'tag': 'message',
                    'attrs': {
                        'to': jid,
                        'id': msg_id,
                        'type': _get_message_type(message),
                        **(additional_attributes or {}),
                    },
                    'content': binary_node_content,
                }
                if logger is not None:
                    logger.debug({'msgId': msg_id}, f'sending newsletter message to {jid}')
                await send_node(stanza)
                return

            normalized = normalize_message_content(message)
            if (normalized or {}).get('pinInChatMessage') or (normalized or {}).get('reactionMessage'):
                extra_attrs['decrypt-fail'] = 'hide'

            if is_group_or_status and not is_retry_resend:
                async def _get_group_data():
                    group_data = (
                        await cached_group_metadata(jid)
                        if use_cached_group_metadata and cached_group_metadata
                        else None
                    )
                    if group_data and isinstance(group_data.get('participants'), list):
                        if logger is not None:
                            logger.trace(
                                {'jid': jid, 'participants': len(group_data['participants'])},
                                'using cached group metadata',
                            )
                    elif not is_status:
                        group_data = await group_metadata(jid)
                    return group_data

                async def _get_sender_key_map():
                    if not participant and not is_status:
                        result = await auth_state['keys'].get('sender-key-memory', [jid])
                        return (result or {}).get(jid) or {}
                    return {}

                group_data, sender_key_map = await asyncio.gather(_get_group_data(), _get_sender_key_map())

                participants_list = [p['id'] for p in (group_data.get('participants') or []) if 'id' in p]

                if group_data and group_data.get('ephemeralDuration', 0) > 0:
                    additional_attributes = {
                        **(additional_attributes or {}),
                        'expiration': str(group_data['ephemeralDuration']),
                    }

                if is_status and status_jid_list:
                    participants_list.extend(status_jid_list)

                additional_devices = await get_usync_devices(participants_list, bool(use_user_devices_cache), False)
                devices.extend(additional_devices)

                if is_group:
                    additional_attributes = {
                        **(additional_attributes or {}),
                        'addressing_mode': group_data.get('addressingMode') or 'lid',
                    }

                patched = await patch_message_before_sending(message)
                if isinstance(patched, list):
                    raise Boom('Per-jid patching is not supported in groups')

                bytes_ = encode_wa_message(patched)
                reporting_message = patched
                group_addressing_mode = (additional_attributes or {}).get('addressing_mode') or (
                    group_data.get('addressingMode') if group_data else None
                ) or 'lid'
                group_sender_identity = me_lid if group_addressing_mode == 'lid' and me_lid else me_id

                result = await signal_repository['encryptGroupMessage'](
                    {'group': destination_jid, 'data': bytes_, 'meId': group_sender_identity}
                )

                sender_key_recipients = []
                for device in devices:
                    device_jid = device['jid']
                    has_key = sender_key_map.get(device_jid)
                    if (
                        (not has_key or participant)
                        and not is_hosted_lid_user(device_jid)
                        and not is_hosted_pn_user(device_jid)
                        and device.get('device') != 99
                    ):
                        sender_key_recipients.append(device_jid)
                        sender_key_map[device_jid] = True

                if sender_key_recipients:
                    if logger is not None:
                        logger.debug({'senderKeyJids': sender_key_recipients}, 'sending new sender key')

                    sender_key_msg = {
                        'senderKeyDistributionMessage': {
                            'axolotlSenderKeyDistributionMessage': result['senderKeyDistributionMessage'],
                            'groupId': destination_jid,
                        }
                    }

                    await assert_sessions(sender_key_recipients)

                    result_nodes = await create_participant_nodes(sender_key_recipients, sender_key_msg, extra_attrs)
                    should_include_device_identity = (
                        should_include_device_identity or result_nodes['shouldIncludeDeviceIdentity']
                    )
                    participants.extend(result_nodes['nodes'])

                binary_node_content.append(
                    {'tag': 'enc', 'attrs': {'v': '2', 'type': 'skmsg', **extra_attrs}, 'content': result['ciphertext']}
                )

                await auth_state['keys'].set({'sender-key-memory': {jid: sender_key_map}})
            else:
                own_id = me_lid if is_lid and me_lid else me_id
                if is_lid and me_lid:
                    if logger is not None:
                        logger.debug({'to': jid, 'ownId': own_id}, 'Using LID identity for @lid conversation')
                elif logger is not None:
                    logger.debug({'to': jid, 'ownId': own_id}, 'Using PN identity for @s.whatsapp.net conversation')

                own_user = jid_decode(own_id).user if jid_decode(own_id) else None
                if not participant:
                    patched_for_reporting = await patch_message_before_sending(message, [jid])
                    if isinstance(patched_for_reporting, list):
                        reporting_message = (
                            next((item for item in patched_for_reporting if item['recipientJid'] == jid), None)
                            or patched_for_reporting[0]
                        )
                    else:
                        reporting_message = patched_for_reporting

                if not is_retry_resend:
                    target_user_server = 'lid' if is_lid else 's.whatsapp.net'
                    devices.append({'user': user, 'device': 0, 'jid': jid_encode(user, target_user_server, 0)})

                    if user != own_user:
                        own_user_server = 'lid' if is_lid else 's.whatsapp.net'
                        own_user_for_addressing = (
                            jid_decode(me_lid).user if is_lid and me_lid else (jid_decode(me_id).user if jid_decode(me_id) else None)
                        )
                        devices.append(
                            {'user': own_user_for_addressing, 'device': 0, 'jid': jid_encode(own_user_for_addressing, own_user_server, 0)}
                        )

                    if (additional_attributes or {}).get('category') != 'peer':
                        devices = []
                        sender_identity = (
                            jid_encode(jid_decode(me_lid).user, 'lid', None)
                            if is_lid and me_lid
                            else jid_encode(jid_decode(me_id).user, 's.whatsapp.net', None)
                        )
                        session_devices = await get_usync_devices([sender_identity, jid], True, False)
                        devices.extend(session_devices)

                        if logger is not None:
                            logger.debug(
                                {
                                    'deviceCount': len(devices),
                                    'devices': [
                                        f"{d['user']}:{d['device']}@{jid_decode(d['jid']).server if jid_decode(d['jid']) else ''}"
                                        for d in devices
                                    ],
                                },
                                'Device enumeration complete with unified addressing',
                            )

                all_recipients = []
                me_recipients = []
                other_recipients = []
                me_pn_user = jid_decode(me_id).user if jid_decode(me_id) else None
                me_lid_user = jid_decode(me_lid).user if me_lid and jid_decode(me_lid) else None

                for device in devices:
                    device_user = device['user']
                    device_jid = device['jid']
                    is_exact_sender_device = device_jid == me_id or (me_lid and device_jid == me_lid)
                    if is_exact_sender_device:
                        if logger is not None:
                            logger.debug({'jid': device_jid, 'meId': me_id, 'meLid': me_lid}, 'Skipping exact sender device (whatsmeow pattern)')
                        continue

                    is_me = device_user == me_pn_user or device_user == me_lid_user

                    if is_me:
                        me_recipients.append(device_jid)
                    else:
                        other_recipients.append(device_jid)
                    all_recipients.append(device_jid)

                await assert_sessions(all_recipients)

                me_result, other_result = await asyncio.gather(
                    create_participant_nodes(me_recipients, me_msg or message, extra_attrs),
                    create_participant_nodes(other_recipients, message, extra_attrs, me_msg),
                )
                participants.extend(me_result['nodes'])
                participants.extend(other_result['nodes'])

                if me_recipients or other_recipients:
                    extra_attrs['phash'] = generate_participant_hash_v2([*me_recipients, *other_recipients])

                should_include_device_identity = (
                    should_include_device_identity or me_result['shouldIncludeDeviceIdentity'] or other_result['shouldIncludeDeviceIdentity']
                )

            if is_retry_resend:
                is_participant_lid = is_lid_user(participant['jid'])
                is_me = are_jids_same_user(participant['jid'], me_lid if is_participant_lid else me_id)

                message_to_send = message
                if is_group_or_status:
                    group_sender_identity = None
                    if me_lid and await signal_repository['hasSenderKey']({'group': destination_jid, 'meId': me_lid}):
                        group_sender_identity = me_lid
                    elif await signal_repository['hasSenderKey']({'group': destination_jid, 'meId': me_id}):
                        group_sender_identity = me_id

                    if group_sender_identity:
                        try:
                            skdm = await signal_repository['getSenderKeyDistributionMessage'](
                                {'group': destination_jid, 'meId': group_sender_identity}
                            )
                            message_to_send = {
                                **message,
                                'senderKeyDistributionMessage': {
                                    'groupId': destination_jid,
                                    'axolotlSenderKeyDistributionMessage': skdm,
                                },
                            }
                        except Exception as err:
                            if logger is not None:
                                logger.warn(
                                    {'err': err, 'jid': destination_jid}, 'failed to build SKDM for retry, sending without it'
                                )

                encoded_message_to_send = (
                    encode_wa_message(
                        {'deviceSentMessage': {'destinationJid': destination_jid, 'message': message_to_send}}
                    )
                    if is_me
                    else encode_wa_message(message_to_send)
                )

                result = await signal_repository['encryptMessage'](
                    {'data': encoded_message_to_send, 'jid': participant['jid']}
                )
                binary_node_content.append(
                    {
                        'tag': 'enc',
                        'attrs': {'v': '2', 'type': result['type'], 'count': str(participant['count'])},
                        'content': result['ciphertext'],
                    }
                )

            if participants:
                if (additional_attributes or {}).get('category') == 'peer':
                    peer_node = participants[0].get('content', [None])[0] if participants[0].get('content') else None
                    if peer_node:
                        binary_node_content.append(peer_node)
                else:
                    binary_node_content.append({'tag': 'participants', 'attrs': {}, 'content': participants})

            stanza = {
                'tag': 'message',
                'attrs': {
                    'id': msg_id,
                    'to': destination_jid,
                    'type': _get_message_type(message),
                    **(additional_attributes or {}),
                },
                'content': binary_node_content,
            }

            if participant:
                if is_jid_group(destination_jid):
                    stanza['attrs']['to'] = destination_jid
                    stanza['attrs']['participant'] = participant['jid']
                elif are_jids_same_user(participant['jid'], me_id):
                    stanza['attrs']['to'] = participant['jid']
                    stanza['attrs']['recipient'] = destination_jid
                else:
                    stanza['attrs']['to'] = participant['jid']
            else:
                stanza['attrs']['to'] = destination_jid

            if should_include_device_identity:
                from ..Utils.validate_connection import encode_signed_device_identity

                stanza['content'].append(
                    {
                        'tag': 'device-identity',
                        'attrs': {},
                        'content': encode_signed_device_identity(auth_state['creds']['account'], True),
                    }
                )
                if logger is not None:
                    logger.debug({'jid': jid}, 'adding device identity')

            reporting_content = getattr(reporting_message, 'messageContextInfo', None) if reporting_message else None
            from ..WAProto.runtime import Message as _ProtoBase

            if isinstance(reporting_content, _ProtoBase):
                from ..Utils.messages import _message_to_plain_dict

                reporting_content = _message_to_plain_dict(reporting_content)
            if (
                not is_newsletter
                and not is_retry_resend
                and reporting_content
                and reporting_content.get('messageSecret')
                and should_include_reporting_token(reporting_message)
            ):
                try:
                    encoded = encode_wa_message(reporting_message)
                    reporting_key = {
                        'id': msg_id,
                        'fromMe': True,
                        'remoteJid': destination_jid,
                        'participant': participant['jid'] if participant else None,
                    }
                    reporting_node = await get_message_reporting_token(encoded, reporting_message, reporting_key)
                    if reporting_node:
                        stanza['content'].append(reporting_node)
                        if logger is not None:
                            logger.trace({'jid': jid}, 'added reporting token to message')
                except Exception as error:
                    if logger is not None:
                        logger.warn({'jid': jid, 'trace': getattr(error, 'stack', None)}, 'failed to attach reporting token')

            is_peer_message = (additional_attributes or {}).get('category') == 'peer'
            is_1on1_send = not is_group and not is_retry_resend and not is_status and not is_newsletter and not is_peer_message

            tc_token_jid = await resolve_tc_token_jid(destination_jid, get_lid_for_pn) if is_1on1_send else destination_jid
            contact_tc_token_data = await auth_state['keys'].get('tctoken', [tc_token_jid]) if is_1on1_send else {}
            existing_token_entry = contact_tc_token_data.get(tc_token_jid)
            tc_token_buffer = (existing_token_entry or {}).get('token')

            if tc_token_buffer and is_tc_token_expired((existing_token_entry or {}).get('timestamp')):
                if logger is not None:
                    logger.debug(
                        {'jid': destination_jid, 'timestamp': (existing_token_entry or {}).get('timestamp')},
                        'tctoken expired, clearing',
                    )
                tc_token_buffer = None
                cleared = (
                    {'token': b'', 'senderTimestamp': existing_token_entry['senderTimestamp']}
                    if existing_token_entry and existing_token_entry.get('senderTimestamp') is not None
                    else None
                )
                try:
                    await auth_state['keys'].set({'tctoken': {tc_token_jid: cleared}})
                except Exception as err:
                    if logger is not None:
                        logger.debug(
                            {'jid': destination_jid, 'err': str(err)}, 'failed to persist tctoken expiry cleanup'
                        )

            server_props = sock.get('serverProps') or {}
            if tc_token_buffer and server_props.get('privacyTokenOn1to1'):
                stanza['content'].append({'tag': 'tctoken', 'attrs': {}, 'content': tc_token_buffer})

            if additional_nodes:
                stanza['content'].extend(additional_nodes)

            if logger is not None:
                logger.debug({'msgId': msg_id}, f'sending message to {len(participants)} devices')

            await send_node(stanza)

            is_protocol_msg = bool((normalize_message_content(message) or {}).get('protocolMessage'))
            is_bot_or_psa = destination_jid == PSA_WID or is_jid_bot(destination_jid) or is_jid_meta_ai(destination_jid)
            if (
                is_1on1_send
                and not is_protocol_msg
                and not is_bot_or_psa
                and should_send_new_tc_token((existing_token_entry or {}).get('senderTimestamp'))
                and tc_token_jid not in in_flight_tc_token_issuance
            ):
                in_flight_tc_token_issuance.add(tc_token_jid)
                issue_timestamp = unix_timestamp_seconds()
                get_pn_for_lid = signal_repository['lidMapping'].get_pn_for_lid

                async def _issue_flow():
                    try:
                        issue_jid = await resolve_issuance_jid(
                            destination_jid, server_props.get('lidTrustedTokenIssueToLid'), get_lid_for_pn, get_pn_for_lid
                        )
                        result = await issue_privacy_tokens([issue_jid], issue_timestamp)
                        await store_tc_tokens_from_iq_result(
                            {'result': result, 'fallbackJid': tc_token_jid, 'keys': auth_state['keys'], 'getLIDForPN': get_lid_for_pn}
                        )
                        current_data = await auth_state['keys'].get('tctoken', [tc_token_jid])
                        current_entry = current_data.get(tc_token_jid)
                        index_write = await build_merged_tc_token_index_write(auth_state['keys'], [tc_token_jid])
                        await auth_state['keys'].set(
                            {
                                'tctoken': {
                                    tc_token_jid: {
                                        'token': b'',
                                        **(current_entry or {}),
                                        'senderTimestamp': issue_timestamp,
                                    },
                                    **index_write,
                                }
                            }
                        )
                    except Exception as err:
                        if logger is not None:
                            logger.debug(
                                {'jid': destination_jid, 'err': str(err)}, 'fire-and-forget tctoken issuance failed'
                            )
                    finally:
                        in_flight_tc_token_issuance.discard(tc_token_jid)

                asyncio.ensure_future(_issue_flow())

            if message_retry_manager and not participant:
                message_retry_manager.add_recent_message(destination_jid, msg_id, message)

        await auth_state['keys'].transaction(_run, me_id)

        return msg_id

    async def issue_privacy_tokens(jids, timestamp=None):
        t = str(timestamp if timestamp is not None else unix_timestamp_seconds())
        result = await query(
            {
                'tag': 'iq',
                'attrs': {'to': S_WHATSAPP_NET, 'type': 'set', 'xmlns': 'privacy'},
                'content': [
                    {
                        'tag': 'tokens',
                        'attrs': {},
                        'content': [
                            {
                                'tag': 'token',
                                'attrs': {'jid': jid_normalized_user(jid), 't': t, 'type': 'trusted_contact'},
                            }
                            for jid in jids
                        ],
                    }
                ],
            }
        )
        return result

    wa_upload_to_server = get_wa_upload_to_server(config, refresh_media_conn)

    wait_for_msg_media_update = bind_wait_for_event(ev, 'messages.media-update')

    def _on_socket_end(error):
        nonlocal media_conn
        if not config.get('userDevicesCache'):
            if hasattr(user_devices_cache, 'close'):
                user_devices_cache.close()
            elif hasattr(user_devices_cache, 'clear'):
                user_devices_cache.clear()

        media_conn = None
        if message_retry_manager:
            message_retry_manager.clear()

    register_socket_end_handler(_on_socket_end)

    async def update_media_message(message):
        content = assert_media_content(message['message'])
        media_key = content['mediaKey']
        me_id = auth_state['creds']['me']['id']
        node = None
        from ..Utils.messages_media import encrypt_media_retry_request

        node = encrypt_media_retry_request(message['key'], media_key, me_id)

        error = None

        async def _check_update(update):
            nonlocal error
            result = next((c for c in update if c['key']['id'] == message['key']['id']), None)
            if result:
                if result.get('error'):
                    error = result['error']
                else:
                    try:
                        media = decrypt_media_retry_data(result['media'], media_key, result['key']['id'])
                        from ..WAProto.runtime import Message as _ProtoBase

                        if isinstance(media, _ProtoBase):
                            from ..Utils.messages import _message_to_plain_dict

                            media = _message_to_plain_dict(media)
                        if media['result'] != proto.MediaRetryNotification.ResultType.SUCCESS:
                            result_str = proto.MediaRetryNotification.ResultType(media['result']).name
                            raise Boom(
                                f'Media re-upload failed by device ({result_str})',
                                data=media,
                                status_code=get_status_code_for_media_retry(media['result']) or 404,
                            )
                        content['directPath'] = media['directPath']
                        content['url'] = get_url_from_direct_path(content['directPath'], media_host)
                        if logger is not None:
                            logger.debug({'directPath': media['directPath'], 'key': result['key']}, 'media update successful')
                    except Exception as err:
                        error = err
                return True
            return None

        await asyncio.gather(send_node(node), wait_for_msg_media_update(_check_update))

        if error:
            raise error

        ev.emit('messages.update', [{'key': message['key'], 'update': {'message': message['message']}}])

        return message

    async def send_message(jid, content, options=None):
        options = dict(options or {})
        user_jid = auth_state['creds']['me']['id']
        if isinstance(content, dict) and 'disappearingMessagesInChat' in content and content.get('disappearingMessagesInChat') is not None and is_jid_group(jid):
            disappearing_messages_in_chat = content['disappearingMessagesInChat']
            value = (
                (WA_DEFAULT_EPHEMERAL if disappearing_messages_in_chat else 0)
                if isinstance(disappearing_messages_in_chat, bool)
                else disappearing_messages_in_chat
            )
            await group_toggle_ephemeral(jid, value)
        else:
            from ..Utils.link_preview import get_url_info

            full_msg = await generate_wa_message(
                jid,
                content,
                {
                    'logger': logger,
                    'userJid': user_jid,
                    'getUrlInfo': lambda text: get_url_info(
                        text,
                        {
                            'thumbnailWidth': link_preview_image_thumbnail_width,
                            'fetchOpts': {'timeout': 3000, **(http_request_options or {})},
                            'logger': logger,
                            'uploadImage': wa_upload_to_server if generate_high_quality_link_preview else None,
                        },
                    ),
                    'getProfilePicUrl': sock.get('profilePictureUrl'),
                    'getCallLink': sock.get('createCallLink'),
                    'upload': wa_upload_to_server,
                    'mediaCache': config.get('mediaCache'),
                    'options': config.get('options'),
                    'messageId': generate_message_id_v2((sock.get('user') or {}).get('id') if sock.get('user') else None),
                    **options,
                },
            )
            is_event_msg = isinstance(content, dict) and content.get('event')
            is_delete_msg = isinstance(content, dict) and content.get('delete')
            is_edit_msg = isinstance(content, dict) and content.get('edit')
            is_pin_msg = isinstance(content, dict) and content.get('pin')
            is_poll_message = isinstance(content, dict) and content.get('poll')
            additional_attributes = {}
            additional_nodes = []
            if is_delete_msg:
                if is_jid_group(content['delete'].get('remoteJid')) and not content['delete'].get('fromMe'):
                    additional_attributes['edit'] = '8'
                else:
                    additional_attributes['edit'] = '7'
            elif is_edit_msg:
                additional_attributes['edit'] = '1'
            elif is_pin_msg:
                additional_attributes['edit'] = '2'
            elif is_poll_message:
                additional_nodes.append({'tag': 'meta', 'attrs': {'polltype': 'creation'}})
            elif is_event_msg:
                additional_nodes.append({'tag': 'meta', 'attrs': {'event_type': 'creation'}})

            await relay_message(
                jid,
                full_msg['message'],
                {
                    'messageId': full_msg['key']['id'],
                    'useCachedGroupMetadata': options.get('useCachedGroupMetadata'),
                    'additionalAttributes': additional_attributes,
                    'statusJidList': options.get('statusJidList'),
                    'additionalNodes': additional_nodes,
                },
            )
            if config.get('emitOwnEvents'):
                asyncio.ensure_future(message_mutex['mutex'](lambda: upsert_message(full_msg, 'append')))

            return full_msg

    return {
        **sock,
        'userDevicesCache': user_devices_cache,
        'devicesMutex': devices_mutex,
        'issuePrivacyTokens': issue_privacy_tokens,
        'assertSessions': assert_sessions,
        'relayMessage': relay_message,
        'sendReceipt': send_receipt,
        'sendReceipts': send_receipts,
        'readMessages': read_messages,
        'refreshMediaConn': refresh_media_conn,
        'getMediaHost': lambda: media_host,
        'waUploadToServer': wa_upload_to_server,
        'fetchPrivacySettings': fetch_privacy_settings,
        'sendPeerDataOperationMessage': send_peer_data_operation_message,
        'createParticipantNodes': create_participant_nodes,
        'getUSyncDevices': get_usync_devices,
        'messageRetryManager': message_retry_manager,
        'updateMemberLabel': update_member_label,
        'updateMediaMessage': update_media_message,
        'sendMessage': send_message,
    }
