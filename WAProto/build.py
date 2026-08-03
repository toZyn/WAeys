"""Build the generated WAProto.py module from WAProto.proto.

Usage: python -m WAeys.WAProto.build

The generated module exposes every message/enum class at top level plus
protobufjs-style nesting. A `_link()` pass at import time patches each
FieldDescriptor with its resolved message_cls / enum_cls by walking the
module namespace (classes/enums are created in dependency order).
"""
import enum
import io
import os

try:
    from .generator import generate as build_classes
    from .runtime import Message, FieldDescriptor
except ImportError:
    from generator import generate as build_classes
    from runtime import Message, FieldDescriptor

MessageBase = Message

try:
    from pathlib import Path
    HERE = str(Path(__file__).resolve().parent)
except Exception:
    HERE = os.path.dirname(os.path.abspath(__file__))

HEADER = '''"""Generated from WAProto.proto — do not edit by hand.

Pure-Python protobuf classes (see runtime.py). Enums are enum.IntEnum.
The base is aliased as MessageBase so the proto's own `Message` type
cannot shadow it in the module namespace.
"""
import enum

from .runtime import Message as MessageBase, FieldDescriptor

'''

LINK_CODE = '''

# --- post-linking: resolve message_cls / enum_cls references ---

def _walk_classes(cls):
    yield cls
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, type) and issubclass(attr, MessageBase) and attr is not MessageBase:
            yield from _walk_classes(attr)


def _find_in_namespace(root, path_parts):
    node = root
    for part in path_parts:
        if isinstance(node, dict):
            node = node.get(part)
        else:
            node = getattr(node, part, None)
        if node is None:
            return None
    return node


def _link():
    # module globals serve as the top-level namespace
    root = {name: obj for name, obj in globals().items()
            if isinstance(obj, type) and (issubclass(obj, MessageBase) or issubclass(obj, enum.IntEnum))}
    seen = set()
    for name, obj in root.items():
        if not (isinstance(obj, type) and issubclass(obj, MessageBase)):
            continue
        for cls in _walk_classes(obj):
            if id(cls) in seen:
                continue
            seen.add(id(cls))
            for fd in cls.FIELDS.values():
                if fd.field_type == "message" and fd._msg_path is not None:
                    fd.message_cls = _find_in_namespace(root, fd._msg_path.split("."))
                elif fd.field_type == "enum" and fd._enum_path is not None:
                    fd.enum_cls = _find_in_namespace(root, fd._enum_path.split("."))
                elif fd.field_type == "map":
                    mv = fd.map_value
                    if mv.field_type == "message" and mv._msg_path is not None:
                        mv.message_cls = _find_in_namespace(root, mv._msg_path.split("."))
                    elif mv.field_type == "enum" and mv._enum_path is not None:
                        mv.enum_cls = _find_in_namespace(root, mv._enum_path.split("."))


_link()
'''


def _enum_source(cls, name, indent=0):
    pad = " " * indent
    lines = [f"{pad}class {name}(enum.IntEnum):"]
    members = list(cls.__members__.items())
    if not members:
        lines.append(f"{pad}    pass")
    for vname, vmem in members:
        lines.append(f"{pad}    {vname} = {vmem.value}")
    return lines


def _message_source(cls, name, indent=0, seen=None):
    if seen is None:
        seen = set()
    pad = " " * indent
    lines = [f"{pad}class {name}(MessageBase):"]
    body = []
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, type) and issubclass(attr, enum.IntEnum):
            body.extend(_enum_source(attr, attr_name, indent + 4))
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, type) and issubclass(attr, MessageBase) and attr is not MessageBase:
            if id(attr) in seen:
                continue
            seen.add(id(attr))
            body.extend(_message_source(attr, attr_name, indent + 4, seen))
    body.extend(_fields_source(cls, indent + 4))
    if not body:
        lines.append(f"{pad}    pass")
    else:
        lines.extend(body)
    return lines


def _fields_source(cls, indent):
    pad = " " * indent
    lines = [f"{pad}FIELDS = {{"]
    for fname, fd in cls.FIELDS.items():
        if fd.field_type == "map":
            mv = fd.map_value
            val = (f'FieldDescriptor({fname!r}, {fd.number}, "map", repeated=True, '
                   f'map_key_type={mv.map_key_type!r}, map_value=FieldDescriptor("value", 2, {mv.field_type!r}))')
        else:
            val = (f'FieldDescriptor({fname!r}, {fd.number}, {fd.field_type!r}, '
                   f'repeated={fd.repeated}, packed={fd.packed})')
        lines.append(f"{pad}    {fname!r}: {val},")
    lines.append(f"{pad}}}")
    lines.append(f"{pad}_BY_NUMBER = {{fd.number: name for name, fd in FIELDS.items()}}")
    return lines


def _mark_paths(cls, prefix, msg_paths, enum_paths):
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, type) and issubclass(attr, enum.IntEnum):
            enum_paths.add(f"{prefix}.{attr_name}")
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, type) and issubclass(attr, MessageBase) and attr is not MessageBase:
            msg_paths.add(f"{prefix}.{attr_name}")
            _mark_paths(attr, f"{prefix}.{attr_name}", msg_paths, enum_paths)


