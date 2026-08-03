"""Generic utilities mirroring src/Utils/generics.ts.

Note: proto-dependent helpers (encodeWAMessage, getStatusFromReceiptType, ...)
lazy-import WAProto once it is ported.
"""
import asyncio
import base64
import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone

from .crypto import sha256
from ..WABinary.generic_utils import get_all_binary_node_children
from ..WABinary.jid_utils import jid_decode


def to_base64(buf: bytes) -> str:
    return base64.b64encode(bytes(buf)).decode("ascii")


def _is_buffer_value(value) -> bool:
    if isinstance(value, (bytes, bytearray, memoryview)):
        return True
    if isinstance(value, dict) and value.get("type") == "Buffer":
        return True
    return False


def _is_uint8_or_buffer_array(value) -> bool:
    return isinstance(value, (bytes, bytearray)) or (
        isinstance(value, list) and all(isinstance(v, int) for v in value)
    )


class BufferJSON:
    """JSON replacer/reviver that serializes bytes as {type:'Buffer', data: base64}.

    Usable directly as json.dumps(default=...) and json.loads(object_hook=...);
    the key argument of the JS originals is ignored.
    """

    @staticmethod
    def replacer(value):
        if _is_buffer_value(value):
            data = value.get("data") if isinstance(value, dict) and value.get("type") == "Buffer" else value
            return {"type": "Buffer", "data": to_base64(data)}
        return value

    @staticmethod
    def reviver(value):
        if isinstance(value, dict) and value.get("type") == "Buffer" and isinstance(value.get("data"), str):
            return base64.b64decode(value["data"])
        if (
            isinstance(value, dict)
            and value.get("type") == "Buffer"
            and isinstance(value.get("data"), list)
        ):
            data = value["data"]
            if all(isinstance(v, int) for v in data):
                return bytes(v & 0xFF for v in data)
        if (
            isinstance(value, dict)
            and len(value) > 0
            and all(re.fullmatch(r"\d+", k) is not None for k in value.keys())
        ):
            values = list(value.values())
            if all(isinstance(v, (int, float)) for v in values):
                return bytes(int(v) & 0xFF for v in values)
        return value


