"""Port of src/Utils/messages.ts — message content helpers and WAMessage generation.

Media download lives in messages_media.py; message relaying in
Socket/messages_send.py.
"""

from __future__ import annotations

import random
import re
from datetime import datetime

from ..Defaults.index import CALL_AUDIO_PREFIX, CALL_VIDEO_PREFIX, WA_DEFAULT_EPHEMERAL
from ..WAProto import WAProto as proto
from ..WABinary.jid_utils import is_jid_group, is_jid_newsletter, is_jid_status_broadcast, jid_normalized_user
from .crypto import sha256
from .generics import Boom, generate_message_id_v2, get_key_author, unix_timestamp_seconds
from .reporting_utils import should_include_reporting_token

URL_REGEX = re.compile(
    r'https?://[\w-]+(?:\.[\w-]+)+(?:/[\w\-._~:/?#[\]@!$&\'()*+,;=%]*)?', re.IGNORECASE
)

MIMETYPE_MAP = {
    'image': 'image/jpeg',
    'video': 'video/mp4',
    'document': 'application/pdf',
    'audio': 'audio/ogg; codecs=opus',
    'sticker': 'image/webp',
    'product-catalog-image': 'image/jpeg',
}

MESSAGE_TYPE_PROTO = {
    'image': proto.Message.ImageMessage,
    'video': proto.Message.VideoMessage,
    'audio': proto.Message.AudioMessage,
    'sticker': proto.Message.StickerMessage,
    'document': proto.Message.DocumentMessage,
}


def get_content_type(content):
    """Return the first key of the message content (TS getContentType)."""
    if content is None:
        return None
    if isinstance(content, proto.Message):
        content = _message_to_plain_dict(content)
    keys = [k for k in content if content.get(k) is not None]
    key = next(
        (k for k in keys if (k == 'conversation' or 'Message' in k) and k != 'senderKeyDistributionMessage'),
        None,
    )
    return key


def _message_to_plain_dict(msg) -> dict:
    out = {}
    for name in getattr(msg, 'FIELDS', {}):
        value = getattr(msg, name, None)
        if value is not None:
            out[name] = _proto_value_to_plain(value)
    return out


def _proto_value_to_plain(value):
    from ..WAProto.runtime import Message as _ProtoBase

    if isinstance(value, _ProtoBase):
        return _message_to_plain_dict(value)
    if isinstance(value, list):
        return [_proto_value_to_plain(v) for v in value]
    if isinstance(value, bytes):
        return value
    if isinstance(value, int) and hasattr(value, 'name') and type(value).__name__.endswith('Enum'):
        return int(value)
    return value


def normalize_message_content(content):
    """Mirror TS normalizeMessageContent: unwrap ephemeral/view-once messages."""
    if content is None:
        return None

    if isinstance(content, proto.Message):
        content = _message_to_plain_dict(content)

    def get_future_proof_message(message):
        if isinstance(message, proto.Message):
            message = _message_to_plain_dict(message)
        for key in (
            'ephemeralMessage',
            'viewOnceMessage',
            'documentWithCaptionMessage',
            'viewOnceMessageV2',
            'viewOnceMessageV2Extension',
            'editedMessage',
            'associatedChildMessage',
            'groupStatusMessage',
            'groupStatusMessageV2',
        ):
            inner = (message or {}).get(key)
            if inner is not None:
                return inner
        return None

    for _ in range(5):
        inner = get_future_proof_message(content)
        if not inner:
            break
        content = inner.get('message')

    return content


def extract_url_from_text(text: str) -> str | None:
    m = URL_REGEX.search(text or '')
    return m.group(0) if m else None


async def generate_link_preview_if_required(text, get_url_info, logger):
    url = extract_url_from_text(text)
    if get_url_info and url:
        try:
            return await get_url_info(url)
        except Exception as error:
            if logger is not None:
                logger.warn({'trace': getattr(error, 'stack', None)}, 'url generation failed')
    return None


def assert_color(color):
    if isinstance(color, int):
        return color if color > 0 else 0xFFFFFFFF + color + 1
    if color is None:
        return None
    hex_str = str(color).strip().replace('#', '')
    if len(hex_str) <= 6:
        hex_str = 'FF' + hex_str.rjust(6, '0')
    return int(hex_str, 16)


def has_non_nullish_property(message, key):
    return (
        isinstance(message, dict)
        and message is not None
        and key in message
        and message[key] is not None
    )


