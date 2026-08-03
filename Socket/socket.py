"""Port of src/Socket/socket.ts — makeSocket: the low-level WA Web socket.

Implements:
- connection handshake (Noise protocol over the WS)
- pre-key generation/upload
- QR / pairing-code flows
- generic query / wait-for-message
- keep-alive, event buffer, signal repository wiring
"""

from __future__ import annotations

import asyncio
import base64
import os
import random
import time
from urllib.parse import urlparse, parse_qs, urlencode

from ..Defaults.index import (
    DEF_CALLBACK_PREFIX,
    DEF_TAG_PREFIX,
    INITIAL_PREKEY_COUNT,
    MIN_PREKEY_COUNT,
    NOISE_WA_HEADER,
    TimeMs,
    UPLOAD_TIMEOUT,
    _init_processable_history_types,
)
from ..Defaults import index as _defaults_module
from ..Types.index import DisconnectReason, QueryIds, ReachoutTimelockEnforcementType, XWAPaths
from ..WAProto import WAProto as proto
from ..WAUSync import USyncQuery, USyncUser
from ..WABinary.encode import encode_binary_node
from ..WABinary.generic_utils import (
    assert_node_error_free,
    binary_node_to_string,
    get_all_binary_node_children,
    get_binary_node_child,
    get_binary_node_child_buffer,
    get_binary_node_children,
    reduce_binary_node_to_dictionary,
)
from ..WABinary.jid_utils import S_WHATSAPP_NET, is_lid_user, jid_decode, jid_encode
from ..WABinary.types import BinaryNode
from ..WAM import BinaryInfo
from ..Utils.auth_utils import add_transaction_capability
from ..Utils.companion_reg_client_utils import build_pairing_qr_data, get_companion_platform_id, get_pairing_code_platform
from ..Utils.crypto import (
    Curve,
    aes_decrypt_ctr,
    aes_encrypt_ctr,
    aes_gcm_encrypt,
    derive_pairing_code_key,
    hkdf,
    signed_key_pair,
)
from ..Utils.event_buffer import make_event_buffer
from ..Utils.generics import (
    Boom,
    bind_wait_for_connection_update,
    bytes_to_crockford,
    generate_md_tag_prefix,
    get_code_from_ws_error,
    get_error_code_from_stream_error,
    promise_timeout,
)
from ..Utils.noise_handler import make_noise_handler
from ..Utils.make_mutex import make_mutex
from ..Utils.signal import get_next_pre_keys_node, xmpp_signed_pre_key
from ..Utils.validate_connection import configure_successful_pairing, generate_login_node, generate_registration_node
from .Client import WebSocketClient
from .mex import execute_wmex_query


def _epoch():
    e = 0
    while True:
        yield e
        e += 1


def map_web_socket_error(handler):
    def mapped(error):
        handler(Boom(f'WebSocket Error ({getattr(error, "message", None) or error})',
                     status_code=get_code_from_ws_error(error), data=error))

    return mapped


