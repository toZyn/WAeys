"""Generator: parses WAProto.proto into Python Message/enum classes.

Supports proto3: optional/repeated labels, scalar + message + enum fields,
nested messages/enums, oneof groups (plain optional fields), map<k,v> (as
dict), and [packed=true].

Strategy: parse the whole file into a tree of definitions, register every
type under its fully-qualified path, then build classes in two passes so
field references resolve correctly (second pass links message_cls/enum_cls).
"""
import enum
import os
import re

try:
    from .runtime import Message, FieldDescriptor
except ImportError:
    from runtime import Message, FieldDescriptor

try:
    from pathlib import Path
    PROTO_PATH = str(Path(__file__).resolve().parent / "WAProto.proto")
except Exception:
    PROTO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "WAProto.proto")

SCALAR_TYPES = {
    "int32", "int64", "uint32", "uint64", "sint32", "sint64",
    "fixed32", "fixed64", "sfixed32", "sfixed64",
    "bool", "string", "bytes", "float", "double",
}


def _strip_comments_and_split(text: str):
    """Remove // and /* */ comments, preserving newlines; return token stream lines."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        if text[i:i + 2] == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl + 1
        elif text[i:i + 2] == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _tokenize(text: str):
    """Split proto into lexical tokens (identifiers, numbers, punctuation)."""
    text = _strip_comments_and_split(text)
    tokens = []
    i = 0
    n = len(text)
    pattern = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*|-?\d+|[{}<>=;,\(\)\[\]]|\"([^\"]*)\"|'([^']*)'")
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
            continue
        m = pattern.match(text, i)
        if not m:
            i += 1
            continue
        tok = m.group(0)
        tokens.append(tok)
        i = m.end()
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, tok):
        got = self.next()
        if got != tok:
            raise SyntaxError(f"expected {tok!r}, got {got!r} at token {self.pos}")

    def parse(self):
        """Returns (messages_tree, enums_tree)."""
        self.messages = {}
        self.enums = {}
        while self.pos < len(self.tokens):
            kw = self.next()
            if kw == "syntax":
                self.expect("=")
                self.next()  # "proto3"
                self.expect(";")
            elif kw == "package":
                self.next()
                self.expect(";")
            elif kw == "import":
                self.next()
                self.expect(";")
            elif kw == "option":
                self._skip_to_semicolon()
            elif kw == "message":
                name = self.next()
                self.messages[name] = self._parse_message()
            elif kw == "enum":
                name = self.next()
                self.enums[name] = self._parse_enum()
            else:
                self._skip_to_semicolon()
        return self.messages, self.enums

    def _skip_to_semicolon(self):
        while self.pos < len(self.tokens):
            if self.next() == ";":
                return

    def _parse_message(self):
        self.expect("{")
        mdef = {"fields": [], "messages": {}, "enums": {}, "oneofs": []}
        while True:
            tok = self.peek()
            if tok is None:
                break
            if tok == "}":
                self.next()
                break
            if tok == "message":
                self.next()
                name = self.next()
                mdef["messages"][name] = self._parse_message()
            elif tok == "enum":
                self.next()
                name = self.next()
                mdef["enums"][name] = self._parse_enum()
            elif tok == "oneof":
                self.next()
                oname = self.next()
                self.expect("{")
                while self.peek() != "}":
                    mdef["fields"].append(self._parse_field())
                self.expect("}")
                mdef["oneofs"].append(oname)
            elif tok == "map":
                self.next()
                self.expect("<")
                key_type = self.next()
                self.expect(",")
                value_type = self.next()
                self.expect(">")
                name = self.next()
                self.expect("=")
                number = int(self.next())
                self._consume_field_options()
                self.expect(";")
                mdef["fields"].append({
                    "label": "map", "type": value_type, "key_type": key_type,
                    "name": name, "number": number,
                })
            elif tok == "reserved" or tok == "extensions" or tok == "option":
                self._skip_to_semicolon()
            else:
                mdef["fields"].append(self._parse_field())
        return mdef

    def _consume_field_options(self):
        if self.peek() == "[":
            depth = 0
            while True:
                t = self.next()
                if t == "[":
                    depth += 1
                elif t == "]":
                    depth -= 1
                    if depth == 0:
                        return

    def _parse_field(self):
        label = "optional"
        tok = self.peek()
        if tok in ("optional", "repeated", "required"):
            self.next()
            label = tok
        ftype = self.next()
        name = self.next()
        self.expect("=")
        number = int(self.next())
        packed = False
        if self.peek() == "[":
            self.next()
            while True:
                opt = self.next()
                if opt == "packed":
                    self.expect("=")
                    packed = self.next() == "true"
                if opt == "]":
                    break
        self.expect(";")
        return {
            "label": label, "type": ftype, "name": name,
            "number": number, "packed": packed,
        }

    def _parse_enum(self):
        self.expect("{")
        values = []
        while True:
            tok = self.peek()
            if tok is None:
                break
            if tok == "}":
                self.next()
                break
            if tok == "option":
                self._skip_to_semicolon()
                continue
            name = self.next()
            self.expect("=")
            num = int(self.next())
            self.expect(";")
            values.append((name, num))
        return {"name": None, "values": values}


def _collect_registry(messages, enums):
    """Return {full_path: ("message", mdef)} and {full_path: ("enum", edef)}."""
    msg_reg = {}
    enum_reg = {}

    def walk(mdef, prefix):
        full = f"{prefix}.{mdef_name}" if prefix else mdef_name
        for mdef_name, sub in mdef["messages"].items():
            walk(sub, full)

    def walk_msg(mdef, path):
        msg_reg[path] = mdef
        for mname, sub in mdef["messages"].items():
            walk_msg(sub, f"{path}.{mname}")
        for ename, edef in mdef["enums"].items():
            enum_reg[f"{path}.{ename}"] = edef

    for mname, mdef in messages.items():
        walk_msg(mdef, mname)
    for ename, edef in enums.items():
        enum_reg[ename] = edef
    return msg_reg, enum_reg


def _resolve_path(name, msg_reg, enum_reg, scope):
    """Resolve a type name to a full path using the enclosing scope."""
    if name in SCALAR_TYPES:
        return name
    # try from innermost scope outward
    parts = scope.split(".") if scope else []
    for i in range(len(parts), -1, -1):
        prefix = ".".join(parts[:i])
        candidate = f"{prefix}.{name}" if prefix else name
        if candidate in msg_reg or candidate in enum_reg:
            return candidate
    return name


def _build_enum_class(edef, class_name):
    name = class_name.split(".")[-1]
    members = {}
    for vname, vnum in edef["values"]:
        members[vname] = vnum
    try:
        return enum.IntEnum(name, members)
    except ValueError:
        return enum.IntEnum(name, members, boundary=enum.KEEP)


def _build_message_class(mdef, class_name, msg_reg, enum_reg, scope):
    cls = type(class_name, (Message,), {})
    # build nested messages and enums first
    for mname, sub in mdef["messages"].items():
        sub_cls = _build_message_class(sub, f"{class_name}.{mname}", msg_reg, enum_reg,
                                       f"{scope}.{mname}" if scope else mname)
        setattr(cls, mname, sub_cls)
    for ename, edef in mdef["enums"].items():
        e_cls = _build_enum_class(edef, f"{class_name}.{ename}")
        setattr(cls, ename, e_cls)

    fields = {}
    for f in mdef["fields"]:
        if f["label"] == "map":
            map_value = _field_value_descriptor(f["type"], msg_reg, enum_reg, scope)
            fd = FieldDescriptor(
                f["name"], f["number"], "map", repeated=True,
                map_key_type=f["key_type"], map_value=map_value,
            )
        elif f["type"] in SCALAR_TYPES:
            fd = FieldDescriptor(f["name"], f["number"], f["type"],
                                 repeated=f["label"] == "repeated", packed=f["packed"])
        else:
            resolved = _resolve_path(f["type"], msg_reg, enum_reg, scope)
            if resolved in enum_reg:
                fd = FieldDescriptor(f["name"], f["number"], "enum",
                                     repeated=f["label"] == "repeated", packed=f["packed"])
                fd._enum_path = resolved
            else:
                fd = FieldDescriptor(f["name"], f["number"], "message",
                                     repeated=f["label"] == "repeated")
                fd._msg_path = resolved
        fields[f["name"]] = fd
    cls.FIELDS = fields
    cls._BY_NUMBER = {fd.number: name for name, fd in fields.items()}
    return cls


def _field_value_descriptor(ftype, msg_reg, enum_reg, scope):
    if ftype in SCALAR_TYPES:
        return FieldDescriptor("value", 2, ftype)
    resolved = _resolve_path(ftype, msg_reg, enum_reg, scope)
    if resolved in enum_reg:
        fd = FieldDescriptor("value", 2, "enum")
        fd._enum_path = resolved
        return fd
    fd = FieldDescriptor("value", 2, "message")
    fd._msg_path = resolved
    return fd


def _link_fields(namespace, msg_reg, enum_reg):
    """Patch FieldDescriptor.message_cls / enum_cls via the registry."""

    def link_cls(cls):
        for fd in cls.FIELDS.values():
            if fd.field_type == "map":
                link_fd(fd.map_value)
            elif fd.field_type == "message" and fd._msg_path is not None:
                link_fd(fd)
            elif fd.field_type == "enum" and fd._enum_path is not None:
                link_fd(fd)
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, type) and issubclass(attr, Message) and attr is not Message:
                link_cls(attr)

    def link_fd(fd):
        if fd.field_type == "message":
            fd.message_cls = _lookup_class(msg_reg[fd._msg_path], fd._msg_path, namespace, msg_reg, enum_reg)
        elif fd.field_type == "enum":
            fd.enum_cls = _lookup_enum(fd._enum_path, namespace, enum_reg)

    for name, cls in namespace.items():
        if isinstance(cls, type) and issubclass(cls, Message) and cls is not Message:
            link_cls(cls)


def _lookup_enum(path, namespace, enum_reg):
    parts = path.split(".")
    cur = namespace
    for i, part in enumerate(parts[:-1]):
        cur = cur.get(part) if isinstance(cur, dict) else getattr(cur, part, None)
        if cur is None:
            break
    if cur is not None:
        if isinstance(cur, dict):
            return cur.get(parts[-1])
        return getattr(cur, parts[-1], None)
    return None


def _lookup_class(mdef, path, namespace, msg_reg, enum_reg):
    def find_cls(node, parts):
        if not parts:
            return node
        attr = (node.get(parts[0]) if isinstance(node, dict) else getattr(node, parts[0], None))
        if attr is None:
            return None
        return find_cls(attr, parts[1:])

    return find_cls(namespace, path.split("."))


def generate():
    """Parse WAProto.proto and return a namespace dict of classes."""
    with open(PROTO_PATH, "r") as fh:
        text = fh.read()
    tokens = _tokenize(text)
    parser = Parser(tokens)
    messages, enums = parser.parse()

    msg_reg, enum_reg = _collect_registry(messages, enums)

    namespace = {}
    for ename, edef in enums.items():
        namespace[ename] = _build_enum_class(edef, ename)
    for mname, mdef in messages.items():
        namespace[mname] = _build_message_class(mdef, mname, msg_reg, enum_reg, mname)

    _link_fields(namespace, msg_reg, enum_reg)
    return namespace


if __name__ == "__main__":
    ns = generate()
    print("messages:", len([c for c in ns.values() if isinstance(c, type) and issubclass(c, Message) and c is not Message]))
    print("enums:", len([c for c in ns.values() if isinstance(c, enum.IntEnum)]))