def has_optional_property(obj, key):
    return isinstance(obj, dict) and obj is not None and key in obj and obj[key] is not None


async def prepare_wa_message_media(message, options):
    logger = options.get('logger')
    from ..Defaults.index import MEDIA_KEYS
    from .messages_media import (
        encrypted_stream,
        generate_thumbnail,
        get_audio_duration,
        get_audio_waveform,
        get_raw_media_upload_data,
    )

    media_type = None
    for key in MEDIA_KEYS:
        if key in message:
            media_type = key

    if not media_type:
        raise Boom('Invalid media type', status_code=400)

    upload_data = dict(message)
    upload_data['media'] = upload_data.pop(media_type)
    # check if cacheable + generate cache key
    cacheable_key = (
        isinstance(upload_data.get('media'), dict)
        and 'url' in upload_data['media']
        and bool(upload_data['media']['url'])
        and bool(options.get('mediaCache'))
    )
    if cacheable_key:
        cacheable_key = media_type + ':' + str(upload_data['media']['url'])

    if media_type == 'document' and not upload_data.get('fileName'):
        upload_data['fileName'] = 'file'

    if not upload_data.get('mimetype'):
        upload_data['mimetype'] = MIMETYPE_MAP.get(media_type)

    if cacheable_key and options.get('mediaCache'):
        media_buff = await options['mediaCache'].get(cacheable_key)
        if media_buff is not None:
            if logger is not None:
                logger.debug({'cacheableKey': cacheable_key}, 'got media cache hit')
            obj = proto.Message.decode(bytes(media_buff))
            key = f'{media_type}Message'
            current = getattr(obj, key, None)
            if current is not None:
                for k, v in upload_data.items():
                    if k == 'media':
                        continue
                    setattr(current, k, v)
            return obj

    is_newsletter = bool(options.get('jid')) and is_jid_newsletter(options['jid'])
    if is_newsletter:
        if logger is not None:
            logger.info({'key': cacheable_key}, 'Preparing raw media for newsletter')
        data = await get_raw_media_upload_data(
            upload_data['media'], options.get('mediaTypeOverride') or media_type, logger
        )
        file_sha256_b64 = base64_b64encode(data['fileSha256'])
        upload_result = await options['upload'](data['filePath'], {
            'fileEncSha256B64': file_sha256_b64,
            'mediaType': media_type,
            'timeoutMs': options.get('mediaUploadTimeoutMs'),
        })
        media_url = upload_result['mediaUrl']
        direct_path = upload_result['directPath']

        import os
        try:
            os.unlink(data['filePath'])
        except OSError:
            pass

        obj = proto.Message.from_object({
            f'{media_type}Message': MESSAGE_TYPE_PROTO[media_type].from_object({
                'url': media_url,
                'directPath': direct_path,
                'fileSha256': data['fileSha256'],
                'fileLength': data['fileLength'],
                **{k: v for k, v in upload_data.items() if k != 'media'},
            })
        })

        if upload_data.get('ptv'):
            obj.ptvMessage = obj.videoMessage
            del obj.videoMessage

        if obj.stickerMessage is not None:
            obj.stickerMessage.stickerSentTs = int(datetime.now().timestamp() * 1000)

        if cacheable_key and options.get('mediaCache'):
            if logger is not None:
                logger.debug({'cacheableKey': cacheable_key}, 'set cache')
            await options['mediaCache'].set(cacheable_key, proto.Message.encode(obj))

        return obj

    requires_duration_computation = media_type == 'audio' and 'seconds' not in upload_data
    requires_thumbnail_computation = (
        (media_type == 'image' or media_type == 'video') and 'jpegThumbnail' not in upload_data
    )
    requires_waveform_processing = media_type == 'audio' and upload_data.get('ptt') is True and 'waveform' not in upload_data
    requires_audio_background = options.get('backgroundColor') and media_type == 'audio' and upload_data.get('ptt') is True
    requires_original_for_some_processing = requires_duration_computation or requires_thumbnail_computation

    enc = await encrypted_stream(
        upload_data['media'],
        options.get('mediaTypeOverride') or media_type,
        {
            'logger': logger,
            'saveOriginalFileIfRequired': requires_original_for_some_processing,
            'opts': options.get('options'),
        },
    )
    media_key = enc['mediaKey']
    enc_file_path = enc['encFilePath']
    original_file_path = enc['originalFilePath']
    file_enc_sha256 = enc['fileEncSha256']
    file_sha256 = enc['fileSha256']
    file_length = enc['fileLength']

    file_enc_sha256_b64 = base64_b64encode(file_enc_sha256)

    upload_promise = None
    extra_info_promise = None

    async def _upload():
        result = await options['upload'](enc_file_path, {
            'fileEncSha256B64': file_enc_sha256_b64,
            'mediaType': media_type,
            'timeoutMs': options.get('mediaUploadTimeoutMs'),
        })
        if logger is not None:
            logger.debug({'mediaType': media_type, 'cacheableKey': cacheable_key}, 'uploaded media')
        return result

    async def _extra_info():
        try:
            if requires_thumbnail_computation:
                thumb_result = generate_thumbnail(original_file_path, media_type, options)
                thumbnail = thumb_result.get('thumbnail')
                original_image_dimensions = thumb_result.get('originalImageDimensions')
                upload_data['jpegThumbnail'] = thumbnail
                if not upload_data.get('width') and original_image_dimensions:
                    upload_data['width'] = original_image_dimensions.get('width')
                    upload_data['height'] = original_image_dimensions.get('height')
                    if logger is not None:
                        logger.debug('set dimensions')
                if logger is not None:
                    logger.debug('generated thumbnail')

            if requires_duration_computation:
                upload_data['seconds'] = await get_audio_duration(original_file_path)
                if logger is not None:
                    logger.debug('computed audio duration')

            if requires_waveform_processing:
                upload_data['waveform'] = await get_audio_waveform(original_file_path, logger)
                if logger is not None:
                    logger.debug('processed waveform')

            if requires_audio_background:
                upload_data['backgroundArgb'] = assert_color(options.get('backgroundColor'))
                if logger is not None:
                    logger.debug('computed backgroundColor audio status')
        except Exception as error:
            if logger is not None:
                logger.warn({'trace': getattr(error, 'stack', None)}, 'failed to obtain extra info')

    upload_promise = asyncio_task(_upload())
    extra_info_promise = asyncio_task(_extra_info())

    import asyncio

    upload_result = await upload_promise
    await extra_info_promise
    media_url = upload_result['mediaUrl']
    direct_path = upload_result['directPath']

    try:
        import os
        os.unlink(enc_file_path)
        if original_file_path:
            os.unlink(original_file_path)
        if logger is not None:
            logger.debug('removed tmp files')
    except Exception as error:
        if logger is not None:
            logger.warn('failed to remove tmp file')

    obj = proto.Message.from_object({
        f'{media_type}Message': MESSAGE_TYPE_PROTO[media_type].from_object({
            'url': media_url,
            'directPath': direct_path,
            'mediaKey': media_key,
            'fileEncSha256': file_enc_sha256,
            'fileSha256': file_sha256,
            'fileLength': file_length,
            'mediaKeyTimestamp': unix_timestamp_seconds(),
            **{k: v for k, v in upload_data.items() if k != 'media'},
        })
    })

    if upload_data.get('ptv'):
        obj.ptvMessage = obj.videoMessage
        del obj.videoMessage

    if cacheable_key and options.get('mediaCache'):
        if logger is not None:
            logger.debug({'cacheableKey': cacheable_key}, 'set cache')
        await options['mediaCache'].set(cacheable_key, proto.Message.encode(obj))

    return obj