def make_socket(config: dict):
    _init_processable_history_types()
    processable_history_types = _defaults_module.PROCESSABLE_HISTORY_TYPES

    wa_web_socket_url = config.get('waWebSocketUrl')
    connect_timeout_ms = config.get('connectTimeoutMs')
    logger = config.get('logger')
    keep_alive_interval_ms = config.get('keepAliveIntervalMs')
    browser = config.get('browser')
    auth_state = config.get('auth')
    print_qr_in_terminal = config.get('printQRInTerminal')
    default_query_timeout_ms = config.get('defaultQueryTimeoutMs')
    transaction_opts = config.get('transactionOpts')
    qr_timeout = config.get('qrTimeout')
    make_signal_repository = config.get('makeSignalRepository')

    public_wam_buffer = BinaryInfo()

    server_time_offset_ms = 0

    uq_tag_id = generate_md_tag_prefix()
    epoch_gen = _epoch()

    def generate_message_tag() -> str:
        return f'{uq_tag_id}{next(epoch_gen)}'

    if print_qr_in_terminal:
        logger.warn(
            {},
            'The printQRInTerminal option has been deprecated. You will no longer receive QR codes in the terminal automatically. '
            'Please listen to the connection.update event yourself and handle the QR your way.',
        )

    if browser[1].lower().find('android') >= 0:
        logger.warn('Using the Android browser is experimental and may lead to unexpected behavior. Use at your own risk.')

    sync_disabled = (
        len([st for st in processable_history_types if config['shouldSyncHistoryMessage']({'syncType': st})])
        == 0
    )
    if sync_disabled:
        logger.warn(
            'DANGER: DISABLING ALL SYNC BY shouldSyncHistoryMsg PREVENTS BAILEYS FROM ACCESSING INITIAL LID MAPPINGS, '
            'LEADING TO INSTABILITY AND SESSION ERRORS'
        )

    parsed = urlparse(wa_web_socket_url)
    if config.get('mobile') or parsed.scheme == 'tcp':
        raise Boom('Mobile API is not supported anymore', status_code=DisconnectReason.loggedOut)

    url = wa_web_socket_url
    creds = (auth_state or {}).get('creds') or {}
    if parsed.scheme == 'wss' and creds.get('routingInfo'):
        routing_b64 = _base64url(creds['routingInfo'])
        sep = '&' if '?' in url else '?'
        url = f'{url}{sep}ED={routing_b64}'

    ephemeral_key_pair = Curve.generate_key_pair()
    noise = make_noise_handler(
        key_pair=ephemeral_key_pair,
        noise_header=NOISE_WA_HEADER,
        logger=logger,
        routing_info=creds.get('routingInfo'),
    )

    ws = WebSocketClient(url, config)
    ws.connect()

    async def send_raw_message(data: bytes) -> None:
        if not ws.is_open:
            raise Boom('Connection Closed', status_code=DisconnectReason.connectionClosed)

        bytes_ = noise.encode_frame(data)
        await promise_timeout(connect_timeout_ms, lambda resolve, reject: _send_frame(resolve, reject, bytes_))

    def _send_frame(resolve, reject, bytes_):
        def cb(err=None):
            if err:
                reject(err)
            else:
                resolve(None)

        ws.send(bytes_, cb)

    async def send_node(frame) -> None:
        if logger.level == 'trace':
            logger.trace({'xml': binary_node_to_string(frame), 'msg': 'xml send'})
        buff = encode_binary_node(frame)
        await send_raw_message(buff)

    async def wait_for_message(msg_id: str, timeout_ms=None):
        timeout_ms = timeout_ms if timeout_ms is not None else default_query_timeout_ms
        result_holder = {}

        def on_recv(data):
            if 'result' not in result_holder:
                result_holder['result'] = data
                ws.off(f'{DEF_TAG_PREFIX}{msg_id}', on_recv)
                ws.off('close', on_err)
                ws.off('error', on_err)

        def on_err(err=None):
            if 'result' not in result_holder:
                result_holder['error'] = err or Boom('Connection Closed', status_code=DisconnectReason.connectionClosed)
                ws.off(f'{DEF_TAG_PREFIX}{msg_id}', on_recv)
                ws.off('close', on_err)
                ws.off('error', on_err)

        ws.on(f'{DEF_TAG_PREFIX}{msg_id}', on_recv)
        ws.on('close', on_err)
        ws.on('error', on_err)

        try:
            try:
                await promise_timeout(timeout_ms, lambda resolve, reject: _await_result(resolve, reject, result_holder))
            except Boom as boom:
                if boom.statusCode == DisconnectReason.timedOut:
                    logger.warn({'msgId': msg_id}, 'timed out waiting for message')
                    return None
                raise
            if 'error' in result_holder:
                raise result_holder['error']
            return result_holder.get('result')
        finally:
            ws.off(f'{DEF_TAG_PREFIX}{msg_id}', on_recv)
            ws.off('close', on_err)
            ws.off('error', on_err)

    def _await_result(resolve, reject, result_holder):
        async def _poll():
            while True:
                if 'error' in result_holder:
                    reject(result_holder['error'])
                    return
                if 'result' in result_holder:
                    resolve(result_holder['result'])
                    return
                await asyncio.sleep(0.01)

        return _poll()

    async def query(node, timeout_ms=None):
        if not node.attrs.get('id'):
            node.attrs['id'] = generate_message_tag()

        msg_id = node.attrs['id']
        result = await promise_timeout(
            timeout_ms,
            lambda resolve, reject: _do_query(resolve, reject, msg_id, node, timeout_ms),
        )

        if result and getattr(result, 'tag', None) is not None:
            assert_node_error_free(result)

        return result

    async def _do_query(resolve, reject, msg_id, node, timeout_ms):
        wait_task = None
        try:
            wait_task = asyncio.ensure_future(wait_for_message(msg_id, timeout_ms))
            await send_node(node)
            result = await wait_task
            resolve(result)
        except Exception as err:
            if wait_task is not None and not wait_task.done():
                wait_task.cancel()
            reject(err)

    async def digest_key_bundle() -> None:
        res = await query(BinaryNode(tag='iq', attrs={'to': S_WHATSAPP_NET, 'type': 'get', 'xmlns': 'encrypt'},
                                     content=[BinaryNode(tag='digest', attrs={}, content=None)]))
        digest_node = get_binary_node_child(res, 'digest')
        if not digest_node:
            await upload_pre_keys()
            raise Error('encrypt/get digest returned no digest node')

    async def rotate_signed_pre_key() -> None:
        new_id = (creds['signedPreKey'].get('keyId') or 0) + 1
        skey = signed_key_pair(creds['signedIdentityKey'], new_id)
        await query(BinaryNode(tag='iq', attrs={'to': S_WHATSAPP_NET, 'type': 'set', 'xmlns': 'encrypt'},
                               content=[BinaryNode(tag='rotate', attrs={}, content=[xmpp_signed_pre_key(skey)])]))
        ev.emit('creds.update', {'signedPreKey': skey})

    async def execute_usync_query(usync_query: USyncQuery):
        if len(usync_query.protocols) == 0:
            raise Boom('USyncQuery must have at least one protocol')

        valid_users = usync_query.users

        user_nodes = []
        for user in valid_users:
            attrs = {}
            if not user.phone:
                attrs['jid'] = user.id
            content = [a.get_user_element(user) for a in usync_query.protocols]
            content = [a for a in content if a is not None]
            user_nodes.append(BinaryNode(tag='user', attrs=attrs, content=content))

        list_node = BinaryNode(tag='list', attrs={}, content=user_nodes)
        query_node = BinaryNode(tag='query', attrs={}, content=[a.get_query_element() for a in usync_query.protocols])

        iq = BinaryNode(tag='iq', attrs={'to': S_WHATSAPP_NET, 'type': 'get', 'xmlns': 'usync'},
                        content=[BinaryNode(tag='usync', attrs={
                            'context': usync_query.context,
                            'mode': usync_query.mode,
                            'sid': generate_message_tag(),
                            'last': 'true',
                            'index': '0',
                        }, content=[query_node, list_node])])

        result = await query(iq)
        return usync_query.parse_usync_query_result(result)

    async def on_whats_app(*phone_numbers):
        usync_query = USyncQuery()
        contact_enabled = False
        for jid in phone_numbers:
            if is_lid_user(jid):
                logger.warn('LIDs are not supported with onWhatsApp')
                continue
            else:
                if not contact_enabled:
                    contact_enabled = True
                    usync_query = usync_query.with_contact_protocol()
                phone = f"+{jid.replace('+', '').split('@')[0].split(':')[0]}"
                usync_query = usync_query.with_user(USyncUser().with_phone(phone))

        if len(usync_query.users) == 0:
            return []

        results = await execute_usync_query(usync_query)
        if results:
            return [{'jid': item['id'], 'exists': bool(item.get('contact'))}
                    for item in results['list'] if item.get('contact')]

    async def pn_from_lid_usync(jids):
        usync_query = USyncQuery().with_lid_protocol().with_context('background')
        for jid in jids:
            if is_lid_user(jid):
                logger.warn('LID user found in LID fetch call')
                continue
            else:
                usync_query = usync_query.with_user(USyncUser().with_id(jid))

        if len(usync_query.users) == 0:
            return []

        results = await execute_usync_query(usync_query)
        if results:
            return [{'pn': item['id'], 'lid': item.get('lid')} for item in results['list'] if item.get('lid')]
        return []

    ev = make_event_buffer(logger)

    creds = (auth_state or {}).get('creds') or {}
    keys = add_transaction_capability((auth_state or {}).get('keys'), logger, transaction_opts)
    signal_repository = make_signal_repository({'creds': creds, 'keys': keys}, logger, pn_from_lid_usync)

    last_date_recv = None
    keep_alive_req = None
    qr_timer = None
    closed = False
    pairing_ready = False
    pairing_in_progress = False
    pending_pairing_resolve = None
    pending_pairing_reject = None

    socket_end_handlers = []

    def on_unexpected_error(err, msg):
        logger.error({'err': err}, f"unexpected error in '{msg}'")

    async def await_next_message(send_msg=None):
        if not ws.is_open:
            raise Boom('Connection Closed', status_code=DisconnectReason.connectionClosed)

        result_holder = {}

        def on_open(data):
            if 'result' not in result_holder:
                result_holder['result'] = data
                ws.off('frame', on_open)
                ws.off('close', on_close)
                ws.off('error', on_close)

        def on_close(err=None):
            if 'result' not in result_holder:
                result_holder['error'] = Boom(
                    f'WebSocket Error ({getattr(err, "message", None) or err})',
                    status_code=get_code_from_ws_error(err),
                    data=err,
                )
                ws.off('frame', on_open)
                ws.off('close', on_close)
                ws.off('error', on_close)

        ws.on('frame', on_open)
        ws.on('close', on_close)
        ws.on('error', on_close)

        if send_msg is not None:
            asyncio.ensure_future(_safe_send_raw(send_msg))

        await promise_timeout(connect_timeout_ms, lambda resolve, reject: _await_result(resolve, reject, result_holder))
        if 'error' in result_holder:
            raise result_holder['error']
        return result_holder.get('result')

    async def _safe_send_raw(data):
        try:
            await send_raw_message(data)
        except Exception:
            pass

    async def validate_connection():
        nonlocal last_date_recv
        hello_msg = proto.HandshakeMessage.from_object({'clientHello': {'ephemeral': ephemeral_key_pair['public']}})

        logger.info({'browser': browser, 'helloMsg': hello_msg}, 'connected to WA')

        init = proto.HandshakeMessage.encode(hello_msg)

        result = await await_next_message(init)
        handshake = proto.HandshakeMessage.decode(result)

        logger.trace({'handshake': handshake}, 'handshake recv from WA')

        server_hello = getattr(handshake, 'serverHello', None)
        if server_hello is None:
            raise Boom('Invalid server hello in handshake', status_code=400)
        key_enc = noise.process_handshake(server_hello, creds.get('noiseKey'))

        if not creds.get('me'):
            node = generate_registration_node(creds, config)
            logger.info({'node': node}, 'not logged in, attempting registration...')
        else:
            node = generate_login_node(creds['me']['id'], config)
            logger.info({'node': node}, 'logging in...')

        payload_enc = noise.encrypt(proto.ClientPayload.encode(node))
        await send_raw_message(
            proto.HandshakeMessage.encode({
                'clientFinish': {
                    'static': key_enc,
                    'payload': payload_enc,
                }
            })
        )
        await noise.finish_init()
        start_keep_alive_request()
        last_date_recv = None

    async def get_available_pre_keys_on_server():
        result = await query(BinaryNode(tag='iq', attrs={
            'id': generate_message_tag(), 'xmlns': 'encrypt', 'type': 'get', 'to': S_WHATSAPP_NET,
        }, content=[BinaryNode(tag='count', attrs={}, content=None)]))
        count_child = get_binary_node_child(result, 'count')
        return int(count_child.attrs['value'])

    upload_pre_keys_promise = None

    async def upload_pre_keys(count=MIN_PREKEY_COUNT):
        nonlocal upload_pre_keys_promise
        if upload_pre_keys_promise:
            logger.debug('Pre-key upload already in progress, waiting for completion')
            await upload_pre_keys_promise
            return

        async def upload_logic(retry_count):
            logger.info({'count': count, 'retryCount': retry_count}, 'uploading pre-keys')

            async def gen_node():
                logger.debug({'requestedCount': count}, 'generating pre-keys with requested count')
                result = await get_next_pre_keys_node({'creds': creds, 'keys': keys}, count)
                ev.emit('creds.update', result['update'])
                return result['node']

            async def _tx():
                return await _run_in_transaction(keys, gen_node, (creds.get('me') or {}).get('id') or 'upload-pre-keys')

            node = await _tx()

            try:
                await query(node)
                logger.info({'count': count}, 'uploaded pre-keys successfully')
            except Exception as upload_error:
                logger.error({'uploadError': str(upload_error), 'count': count}, 'Failed to upload pre-keys to server')
                if retry_count < 3:
                    backoff_delay = min(1000 * (2 ** retry_count), 10000)
                    logger.info(f'Retrying pre-key upload in {backoff_delay}ms')
                    await asyncio.sleep(backoff_delay / 1000.0)
                    return await upload_logic(retry_count + 1)
                raise upload_error

        async def _timeout_watch():
            await asyncio.sleep(UPLOAD_TIMEOUT / 1000.0)
            raise Boom('Pre-key upload timeout', status_code=408)

        async def _race():
            main_task = asyncio.ensure_future(upload_logic(0))
            timeout_task = asyncio.ensure_future(_timeout_watch())
            try:
                done, _ = await asyncio.wait({main_task, timeout_task}, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    exc = task.exception()
                    if exc is not None:
                        raise exc
            finally:
                for task in (main_task, timeout_task):
                    if not task.done():
                        task.cancel()

        upload_pre_keys_promise = asyncio.ensure_future(_race())
        try:
            await upload_pre_keys_promise
        finally:
            upload_pre_keys_promise = None

    async def _run_in_transaction(tx_keys, work, key):
        return await tx_keys['transaction'](work, key)

    async def verify_current_pre_key_exists():
        current_pre_key_id = creds.get('nextPreKeyId', 0) - 1
        if current_pre_key_id <= 0:
            return {'exists': False, 'currentPreKeyId': 0}
        pre_keys = await keys['get']('pre-key', [str(current_pre_key_id)])
        exists = str(current_pre_key_id) in (pre_keys or {})
        return {'exists': exists, 'currentPreKeyId': current_pre_key_id}

    async def upload_pre_keys_to_server_if_required():
        try:
            count = 0
            pre_key_count = await get_available_pre_keys_on_server()
            if pre_key_count == 0:
                count = INITIAL_PREKEY_COUNT
            elif pre_key_count < MIN_PREKEY_COUNT:
                count = MIN_PREKEY_COUNT

            should_upload = False
            missing_current_pre_key = False
            if count > 0:
                should_upload = True
            else:
                result = await verify_current_pre_key_exists()
                if result['currentPreKeyId'] > 0 and not result['exists']:
                    missing_current_pre_key = True
                    should_upload = True

            if should_upload:
                reasons = []
                if count > 0:
                    reasons.append(f'server count low ({pre_key_count})')
                if missing_current_pre_key:
                    reasons.append(f'current prekey {result["currentPreKeyId"]} missing from storage')
                logger.info(f'Uploading PreKeys due to: {", ".join(reasons)}')
                await upload_pre_keys(count)
            else:
                logger.info('PreKey validation passed')
        except Exception as error:
            logger.error({'error': error}, 'Failed to check/upload pre-keys during initialization')

    async def on_message_received(data: bytes):
        nonlocal last_date_recv
        await noise.decode_frame(data, lambda frame: _process_frame(frame))

    def _process_frame(frame):
        nonlocal last_date_recv
        last_date_recv = time.time()
        any_triggered = ws.emit('frame', frame)
        if not isinstance(frame, bytes):
            msg_id = (frame.attrs or {}).get('id')
            if logger.level == 'trace':
                logger.trace({'xml': binary_node_to_string(frame), 'msg': 'recv xml'})

            any_triggered = ws.emit(f'{DEF_TAG_PREFIX}{msg_id}', frame) or any_triggered

            l0 = frame.tag
            l1 = frame.attrs or {}
            l2 = ''
            if isinstance(frame.content, list) and frame.content:
                l2 = frame.content[0].tag if getattr(frame.content[0], 'tag', None) else ''

            for key in l1:
                any_triggered = ws.emit(f'{DEF_CALLBACK_PREFIX}{l0},{key}:{l1[key]},{l2}', frame) or any_triggered
                any_triggered = ws.emit(f'{DEF_CALLBACK_PREFIX}{l0},{key}:{l1[key]}', frame) or any_triggered
                any_triggered = ws.emit(f'{DEF_CALLBACK_PREFIX}{l0},{key}', frame) or any_triggered

            any_triggered = ws.emit(f'{DEF_CALLBACK_PREFIX}{l0},,{l2}', frame) or any_triggered
            any_triggered = ws.emit(f'{DEF_CALLBACK_PREFIX}{l0}', frame) or any_triggered

            if not any_triggered and logger.level == 'debug':
                logger.debug({'unhandled': True, 'msgId': msg_id, 'fromMe': False, 'frame': frame}, 'communication recv')

    async def end(error=None):
        nonlocal closed, pairing_ready, pairing_in_progress, pending_pairing_resolve, pending_pairing_reject
        if closed:
            logger.trace({'trace': getattr(error, 'stack', None)}, 'connection already closed')
            return

        closed = True
        logger.info({'trace': getattr(error, 'stack', None)}, 'connection errored' if error else 'connection closed')

        if keep_alive_req is not None:
            keep_alive_req.cancel()
        if qr_timer is not None:
            qr_timer.cancel()

        if pending_pairing_reject is not None:
            pending_pairing_reject(
                error or Boom('Connection closed before pairing completed', status_code=DisconnectReason.connectionClosed)
            )
            pending_pairing_resolve = None
            pending_pairing_reject = None

        pairing_ready = False
        pairing_in_progress = False

        ws.remove_all_listeners('close')
        ws.remove_all_listeners('open')
        ws.remove_all_listeners('message')

        if callable(getattr(signal_repository, 'close', None)):
            signal_repository['close']()

        if not ws.is_closed and not ws.is_closing:
            try:
                await ws.close()
            except Exception:
                pass

        for handler in socket_end_handlers:
            try:
                result = handler(error)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as err:
                logger.error({'err': err}, 'error in socket end handler')

        ev.emit('connection.update', {
            'connection': 'close',
            'lastDisconnect': {'error': error, 'date': time.time()},
        })
        ev.remove_all_listeners('connection.update')
        ev.destroy()

    async def wait_for_socket_open():
        if ws.is_open:
            return
        if ws.is_closed or ws.is_closing:
            raise Boom('Connection Closed', status_code=DisconnectReason.connectionClosed)

        result_holder = {}

        def on_open():
            if 'done' not in result_holder:
                result_holder['done'] = True
                ws.off('open', on_open)
                ws.off('close', on_close)
                ws.off('error', on_close)

        def on_close(err=None):
            if 'done' not in result_holder:
                result_holder['done'] = True
                result_holder['error'] = Boom(
                    f'WebSocket Error ({getattr(err, "message", None) or err})',
                    status_code=get_code_from_ws_error(err),
                    data=err,
                )
                ws.off('open', on_open)
                ws.off('close', on_close)
                ws.off('error', on_close)

        ws.on('open', on_open)
        ws.on('close', on_close)
        ws.on('error', on_close)

        while 'done' not in result_holder:
            await asyncio.sleep(0.01)
        if 'error' in result_holder:
            raise result_holder['error']

    def start_keep_alive_request():
        nonlocal keep_alive_req

        async def _keep_alive():
            nonlocal last_date_recv
            while True:
                await asyncio.sleep(keep_alive_interval_ms / 1000.0)
                if last_date_recv is None:
                    last_date_recv = time.time()
                diff = (time.time() - last_date_recv) * 1000
                if diff > keep_alive_interval_ms + 5000:
                    asyncio.ensure_future(end(Boom('Connection was lost', status_code=DisconnectReason.connectionLost)))
                elif ws.is_open:
                    async def _ping():
                        try:
                            await query(BinaryNode(tag='iq', attrs={
                                'id': generate_message_tag(), 'to': S_WHATSAPP_NET, 'type': 'get', 'xmlns': 'w:p',
                            }, content=[BinaryNode(tag='ping', attrs={}, content=None)]))
                        except Exception as err:
                            logger.error({'trace': getattr(err, 'stack', None)}, 'error in sending keep alive')

                    asyncio.ensure_future(_ping())
                else:
                    logger.warn('keep alive called when WS not open')

        keep_alive_req = asyncio.ensure_future(_keep_alive())

    async def send_passive_iq(tag):
        return await query(BinaryNode(tag='iq', attrs={
            'to': S_WHATSAPP_NET, 'xmlns': 'passive', 'type': 'set',
        }, content=[BinaryNode(tag=tag, attrs={}, content=None)]))

    async def logout(msg=None):
        jid = (creds.get('me') or {}).get('id')
        if jid:
            await send_node(BinaryNode(tag='iq', attrs={
                'to': S_WHATSAPP_NET, 'type': 'set', 'id': generate_message_tag(), 'xmlns': 'md',
            }, content=[BinaryNode(tag='remove-companion-device', attrs={'jid': jid, 'reason': 'user_initiated'}, content=None)]))
        asyncio.ensure_future(end(Boom(msg or 'Intentional Logout', status_code=DisconnectReason.loggedOut)))

    async def send_pairing_code_request(phone_number: str, custom_pairing_code=None):
        nonlocal pending_pairing_resolve, pending_pairing_reject
        pairing_code = custom_pairing_code if custom_pairing_code is not None else bytes_to_crockford(os.urandom(5))

        if custom_pairing_code is not None and len(custom_pairing_code) != 8:
            raise Error('Custom pairing code must be exactly 8 chars')

        auth_state['creds']['pairingCode'] = pairing_code

        jid = jid_encode(phone_number, 's.whatsapp.net')
        pairing_platform = get_pairing_code_platform(browser)

        try:
            result = await query(BinaryNode(tag='iq', attrs={
                'to': S_WHATSAPP_NET, 'type': 'set', 'id': generate_message_tag(), 'xmlns': 'md',
            }, content=[BinaryNode(tag='link_code_companion_reg', attrs={
                'jid': jid,
                'stage': 'companion_hello',
                'should_show_push_notification': 'true',
            }, content=[
                BinaryNode(tag='link_code_pairing_wrapped_companion_ephemeral_pub', attrs={}, content=await generate_pairing_key()),
                BinaryNode(tag='companion_server_auth_key_pub', attrs={}, content=auth_state['creds']['noiseKey']['public']),
                BinaryNode(tag='companion_platform_id', attrs={}, content=pairing_platform['id']),
                BinaryNode(tag='companion_platform_display', attrs={}, content=pairing_platform['display']),
                BinaryNode(tag='link_code_pairing_nonce', attrs={}, content='0'),
            ])]))

            if not result:
                raise Boom('Timed out waiting for pairing code response', status_code=DisconnectReason.timedOut)
        except Exception as error:
            if auth_state['creds'].get('pairingCode') == pairing_code:
                auth_state['creds']['pairingCode'] = None
            raise error

        auth_state['creds']['me'] = {'id': jid, 'name': '~'}
        ev.emit('creds.update', auth_state['creds'])

        return pairing_code

    async def request_pairing_code(phone_number: str, custom_pairing_code=None):
        nonlocal pairing_in_progress
        if custom_pairing_code is not None and len(custom_pairing_code) != 8:
            raise Error('Custom pairing code must be exactly 8 chars')

        if pairing_in_progress:
            raise Boom('A pairing request is already in progress', status_code=400)

        pairing_in_progress = True

        try:
            if not pairing_ready:
                logger.debug('pairing not ready yet, queuing request until pair-device is received')
                await _wait_for_pairing_ready()
            return await send_pairing_code_request(phone_number, custom_pairing_code)
        finally:
            pairing_in_progress = False

    async def _wait_for_pairing_ready():
        nonlocal pending_pairing_resolve, pending_pairing_reject
        done = asyncio.get_event_loop().create_future()

        def resolve():
            nonlocal pending_pairing_resolve, pending_pairing_reject
            pending_pairing_resolve = None
            pending_pairing_reject = None
            if not done.done():
                done.set_result(None)

        def reject(err):
            nonlocal pending_pairing_resolve, pending_pairing_reject
            pending_pairing_resolve = None
            pending_pairing_reject = None
            if not done.done():
                done.set_exception(err)

        pending_pairing_resolve = resolve
        pending_pairing_reject = reject
        await done

    async def generate_pairing_key():
        salt = os.urandom(32)
        random_iv = os.urandom(16)
        key = derive_pairing_code_key(auth_state['creds']['pairingCode'], salt)
        ciphered = aes_encrypt_ctr(auth_state['creds']['pairingEphemeralKeyPair']['public'], key, random_iv)
        return b''.join([salt, random_iv, ciphered])

    async def send_wam_buffer(wam_buffer: bytes):
        return await query(BinaryNode(tag='iq', attrs={
            'to': S_WHATSAPP_NET, 'id': generate_message_tag(), 'xmlns': 'w:stats',
        }, content=[BinaryNode(tag='add', attrs={'t': str(int(time.time()))}, content=wam_buffer)]))

    ws.on('message', lambda data: asyncio.ensure_future(on_message_received(data)))

    ws.on('open', lambda: asyncio.ensure_future(_on_open()))

    async def _on_open():
        try:
            await validate_connection()
        except Exception as err:
            logger.error({'err': err}, 'error in validating connection')
            asyncio.ensure_future(end(err))

    ws.on('error', map_web_socket_error(lambda err: asyncio.ensure_future(end(err))))
    ws.on('close', lambda err: asyncio.ensure_future(end(Boom('Connection Terminated', status_code=DisconnectReason.connectionClosed))))

    ws.on('CB:xmlstreamend', lambda node: asyncio.ensure_future(
        end(Boom('Connection Terminated by Server', status_code=DisconnectReason.connectionClosed))))

    ws.on('CB:iq,type:set,pair-device', lambda stanza: asyncio.ensure_future(_on_pair_device(stanza)))

    async def _on_pair_device(stanza):
        nonlocal pairing_ready, pending_pairing_resolve, pending_pairing_reject
        iq = BinaryNode(tag='iq', attrs={'to': S_WHATSAPP_NET, 'type': 'result', 'id': stanza.attrs.get('id')}, content=None)
        await send_node(iq)

        pairing_ready = True
        if pending_pairing_resolve is not None:
            logger.debug('pair-device received, flushing queued pairing request')
            resolve = pending_pairing_resolve
            pending_pairing_resolve = None
            pending_pairing_reject = None
            resolve()

        pair_device_node = get_binary_node_child(stanza, 'pair-device')
        ref_nodes = get_binary_node_children(pair_device_node, 'ref')
        noise_key_b64 = _b64encode(creds['noiseKey']['public'])
        identity_key_b64 = _b64encode(creds['signedIdentityKey']['public'])
        adv_b64 = creds['advSecretKey']

        qr_ms = qr_timeout or 60_000

        async def gen_pair_qr():
            if not ws.is_open:
                return
            if not ref_nodes:
                asyncio.ensure_future(end(Boom('QR refs attempts ended', status_code=DisconnectReason.timedOut)))
                return
            ref_node = ref_nodes.pop(0)
            ref = ref_node.content.decode('utf-8') if isinstance(ref_node.content, bytes) else str(ref_node.content)
            qr = build_pairing_qr_data(ref, noise_key_b64, identity_key_b64, adv_b64, browser)
            ev.emit('connection.update', {'qr': qr})
            nonlocal qr_timer
            qr_timer = asyncio.get_event_loop().call_later(qr_ms / 1000.0, lambda: asyncio.ensure_future(gen_pair_qr()))

        asyncio.ensure_future(gen_pair_qr())

    ws.on('CB:iq,,pair-success', lambda stanza: asyncio.ensure_future(_on_pair_success(stanza)))

    async def _on_pair_success(stanza):
        logger.debug('pair success recv')
        try:
            update_server_time_offset(stanza)
            result = configure_successful_pairing(stanza, creds)
            reply, updated_creds = result['reply'], result['creds']

            logger.info({'me': updated_creds['me'], 'platform': updated_creds['platform']},
                        'pairing configured successfully, expect to restart the connection...')

            ev.emit('creds.update', updated_creds)
            ev.emit('connection.update', {'isNewLogin': True, 'qr': None})

            await send_node(reply)
            asyncio.ensure_future(send_unified_session())
        except Exception as error:
            logger.info({'trace': getattr(error, 'stack', None)}, 'error in pairing')
            asyncio.ensure_future(end(error))

    ws.on('CB:notification,type:link_code_companion_reg', lambda node: asyncio.ensure_future(_on_link_code_companion_reg(node)))

    def _to_required_buffer(data) -> bytes:
        if data is None:
            raise Boom('Invalid buffer', status_code=400)
        return bytes(data)

    async def _on_link_code_companion_reg(node):
        try:
            link_code_companion_reg = get_binary_node_child(node, 'link_code_companion_reg')
            ref = _to_required_buffer(get_binary_node_child_buffer(link_code_companion_reg, 'link_code_pairing_ref'))
            primary_identity_public_key = _to_required_buffer(
                get_binary_node_child_buffer(link_code_companion_reg, 'primary_identity_pub')
            )
            primary_ephemeral_public_key_wrapped = _to_required_buffer(
                get_binary_node_child_buffer(link_code_companion_reg, 'link_code_pairing_wrapped_primary_ephemeral_pub')
            )
            code_pairing_public_key = decipher_link_public_key(primary_ephemeral_public_key_wrapped)
            companion_shared_key = Curve.shared_key(
                creds['pairingEphemeralKeyPair']['private'],
                code_pairing_public_key,
            )
            random = os.urandom(32)
            link_code_salt = os.urandom(32)
            link_code_pairing_expanded = hkdf(companion_shared_key, 32, b'link_code_pairing_key_bundle_encryption_key', link_code_salt)
            encrypt_payload = bytes(creds['signedIdentityKey']['public']) + bytes(primary_identity_public_key) + random
            encrypt_iv = os.urandom(12)
            encrypted = aes_gcm_encrypt(encrypt_payload, link_code_pairing_expanded, encrypt_iv, b'')
            encrypted_payload = link_code_salt + encrypt_iv + encrypted
            identity_shared_key = Curve.shared_key(creds['signedIdentityKey']['private'], primary_identity_public_key)
            identity_payload = companion_shared_key + identity_shared_key + random
            creds['advSecretKey'] = base64.b64encode(hkdf(identity_payload, 32, b'adv_secret')).decode('utf-8')
            await query(BinaryNode(tag='iq', attrs={
                'to': S_WHATSAPP_NET,
                'type': 'set',
                'id': generate_message_tag(),
                'xmlns': 'md',
            }, content=[BinaryNode(tag='link_code_companion_reg', attrs={
                'jid': creds['me']['id'],
                'stage': 'companion_finish',
            }, content=[
                BinaryNode(tag='link_code_pairing_wrapped_key_bundle', attrs={}, content=encrypted_payload),
                BinaryNode(tag='companion_identity_public', attrs={}, content=creds['signedIdentityKey']['public']),
                BinaryNode(tag='link_code_pairing_ref', attrs={}, content=ref),
            ])]))
            creds['registered'] = True
            ev.emit('creds.update', creds)
        except Exception as err:
            logger.error({'err': err}, 'error in link_code_companion_reg')

    def decipher_link_public_key(data: bytes) -> bytes:
        buffer = _to_required_buffer(data)
        salt = buffer[:32]
        secret_key = derive_pairing_code_key(creds['pairingCode'], salt)
        iv = buffer[32:48]
        payload = buffer[48:80]
        return aes_decrypt_ctr(payload, secret_key, iv)

    ws.on('CB:success', lambda node: asyncio.ensure_future(_on_success(node)))

    async def _on_success(node):
        try:
            update_server_time_offset(node)
            await upload_pre_keys_to_server_if_required()
            await send_passive_iq('active')
            try:
                await digest_key_bundle()
            except Exception as e:
                logger.warn({'e': e}, 'failed to run digest after login')
        except Exception as err:
            logger.warn({'err': err}, 'failed to send initial passive iq')

        logger.info('opened connection to WA')
        if qr_timer is not None:
            qr_timer.cancel()

        ev.emit('creds.update', {'me': {**creds.get('me', {}), 'lid': node.attrs.get('lid')}})
        ev.emit('connection.update', {'connection': 'open'})
        asyncio.ensure_future(send_unified_session())

        my_lid = node.attrs.get('lid')
        if my_lid and (creds.get('me') or {}).get('id'):
            async def _init_own_lid():
                try:
                    my_pn = creds['me']['id']
                    await signal_repository['lidMapping'].store_lidpn_mappings([{'lid': my_lid, 'pn': my_pn}])
                    decoded = jid_decode(my_pn)
                    user = decoded.user
                    device = decoded.device
                    await keys['set']({'device-list': {user: [str(device) if device else '0']}})
                    await signal_repository['migrateSession'](my_pn, my_lid)
                    logger.info({'myPN': my_pn, 'myLID': my_lid}, 'Own LID session created successfully')
                except Exception as error:
                    logger.error({'error': error, 'lid': my_lid}, 'Failed to create own LID session')

            loop = asyncio.get_event_loop()
            loop.call_soon(lambda: asyncio.ensure_future(_init_own_lid()))

    ws.on('CB:stream:error', lambda node: asyncio.ensure_future(_on_stream_error(node)))

    def _on_stream_error(node):
        reason_node_list = get_all_binary_node_children(node)
        reason_node = reason_node_list[0] if reason_node_list else None
        logger.error({'reasonNode': reason_node, 'fullErrorNode': node}, 'stream errored out')
        result = get_error_code_from_stream_error(node)
        reason, status_code = result['reason'], result['statusCode']
        asyncio.ensure_future(end(Boom(f'Stream Errored ({reason})', status_code=status_code, data=reason_node or node)))

    ws.on('CB:failure', lambda node: _on_failure(node))

    def _on_failure(node):
        reason = int((node.attrs or {}).get('reason') or 500)
        asyncio.ensure_future(end(Boom('Connection Failure', status_code=reason, data=node.attrs)))
    ws.on('CB:ib,,downgrade_webclient', lambda node: asyncio.ensure_future(
        end(Boom('Multi-device beta not joined', status_code=DisconnectReason.multideviceMismatch))))

    ws.on('CB:ib,,offline_preview', lambda node: asyncio.ensure_future(_on_offline_preview(node)))

    async def _on_offline_preview(node):
        logger.info('offline preview received', json_dumps(node))
        await send_node(BinaryNode(tag='ib', attrs={}, content=[BinaryNode(tag='offline_batch', attrs={'count': '100'}, content=None)]))

    ws.on('CB:ib,,edge_routing', lambda node: asyncio.ensure_future(_on_edge_routing(node)))

    def _on_edge_routing(node):
        edge_routing_node = get_binary_node_child(node, 'edge_routing')
        routing_info = get_binary_node_child(edge_routing_node, 'routing_info')
        if routing_info is not None and routing_info.content is not None:
            auth_state['creds']['routingInfo'] = bytes(routing_info.content)
            ev.emit('creds.update', auth_state['creds'])

    did_start_buffer = False

    def _initial_setup():
        nonlocal did_start_buffer
        if (creds.get('me') or {}).get('id'):
            ev.buffer()
            did_start_buffer = True
        ev.emit('connection.update', {'connection': 'connecting', 'receivedPendingNotifications': False, 'qr': None})

    asyncio.get_event_loop().call_soon(_initial_setup)

    ws.on('CB:ib,,offline', lambda node: asyncio.ensure_future(_on_offline(node)))

    def _on_offline(node):
        nonlocal did_start_buffer
        child = get_binary_node_child(node, 'offline')
        offline_notifs = int((child.attrs or {}).get('count') or 0) if child else 0
        logger.info(f'handled {offline_notifs} offline messages/notifications')
        if did_start_buffer:
            ev.flush()
            logger.trace('flushed events for initial buffer')
        ev.emit('connection.update', {'receivedPendingNotifications': True})

    def _on_creds_update(update):
        name = (update.get('me') or {}).get('name')
        if (creds.get('me') or {}).get('name') != name:
            logger.debug({'name': name}, 'updated pushName')
            if name is not None:
                async def _send_presence():
                    try:
                        await send_node(BinaryNode(tag='presence', attrs={'name': name}, content=None))
                    except Exception as err:
                        logger.warn({'trace': getattr(err, 'stack', None)}, 'error in sending presence update on name change')

                asyncio.ensure_future(_send_presence())
        creds.update(update)

    ev.on('creds.update', _on_creds_update)

    def update_server_time_offset(node):
        nonlocal server_time_offset_ms
        attrs = getattr(node, 'attrs', None) or {}
        t_value = attrs.get('t')
        if not t_value:
            return
        try:
            parsed = float(t_value)
        except (TypeError, ValueError):
            return
        if parsed != parsed or parsed <= 0:
            return
        server_time_offset_ms = int(parsed * 1000 - time.time() * 1000)
        logger.debug({'offset': server_time_offset_ms}, 'calculated server time offset')

    def get_unified_session_id():
        offset_ms = 3 * TimeMs['Day']
        now = time.time() * 1000 + server_time_offset_ms
        session_id = (now + offset_ms) % TimeMs['Week']
        return str(int(session_id))

    async def send_unified_session():
        if not ws.is_open:
            return
        node = BinaryNode(tag='ib', attrs={}, content=[BinaryNode(tag='unified_session', attrs={'id': get_unified_session_id()}, content=None)])
        try:
            await send_node(node)
        except Exception as error:
            logger.debug({'error': error}, 'failed to send unified_session telemetry')

    def register_socket_end_handler(handler):
        socket_end_handlers.append(handler)

    async def fetch_account_reachout_timelock():
        query_result = await execute_wmex_query(
            {}, QueryIds.REACHOUT_TIMELOCK, XWAPaths.xwa2_fetch_account_reachout_timelock, query, generate_message_tag
        )
        result = {
            'isActive': bool((query_result or {}).get('is_active')),
            'timeEnforcementEnds': (
                _parse_ts((query_result or {}).get('time_enforcement_ends'))
                if (query_result or {}).get('time_enforcement_ends')
                else None
            ),
            'enforcementType': (query_result or {}).get('enforcement_type') or ReachoutTimelockEnforcementType.DEFAULT,
        }
        ev.emit('connection.update', {'reachoutTimeLock': result})
        return result

    async def fetch_new_chat_message_cap():
        return await execute_wmex_query(
            {'input': {'type': 'INDIVIDUAL_NEW_CHAT_MSG'}},
            QueryIds.MESSAGE_CAPPING_INFO,
            XWAPaths.xwa2_message_capping_info,
            query,
            generate_message_tag,
        )

    message_mutex = make_mutex()

    async def upsert_message(msg: dict, type_: str) -> None:
        ev.emit('messages.upsert', {'messages': [msg], 'type': type_})

    privacy_settings_cache = {}

    async def fetch_privacy_settings(force=False) -> dict:
        if not privacy_settings_cache or force:
            result = await query(
                BinaryNode(
                    tag='iq',
                    attrs={'xmlns': 'privacy', 'to': S_WHATSAPP_NET, 'type': 'get'},
                    content=[BinaryNode(tag='privacy', attrs={})],
                )
            )
            content = result.content or []
            privacy_settings_cache.update(reduce_binary_node_to_dictionary(content[0], 'category') if content else {})
        return dict(privacy_settings_cache)

    async def group_metadata(jid: str) -> dict:
        from .messages_recv import extract_group_metadata

        result = await query(
            BinaryNode(
                tag='iq',
                attrs={'type': 'get', 'xmlns': 'w:g2', 'to': jid},
                content=[BinaryNode(tag='query', attrs={'request': 'interactive'})],
            )
        )
        return extract_group_metadata(result)

    async def group_toggle_ephemeral(jid: str, ephemeral_expiration) -> None:
        content = (
            BinaryNode(tag='ephemeral', attrs={'expiration': str(ephemeral_expiration)})
            if ephemeral_expiration
            else BinaryNode(tag='not_ephemeral', attrs={})
        )
        await query(
            BinaryNode(
                tag='iq',
                attrs={'type': 'set', 'xmlns': 'w:g2', 'to': jid},
                content=[content],
            )
        )

    result = {
        'type': 'md',
        'ws': ws,
        'ev': ev,
        'authState': {'creds': creds, 'keys': keys},
        'signalRepository': signal_repository,
        'user': lambda: creds.get('me'),
        'generateMessageTag': generate_message_tag,
        'query': query,
        'waitForMessage': wait_for_message,
        'waitForSocketOpen': wait_for_socket_open,
        'sendRawMessage': send_raw_message,
        'sendNode': send_node,
        'logout': logout,
        'end': end,
        'registerSocketEndHandler': register_socket_end_handler,
        'onUnexpectedError': on_unexpected_error,
        'uploadPreKeys': upload_pre_keys,
        'uploadPreKeysToServerIfRequired': upload_pre_keys_to_server_if_required,
        'digestKeyBundle': digest_key_bundle,
        'rotateSignedPreKey': rotate_signed_pre_key,
        'requestPairingCode': request_pairing_code,
        'updateServerTimeOffset': update_server_time_offset,
        'sendUnifiedSession': send_unified_session,
        'wamBuffer': public_wam_buffer,
        'waitForConnectionUpdate': bind_wait_for_connection_update(ev),
        'sendWAMBuffer': send_wam_buffer,
        'executeUSyncQuery': execute_usync_query,
        'onWhatsApp': on_whats_app,
        'fetchAccountReachoutTimelock': fetch_account_reachout_timelock,
        'fetchNewChatMessageCap': fetch_new_chat_message_cap,
        'messageMutex': message_mutex,
        'upsertMessage': upsert_message,
        'fetchPrivacySettings': fetch_privacy_settings,
        'groupMetadata': group_metadata,
        'groupToggleEphemeral': group_toggle_ephemeral,
    }

    from .messages_recv import make_messages_recv_socket

    return make_messages_recv_socket(result, config)


class Error(Exception):
    pass


def _base64url(data: bytes) -> str:
    import base64

    return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')


def _b64encode(data: bytes) -> str:
    import base64

    return base64.b64encode(data).decode('ascii')


def _parse_ts(value) -> float:
    try:
        return float(value) * 1000
    except (TypeError, ValueError):
        return None


def json_dumps(obj) -> str:
    import json

    return json.dumps(obj, default=str)
