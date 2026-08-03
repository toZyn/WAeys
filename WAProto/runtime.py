"""Pure-Python protobuf wire codec + message base used by the generated WAProto module.

Mirrors the protobufjs semantics Baileys relies on:
  - proto.X.encode(obj) -> bytes (via .encode() classmethod returning bytes)
  - proto.X.decode(bytes) -> instance with attribute field access
  - enums are IntEnum (compare == int, reverse lookup by name)
  - maps become Python dicts, repeated become lists
"""
import struct

VARINT = 0
I64 = 1
LEN = 2
SGROUP = 3
EGROUP = 4
I32 = 5

WIRE_BY_FIELD_TYPE = {
    "int32": VARINT, "int64": VARINT, "uint32": VARINT, "uint64": VARINT,
    "sint32": VARINT, "sint64": VARINT, "bool": VARINT, "enum": VARINT,
    "fixed64": I64, "sfixed64": I64, "double": I64,
    "string": LEN, "bytes": LEN, "message": LEN,
    "fixed32": I32, "sfixed32": I32, "float": I32,
}


def encode_varint(value: int) -> bytes:
    value &= 0xFFFFFFFFFFFFFFFF
    out = bytearray()
    while value >= 0x80:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def decode_varint(buf, pos):
    result = 0
    shift = 0
    while True:
        if pos >= len(buf):
            raise ValueError("varint overflow / truncated")
        b = buf[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
        if shift > 63:
            raise ValueError("varint too long")
    return result, pos


def zigzag_encode(n: int) -> int:
    return (n << 1) ^ (n >> 63)


def zigzag_decode(n: int) -> int:
    return (n >> 1) ^ -(n & 1)


def encode_key(field_number: int, wire_type: int) -> bytes:
    return encode_varint((field_number << 3) | wire_type)


class Message:
    """Base class for generated proto messages.

    Field values are stored in instance attributes; unset optional fields
    read back as None. encode() returns the serialized bytes.
    """

    FIELDS = {}       # name -> FieldDescriptor
    _BY_NUMBER = {}   # number -> name
    _wkt = False

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self.FIELDS:
            return None
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return
        if name in self.FIELDS:
            object.__setattr__(self, name, value)
            return
        raise AttributeError(f"unknown field: {name}")

    # ----- encoding -----
    @classmethod
    def encode(cls, message) -> bytes:
        if not isinstance(message, cls):
            obj = cls()
            for k, v in (message.items() if hasattr(message, "items") else {}):
                setattr(obj, k, v)
            message = obj
        return message._encode()

    def _encode(self) -> bytes:
        parts = []
        for name, fd in self.FIELDS.items():
            value = getattr(self, name, None)
            if value is None:
                continue
            parts.append(_encode_field(fd, value))
        return b"".join(parts)

    def _encode_into(self, out: bytearray):
        for name, fd in self.FIELDS.items():
            value = getattr(self, name, None)
            if value is None:
                continue
            out += _encode_field(fd, value)

    @classmethod
    def from_object(cls, obj) -> "Message":
        """Mirror protobufjs' Message.fromObject: build a message from a plain dict."""
        if isinstance(obj, cls):
            return obj
        if not isinstance(obj, dict):
            raise TypeError(f"from_object expects a dict, got {type(obj).__name__}")
        message = cls()
        for k, v in obj.items():
            if k not in cls.FIELDS:
                continue
            fd = cls.FIELDS[k]
            if fd.field_type == 'message' and isinstance(v, dict) and fd.message_cls is not None:
                v = fd.message_cls.from_object(v)
            elif fd.field_type == 'message' and isinstance(v, list) and fd.message_cls is not None:
                v = [fd.message_cls.from_object(item) if isinstance(item, dict) else item for item in v]
            setattr(message, k, v)
        return message

    fromObject = from_object

    # ----- decoding -----
    @classmethod
    def decode(cls, buf) -> "Message":
        if isinstance(buf, memoryview):
            buf = bytes(buf)
        obj = cls()
        pos = 0
        while pos < len(buf):
            key, pos = decode_varint(buf, pos)
            field_number = key >> 3
            wire_type = key & 7
            name = cls._BY_NUMBER.get(field_number)
            fd = cls.FIELDS.get(name) if name else None
            if fd is None:
                # skip unknown field
                pos = _skip_field(buf, pos, wire_type)
                continue
            pos = _read_field(buf, pos, wire_type, fd, obj)
        return obj


class FieldDescriptor:
    __slots__ = ("name", "number", "field_type", "repeated", "packed",
                 "message_cls", "enum_cls", "map_key_type", "map_value",
                 "_msg_path", "_enum_path")

    def __init__(self, name, number, field_type, repeated=False, packed=False,
                 message_cls=None, enum_cls=None, map_key_type=None, map_value=None,
                 _msg_path=None, _enum_path=None):
        self.name = name
        self.number = number
        self.field_type = field_type  # scalar name, 'message', 'enum', 'map'
        self.repeated = repeated
        self.packed = packed
        self.message_cls = message_cls
        self.enum_cls = enum_cls
        self.map_key_type = map_key_type  # scalar type name for map key
        self.map_value = map_value        # FieldDescriptor-ish for map value
        self._msg_path = _msg_path
        self._enum_path = _enum_path

    def wire_type(self):
        if self.field_type == "map":
            return LEN
        return WIRE_BY_FIELD_TYPE[self.field_type]


def _encode_field(fd, value) -> bytes:
    out = bytearray()
    if fd.field_type == "map":
        # value: dict
        entries = []
        for k, v in (value or {}).items():
            entry = bytearray()
            entry += encode_key(1, WIRE_BY_FIELD_TYPE[fd.map_key_type])
            entry += _encode_scalar(fd.map_key_type, k)
            entry += encode_key(2, WIRE_BY_FIELD_TYPE[fd.map_value.field_type])
            entry += _encode_scalar_or_msg(fd.map_value, v)
            entries.append(b"".join([encode_key(fd.number, LEN), encode_varint(len(entry)), bytes(entry)]))
        return b"".join(entries)

    if fd.repeated:
        items = list(value)
        if fd.packed and fd.field_type in ("int32", "int64", "uint32", "uint64",
                                           "sint32", "sint64", "bool", "enum",
                                           "fixed32", "sfixed32", "fixed64", "sfixed64"):
            payload = b"".join(_encode_scalar(fd.field_type, v) for v in items)
            out += encode_key(fd.number, LEN)
            out += encode_varint(len(payload))
            out += payload
        else:
            for v in items:
                out += encode_key(fd.number, fd.wire_type())
                out += _encode_scalar_or_msg(fd, v)
        return bytes(out)

    out += encode_key(fd.number, fd.wire_type())
    out += _encode_scalar_or_msg(fd, value)
    return bytes(out)


def _encode_scalar_or_msg(fd, value) -> bytes:
    if fd.field_type == "message":
        payload = fd.message_cls.encode(value) if not isinstance(value, fd.message_cls) else value._encode()
        return encode_varint(len(payload)) + payload
    if fd.field_type == "enum":
        if isinstance(value, int):
            return encode_varint(value)
        return encode_varint(int(value))
    return _encode_scalar(fd.field_type, value)


def _encode_scalar(ftype, value) -> bytes:
    if ftype in ("int32", "int64", "uint32", "uint64", "bool"):
        return encode_varint(int(value))
    if ftype == "sint32":
        return encode_varint(zigzag_encode(int(value)) & 0xFFFFFFFF)
    if ftype == "sint64":
        return encode_varint(zigzag_encode(int(value)))
    if ftype == "fixed32":
        return struct.pack("<I", int(value))
    if ftype == "sfixed32":
        return struct.pack("<i", int(value))
    if ftype == "fixed64":
        return struct.pack("<Q", int(value))
    if ftype == "sfixed64":
        return struct.pack("<q", int(value))
    if ftype == "float":
        return struct.pack("<f", float(value))
    if ftype == "double":
        return struct.pack("<d", float(value))
    if ftype == "string":
        if isinstance(value, bytes):
            b = value
        else:
            b = value.encode("utf-8")
        return encode_varint(len(b)) + b
    if ftype == "bytes":
        return encode_varint(len(bytes(value))) + bytes(value)
    raise ValueError(f"unknown scalar type: {ftype}")


def _read_field(buf, pos, wire_type, fd, obj):
    if fd.field_type == "map":
        return _read_map(buf, pos, fd, obj)

    if fd.repeated and not (fd.packed and wire_type == LEN):
        # unpacked element
        value, pos = _read_scalar_or_msg(buf, pos, wire_type, fd)
        lst = getattr(obj, fd.name, None)
        if lst is None:
            lst = []
            setattr(obj, fd.name, lst)
        lst.append(value)
        return pos

    if fd.repeated and fd.packed and wire_type == LEN:
        length, pos = decode_varint(buf, pos)
        end = pos + length
        lst = getattr(obj, fd.name, None)
        if lst is None:
            lst = []
            setattr(obj, fd.name, lst)
        while pos < end:
            value, pos = _read_scalar_plain(buf, pos, fd.field_type)
            lst.append(value)
        return pos

    # single value (last-wins semantics)
    value, pos = _read_scalar_or_msg(buf, pos, wire_type, fd)
    setattr(obj, fd.name, value)
    return pos


def _read_scalar_or_msg(buf, pos, wire_type, fd):
    if fd.field_type == "message":
        length, pos = decode_varint(buf, pos)
        payload = bytes(buf[pos:pos + length])
        return fd.message_cls.decode(payload), pos + length
    if fd.field_type == "enum":
        value, pos = decode_varint(buf, pos)
        try:
            return fd.enum_cls(value), pos
        except ValueError:
            return value, pos
    return _read_scalar_plain(buf, pos, fd.field_type)


def _read_scalar_plain(buf, pos, ftype):
    if ftype in ("int32", "int64", "uint32", "uint64", "bool"):
        value, pos = decode_varint(buf, pos)
        if ftype == "bool":
            return bool(value), pos
        if ftype in ("int32", "int64"):
            return (value - (1 << 64)) if value >= (1 << 63) else value, pos
        return value, pos
    if ftype == "sint32":
        value, pos = decode_varint(buf, pos)
        return zigzag_decode(value & 0xFFFFFFFF) if value else zigzag_decode(value), pos
    if ftype == "sint64":
        value, pos = decode_varint(buf, pos)
        return zigzag_decode(value), pos
    if ftype == "fixed32":
        return struct.unpack_from("<I", buf, pos)[0], pos + 4
    if ftype == "sfixed32":
        return struct.unpack_from("<i", buf, pos)[0], pos + 4
    if ftype == "fixed64":
        return struct.unpack_from("<Q", buf, pos)[0], pos + 8
    if ftype == "sfixed64":
        return struct.unpack_from("<q", buf, pos)[0], pos + 8
    if ftype == "float":
        return struct.unpack_from("<f", buf, pos)[0], pos + 4
    if ftype == "double":
        return struct.unpack_from("<d", buf, pos)[0], pos + 8
    if ftype == "string":
        length, pos = decode_varint(buf, pos)
        return bytes(buf[pos:pos + length]).decode("utf-8"), pos + length
    if ftype == "bytes":
        length, pos = decode_varint(buf, pos)
        return bytes(buf[pos:pos + length]), pos + length
    raise ValueError(f"unknown scalar type: {ftype}")


def _read_map(buf, pos, fd, obj):
    length, pos = decode_varint(buf, pos)
    end = pos + length
    k = None
    v = None
    while pos < end:
        key, pos = decode_varint(buf, pos)
        field_number = key >> 3
        wire_type = key & 7
        if field_number == 1:
            k, pos = _read_scalar_plain(buf, pos, fd.map_key_type)
        elif field_number == 2:
            v, pos = _read_scalar_or_msg(buf, pos, wire_type, fd.map_value)
        else:
            pos = _skip_field(buf, pos, wire_type)
    d = getattr(obj, fd.name, None)
    if d is None:
        d = {}
        setattr(obj, fd.name, d)
    d[k] = v
    return pos


def _skip_field(buf, pos, wire_type):
    if wire_type == VARINT:
        _, pos = decode_varint(buf, pos)
        return pos
    if wire_type == I64:
        return pos + 8
    if wire_type == LEN:
        length, pos = decode_varint(buf, pos)
        return pos + length
    if wire_type == I32:
        return pos + 4
    raise ValueError(f"unsupported wire type {wire_type}")