def asyncio_task(coro):
    import asyncio

    return asyncio.ensure_future(coro)


def base64_b64encode(data: bytes) -> str:
    import base64

    return base64.b64encode(bytes(data)).decode('ascii')


def prepare_disappearing_message_setting_content(ephemeral_expiration=None):
    ephemeral_expiration = ephemeral_expiration or 0
    content = {
        'ephemeralMessage': {
            'message': {
                'protocolMessage': {
                    'type': proto.Message.ProtocolMessage.Type.EPHEMERAL_SETTING,
                    'ephemeralExpiration': ephemeral_expiration,
                }
            }
        }
    }
    return proto.Message.from_object(content)


def generate_forward_message_content(message, force_forward=None):
    content = message.get('message')
    if content is None:
        raise Boom('no content in message', status_code=400)

    content = normalize_message_content(content)
    content = _message_to_plain_dict(proto.Message.decode(proto.Message.encode(content)))

    key = next(iter(content.keys()), None)

    key_content = content.get(key)
    context_info = key_content.get('contextInfo') if isinstance(key_content, dict) else None
    score = (context_info or {}).get('forwardingScore') or 0
    score += 0 if (message.get('key', {}).get('fromMe') and not force_forward) else 1
    if key == 'conversation':
        content['extendedTextMessage'] = {'text': content[key]}
        del content['conversation']
        key = 'extendedTextMessage'

    key_ = content.get(key) or {}
    if score > 0:
        key_['contextInfo'] = {'forwardingScore': score, 'isForwarded': True}
    else:
        key_['contextInfo'] = {}
    content[key] = key_

    return content


