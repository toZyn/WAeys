"""Pure-Python implementations of the crypto primitives used by Baileys.

This module replaces Node's `crypto` + `libsignal` + `whatsapp-rust-bridge`
without any external native dependencies. Everything here is standard
Python (`hashlib`, `hmac`, `secrets`) plus self-contained pure-Python
implementations of AES, X25519, and Ed25519.
"""

import hashlib
import hmac as _hmac
import secrets

KEY_BUNDLE_TYPE = b'\x05'


# ---------------------------------------------------------------------------
# AES (pure Python, FIPS-197)
# ---------------------------------------------------------------------------

_SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]

_INV_SBOX = [
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
]

_RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D]


def _xtime(a):
    a <<= 1
    if a & 0x100:
        a ^= 0x11B
    return a & 0xFF


def _gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


class _AES:
    """AES block cipher (128/192/256)."""

    def __init__(self, key: bytes):
        self._n_b = 4
        self._n_k = len(key) // 4
        self._n_r = {4: 10, 6: 12, 8: 14}[self._n_k]
        self._round_keys = self._expand_key(list(key))

    def _expand_key(self, key: list):
        n_k, n_b, n_r = self._n_k, self._n_b, self._n_r
        w = []
        for i in range(n_k):
            w.append(key[4 * i:4 * i + 4])
        for i in range(n_k, n_b * (n_r + 1)):
            temp = list(w[i - 1])
            if i % n_k == 0:
                temp = temp[1:] + temp[:1]
                temp = [_SBOX[b] for b in temp]
                temp[0] ^= _RCON[i // n_k - 1]
            elif n_k > 6 and i % n_k == 4:
                temp = [_SBOX[b] for b in temp]
            w.append([w[i - n_k][j] ^ temp[j] for j in range(4)])
        # flatten to a single 16*(n_r+1) byte round-key array
        flat = []
        for word in w:
            flat.extend(word)
        return flat

    # state is a flat 16-byte list; byte[r + 4*c] == AES state[r][c]
    def _add_round_key(self, state, rk):
        return [state[i] ^ rk[i] for i in range(16)]

    def _sub_bytes(self, state, table):
        return [table[b] for b in state]

    def _inv_sub_bytes(self, state):
        return [_INV_SBOX[b] for b in state]

    def _shift_rows(self, state):
        return [
            state[0], state[5], state[10], state[15],
            state[4], state[9], state[14], state[3],
            state[8], state[13], state[2], state[7],
            state[12], state[1], state[6], state[11],
        ]

    def _inv_shift_rows(self, state):
        return [
            state[0], state[13], state[10], state[7],
            state[4], state[1], state[14], state[11],
            state[8], state[5], state[2], state[15],
            state[12], state[9], state[6], state[3],
        ]

    def _mix_columns(self, state):
        out = [0] * 16
        for c in range(4):
            a0, a1, a2, a3 = state[4 * c], state[4 * c + 1], state[4 * c + 2], state[4 * c + 3]
            out[4 * c] = _gmul(a0, 2) ^ _gmul(a1, 3) ^ a2 ^ a3
            out[4 * c + 1] = a0 ^ _gmul(a1, 2) ^ _gmul(a2, 3) ^ a3
            out[4 * c + 2] = a0 ^ a1 ^ _gmul(a2, 2) ^ _gmul(a3, 3)
            out[4 * c + 3] = _gmul(a0, 3) ^ a1 ^ a2 ^ _gmul(a3, 2)
        return out

    def _inv_mix_columns(self, state):
        out = [0] * 16
        for c in range(4):
            a0, a1, a2, a3 = state[4 * c], state[4 * c + 1], state[4 * c + 2], state[4 * c + 3]
            out[4 * c] = _gmul(a0, 14) ^ _gmul(a1, 11) ^ _gmul(a2, 13) ^ _gmul(a3, 9)
            out[4 * c + 1] = _gmul(a0, 9) ^ _gmul(a1, 14) ^ _gmul(a2, 11) ^ _gmul(a3, 13)
            out[4 * c + 2] = _gmul(a0, 13) ^ _gmul(a1, 9) ^ _gmul(a2, 14) ^ _gmul(a3, 11)
            out[4 * c + 3] = _gmul(a0, 11) ^ _gmul(a1, 13) ^ _gmul(a2, 9) ^ _gmul(a3, 14)
        return out

    def _encrypt_block(self, block: list) -> list:
        state = self._add_round_key(block, self._round_keys[:16])
        for rnd in range(1, self._n_r):
            state = self._sub_bytes(state, _SBOX)
            state = self._shift_rows(state)
            state = self._mix_columns(state)
            state = self._add_round_key(state, self._round_keys[16 * rnd:16 * rnd + 16])
        state = self._sub_bytes(state, _SBOX)
        state = self._shift_rows(state)
        state = self._add_round_key(state, self._round_keys[16 * self._n_r:16 * self._n_r + 16])
        return state

    def _decrypt_block(self, block: list) -> list:
        state = self._add_round_key(block, self._round_keys[16 * self._n_r:16 * self._n_r + 16])
        for rnd in range(self._n_r - 1, 0, -1):
            state = self._inv_shift_rows(state)
            state = self._inv_sub_bytes(state)
            state = self._add_round_key(state, self._round_keys[16 * rnd:16 * rnd + 16])
            state = self._inv_mix_columns(state)
        state = self._inv_shift_rows(state)
        state = self._inv_sub_bytes(state)
        state = self._add_round_key(state, self._round_keys[:16])
        return state

    def encrypt(self, data: bytes) -> bytes:
        assert len(data) % 16 == 0
        out = bytearray()
        for i in range(0, len(data), 16):
            out.extend(self._encrypt_block(list(data[i:i + 16])))
        return bytes(out)

    def decrypt(self, data: bytes) -> bytes:
        assert len(data) % 16 == 0
        out = bytearray()
        for i in range(0, len(data), 16):
            out.extend(self._decrypt_block(list(data[i:i + 16])))
        return bytes(out)


def _pad_pkcs7(data: bytes, block_size: int = 16) -> bytes:
    pad = block_size - (len(data) % block_size)
    return data + bytes([pad] * pad)


def _unpad_pkcs7(data: bytes) -> bytes:
    if not data:
        raise ValueError('empty')
    pad = data[-1]
    if pad < 1 or pad > 16:
        raise ValueError('invalid padding')
    return data[:-pad]


def aes_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """AES-256-CBC with PKCS7 padding applied (single-shot convenience)."""
    return aes_cbc_encrypt_raw(_pad_pkcs7(plaintext), key, iv)


def aes_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """AES-256-CBC decrypt and strip PKCS7 padding (single-shot convenience)."""
    return _unpad_pkcs7(aes_cbc_decrypt_raw(ciphertext, key, iv))


def aes_cbc_encrypt_raw(data: bytes, key: bytes, iv: bytes) -> bytes:
    """Raw AES-256-CBC (no padding applied) — caller handles block alignment.

    Mirrors Node's crypto.createCipheriv('aes-256-cbc', key, iv).update()
    which only emits whole cipher blocks and never pads.
    """
    if len(iv) != 16:
        raise ValueError('iv must be 16 bytes')
    if len(data) % 16 != 0:
        raise ValueError('data not a multiple of block size')
    aes = _AES(key)
    prev = iv
    out = bytearray()
    for i in range(0, len(data), 16):
        block = bytes(a ^ b for a, b in zip(data[i:i + 16], prev))
        enc = aes.encrypt(block)
        out.extend(enc)
        prev = enc
    return bytes(out)


def aes_cbc_decrypt_raw(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """Raw AES-256-CBC decrypt (no padding stripped) — caller handles padding.

    Mirrors Node's crypto.createDecipheriv('aes-256-cbc', key, iv).update()
    with setAutoPadding(false), which never strips padding.
    """
    if len(iv) != 16:
        raise ValueError('iv must be 16 bytes')
    if len(ciphertext) % 16 != 0:
        raise ValueError('ciphertext not a multiple of block size')
    aes = _AES(key)
    prev = iv
    out = bytearray()
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i + 16]
        dec = aes.decrypt(block)
        out.extend(bytes(a ^ b for a, b in zip(dec, prev)))
        prev = block
    return bytes(out)


def aes_ctr_crypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    """AES-256-CTR (native byte counter, no padding)."""
    if len(iv) != 16:
        raise ValueError('iv must be 16 bytes')
    aes = _AES(key)
    out = bytearray()
    counter = bytearray(iv)
    for i in range(0, len(data), 16):
        keystream = aes.encrypt(bytes(counter))
        chunk = data[i:i + 16]
        out.extend(bytes(a ^ b for a, b in zip(chunk, keystream)))
        # increment counter (128-bit big-endian)
        for j in range(15, -1, -1):
            counter[j] = (counter[j] + 1) & 0xFF
            if counter[j] != 0:
                break
    return bytes(out)


def _gf_mul(a: int, b: int) -> int:
    """Multiply in GF(2^128) with poly 0x87 (for GHASH).

    NIST SP 800-38D algorithm: iterate bits of `b` MSB-first,
    shift `v` right and reduce when its LSB is set.
    """
    z = 0
    v = a
    r = 0xE1000000000000000000000000000000
    for i in range(128):
        if (b >> (127 - i)) & 1:
            z ^= v
        if v & 1:
            v = (v >> 1) ^ r
        else:
            v >>= 1
    return z


def _ghash(h: bytes, blocks: bytes) -> bytes:
    y = 0
    h_int = int.from_bytes(h, 'big')
    for i in range(0, len(blocks), 16):
        block = int.from_bytes(blocks[i:i + 16], 'big')
        y = _gf_mul(h_int, y ^ block)
    return y.to_bytes(16, 'big')


def _gcm_j0(aes, iv: bytes) -> bytes:
    """Pre-counter block J0 per NIST SP 800-38D step 2."""
    if len(iv) == 12:
        return iv + b'\x00\x00\x00\x01'
    s = 128 * ((len(iv) + 15) // 16) - len(iv) * 8
    h = aes.encrypt(bytes(16))
    gh = _ghash(h, iv + bytes(s // 8 + 8) + (len(iv) * 8).to_bytes(8, 'big'))
    return gh


def _gcm_counter_start(aes, iv: bytes) -> bytearray:
    j0 = bytearray(_gcm_j0(aes, iv))
    for j in range(15, 11, -1):
        j0[j] = (j0[j] + 1) & 0xFF
        if j0[j] != 0:
            break
    return j0


def _gcm_tag(ciphertext: bytes, key: bytes, iv: bytes, additional_data: bytes, h: bytes) -> bytes:
    aad_pad = additional_data + bytes((-len(additional_data)) % 16)
    ct_pad = ciphertext + bytes((-len(ciphertext)) % 16)
    lens = (len(additional_data) * 8).to_bytes(8, 'big') + (len(ciphertext) * 8).to_bytes(8, 'big')
    tag = _ghash(h, aad_pad + ct_pad + lens)
    aes = _AES(key)
    j0 = _gcm_j0(aes, iv)
    return bytes(a ^ b for a, b in zip(tag, aes.encrypt(j0)))


def aes_gcm_encrypt(plaintext: bytes, key: bytes, iv: bytes, additional_data: bytes = b'') -> bytes:
    """AES-GCM; auth tag appended to ciphertext (matches Baileys)."""
    aes = _AES(key)
    h = aes.encrypt(bytes(16))

    counter = _gcm_counter_start(aes, iv)
    out = bytearray()
    for i in range(0, len(plaintext), 16):
        ks = aes.encrypt(bytes(counter))
        chunk = plaintext[i:i + 16]
        out.extend(bytes(a ^ b for a, b in zip(chunk, ks)))
        for j in range(15, 11, -1):
            counter[j] = (counter[j] + 1) & 0xFF
            if counter[j] != 0:
                break

    tag = _gcm_tag(bytes(out), key, iv, additional_data, h)
    return bytes(out) + tag


def aes_gcm_decrypt(ciphertext: bytes, key: bytes, iv: bytes, additional_data: bytes = b'') -> bytes:
    if len(ciphertext) < 16:
        raise ValueError('ciphertext too short')
    ct, tag = ciphertext[:-16], ciphertext[-16:]
    aes = _AES(key)
    h = aes.encrypt(bytes(16))
    expected = _gcm_tag(ct, key, iv, additional_data, h)
    if not _hmac.compare_digest(expected, tag):
        raise ValueError('GCM authentication tag mismatch')

    # decrypt: same keystream as encryption, starting at inc32(J0)
    counter = _gcm_counter_start(aes, iv)
    out = bytearray()
    for i in range(0, len(ct), 16):
        ks = aes.encrypt(bytes(counter))
        chunk = ct[i:i + 16]
        out.extend(bytes(a ^ b for a, b in zip(chunk, ks)))
        for j in range(15, 11, -1):
            counter[j] = (counter[j] + 1) & 0xFF
            if counter[j] != 0:
                break
    return bytes(out)


# ---------------------------------------------------------------------------
# Hashes / MAC / KDF
# ---------------------------------------------------------------------------

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def sha512(data: bytes) -> bytes:
    return hashlib.sha512(data).digest()


def md5(data: bytes) -> bytes:
    return hashlib.md5(data).digest()


def hmac_sign(buffer: bytes, key: bytes, variant: str = 'sha256') -> bytes:
    digestmod = hashlib.sha256 if variant == 'sha256' else hashlib.sha512
    return _hmac.new(key, buffer, digestmod).digest()


def hkdf(input_key_material: bytes, num_bytes: int = 32, info: bytes = b'', salt: bytes = b'') -> bytes:
    """RFC 5869 HKDF."""
    if not salt:
        salt = bytes(32)
    prk = _hmac.new(salt, input_key_material, hashlib.sha256).digest()
    okm = b''
    t = b''
    counter = 1
    while len(okm) < num_bytes:
        t = _hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        okm += t
        counter += 1
    return okm[:num_bytes]


def pbkdf2_sha256(password: bytes, salt: bytes, iterations: int, length: int) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', password, salt, iterations, length)


# ---------------------------------------------------------------------------
# X25519 (Montgomery ladder, RFC 7748)
# ---------------------------------------------------------------------------

_P = 2 ** 255 - 19
_A24 = 121665


def _x25519(scalar: bytes, u: bytes) -> bytes:
    if len(scalar) != 32 or len(u) != 32:
        raise ValueError('x25519 requires 32-byte inputs')
    k = bytearray(scalar)
    k[0] &= 248
    k[31] &= 127
    k[31] |= 64

    x1 = int.from_bytes(u, 'little') % _P
    x2, z2 = 1, 0
    x3, z3 = x1, 1
    swap = 0

    for t in range(254, -1, -1):
        k_t = (k[t // 8] >> (t % 8)) & 1
        swap ^= k_t
        if swap:
            x2, x3 = x3, x2
            z2, z3 = z3, z2
        swap = k_t

        a = (x2 + z2) % _P
        aa = (a * a) % _P
        b = (x2 - z2) % _P
        bb = (b * b) % _P
        e = (aa - bb) % _P
        c = (x3 + z3) % _P
        d = (x3 - z3) % _P
        da = (d * a) % _P
        cb = (c * b) % _P
        x3 = ((da + cb) % _P) ** 2 % _P
        z3 = (x1 * ((da - cb) % _P) ** 2) % _P
        x2 = (aa * bb) % _P
        z2 = (e * ((aa + _A24 * e) % _P)) % _P

    if swap:
        x2, x3 = x3, x2
        z2, z3 = z3, z2

    return (x2 * pow(z2, _P - 2, _P) % _P).to_bytes(32, 'little')


def x25519_generate_key_pair() -> tuple:
    """Returns (private_key, public_key), 32 bytes each."""
    private = secrets.token_bytes(32)
    public = x25519_public_key(private)
    return private, public


def x25519_public_key(private: bytes) -> bytes:
    basepoint = bytearray(32)
    basepoint[0] = 9
    return _x25519(private, bytes(basepoint))


def x25519_shared_key(private: bytes, public: bytes) -> bytes:
    return _x25519(private, public)


# ---------------------------------------------------------------------------
# Ed25519 (RFC 8032) - for signed prekeys / certificates
# ---------------------------------------------------------------------------

_Q = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
_B = None


def _ed_recover_x(y):
    """Recover x coordinate from y (RFC 8032, Ed25519: -x^2 + y^2 = 1 + d x^2 y^2)."""
    d = 37095705934669439343138083508754565189542113879843219016388785533085940283555
    y2 = (y * y) % _Q
    xx = ((y2 - 1) * pow((d * y2 + 1) % _Q, _Q - 2, _Q)) % _Q
    x = pow(xx, (_Q + 3) // 8, _Q)
    if (x * x - xx) % _Q != 0:
        x = (x * pow(2, (_Q - 1) // 4, _Q)) % _Q
    if (x * x - xx) % _Q != 0:
        raise ValueError('point not on curve')
    if x % 2 != 0:
        x = _Q - x
    return x


def _ed_point_add(p, q):
    x1, y1 = p
    x2, y2 = q
    d = 37095705934669439343138083508754565189542113879843219016388785533085940283555
    x3 = ((x1 * y2 + x2 * y1) * pow(1 + d * x1 * x2 * y1 * y2, _Q - 2, _Q)) % _Q
    y3 = ((y1 * y2 + x1 * x2) * pow(1 - d * x1 * x2 * y1 * y2, _Q - 2, _Q)) % _Q
    return (x3, y3)


def _ed_point_scalar_mul(scalar, point):
    result = (0, 1)
    addend = point
    while scalar > 0:
        if scalar & 1:
            result = _ed_point_add(result, addend)
        addend = _ed_point_add(addend, addend)
        scalar >>= 1
    return result


def _ed_point_compress(point):
    x, y = point
    return (y | ((x & 1) << 255)).to_bytes(32, 'little')


def _ed_point_decompress(s):
    y = int.from_bytes(s, 'little') & ((1 << 255) - 1)
    x = _ed_recover_x(y)
    if x & 1 != (int.from_bytes(s, 'little') >> 255) & 1:
        x = _Q - x
    return (x, y)


def _ed_double_and_add(scalar, point):
    return _ed_point_scalar_mul(scalar, point)


_ED_BASE_Y = 4 * pow(5, _Q - 2, _Q) % _Q
_B = (_ed_recover_x(_ED_BASE_Y), _ED_BASE_Y)


def ed25519_generate_key_pair(seed: bytes | None = None) -> tuple:
    """Returns (public_key, private_key) — private is seed (32 bytes)."""
    seed = seed or secrets.token_bytes(32)
    h = hashlib.sha512(seed).digest()
    a = int.from_bytes(h[:32], 'little')
    a &= (1 << 254) - 8
    a |= 1 << 254
    public = _ed_point_compress(_ed_point_scalar_mul(a, _B))
    return public, seed


def ed25519_sign(message: bytes, private_key: bytes) -> bytes:
    h = hashlib.sha512(private_key).digest()
    a = int.from_bytes(h[:32], 'little')
    a &= (1 << 254) - 8
    a |= 1 << 254
    prefix = h[32:]
    r = int.from_bytes(hashlib.sha512(prefix + message).digest(), 'little') % _L
    r_point = _ed_point_scalar_mul(r, _B)
    r_enc = _ed_point_compress(r_point)
    k = int.from_bytes(hashlib.sha512(r_enc + _ed_point_compress(_ed_point_scalar_mul(a, _B)) + message).digest(), 'little') % _L
    s = (r + k * a) % _L
    return r_enc + s.to_bytes(32, 'little')


def ed25519_verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    try:
        if len(public_key) != 32 or len(signature) != 64:
            return False
        r_enc = signature[:32]
        s = int.from_bytes(signature[32:], 'little')
        if s >= _L:
            return False
        a_point = _ed_point_decompress(public_key)
        k = int.from_bytes(hashlib.sha512(r_enc + public_key + message).digest(), 'little') % _L
        r_point = _ed_point_add(
            _ed_point_scalar_mul(s, _B),
            _ed_point_scalar_mul(_L - k, a_point),
        )
        if r_point == (0, 1):
            return False
        return _hmac.compare_digest(_ed_point_compress(r_point), r_enc)
    except Exception:
        return False


def curve25519_donna_sign(private_key: bytes, message: bytes) -> bytes:
    """Curve25519-donna signature (libsignal `curve.sign` / curve25519-js).

    Signs with the raw clamped X25519 scalar directly (NOT RFC 8032 Ed25519).
    Nonce = SHA-512(clamped_sk || message); S = r + h*sk mod L; the sign bit
    of the derived edwards public key is copied into the last byte of S.
    """
    sk = bytearray(private_key)
    sk[0] &= 248
    sk[31] &= 127
    sk[31] |= 64
    sk_int = int.from_bytes(sk, 'little')
    A_enc = _ed_point_compress(_ed_point_scalar_mul(sk_int, _B))
    sign_bit = A_enc[31] & 128
    r = int.from_bytes(hashlib.sha512(bytes(sk) + message).digest(), 'little') % _L
    R_enc = _ed_point_compress(_ed_point_scalar_mul(r, _B))
    h = int.from_bytes(hashlib.sha512(R_enc + A_enc + message).digest(), 'little') % _L
    s = ((r + h * sk_int) % _L).to_bytes(32, 'little')
    return R_enc + s[:31] + bytes([s[31] | sign_bit])


def curve25519_donna_verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    """Verify a curve25519-donna signature against a 32-byte X25519 public key.

    Accepts either a bare 32-byte key or a 33-byte key with the 0x05 version
    byte prefix (stripped internally, mirroring libsignal's scrubPubKeyFormat).
    """
    try:
        if len(public_key) == 33 and public_key[0] == 0x05:
            public_key = public_key[1:]
        if len(public_key) != 32 or len(signature) != 64:
            return False
        sig = bytearray(signature)
        sign_bit = sig[63] & 128
        sig[63] &= 127
        R_enc = bytes(sig[:32])
        s = int.from_bytes(sig[32:], 'little')
        if s >= _L:
            return False
        x = int.from_bytes(public_key, 'little')
        y_ed = ((x - 1) * pow((x + 1) % _Q, _Q - 2, _Q)) % _Q
        edpk = bytearray(y_ed.to_bytes(32, 'little'))
        edpk[31] |= sign_bit
        a_point = _ed_point_decompress(bytes(edpk))
        h = int.from_bytes(hashlib.sha512(R_enc + bytes(edpk) + message).digest(), 'little') % _L
        # A valid donna signature satisfies S*B = R + h*A, i.e. R = S*B - h*A
        r_point = _ed_point_add(
            _ed_point_scalar_mul(s, _B),
            _ed_point_scalar_mul(_L - h, a_point),
        )
        return _ed_point_compress(r_point) == R_enc
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Baileys-level curve helpers (mirror of Utils/crypto.ts)
# ---------------------------------------------------------------------------

class Curve:
    @staticmethod
    def generate_key_pair() -> dict:
        """Returns {'private': bytes(32), 'public': bytes(32)} (no version byte)."""
        private, public = x25519_generate_key_pair()
        return {'private': private, 'public': public}

    @staticmethod
    def shared_key(private_key: bytes, public_key: bytes) -> bytes:
        # prefix version byte to pub key (KEY_BUNDLE_TYPE = 0x05) if missing
        if len(public_key) != 32:
            raise ValueError('public key must be 32 bytes')
        return x25519_shared_key(private_key, public_key)

    @staticmethod
    def sign(private_key: bytes, buf: bytes) -> bytes:
        # libsignal signs with curve25519-donna (NOT RFC 8032 Ed25519)
        return curve25519_donna_sign(private_key, buf)

    @staticmethod
    def verify(pub_key: bytes, message: bytes, signature: bytes) -> bool:
        try:
            return curve25519_donna_verify(pub_key, message, signature)
        except Exception:
            return False


def generate_signal_pub_key(pub_key: bytes) -> bytes:
    """Prefix the 0x05 version byte to a public key when required."""
    if len(pub_key) == 33:
        return pub_key
    return KEY_BUNDLE_TYPE + pub_key


def signed_key_pair(identity_key_pair: dict, key_id: int) -> dict:
    pre_key = Curve.generate_key_pair()
    pub_key = generate_signal_pub_key(pre_key['public'])
    signature = Curve.sign(identity_key_pair['private'], pub_key)
    return {'keyPair': pre_key, 'signature': signature, 'keyId': key_id}


def aes_encrypt_gcm(plaintext: bytes, key: bytes, iv: bytes, additional_data: bytes) -> bytes:
    return aes_gcm_encrypt(plaintext, key, iv, additional_data)


def aes_decrypt_gcm(ciphertext: bytes, key: bytes, iv: bytes, additional_data: bytes) -> bytes:
    return aes_gcm_decrypt(ciphertext, key, iv, additional_data)


def aes_encrypt_ctr(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_ctr_crypt(plaintext, key, iv)


def aes_decrypt_ctr(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_ctr_crypt(ciphertext, key, iv)


def aes_decrypt(buffer: bytes, key: bytes) -> bytes:
    """IV prefixed to the buffer."""
    return aes_cbc_decrypt(buffer[16:], key, buffer[:16])


def aes_decrypt_with_iv(buffer: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_cbc_decrypt(buffer, key, iv)


def aes_encrypt(buffer: bytes, key: bytes) -> bytes:
    iv = secrets.token_bytes(16)
    return iv + aes_cbc_encrypt(buffer, key, iv)


def aes_encrypt_with_iv(buffer: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_cbc_encrypt(buffer, key, iv)


def derive_pairing_code_key(pairing_code: str, salt: bytes) -> bytes:
    """PBKDF2-SHA256, 131072 iterations, 32 bytes (matches WA pairing code key)."""
    return pbkdf2_sha256(pairing_code.encode('utf-8'), salt, 2 << 16, 32)


# aliases kept for parity with the TS module
Curve.generateKeyPair = Curve.generate_key_pair
Curve.sharedKey = Curve.shared_key
Curve.sign = Curve.sign
Curve.verify = Curve.verify