def _needs_path(ftype, msg_paths, enum_paths):
    """Return ("message", path) / ("enum", path) / None for a bare type name."""
    for path in msg_paths:
        if path.split(".")[-1] == ftype:
            return ("message", path)
    for path in enum_paths:
        if path.split(".")[-1] == ftype:
            return ("enum", path)
    return None


def generate_module_text(namespace):
    out = io.StringIO()
    out.write(HEADER)

    # collect path sets for resolution of bare field type names
    msg_paths = set()
    enum_paths = set()
    for name, cls in namespace.items():
        if isinstance(cls, type) and issubclass(cls, Message) and cls is not Message:
            msg_paths.add(name)
            _mark_paths(cls, name, msg_paths, enum_paths)
    for name, cls in namespace.items():
        if isinstance(cls, type) and issubclass(cls, enum.IntEnum):
            enum_paths.add(name)

    # top-level enums first
    for name, cls in namespace.items():
        if isinstance(cls, type) and issubclass(cls, enum.IntEnum):
            for line in _enum_source(cls, name):
                out.write(line + "\n")
            out.write("\n")

    # top-level messages with explicit path annotations on FIELDS
    for name, cls in namespace.items():
        if isinstance(cls, type) and issubclass(cls, Message) and cls is not Message:
            for line in _message_source_paths(cls, name, msg_paths, enum_paths):
                out.write(line + "\n")
            out.write("\n")

    out.write(LINK_CODE)
    return out.getvalue()


def _message_source_paths(cls, name, msg_paths, enum_paths, indent=0, seen=None):
    if seen is None:
        seen = set()
    pad = " " * indent
    lines = [f"{pad}class {name}(MessageBase):"]
    body = []
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, type) and issubclass(attr, enum.IntEnum):
            body.extend(_enum_source(attr, attr_name, indent + 4))
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, type) and issubclass(attr, MessageBase) and attr is not MessageBase:
            if id(attr) in seen:
                continue
            seen.add(id(attr))
            body.extend(_message_source_paths(attr, attr_name, msg_paths, enum_paths, indent + 4, seen))
    body.extend(_fields_source_paths(cls, indent + 4, msg_paths, enum_paths))
    if not body:
        lines.append(f"{pad}    pass")
    else:
        lines.extend(body)
    return lines


def _fields_source_paths(cls, indent, msg_paths, enum_paths):
    pad = " " * indent
    lines = [f"{pad}FIELDS = {{"]
    for fname, fd in cls.FIELDS.items():
        if fd.field_type == "map":
            mv = fd.map_value
            if mv.field_type == "message":
                p = repr(mv._msg_path) if mv._msg_path is not None else "None"
                val = (f'FieldDescriptor({fname!r}, {fd.number}, "map", repeated=True, '
                       f'map_key_type={fd.map_key_type!r}, map_value=FieldDescriptor("value", 2, "message", _msg_path={p}))')
            elif mv.field_type == "enum":
                p = repr(mv._enum_path) if mv._enum_path is not None else "None"
                val = (f'FieldDescriptor({fname!r}, {fd.number}, "map", repeated=True, '
                       f'map_key_type={fd.map_key_type!r}, map_value=FieldDescriptor("value", 2, "enum", _enum_path={p}))')
            else:
                val = (f'FieldDescriptor({fname!r}, {fd.number}, "map", repeated=True, '
                       f'map_key_type={fd.map_key_type!r}, map_value=FieldDescriptor("value", 2, {mv.field_type!r}))')
        elif fd.field_type == "message":
            if fd._msg_path is not None:
                val = (f'FieldDescriptor({fname!r}, {fd.number}, "message", repeated={fd.repeated}, '
                       f'packed={fd.packed}, _msg_path={fd._msg_path!r})')
            else:
                val = (f'FieldDescriptor({fname!r}, {fd.number}, "message", repeated={fd.repeated}, '
                       f'packed={fd.packed})')
        elif fd.field_type == "enum":
            if fd._enum_path is not None:
                val = (f'FieldDescriptor({fname!r}, {fd.number}, "enum", repeated={fd.repeated}, '
                       f'packed={fd.packed}, _enum_path={fd._enum_path!r})')
            else:
                val = (f'FieldDescriptor({fname!r}, {fd.number}, "enum", repeated={fd.repeated}, '
                       f'packed={fd.packed})')
        else:
            val = (f'FieldDescriptor({fname!r}, {fd.number}, {fd.field_type!r}, '
                   f'repeated={fd.repeated}, packed={fd.packed})')
        lines.append(f"{pad}    {fname!r}: {val},")
    lines.append(f"{pad}}}")
    lines.append(f"{pad}_BY_NUMBER = {{fd.number: name for name, fd in FIELDS.items()}}")
    return lines


def build():
    ns = build_classes()
    text = generate_module_text(ns)
    output_path = os.path.join(HERE, "WAProto.py")
    with open(output_path, "w") as fh:
        fh.write(text)
    print("wrote", output_path)


if __name__ == "__main__":
    build()