async def generate_wa_message_content(message, options):
    m = {}

    if has_non_nullish_property(message, 'text'):
        ext_content = {'text': message['text']}

        url_info = message.get('linkPreview')
        if url_info is None:
            url_info = await generate_link_preview_if_required(message['text'], options.get('getUrlInfo'), options.get('logger'))

        if url_info:
            ext_content['matchedText'] = url_info.get('matched-text')
            ext_content['jpegThumbnail'] = url_info.get('jpegThumbnail')
            ext_content['description'] = url_info.get('description')
            ext_content['title'] = url_info.get('title')
            ext_content['previewType'] = 0

            img = url_info.get('highQualityThumbnail')
            if img:
                ext_content['thumbnailDirectPath'] = img.get('directPath')
                ext_content['mediaKey'] = img.get('mediaKey')
                ext_content['mediaKeyTimestamp'] = img.get('mediaKeyTimestamp')
                ext_content['thumbnailWidth'] = img.get('width')
                ext_content['thumbnailHeight'] = img.get('height')
                ext_content['thumbnailSha256'] = img.get('fileSha256')
                ext_content['thumbnailEncSha256'] = img.get('fileEncSha256')

        if options.get('backgroundColor'):
            ext_content['backgroundArgb'] = assert_color(options['backgroundColor'])

        if options.get('font'):
            ext_content['font'] = options['font']

        m['extendedTextMessage'] = ext_content
    elif has_non_nullish_property(message, 'contacts'):
        contact_len = len(message['contacts']['contacts'])
        if not contact_len:
            raise Boom('require atleast 1 contact', status_code=400)

        if contact_len == 1:
            m['contactMessage'] = proto.Message.ContactMessage.from_object(message['contacts']['contacts'][0])
        else:
            m['contactsArrayMessage'] = proto.Message.ContactsArrayMessage.from_object(message['contacts'])
    elif has_non_nullish_property(message, 'location'):
        m['locationMessage'] = proto.Message.LocationMessage.from_object(message['location'])
    elif has_non_nullish_property(message, 'react'):
        if not message['react'].get('senderTimestampMs'):
            message['react']['senderTimestampMs'] = int(datetime.now().timestamp() * 1000)
        m['reactionMessage'] = proto.Message.ReactionMessage.from_object(message['react'])
    elif has_non_nullish_property(message, 'delete'):
        m['protocolMessage'] = {
            'key': message['delete'],
            'type': proto.Message.ProtocolMessage.Type.REVOKE,
        }
    elif has_non_nullish_property(message, 'forward'):
        m = generate_forward_message_content(message['forward'], message.get('force'))
    elif has_non_nullish_property(message, 'disappearingMessagesInChat'):
        exp = (
            message['disappearingMessagesInChat'] if not isinstance(message['disappearingMessagesInChat'], bool)
            else (WA_DEFAULT_EPHEMERAL if message['disappearingMessagesInChat'] else 0)
        )
        m = prepare_disappearing_message_setting_content(exp)
    elif has_non_nullish_property(message, 'groupInvite'):
        m['groupInviteMessage'] = {
            'inviteCode': message['groupInvite'].get('inviteCode'),
            'inviteExpiration': message['groupInvite'].get('inviteExpiration'),
            'caption': message['groupInvite'].get('text'),
            'groupJid': message['groupInvite'].get('jid'),
            'groupName': message['groupInvite'].get('subject'),
        }
        if options.get('getProfilePicUrl'):
            pfp_url = await options['getProfilePicUrl'](message['groupInvite']['jid'], 'preview')
            if pfp_url:
                from .messages_media import _download_bytes
                try:
                    buf = _download_bytes(str(pfp_url), {})
                    m['groupInviteMessage']['jpegThumbnail'] = buf
                except Exception:
                    pass
    elif has_non_nullish_property(message, 'pin'):
        m['pinInChatMessage'] = {
            'key': message['pin'],
            'type': message.get('type'),
            'senderTimestampMs': int(datetime.now().timestamp() * 1000),
        }
        m['messageContextInfo'] = {
            'messageAddOnDurationInSecs': message.get('time') or 86400 if message.get('type') == 1 else 0,
        }
    elif has_non_nullish_property(message, 'buttonReply'):
        if message['type'] == 'template':
            m['templateButtonReplyMessage'] = {
                'selectedDisplayText': message['buttonReply'].get('displayText'),
                'selectedId': message['buttonReply'].get('id'),
                'selectedIndex': message['buttonReply'].get('index'),
            }
        elif message['type'] == 'plain':
            m['buttonsResponseMessage'] = {
                'selectedButtonId': message['buttonReply'].get('id'),
                'selectedDisplayText': message['buttonReply'].get('displayText'),
                'type': proto.Message.ButtonsResponseMessage.Type.DISPLAY_TEXT,
            }
    elif has_optional_property(message, 'ptv') and message.get('ptv'):
        media_result = await prepare_wa_message_media({'video': message['video']}, options)
        m['ptvMessage'] = media_result.videoMessage
    elif has_non_nullish_property(message, 'product'):
        media_result = await prepare_wa_message_media({'image': message['product']['productImage']}, options)
        m['productMessage'] = proto.Message.ProductMessage.from_object({
            **message,
            'product': {
                **message['product'],
                'productImage': media_result.imageMessage,
            },
        })
    elif has_non_nullish_property(message, 'listReply'):
        m['listResponseMessage'] = dict(message['listReply'])
    elif has_non_nullish_property(message, 'event'):
        m['eventMessage'] = {}
        start_time = int(message['event']['startDate'].timestamp()) if message['event'].get('startDate') else 0
        if message['event'].get('call') and options.get('getCallLink'):
            token = await options['getCallLink'](message['event']['call'], {'startTime': start_time})
            m['eventMessage']['joinLink'] = (CALL_AUDIO_PREFIX if message['event']['call'] == 'audio' else CALL_VIDEO_PREFIX) + token
        m['messageContextInfo'] = {
            'messageSecret': message['event'].get('messageSecret') or random_bytes(32),
        }
        m['eventMessage']['name'] = message['event'].get('name')
        m['eventMessage']['description'] = message['event'].get('description')
        m['eventMessage']['startTime'] = start_time
        end_date = message['event'].get('endDate')
        m['eventMessage']['endTime'] = int(end_date.timestamp()) if end_date else None
        m['eventMessage']['isCanceled'] = message['event'].get('isCancelled', False)
        m['eventMessage']['extraGuestsAllowed'] = message['event'].get('extraGuestsAllowed')
        m['eventMessage']['isScheduleCall'] = message['event'].get('isScheduleCall', False)
        m['eventMessage']['location'] = message['event'].get('location')
    elif has_non_nullish_property(message, 'poll'):
        poll = message['poll']
        poll['selectableCount'] = poll.get('selectableCount') or 0
        poll['toAnnouncementGroup'] = poll.get('toAnnouncementGroup') or False

        if not isinstance(poll.get('values'), list):
            raise Boom('Invalid poll values', status_code=400)

        if poll['selectableCount'] < 0 or poll['selectableCount'] > len(poll['values']):
            raise Boom(f"poll.selectableCount in poll should be >= 0 and <= {len(poll['values'])}", status_code=400)

        m['messageContextInfo'] = {
            'messageSecret': poll.get('messageSecret') or random_bytes(32),
        }

        poll_creation_message = {
            'name': poll.get('name'),
            'selectableOptionsCount': poll['selectableCount'],
            'options': [{'optionName': name} for name in poll['values']],
        }

        if poll['toAnnouncementGroup']:
            m['pollCreationMessageV2'] = poll_creation_message
        else:
            if poll['selectableCount'] == 1:
                m['pollCreationMessageV3'] = poll_creation_message
            else:
                m['pollCreationMessage'] = poll_creation_message
    elif has_non_nullish_property(message, 'album'):
        m['albumMessage'] = {
            'expectedImageCount': message['album'].get('expectedImageCount'),
            'expectedVideoCount': message['album'].get('expectedVideoCount'),
        }
    elif has_non_nullish_property(message, 'sharePhoneNumber'):
        m['protocolMessage'] = {'type': proto.Message.ProtocolMessage.Type.SHARE_PHONE_NUMBER}
    elif has_non_nullish_property(message, 'requestPhoneNumber'):
        m['requestPhoneNumberMessage'] = {}
    elif has_non_nullish_property(message, 'limitSharing'):
        m['protocolMessage'] = {
            'type': proto.Message.ProtocolMessage.Type.LIMIT_SHARING,
            'limitSharing': {
                'sharingLimited': message['limitSharing'] is True,
                'trigger': 1,
                'limitSharingSettingTimestamp': int(datetime.now().timestamp() * 1000),
                'initiatedByMe': True,
            },
        }
    else:
        m = await prepare_wa_message_media(message, options)

    if has_optional_property(message, 'viewOnce') and message.get('viewOnce'):
        m = {'viewOnceMessage': {'message': m}}

    if (has_optional_property(message, 'mentions') and message.get('mentions')) or (
        has_optional_property(message, 'mentionAll') and message.get('mentionAll')
    ):
        message_type = next(iter(m.keys())) if isinstance(m, dict) else None
        key = m.get(message_type) if message_type else None
        if key is not None and isinstance(key, dict):
            if 'contextInfo' in key:
                key['contextInfo'] = key.get('contextInfo') or {}
                if message.get('mentions'):
                    key['contextInfo']['mentionedJid'] = message['mentions']
                if message.get('mentionAll'):
                    key['contextInfo']['nonJidMentions'] = 1
            else:
                key['contextInfo'] = {
                    'mentionedJid': message.get('mentions'),
                    'nonJidMentions': 1 if message.get('mentionAll') else 0,
                }
        elif key is not None:
            key['contextInfo'] = {
                'mentionedJid': message.get('mentions'),
                'nonJidMentions': 1 if message.get('mentionAll') else 0,
            }

    if has_optional_property(message, 'edit'):
        m = {
            'protocolMessage': {
                'key': message['edit'],
                'editedMessage': m,
                'timestampMs': int(datetime.now().timestamp() * 1000),
                'type': proto.Message.ProtocolMessage.Type.MESSAGE_EDIT,
            }
        }

    if has_optional_property(message, 'contextInfo') and message.get('contextInfo'):
        message_type = next(iter(m.keys())) if isinstance(m, dict) else None
        key = m.get(message_type) if message_type else None
        if isinstance(key, dict):
            if 'contextInfo' in key and key.get('contextInfo'):
                key['contextInfo'] = {**key['contextInfo'], **message['contextInfo']}
            else:
                key['contextInfo'] = message['contextInfo']

    if has_optional_property(message, 'albumParentKey') and message.get('albumParentKey'):
        m['messageContextInfo'] = {
            **(m.get('messageContextInfo') or {}),
            'messageAssociation': {
                'associationType': proto.MessageAssociation.AssociationType.MEDIA_ALBUM,
                'parentMessageKey': message['albumParentKey'],
            },
        }

    if should_include_reporting_token(m):
        m['messageContextInfo'] = m.get('messageContextInfo') or {}
        if not m['messageContextInfo'].get('messageSecret'):
            m['messageContextInfo']['messageSecret'] = random_bytes(32)

    return proto.Message.from_object(m)


