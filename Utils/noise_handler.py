"""Noise_XX_25519_AESGCM_SHA256 transport mirroring src/Utils/noise-handler.ts.

Handles the WhatsApp Web Noise handshake: hash/salt/encKey/decKey chaining,
AES-GCM frames with 3-byte length prefix, and the Transport state with
12-byte counter-based IVs (big-endian counter in bytes 8..11).
"""
from .crypto import (
    Curve,
    aes_decrypt_gcm,
    aes_encrypt_gcm,
    hkdf,
    sha256,
    x25519_shared_key,
)
from .logger import ILogger
from ..Defaults import NOISE_MODE, WA_CERT_DETAILS
from ..WABinary.decode import decode_binary_node

IV_LENGTH = 12

EMPTY_BUFFER = b""


def _generate_iv(counter: int) -> bytes:
    iv = bytearray(IV_LENGTH)
    iv[8] = (counter >> 24) & 0xFF
    iv[9] = (counter >> 16) & 0xFF
    iv[10] = (counter >> 8) & 0xFF
    iv[11] = counter & 0xFF
    return bytes(iv)


def _as_dict(obj):
    """Normalize a decoded protobuf Message (or dict) to plain dicts."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: _as_dict(v) for k, v in obj.items()}
    if hasattr(obj, 'FIELDS'):
        out = {}
        for name in obj.FIELDS:
            value = getattr(obj, name, None)
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                out[name] = [_as_dict(item) for item in value]
            else:
                out[name] = _as_dict(value)
        return out
    return obj


class TransportState:
    def __init__(self, enc_key: bytes, dec_key: bytes):
        self._read_counter = 0
        self._write_counter = 0
        self._iv = bytearray(IV_LENGTH)
        self.enc_key = enc_key
        self.dec_key = dec_key

    def encrypt(self, plaintext: bytes) -> bytes:
        c = self._write_counter
        self._write_counter += 1
        self._iv[8] = (c >> 24) & 0xFF
        self._iv[9] = (c >> 16) & 0xFF
        self._iv[10] = (c >> 8) & 0xFF
        self._iv[11] = c & 0xFF
        return aes_encrypt_gcm(plaintext, self.enc_key, bytes(self._iv), EMPTY_BUFFER)

    def decrypt(self, ciphertext: bytes) -> bytes:
        c = self._read_counter
        self._read_counter += 1
        self._iv[8] = (c >> 24) & 0xFF
        self._iv[9] = (c >> 16) & 0xFF
        self._iv[10] = (c >> 8) & 0xFF
        self._iv[11] = c & 0xFF
        return aes_decrypt_gcm(ciphertext, self.dec_key, bytes(self._iv), EMPTY_BUFFER)


class NoiseHandler:
    def __init__(self, key_pair: dict, noise_header: bytes, logger: ILogger,
                 routing_info: bytes = None):
        self.logger = logger.child({"class": "ns"})
        self.private_key = key_pair["private"]
        self.public_key = key_pair["public"]

        data = bytes(NOISE_MODE.encode("utf-8"))
        self.hash = data if len(data) == 32 else sha256(data)
        self.salt = self.hash
        self.enc_key = self.hash
        self.dec_key = self.hash
        self.counter = 0
        self.sent_intro = False

        self.in_bytes = b""
        self.transport = None
        self.is_waiting_for_transport = False
        self.pending_on_frame = None

        if routing_info is not None:
            self.intro_header = bytearray(7 + len(routing_info) + len(noise_header))
            self.intro_header[0:2] = b"ED"
            self.intro_header[2] = 0
            self.intro_header[3] = 1
            self.intro_header[4] = (len(routing_info) >> 16) & 0xFF
            self.intro_header[5] = (len(routing_info) >> 8) & 0xFF
            self.intro_header[6] = len(routing_info) & 0xFF
            self.intro_header[7:7 + len(routing_info)] = routing_info
            self.intro_header[7 + len(routing_info):] = noise_header
            self.intro_header = bytes(self.intro_header)
        else:
            self.intro_header = bytes(noise_header)

        self.authenticate(noise_header)
        self.authenticate(self.public_key)

    def authenticate(self, data: bytes) -> None:
        if not self.transport:
            self.hash = sha256(self.hash + data)

    def encrypt(self, plaintext: bytes) -> bytes:
        if self.transport is not None:
            return self.transport.encrypt(plaintext)
        result = aes_encrypt_gcm(plaintext, self.enc_key, _generate_iv(self.counter), self.hash)
        self.counter += 1
        self.authenticate(result)
        return result

    def decrypt(self, ciphertext: bytes) -> bytes:
        if self.transport is not None:
            return self.transport.decrypt(ciphertext)
        result = aes_decrypt_gcm(ciphertext, self.dec_key, _generate_iv(self.counter), self.hash)
        self.counter += 1
        self.authenticate(ciphertext)
        return result

    def _local_hkdf(self, data: bytes):
        key = hkdf(data, num_bytes=64, salt=self.salt, info=b"")
        return key[:32], key[32:]

    def mix_into_key(self, data: bytes) -> None:
        write, read = self._local_hkdf(data)
        self.salt = write
        self.enc_key = read
        self.dec_key = read
        self.counter = 0

    async def finish_init(self) -> None:
        self.is_waiting_for_transport = True
        write, read = self._local_hkdf(b"")
        self.transport = TransportState(write, read)
        self.is_waiting_for_transport = False

        self.logger.trace("Noise handler transitioned to Transport state")

        if self.pending_on_frame:
            self.logger.trace(
                {"length": len(self.in_bytes)}, "Flushing buffered frames after transport ready"
            )
            await self.process_data(self.pending_on_frame)
            self.pending_on_frame = None

    async def process_data(self, on_frame) -> None:
        while True:
            if len(self.in_bytes) < 3:
                return
            size = (self.in_bytes[0] << 16) | (self.in_bytes[1] << 8) | self.in_bytes[2]
            if len(self.in_bytes) < size + 3:
                return

            frame = self.in_bytes[3:size + 3]
            self.in_bytes = self.in_bytes[size + 3:]

            if self.transport is not None:
                result = self.transport.decrypt(frame)
                frame = decode_binary_node(result)

            if self.logger.level == "trace":
                attrs = getattr(frame, "attrs", None) or {}
                self.logger.trace({"msg": attrs.get("id")}, "recv frame")

            on_frame(frame)

    def process_handshake(self, server_hello, noise_key: dict) -> bytes:
        from ..WAProto import WAProto  # lazy: proto module dependency
        from ..WAProto.WAProto import CertChain

        server_hello = _as_dict(server_hello)

        self.authenticate(server_hello["ephemeral"])
        self.mix_into_key(x25519_shared_key(self.private_key, server_hello["ephemeral"]))

        dec_static_content = self.decrypt(server_hello["static"])
        self.mix_into_key(x25519_shared_key(self.private_key, dec_static_content))

        cert_decoded = self.decrypt(server_hello["payload"])

        cert = _as_dict(CertChain.decode(cert_decoded))
        cert_intermediate = _as_dict(cert["intermediate"])
        leaf = _as_dict(cert["leaf"])

        if not (leaf and leaf["details"] and leaf["signature"]):
            raise ValueError("invalid noise leaf certificate")

        if not (cert_intermediate and cert_intermediate["details"] and cert_intermediate["signature"]):
            raise ValueError("invalid noise intermediate certificate")

        details = _as_dict(CertChain.NoiseCertificate.Details.decode(cert_intermediate["details"]))
        issuer_serial = details.get("issuerSerial", details.get("serial"))

        verify = Curve.verify(details["key"], leaf["details"], leaf["signature"])
        verify_intermediate = Curve.verify(
            WA_CERT_DETAILS["PUBLIC_KEY"], cert_intermediate["details"], cert_intermediate["signature"]
        )

        if not verify:
            raise ValueError("noise certificate signature invalid")

        if not verify_intermediate:
            raise ValueError("noise intermediate certificate signature invalid")

        if issuer_serial != WA_CERT_DETAILS["SERIAL"]:
            raise ValueError("certification match failed")

        key_enc = self.encrypt(noise_key["public"])
        self.mix_into_key(x25519_shared_key(noise_key["private"], server_hello["ephemeral"]))

        return key_enc

    def encode_frame(self, data: bytes) -> bytes:
        if self.transport is not None:
            data = self.transport.encrypt(data)

        data_len = len(data)
        intro_size = 0 if self.sent_intro else len(self.intro_header)
        frame = bytearray(intro_size + 3 + data_len)

        if not self.sent_intro:
            frame[0:intro_size] = self.intro_header
            self.sent_intro = True

        frame[intro_size] = (data_len >> 16) & 0xFF
        frame[intro_size + 1] = (data_len >> 8) & 0xFF
        frame[intro_size + 2] = data_len & 0xFF

        frame[intro_size + 3:] = data
        return bytes(frame)

    async def decode_frame(self, new_data: bytes, on_frame) -> None:
        if self.is_waiting_for_transport:
            self.in_bytes = self.in_bytes + new_data
            self.pending_on_frame = on_frame
            return

        if len(self.in_bytes) == 0:
            self.in_bytes = bytes(new_data)
        else:
            self.in_bytes = self.in_bytes + new_data

        await self.process_data(on_frame)


def make_noise_handler(key_pair: dict, noise_header: bytes, logger: ILogger,
                       routing_info: bytes = None) -> NoiseHandler:
    return NoiseHandler(key_pair, noise_header, logger, routing_info)
