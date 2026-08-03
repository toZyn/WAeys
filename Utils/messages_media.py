"""Port of src/Utils/messages-media.ts — media encryption/decryption/upload/download.

Pure-Python: uses urllib for HTTP and the crypto module for AES. Image
thumbnail/profile generation requires Pillow; a clear Boom is raised when it
is unavailable (mirrors Baileys' sharp/jimp requirement).
"""

from __future__ import annotations

import base64
import hashlib
import hmac as hmac_mod
import os
import tempfile
import urllib.parse
import urllib.request
import uuid

from ..Defaults import DEFAULT_ORIGIN, MEDIA_HKDF_KEY_MAPPING, MEDIA_PATH_MAP
from ..WABinary.generic_utils import get_binary_node_child, get_binary_node_child_buffer
from ..WABinary.jid_utils import jid_normalized_user
from ..WABinary.types import BinaryNode
from ..WAProto import WAProto as proto
from .crypto import aes_cbc_decrypt_raw, aes_cbc_encrypt_raw, aes_decrypt_gcm, aes_encrypt_gcm, hkdf
from .generics import Boom, generate_message_id_v2

DEF_MEDIA_HOST = 'mmg.whatsapp.net'
AES_CHUNK_SIZE = 16


def hkdf_info_key(media_type: str) -> str:
    hkdf_info = MEDIA_HKDF_KEY_MAPPING.get(media_type, '')
    return f'WhatsApp {hkdf_info} Keys'


def get_media_keys(buffer, media_type: str) -> dict:
    """Generates all the keys required to encrypt/decrypt & sign a media message."""
    if not buffer:
        raise Boom('Cannot derive from empty media key')

    if isinstance(buffer, str):
        buffer = buffer.replace('data:;base64,', '')
        # handle data: URIs
        if ',' in buffer:
            buffer = buffer.split(',', 1)[1]
        buffer = base64.b64decode(buffer)

    buffer = bytes(buffer)

    # expand using HKDF to 112 bytes, also pass in the relevant app info
    expanded_media_key = hkdf(buffer, 112, info=hkdf_info_key(media_type).encode('utf-8'))
    return {
        'iv': expanded_media_key[:16],
        'cipherKey': expanded_media_key[16:48],
        'macKey': expanded_media_key[48:80],
    }


def to_buffer(stream) -> bytes:
    """Consume an iterable of bytes chunks into a single bytes object."""
    chunks = []
    for chunk in stream:
        chunks.append(bytes(chunk))
    return b''.join(chunks)


def get_stream(item, opts=None):
    """Resolve a WAMediaUpload (bytes, dict with 'stream', URL string) into chunks."""
    if isinstance(item, (bytes, bytearray)):
        return _ChunkedIterable([bytes(item)])

    if isinstance(item, dict) and 'stream' in item:
        return item['stream']

    url_str = str(item) if not isinstance(item, dict) else str(item.get('url', ''))

    if url_str.startswith('data:'):
        data_part = url_str.split(',', 1)[1] if ',' in url_str else url_str
        return _ChunkedIterable([base64.b64decode(data_part)])

    if url_str.startswith('http://') or url_str.startswith('https://'):
        return _HttpStream(url_str, opts)

    return _FileChunks(url_str)


class _ChunkedIterable:
    def __init__(self, chunks):
        self._chunks = list(chunks)

    def __iter__(self):
        return iter(self._chunks)

    def destroy(self):
        pass


class _FileChunks:
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        with open(self.path, 'rb') as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                yield chunk

    def destroy(self):
        pass


class _HttpStream:
    def __init__(self, url, opts=None):
        self.url = url
        self.opts = opts or {}
        self._response = None
        self._chunks = None

    def __iter__(self):
        headers = {}
        max_content_length = self.opts.get('maxContentLength')
        req = urllib.request.Request(self.url, headers=headers)
        self._response = urllib.request.urlopen(req)
        total = 0
        while True:
            chunk = self._response.read(65536)
            if not chunk:
                break
            total += len(chunk)
            if max_content_length and total > max_content_length:
                raise Boom(f'content length exceeded when fetching "{self.url}"', status_code=413)
            yield chunk
        self._response.close()

    def destroy(self):
        if self._response is not None:
            try:
                self._response.close()
            except Exception:
                pass