def random_bytes(n: int) -> bytes:
    import os

    return os.urandom(n)


def generate_wa_message_from_content(jid, message, options):
    # set timestamp to now if not specified
    if not options.get('timestamp'):
        options['timestamp'] = datetime.now()

    if isinstance(message, proto.Message):
        message = _message_to_plain_dict(message)

    inner_message = normalize_message_content(message)
    key = get_content_type(inner_message)
    timestamp = unix_timestamp_seconds(options.get('timestamp'))
    quoted = options.get('quoted')
    user_jid = options.get('userJid')

    if quoted and not is_jid_newsletter(jid):
        participant = (
            user_jid if quoted['key'].get('fromMe')
            else quoted.get('participant') or quoted['key'].get('participant') or quoted['key'].get('remoteJid')
        )

        quoted_msg = normalize_message_content(quoted.get('message'))
        msg_type = get_content_type(quoted_msg)
        quoted_msg = {msg_type: quoted_msg[msg_type]}

        quoted_content = quoted_msg.get(msg_type)
        if isinstance(quoted_content, dict) and 'contextInfo' in quoted_content:
            del quoted_content['contextInfo']

        context_info = (
            (inner_message.get(key) or {}).get('contextInfo') if isinstance(inner_message, dict) and key else {}
        ) or {}
        context_info['participant'] = jid_normalized_user(participant)
        context_info['stanzaId'] = quoted['key'].get('id')
        context_info['quotedMessage'] = quoted_msg

        if jid != quoted['key'].get('remoteJid'):
            context_info['remoteJid'] = quoted['key'].get('remoteJid')

        if inner_message and key:
            inner_message[key]['contextInfo'] = context_info

    if (
        options.get('ephemeralExpiration')
        and key != 'protocolMessage'
        and key != 'ephemeralMessage'
        and not is_jid_newsletter(jid)
    ):
        inner_message[key]['contextInfo'] = {
            **(inner_message[key].get('contextInfo') or {}),
            'expiration': options.get('ephemeralExpiration') or WA_DEFAULT_EPHEMERAL,
        }

    message = proto.Message.from_object(message)

    message_json = {
        'key': {
            'remoteJid': jid,
            'fromMe': True,
            'id': options.get('messageId') or generate_message_id_v2(),
        },
        'message': message,
        'messageTimestamp': timestamp,
        'messageStubParameters': [],
        'participant': user_jid if (is_jid_group(jid) or is_jid_status_broadcast(jid)) else None,
        'status': 1,  # WAMessageStatus.PENDING
    }
    return message_json