def node_json_dumps(obj) -> str:
    """Emulate Node's JSON.stringify for objects containing Buffer/Uint8Array.

    Node stringifies a Buffer as {"type":"Buffer","data":[...]} (array form).
    This is what Baileys' `JSON.stringify(key.serialize())` produces on disk.
    """

    def _convert(value):
        if isinstance(value, (bytes, bytearray)):
            return {"type": "Buffer", "data": [b for b in bytes(value)]}
        if isinstance(value, dict):
            return {k: _convert(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_convert(v) for v in value]
        if isinstance(value, tuple):
            return [_convert(v) for v in value]
        return value

    return json.dumps(_convert(obj))


def get_key_author(key, me_id="me"):
    if not key:
        return ""
    if key.get("fromMe"):
        return me_id
    return (
        key.get("participantAlt")
        or key.get("remoteJidAlt")
        or key.get("participant")
        or key.get("remoteJid")
        or ""
    )


def is_string_null_or_empty(value):
    return value is None or value == ""


def write_random_pad_max16(msg: bytes) -> bytes:
    pad = os.urandom(1)
    pad_length = (pad[0] & 0x0F) + 1
    return msg + bytes([pad_length]) * pad_length


def unpad_random_max16(e):
    t = bytes(e)
    if len(t) == 0:
        raise ValueError("unpadPkcs7 given empty bytes")
    r = t[-1]
    if r > len(t):
        raise ValueError(f"unpad given {len(t)} bytes, but pad is {r}")
    return t[: len(t) - r]


def generate_participant_hash_v2(participants: list) -> str:
    participants = sorted(participants)
    sha = sha256("".join(participants).encode("utf-8"))
    b64 = base64.b64encode(sha).decode("ascii")
    return "2:" + b64[:6]


def encode_wa_message(message) -> bytes:
    from ..WAProto import WAProto

    encoded = WAProto.Message.encode(message)
    return write_random_pad_max16(encoded)


def generate_registration_id() -> int:
    return int.from_bytes(os.urandom(2), "little") & 16383


def encode_big_endian(e: int, t: int = 4) -> bytes:
    r = e
    a = bytearray(t)
    for i in range(t - 1, -1, -1):
        a[i] = 0xFF & r
        r >>= 8
    return bytes(a)


def to_number(t):
    if t is None:
        return 0
    if hasattr(t, "toNumber"):
        return t.toNumber()
    if hasattr(t, "low"):
        return t.low
    if isinstance(t, bool):
        return int(t)
    return int(t) if t else 0


def unix_timestamp_seconds(date: datetime = None) -> int:
    if date is None:
        date = datetime.now(timezone.utc)
    return int(date.timestamp())


class DebouncedTimeout:
    def __init__(self, interval_ms=1000, task=None):
        self.interval_ms = interval_ms
        self.task = task
        self._timeout = None

    def start(self, new_interval_ms=None, new_task=None):
        if new_task is not None:
            self.task = new_task
        if new_interval_ms is not None:
            self.interval_ms = new_interval_ms
        if self._timeout is not None:
            self._timeout.cancel()
        if self.task is not None:
            loop = asyncio.get_event_loop()
            self._timeout = loop.call_later(self.interval_ms / 1000.0, self.task)

    def cancel(self):
        if self._timeout is not None:
            self._timeout.cancel()
            self._timeout = None

    def set_task(self, new_task):
        self.task = new_task

    def set_interval(self, new_interval):
        self.interval_ms = new_interval


def debounced_timeout(interval_ms=1000, task=None):
    return DebouncedTimeout(interval_ms, task)


def delay(ms: float):
    """Awaitable resolving after ms. Returns a coroutine."""
    return delay_cancellable(ms)["delay"]


def delay_cancellable(ms: float):
    """Returns {delay: Future, cancel: fn} resolving after ms or cancelling via Boom."""
    loop = asyncio.get_event_loop()
    stack = "".join(asyncio.get_event_loop().get_debug() and [] or [])

    fut = loop.create_future()

    def _done():
        if not fut.done():
            fut.set_result(None)

    handle = loop.call_later(ms / 1000.0, _done)

    def cancel():
        handle.cancel()
        if not fut.done():
            fut.set_exception(Boom("Cancelled", 500, stack=stack))

    return {"delay": fut, "cancel": cancel}


class Boom(Exception):
    """Boom-style error with statusCode + data, mirroring @hapi/boom."""

    def __init__(self, message, status_code=500, data=None, stack=None):
        super().__init__(message)
        self.output = {"statusCode": status_code}
        self.message = message
        self.data = data
        self.stack = stack
        self.isBoom = True

    @property
    def statusCode(self):
        return self.output["statusCode"]


async def promise_timeout(ms, promise):
    """Run promise(resolve, reject); reject with Boom('Timed Out', 408) after ms if unset."""
    if not ms:
        result_holder = {}

        def _resolve(v):
            result_holder["done"] = True
            result_holder["value"] = v

        def _reject(e):
            result_holder["done"] = True
            result_holder["error"] = e

        res = promise(_resolve, _reject)
        if asyncio.iscoroutine(res) or isinstance(res, asyncio.Future):
            await res
        if "error" in result_holder:
            raise result_holder["error"]
        return result_holder.get("value")

    stack = None
    d = delay_cancellable(ms)
    result_holder = {}

    def _resolve(v):
        if not result_holder.get("done"):
            result_holder["done"] = True
            result_holder["value"] = v
            d["cancel"]()

    def _reject(e):
        if not result_holder.get("done"):
            result_holder["done"] = True
            result_holder["error"] = e
            d["cancel"]()

    async def _timeout_watch():
        await d["delay"]
        if not result_holder.get("done"):
            result_holder["done"] = True
            result_holder["error"] = Boom("Timed Out", 408, stack=stack)

    watch = asyncio.ensure_future(_timeout_watch())
    try:
        res = promise(_resolve, _reject)
        if asyncio.iscoroutine(res) or isinstance(res, asyncio.Future):
            await res
        while not result_holder.get("done"):
            await asyncio.sleep(0)
        if "error" in result_holder:
            raise result_holder["error"]
        return result_holder["value"]
    finally:
        watch.cancel()


def generate_message_id_v2(user_id: str = None) -> str:
    data = bytearray(8 + 20 + 16)
    data[0:8] = int(time.time()).to_bytes(8, "big")
    if user_id:
        decoded = jid_decode(user_id)
        if decoded and getattr(decoded, "user", None):
            user = decoded.user
            data[8:8 + len(user)] = user.encode("utf-8")
            data[8 + len(user):8 + len(user) + 5] = b"@c.us"
    data[28:44] = os.urandom(16)
    hash_digest = sha256(bytes(data))
    return "3EB0" + hash_digest.hex().upper()[:18]


def generate_message_id() -> str:
    return "3EB0" + os.urandom(18).hex().upper()


def generate_md_tag_prefix() -> str:
    bytes_ = os.urandom(4)
    return f"{int.from_bytes(bytes_[:2], 'big')}.{int.from_bytes(bytes_[2:], 'big')}-"


def get_status_from_receipt_type(type_):
    from ..WAProto import WAProto

    STATUS_MAP = {
        "sender": WAProto.WebMessageInfo.Status.SERVER_ACK,
        "played": WAProto.WebMessageInfo.Status.PLAYED,
        "read": WAProto.WebMessageInfo.Status.READ,
        "read-self": WAProto.WebMessageInfo.Status.READ,
    }
    if type_ is None:
        return WAProto.WebMessageInfo.Status.DELIVERY_ACK
    return STATUS_MAP.get(type_)


def get_error_code_from_stream_error(node):
    from ..Types import DisconnectReason

    children = get_all_binary_node_children(node)
    reason_node = children[0] if children else None
    reason = reason_node.tag if reason_node else "unknown"
    code = (node.attrs or {}).get("code")
    CODE_MAP = {"conflict": DisconnectReason.connectionReplaced}
    if code is None:
        code = CODE_MAP.get(reason, DisconnectReason.badSession)
    try:
        status_code = int(code)
    except (TypeError, ValueError):
        status_code = CODE_MAP.get(reason, DisconnectReason.badSession)
    if status_code == DisconnectReason.restartRequired:
        reason = "restart required"
    return {"reason": reason, "statusCode": status_code}


def get_call_status_from_node(node):
    tag = node.tag
    attrs = node.attrs or {}
    if tag in ("offer", "offer_notice"):
        return "offer"
    if tag == "terminate":
        return "timeout" if attrs.get("reason") == "timeout" else "terminate"
    if tag == "preaccept":
        return "preaccept"
    if tag == "transport":
        return "transport"
    if tag == "relaylatency":
        return "relaylatency"
    if tag == "reject":
        return "reject"
    if tag == "accept":
        return "accept"
    return "ringing"


UNEXPECTED_SERVER_CODE_TEXT = "Unexpected server response: "


def get_code_from_ws_error(error) -> int:
    status_code = 500
    message = getattr(error, "message", None) or str(error)
    if message and UNEXPECTED_SERVER_CODE_TEXT in message:
        try:
            code = int(message[len(UNEXPECTED_SERVER_CODE_TEXT):])
            if not (code != code or code == float("inf")) and code >= 400:
                status_code = code
        except ValueError:
            pass
    elif (getattr(error, "code", "") or "").startswith("E") or ("timed out" in message):
        status_code = 408
    return status_code


def is_wa_business_platform(platform: str) -> bool:
    return platform == "smbi" or platform == "smba"


def trim_undefined(obj: dict) -> dict:
    for key in list(obj.keys()):
        if obj[key] is None:
            del obj[key]
    return obj


CROCKFORD_CHARACTERS = "123456789ABCDEFGHJKLMNPQRSTVWXYZ"


def bytes_to_crockford(buffer: bytes) -> str:
    value = 0
    bit_count = 0
    crockford = []
    for element in buffer:
        value = (value << 8) | (element & 0xFF)
        bit_count += 8
        while bit_count >= 5:
            crockford.append(CROCKFORD_CHARACTERS[(value >> (bit_count - 5)) & 31])
            bit_count -= 5
    if bit_count > 0:
        crockford.append(CROCKFORD_CHARACTERS[(value << (5 - bit_count)) & 31])
    return "".join(crockford)


def encode_newsletter_message(message) -> bytes:
    from ..WAProto import WAProto

    return WAProto.Message.encode(message)


async def fetch_latest_baileys_version(options=None):
    url = "https://raw.githubusercontent.com/WhiskeySockets/Baileys/master/src/Defaults/index.ts"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8")
        lines = text.split("\n")
        version_line = lines[6] if len(lines) > 6 else ""
        m = re.match(r"const version = \[(\d+),\s*(\d+),\s*(\d+)\]", version_line)
        if m:
            return {"version": [int(m.group(1)), int(m.group(2)), int(m.group(3))], "isLatest": True}
        raise ValueError("Could not parse version from Defaults/index.ts")
    except Exception as error:
        return {"version": [2, 3000, 1043857760], "isLatest": False, "error": error}


async def fetch_latest_wa_web_version(options=None):
    try:
        headers = {
            "sec-fetch-site": "none",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            ),
        }
        req = urllib.request.Request("https://web.whatsapp.com/sw.js", headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8")
        regex = re.compile(r'\\?"client_revision\\?":\s*(\d+)')
        match = regex.search(data)
        if not match:
            return {
                "version": [2, 3000, 1043857760],
                "isLatest": False,
                "error": {"message": "Could not find client revision in the fetched content"},
            }
        client_revision = match.group(1)
        return {"version": [2, 3000, int(client_revision)], "isLatest": True}
    except Exception as error:
        return {"version": [2, 3000, 1043857760], "isLatest": False, "error": error}






def bind_wait_for_event(ev, event):
    async def waiter(check, timeout_ms=None):
        from ..Types import DisconnectReason

        loop = asyncio.get_event_loop()
        future = loop.create_future()
        listeners_registered = {'on': False}

        def _cleanup():
            if listeners_registered['on']:
                ev.off('connection.update', close_listener)
                ev.off(event, listener)
                listeners_registered['on'] = False

        def close_listener(connection_state):
            if connection_state.get('connection') == 'close':
                last_disconnect = connection_state.get('lastDisconnect') or {}
                error = last_disconnect.get('error') or Boom(
                    'Connection Closed', status_code=DisconnectReason.connectionClosed
                )
                _cleanup()
                if not future.done():
                    future.set_exception(error)

        def listener(update):
            if future.done():
                return
            try:
                check_result = check(update)
                if asyncio.iscoroutine(check_result):
                    result = None

                    async def _consume():
                        nonlocal result
                        result = await check_result

                    task = loop.create_task(_consume())
                    task.add_done_callback(lambda t: _resolve_if_true(result))
                    return
                result = check_result
            except Exception:
                result = None
            _resolve_if_true(result)

        def _resolve_if_true(result):
            if result and not future.done():
                _cleanup()
                future.set_result(True)

        ev.on('connection.update', close_listener)
        ev.on(event, listener)
        listeners_registered['on'] = True

        if timeout_ms is not None:
            handle = loop.call_later(timeout_ms / 1000.0, lambda: _cleanup() or future.done() or future.set_result(False))
            try:
                return await future
            finally:
                handle.cancel()
        else:
            return await future

    return waiter


def bind_wait_for_connection_update(ev):
    return bind_wait_for_event(ev, 'connection.update')