def get_url_from_direct_path(direct_path: str, host: str = DEF_MEDIA_HOST) -> str:
    return f'https://{host}{direct_path}'


def _extract_host(url) -> str | None:
    if not url:
        return None
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.hostname
    except Exception:
        return None


def _to_smallest_chunk_size(num: int) -> int:
    return (num // AES_CHUNK_SIZE) * AES_CHUNK_SIZE


async def download_content_from_message(msg: dict, media_type: str, opts: dict = None) -> object:
    """Return an async iterable of decrypted bytes chunks.

    msg: {'mediaKey', 'directPath', 'url'}
    """
    opts = opts or {}
    media_key = msg.get('mediaKey')
    direct_path = msg.get('directPath')
    url = msg.get('url')

    fallback_host = opts.get('host') or _extract_host(url)
    download_url = get_url_from_direct_path(direct_path, fallback_host) if direct_path else url
    if not download_url:
        raise Boom('No valid media URL or directPath present in message', status_code=400)

    keys = get_media_keys(media_key, media_type)
    return download_encrypted_content(download_url, keys, opts)


def _download_bytes(url: str, headers: dict) -> bytes:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def download_encrypted_content(download_url: str, keys: dict, opts: dict = None):
    """Decrypts and downloads an AES256-CBC encrypted file given the keys.

    Returns an async iterator of plaintext chunks.
    """
    opts = opts or {}
    cipher_key = keys['cipherKey']
    iv = keys['iv']
    start_byte = opts.get('startByte')
    end_byte = opts.get('endByte')
    options = opts.get('options') or {}

    bytes_fetched = 0
    start_chunk = 0
    first_block_is_iv = False
    # if a start byte is specified -- then we need to fetch the previous chunk as that will form the IV
    if start_byte:
        chunk = _to_smallest_chunk_size(start_byte or 0)
        if chunk:
            start_chunk = chunk - AES_CHUNK_SIZE
            bytes_fetched = chunk
            first_block_is_iv = True

    end_chunk = _to_smallest_chunk_size(end_byte or 0) + AES_CHUNK_SIZE if end_byte else None

    headers = {'Origin': DEFAULT_ORIGIN}
    if options.get('headers'):
        hdrs = options['headers']
        if isinstance(hdrs, dict):
            headers.update(hdrs)
        else:
            headers.update(dict(hdrs))
    if start_chunk or end_chunk:
        headers['Range'] = f'bytes={start_chunk}-'
        if end_chunk:
            headers['Range'] += str(end_chunk)

    data = _download_bytes(download_url, headers)

    import asyncio

    async def gen():
        remaining = b''
        chunk_size = 65536
        position = 0
        aes = None
        output = bytearray()

        def push_bytes(plain):
            nonlocal bytes_fetched
            if start_byte or end_byte:
                start = None if bytes_fetched >= start_byte else max(start_byte - bytes_fetched, 0)
                end = None if bytes_fetched + len(plain) < end_byte else max(end_byte - bytes_fetched, 0)
                if start is None and end is None:
                    out = plain
                elif start is not None and end is not None:
                    out = plain[start:end]
                elif start is not None:
                    out = plain[start:]
                else:
                    out = plain[:end]
                bytes_fetched += len(plain)
                return out
            return plain

        idx = 0
        while idx < len(data):
            chunk = data[idx:idx + chunk_size]
            idx += chunk_size
            merged = remaining + chunk if remaining else chunk

            decrypt_length = _to_smallest_chunk_size(len(merged))
            remaining = merged[decrypt_length:]
            block = merged[:decrypt_length]

            if aes is None:
                iv_value = iv
                if first_block_is_iv:
                    iv_value = block[:AES_CHUNK_SIZE]
                    block = block[AES_CHUNK_SIZE:]
                aes = _AesCbcDecryptor(cipher_key, iv_value, auto_padding=not end_byte)

            out = push_bytes(aes.update(block))
            if out:
                output += out
            await asyncio.sleep(0)

        out = push_bytes(aes.final())
        if out:
            output += out

        yield bytes(output)

    return gen()


class _AesCbcDecryptor:
    def __init__(self, key, iv, auto_padding=True):
        self.key = key
        self.iv = iv
        self.auto_padding = auto_padding
        self._prev = iv
        self._buffer = b''

    def update(self, data):
        data = self._buffer + data
        align = (len(data) // AES_CHUNK_SIZE) * AES_CHUNK_SIZE
        if self.auto_padding:
            # Node's createDecipheriv holds back the final block so that
            # final() can strip the PKCS7 padding
            align = max(align - AES_CHUNK_SIZE, 0)
        block = data[:align]
        self._buffer = data[align:]
        if not block:
            return b''
        out = aes_cbc_decrypt_raw(block, self.key, self._prev)
        self._prev = block[-AES_CHUNK_SIZE:]
        return out

    def final(self):
        if not self._buffer:
            return b''
        out = aes_cbc_decrypt_raw(self._buffer, self.key, self._prev)
        if self.auto_padding:
            pad = out[-1]
            if 1 <= pad <= AES_CHUNK_SIZE:
                out = out[:-pad]
        return out


def extension_for_media_message(message: dict) -> str:
    def get_extension(mimetype):
        return mimetype.split(';')[0].split('/')[1]

    types = [k for k, v in (message or {}).items() if v is not None]
    type_ = types[0] if types else None
    if type_ in ('locationMessage', 'liveLocationMessage', 'productMessage'):
        return '.jpeg'
    message_content = (message or {}).get(type_) or {}
    return get_extension(message_content.get('mimetype', ''))


def media_message_sha256_b64(message: dict) -> str | None:
    media = next((v for v in (message or {}).values() if v is not None), None)
    file_sha = media.get('fileSha256') if media else None
    return base64.b64encode(bytes(file_sha)).decode('ascii') if file_sha else None


def encode_base64_encoded_string_for_upload(b64: str) -> str:
    return urllib.parse.quote(b64.replace('+', '-').replace('/', '_').rstrip('='))


def extract_image_thumb(buffer, width: int = 32):
    """Requires Pillow. Mirrors extractImageThumb (sharp/jimp)."""
    try:
        from PIL import Image
        import io
    except ImportError:
        raise Boom('No image processing library available')

    img = Image.open(io.BytesIO(bytes(buffer)))
    original = {'width': img.width, 'height': img.height}
    ratio = img.height / img.width
    new_height = int(width * ratio)
    img = img.resize((width, new_height), Image.BILINEAR)
    out = io.BytesIO()
    img.convert('RGB').save(out, format='JPEG', quality=50)
    return {'buffer': out.getvalue(), 'original': original}


def generate_profile_picture(media_upload, dimensions=None):
    """Requires Pillow. Mirrors generateProfilePicture."""
    try:
        from PIL import Image
        import io
    except ImportError:
        raise Boom('No image processing library available')

    w, h = (dimensions or {}).get('width', 640), (dimensions or {}).get('height', 640)

    if isinstance(media_upload, (bytes, bytearray)):
        buffer = bytes(media_upload)
    else:
        buffer = to_buffer(get_stream(media_upload))

    img = Image.open(io.BytesIO(buffer))
    min_side = min(img.width, img.height)
    left = (img.width - min_side) // 2
    top = (img.height - min_side) // 2
    cropped = img.crop((left, top, left + min_side, top + min_side))
    cropped = cropped.resize((w, h), Image.BILINEAR)
    out = io.BytesIO()
    cropped.convert('RGB').save(out, format='JPEG', quality=50)
    return {'img': out.getvalue()}


def get_audio_duration(buffer_or_path):
    """Recreation of TS getAudioDuration (music-metadata) using the stdlib wave
    module. Raises Boom for unsupported formats."""
    import wave

    if isinstance(buffer_or_path, (bytes, bytearray)):
        import io
        f = io.BytesIO(bytes(buffer_or_path))
    else:
        f = buffer_or_path

    try:
        wav = wave.open(f, 'rb')
        try:
            frames = wav.getnframes()
            rate = wav.getframerate()
            return frames / float(rate) if rate else None
        finally:
            wav.close()
    except Exception:
        raise Boom('Failed to parse audio duration (unsupported format)')


def get_audio_waveform(buffer_or_path, logger=None):
    """Recreation of TS getAudioWaveform using the stdlib wave module.

    Returns a list of 64 normalized 0-100 samples, or None on failure.
    """
    import wave

    try:
        if isinstance(buffer_or_path, (bytes, bytearray)):
            import io
            f = io.BytesIO(bytes(buffer_or_path))
        else:
            f = buffer_or_path

        wav = wave.open(f, 'rb')
        try:
            frames = wav.getnframes()
            rate = wav.getframerate()
            channels = wav.getnchannels()
            sampwidth = wav.getsampwidth()
            raw = wav.readframes(frames)
        finally:
            wav.close()

        import struct

        if sampwidth == 1:
            samples = struct.unpack(f'<{len(raw)}B', raw)
            samples = [s - 128 for s in samples]
        elif sampwidth == 2:
            n = len(raw) // 2
            samples = struct.unpack(f'<{n}h', raw[: n * 2])
        else:
            raise ValueError('unsupported sample width')

        # use a single channel
        if channels > 1:
            samples = samples[0::channels]

        num_samples = 64
        if not samples:
            return [0] * num_samples

        block_size = len(samples) // num_samples
        filtered = []
        for i in range(num_samples):
            block_start = block_size * i
            total = 0
            for j in range(block_size):
                total += abs(samples[block_start + j])
            filtered.append(total / block_size if block_size else 0)

        max_val = max(filtered) if filtered else 0
        multiplier = (max_val ** -1) if max_val else 0
        return [int(100 * n * multiplier) for n in filtered]
    except Exception as error:
        if logger is not None:
            logger.debug(f'Failed to generate waveform: {error}')
        return None


def extract_video_thumb(path, dest_path, time='00:00:00', size=None):
    """Recreation of TS extractVideoThumb using ffmpeg if available."""
    import shutil
    import subprocess

    if shutil.which('ffmpeg') is None:
        raise Boom('No ffmpeg available for video thumbnail')

    width = (size or {}).get('width', 32)
    cmd = ['ffmpeg', '-ss', time, '-i', path, '-y', '-vf', f'scale={width}:-1',
           '-vframes', '1', '-f', 'image2', dest_path]
    subprocess.run(cmd, check=True, capture_output=True)


def generate_thumbnail(file, media_type, options=None):
    """Recreation of TS generateThumbnail."""
    options = options or {}
    thumbnail = None
    original_image_dimensions = None

    if media_type == 'image':
        from PIL import Image
        import io
        img = Image.open(file)
        original = {'width': img.width, 'height': img.height}
        with open(file, 'rb') as f:
            raw = f.read()
        result = extract_image_thumb(raw, 32)
        thumbnail = base64.b64encode(result['buffer']).decode('ascii')
        if original.get('width') and original.get('height'):
            original_image_dimensions = original
    elif media_type == 'video':
        import os as os_mod
        img_filename = os.path.join(tempfile.gettempdir(), generate_message_id_v2() + '.jpg')
        try:
            extract_video_thumb(file, img_filename, '00:00:00', {'width': 32, 'height': 32})
            with open(img_filename, 'rb') as f:
                thumbnail = base64.b64encode(f.read()).decode('ascii')
            os_mod.unlink(img_filename)
        except Exception as error:
            if options.get('logger') is not None:
                options['logger'].debug(f'could not generate video thumb: {error}')

    return {'thumbnail': thumbnail, 'originalImageDimensions': original_image_dimensions}


def get_media_retry_key(media_key: bytes) -> bytes:
    return hkdf(media_key, 32, info=b'WhatsApp Media Retry Notification')


def encrypt_media_retry_request(key: dict, media_key: bytes, me_id: str) -> BinaryNode:
    recp = proto.ServerErrorReceipt.from_object({'stanzaId': key.get('id')})
    recp_buffer = proto.ServerErrorReceipt.encode(recp)

    iv = os.urandom(12)
    retry_key = get_media_retry_key(media_key)
    ciphertext = aes_encrypt_gcm(recp_buffer, retry_key, iv, key.get('id', '').encode('utf-8'))

    req = BinaryNode(tag='receipt', attrs={
        'id': key.get('id'),
        'to': jid_normalized_user(me_id),
        'type': 'server-error',
    }, content=[
        # this encrypt node is actually pretty useless
        # the media is returned even without this node
        # keeping it here to maintain parity with WA Web
        BinaryNode(tag='encrypt', attrs={}, content=[
            BinaryNode(tag='enc_p', attrs={}, content=ciphertext),
            BinaryNode(tag='enc_iv', attrs={}, content=iv),
        ]),
        BinaryNode(tag='rmr', attrs={
            'jid': key.get('remoteJid'),
            'from_me': str(bool(key.get('fromMe'))).lower(),
            'participant': key.get('participant'),
        }),
    ])

    return req


def decode_media_retry_node(node: BinaryNode) -> dict:
    rmr_node = get_binary_node_child(node, 'rmr')
    event = {
        'key': {
            'id': (node.attrs or {}).get('id'),
            'remoteJid': (rmr_node.attrs or {}).get('jid'),
            'fromMe': (rmr_node.attrs or {}).get('from_me') == 'true',
            'participant': (rmr_node.attrs or {}).get('participant'),
        }
    }

    error_node = get_binary_node_child(node, 'error')
    if error_node:
        error_code = int((error_node.attrs or {}).get('code', 0))
        event['error'] = Boom(
            f'Failed to re-upload media ({error_code})',
            data=error_node.attrs,
            status_code=get_status_code_for_media_retry(error_code),
        )
    else:
        encrypted_info_node = get_binary_node_child(node, 'encrypt')
        ciphertext = get_binary_node_child_buffer(encrypted_info_node, 'enc_p')
        iv = get_binary_node_child_buffer(encrypted_info_node, 'enc_iv')
        if ciphertext and iv:
            event['media'] = {'ciphertext': ciphertext, 'iv': iv}
        else:
            event['error'] = Boom('Failed to re-upload media (missing ciphertext)', status_code=404)

    return event


def decrypt_media_retry_data(data: dict, media_key: bytes, msg_id: str):
    ciphertext = bytes(data['ciphertext'])
    iv = bytes(data['iv'])
    retry_key = get_media_retry_key(media_key)
    plaintext = aes_decrypt_gcm(ciphertext, retry_key, iv, msg_id.encode('utf-8'))
    return proto.MediaRetryNotification.decode(plaintext)


_MEDIA_RETRY_STATUS_MAP = {
    proto.MediaRetryNotification.ResultType.SUCCESS: 200,
    proto.MediaRetryNotification.ResultType.DECRYPTION_ERROR: 412,
    proto.MediaRetryNotification.ResultType.NOT_FOUND: 404,
    proto.MediaRetryNotification.ResultType.GENERAL_ERROR: 418,
}


def get_status_code_for_media_retry(code: int) -> int:
    return _MEDIA_RETRY_STATUS_MAP.get(code, 500)


async def get_raw_media_upload_data(media, media_type: str, logger=None):
    stream = get_stream(media)
    if logger is not None:
        logger.debug('got stream for raw upload')

    hasher = hashlib.sha256()
    file_path = os.path.join(tempfile.gettempdir(), media_type + generate_message_id_v2())
    file_length = 0

    try:
        chunks = []
        for data in stream:
            data = bytes(data)
            file_length += len(data)
            hasher.update(data)
            chunks.append(data)
        stream.destroy() if hasattr(stream, 'destroy') else None

        with open(file_path, 'wb') as f:
            for c in chunks:
                f.write(c)

        file_sha256 = hasher.digest()
        if logger is not None:
            logger.debug('hashed data for raw upload')
        return {'filePath': file_path, 'fileSha256': file_sha256, 'fileLength': file_length}
    except Exception:
        try:
            os.unlink(file_path)
        except Exception:
            pass
        raise


async def encrypted_stream(media, media_type: str, opts: dict = None):
    """Encrypt a media stream; returns dict with mediaKey, file paths, hashes, mac."""
    opts = opts or {}
    logger = opts.get('logger')
    stream = get_stream(media, opts.get('opts'))

    if logger is not None:
        logger.debug('fetched media stream')

    media_key = os.urandom(32)
    keys = get_media_keys(media_key, media_type)
    cipher_key = keys['cipherKey']
    iv = keys['iv']
    mac_key = keys['macKey']

    enc_file_path = os.path.join(tempfile.gettempdir(), media_type + generate_message_id_v2() + '-enc')
    original_file_path = None
    original_file_stream = None

    if opts.get('saveOriginalFileIfRequired'):
        original_file_path = os.path.join(tempfile.gettempdir(), media_type + generate_message_id_v2() + '-original')
        original_file_stream = open(original_file_path, 'wb')

    file_length = 0
    sha256_plain = hashlib.sha256()
    sha256_enc = hashlib.sha256()
    hmac_obj = hmac_mod.new(mac_key, iv, hashlib.sha256)

    aes = _AesCbcEncryptor(cipher_key, iv)
    enc_chunks = []

    try:
        max_content_length = (opts.get('opts') or {}).get('maxContentLength')
        for data in stream:
            data = bytes(data)
            file_length += len(data)
            if max_content_length and file_length + len(data) > max_content_length:
                raise Boom('content length exceeded when encrypting media', status_code=413)

            if original_file_stream:
                original_file_stream.write(data)

            sha256_plain.update(data)
            cipher_block = aes.update(data)
            sha256_enc.update(cipher_block)
            hmac_obj.update(cipher_block)
            enc_chunks.append(cipher_block)

        final_block = aes.final()
        sha256_enc.update(final_block)
        hmac_obj.update(final_block)
        enc_chunks.append(final_block)

        mac = hmac_obj.digest()[:10]
        sha256_enc.update(mac)
        enc_chunks.append(mac)

        with open(enc_file_path, 'wb') as f:
            for c in enc_chunks:
                f.write(c)

        if original_file_stream:
            original_file_stream.close()

        file_sha256 = sha256_plain.digest()
        file_enc_sha256 = sha256_enc.digest()

        if logger is not None:
            logger.debug('encrypted data successfully')

        return {
            'mediaKey': media_key,
            'originalFilePath': original_file_path,
            'encFilePath': enc_file_path,
            'mac': mac,
            'fileEncSha256': file_enc_sha256,
            'fileSha256': file_sha256,
            'fileLength': file_length,
        }
    except Exception as error:
        try:
            if original_file_stream:
                original_file_stream.close()
        except Exception:
            pass
        try:
            os.unlink(enc_file_path)
        except Exception:
            pass
        if original_file_path:
            try:
                os.unlink(original_file_path)
            except Exception:
                pass
        raise error


class _AesCbcEncryptor:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self._prev = iv
        self._buffer = b''

    def update(self, data):
        data = self._buffer + data
        complete = data[:-(len(data) % AES_CHUNK_SIZE)] if len(data) % AES_CHUNK_SIZE else data
        self._buffer = data[len(complete):]
        if not complete:
            return b''
        out = aes_cbc_encrypt_raw(complete, self.key, self._prev)
        self._prev = out[-AES_CHUNK_SIZE:]
        return out

    def final(self):
        # pad the remaining buffer with PKCS7
        pad_len = AES_CHUNK_SIZE - (len(self._buffer) % AES_CHUNK_SIZE)
        padded = self._buffer + bytes([pad_len]) * pad_len
        self._buffer = b''
        return aes_cbc_encrypt_raw(padded, self.key, self._prev)


def get_wa_upload_to_server(config: dict, refresh_media_conn):
    async def upload(file_path, upload_opts):
        media_type = upload_opts['mediaType']
        file_enc_sha256_b64 = upload_opts['fileEncSha256B64']
        timeout_ms = upload_opts.get('timeoutMs')

        upload_info = await refresh_media_conn(False)

        urls = None
        custom_upload_hosts = config.get('customUploadHosts') or []
        hosts = list(custom_upload_hosts) + list(upload_info.get('hosts') or [])

        file_enc_sha256_b64 = encode_base64_encoded_string_for_upload(file_enc_sha256_b64)

        headers = {'Content-Type': 'application/octet-stream', 'Origin': DEFAULT_ORIGIN}

        for host in hosts:
            hostname = host.get('hostname') if isinstance(host, dict) else getattr(host, 'hostname', None)
            logger = config.get('logger')
            if logger is not None:
                logger.debug(f'uploading to "{hostname}"')

            auth = urllib.parse.quote(upload_info.get('auth', ''))
            url = f'https://{hostname}{MEDIA_PATH_MAP.get(media_type, "")}/{file_enc_sha256_b64}?auth={auth}&token={file_enc_sha256_b64}'

            try:
                result = _upload_media(url, file_path, headers, timeout_ms)
                if result and (result.get('url') or result.get('direct_path')):
                    urls = {
                        'mediaUrl': result.get('url'),
                        'directPath': result.get('direct_path'),
                        'meta_hmac': result.get('meta_hmac'),
                        'fbid': result.get('fbid'),
                        'ts': result.get('ts'),
                    }
                    break
                else:
                    upload_info = await refresh_media_conn(True)
                    raise Exception(f'upload failed, reason: {result}')
            except Exception as error:
                is_last = hostname == (hosts[-1].get('hostname') if isinstance(hosts[-1], dict) else getattr(hosts[-1], 'hostname', None))
                if logger is not None:
                    logger.warn(
                        {'trace': getattr(error, 'stack', None), 'uploadResult': result if 'result' in dir() else None},
                        f'Error in uploading to {hostname} {"" if is_last else ", retrying..."}',
                    )

        if not urls:
            raise Boom('Media upload failed on all hosts', status_code=500)

        return urls

    return upload


def _upload_media(url, file_path, headers, timeout_ms, redirect_count=0):
    """POST a file to the given URL. Returns parsed JSON dict or None.

    Mirrors uploadWithNodeHttp including 3xx redirect handling.
    """
    import json as json_mod

    with open(file_path, 'rb') as f:
        data = f.read()

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=(timeout_ms / 1000.0) if timeout_ms else None) as resp:
            if resp.status >= 300 and resp.status < 400 and resp.headers.get('Location'):
                if redirect_count > 5:
                    raise Exception('Too many redirects')
                new_url = urllib.parse.urljoin(url, resp.headers['Location'])
                return _upload_media(url=new_url, file_path=file_path, headers=headers,
                                     timeout_ms=timeout_ms, redirect_count=redirect_count + 1)
            body = resp.read().decode('utf-8')
        try:
            return json_mod.loads(body)
        except Exception:
            return None
    except Exception:
        return None