async def generate_wa_message(jid, content, options):
    options = dict(options or {})
    # Pass jid in the options to generateWAMessageContent
    content_opts = {**options, 'jid': jid}
    generated = await generate_wa_message_content(content, content_opts)
    return generate_wa_message_from_content(jid, generated, options)


def extract_message_content(content):
    def extract_from_template_message(msg):
        if msg.get('imageMessage'):
            return {'imageMessage': msg['imageMessage']}
        if msg.get('documentMessage'):
            return {'documentMessage': msg['documentMessage']}
        if msg.get('videoMessage'):
            return {'videoMessage': msg['videoMessage']}
        if msg.get('locationMessage'):
            return {'locationMessage': msg['locationMessage']}
        return {
            'conversation': (
                msg.get('contentText')
                if 'contentText' in msg
                else msg.get('hydratedContentText')
                if 'hydratedContentText' in msg
                else ''
            )
        }

    content = normalize_message_content(content)

    if content and content.get('buttonsMessage'):
        return extract_from_template_message(content['buttonsMessage'])
    if content and content.get('templateMessage') and content['templateMessage'].get('hydratedFourRowTemplate'):
        return extract_from_template_message(content['templateMessage']['hydratedFourRowTemplate'])
    if content and content.get('templateMessage') and content['templateMessage'].get('hydratedTemplate'):
        return extract_from_template_message(content['templateMessage']['hydratedTemplate'])
    if content and content.get('templateMessage') and content['templateMessage'].get('fourRowTemplate'):
        return extract_from_template_message(content['templateMessage']['fourRowTemplate'])

    return content


def update_message_with_receipt(msg: dict, receipt: dict) -> None:
    msg['userReceipt'] = msg.get('userReceipt') or []
    for recp in msg['userReceipt']:
        if recp.get('userJid') == receipt.get('userJid'):
            recp.update(receipt)
            return
    msg['userReceipt'].append(receipt)


def update_message_with_reaction(msg: dict, reaction: dict) -> None:
    author_id = get_key_author(reaction.get('key'))
    reactions = [r for r in (msg.get('reactions') or []) if get_key_author(r.get('key')) != author_id]
    reaction['text'] = reaction.get('text') or ''
    reactions.append(reaction)
    msg['reactions'] = reactions


def update_message_with_poll_update(msg: dict, update: dict) -> None:
    author_id = get_key_author(update.get('pollUpdateMessageKey'))
    reactions = [
        r for r in (msg.get('pollUpdates') or []) if get_key_author(r.get('pollUpdateMessageKey')) != author_id
    ]
    selected = (update.get('vote') or {}).get('selectedOptions') or []
    if len(selected):
        reactions.append(update)
    msg['pollUpdates'] = reactions


def update_message_with_event_response(msg: dict, update: dict) -> None:
    author_id = get_key_author(update.get('eventResponseMessageKey'))
    responses = [
        r for r in (msg.get('eventResponses') or []) if get_key_author(r.get('eventResponseMessageKey')) != author_id
    ]
    responses.append(update)
    msg['eventResponses'] = responses


def get_aggregate_votes_in_poll_message(msg: dict, me_id: str | None = None) -> list:
    message = msg.get('message') or {}
    options = (
        (message.get('pollCreationMessage') or {}).get('options')
        or (message.get('pollCreationMessageV2') or {}).get('options')
        or (message.get('pollCreationMessageV3') or {}).get('options')
        or []
    )
    vote_hash_map = {}
    for opt in options:
        name = opt.get('optionName') or ''
        vote_hash_map[sha256(name.encode('utf-8')).hex()] = {'name': name, 'voters': []}

    for update in msg.get('pollUpdates') or []:
        vote = update.get('vote')
        if not vote:
            continue
        for option in vote.get('selectedOptions') or []:
            hash_ = str(option)
            data = vote_hash_map.get(hash_)
            if not data:
                vote_hash_map[hash_] = {'name': 'Unknown', 'voters': []}
                data = vote_hash_map[hash_]
            data['voters'].append(get_key_author(update.get('pollUpdateMessageKey'), me_id))

    return list(vote_hash_map.values())


def get_aggregate_responses_in_event_message(msg: dict, me_id: str | None = None) -> list:
    response_types = ['GOING', 'NOT_GOING', 'MAYBE']
    response_map = {t: {'response': t, 'responders': []} for t in response_types}

    for update in msg.get('eventResponses') or []:
        response_type = update.get('eventResponse') or 'UNKNOWN'
        if response_type != 'UNKNOWN' and response_type in response_map:
            response_map[response_type]['responders'].append(
                get_key_author(update.get('eventResponseMessageKey'), me_id)
            )

    return list(response_map.values())


def aggregate_message_keys_not_from_me(keys):
    key_map = {}
    for key in keys:
        remote_jid = key.get('remoteJid')
        id_ = key.get('id')
        participant = key.get('participant')
        from_me = key.get('fromMe')
        if not from_me:
            uq_key = f'{remote_jid}:{participant or ""}'
            if uq_key not in key_map:
                key_map[uq_key] = {
                    'jid': remote_jid,
                    'participant': participant,
                    'messageIds': [],
                }
            key_map[uq_key]['messageIds'].append(id_)

    return list(key_map.values())


REUPLOAD_REQUIRED_STATUS = [410, 404]


async def download_media_message(message, type_, options, ctx=None):
    async def download_msg():
        m_content = extract_message_content(message.get('message'))
        if not m_content:
            raise Boom('No message present', status_code=400, data=message)

        content_type = get_content_type(m_content)
        media_type = content_type.replace('Message', '') if content_type else ''
        media = m_content.get(content_type) if content_type else None

        if media is None or not isinstance(media, dict) or (
            'url' not in media and 'thumbnailDirectPath' not in media
        ):
            raise Boom(f'"{content_type}" message is not a media message')

        download = None
        if 'thumbnailDirectPath' in media and 'url' not in media:
            download = {'directPath': media['thumbnailDirectPath'], 'mediaKey': media.get('mediaKey')}
            media_type = 'thumbnail-link'
        else:
            download = media

        from .messages_media import download_content_from_message

        stream = await download_content_from_message(download, media_type, options)
        if type_ == 'buffer':
            chunks = [chunk async for chunk in stream]
            return b''.join(chunks)
        return stream

    result = None
    try:
        result = await download_msg()
    except Exception as error:
        if (
            ctx
            and isinstance(error, Exception)
            and hasattr(error, 'statusCode')
            and error.statusCode in REUPLOAD_REQUIRED_STATUS
        ):
            if ctx.get('logger'):
                ctx['logger'].info({'key': message.get('key')}, 'sending reupload media request...')
            message = await ctx['reuploadRequest'](message)
            result = await download_msg()
        else:
            raise error

    return result


def assert_media_content(content):
    content = extract_message_content(content)
    media_content = (
        (content or {}).get('documentMessage')
        or (content or {}).get('imageMessage')
        or (content or {}).get('videoMessage')
        or (content or {}).get('audioMessage')
        or (content or {}).get('stickerMessage')
    )
    if not media_content:
        raise Boom('given message is not a media message', status_code=400, data=content)

    return media_content
