# WAeys — Complete User Guide (English)

> **Pure-Python port of [Baileys](https://github.com/WhiskeySockets/Baileys)** — a WhatsApp Web protocol client that runs **without Node.js**. All cryptography (Signal E2EE, Noise handshake, AES, Curve25519) is implemented in pure Python.

This guide is the full reference for installing, configuring, connecting, pairing, sending and receiving messages, and deploying a bot built on **WAeys**.

---

## Table of contents

1. [Overview](#1-overview)
2. [Requirements & installation](#2-requirements--installation)
3. [First connection](#3-first-connection)
4. [Authentication & session persistence](#4-authentication--session-persistence)
5. [Pairing with a code (alternative to QR)](#5-pairing-with-a-code-alternative-to-qr)
6. [Configuration reference](#6-configuration-reference)
7. [The socket object](#7-the-socket-object)
8. [Events & event listeners](#8-events--event-listeners)
9. [Sending messages](#9-sending-messages)
10. [Sending media](#10-sending-media)
11. [Interactive messages (buttons, lists, templates)](#11-interactive-messages-buttons-lists-templates)
12. [Reading & reacting to incoming messages](#12-reading--reacting-to-incoming-messages)
13. [Read receipts & presence](#13-read-receipts--presence)
14. [Session lifecycle: logout, reconnection, retries](#14-session-lifecycle-logout-reconnection-retries)
15. [Low-level API](#15-low-level-api)
16. [Production tips & anti-ban](#16-production-tips--anti-ban)
17. [Troubleshooting](#17-troubleshooting)
18. [Full API reference table](#18-full-api-reference-table)
19. [Project structure](#19-project-structure)
20. [Legal disclaimer](#20-legal-disclaimer)

---

## 1. Overview

WAeys is a from-scratch Python translation of the Baileys library. It speaks the same binary XMPP-like protocol that WhatsApp Web uses, over a Noise-encrypted WebSocket connection.

What it gives you:

- **QR login** and **phone-number pairing code** login.
- **End-to-end encryption** using the Signal protocol (sessions, prekeys, signed prekeys, identity keys).
- **A full event bus** (`ev`) mirroring Baileys: `connection.update`, `messages.upsert`, `contacts.upsert`, `chats.upsert`, `creds.update`, and more.
- **Message sending**: text, image, video, audio, sticker, document, contacts, location, polls, reactions, events, albums, and interactive messages (buttons/lists/templates via raw protobuf).
- **Media pipeline**: upload, encryption, thumbnails, and download helpers.
- **Message retry manager** for undelivered messages.
- **Session persistence** through a pluggable key store (`get`/`set`/`clear`).

### Terminology

| Term | Meaning |
|---|---|
| `sock` | The socket dictionary returned by `make_socket()`. Holds methods and state. |
| `ev` | The event bus; listen with `ev.on('event.name', handler)`. |
| `auth` / `authState` | `{'creds': {...}, 'keys': store}` — credentials + signal key store. |
| `creds` | The JSON-serializable credential object (me, keys, registration id, etc.). |
| `jid` | "Jabber ID": the WhatsApp address of a chat or user, e.g. `123456789@s.whatsapp.net`. |
| `lid` | Long-term identity (LID) used by newer WhatsApp accounts. |
| `pairing code` | A 8-character code to link a phone instead of scanning a QR. |

---

## 2. Requirements & installation

### 2.1 Supported environments

WAeys is **pure Python** and platform-independent. It runs anywhere Python 3.10+ runs:

- Linux (Debian/Ubuntu, Arch, Fedora, …)
- macOS
- Windows (CPython)
- Android via **Termux**
- Docker containers, VPS servers, Raspberry Pi

The only runtime dependency is **`websockets` (>= 12.0)**. There is **no Node.js** involved.

### 2.2 Install from PyPI

```bash
pip install waeys
```

### 2.3 Install from source (development)

```bash
git clone https://github.com/toZyn/WAeys.git
cd WAeys
pip install -e .            # editable install
# or, to build a wheel:
pip install build
python -m build
pip install dist/waeys-0.1.0-py3-none-any.whl
```

### 2.4 Verify the install

```python
import WAeys
print(WAeys.__version__)   # "0.1.0"
```

If you get `ModuleNotFoundError: No module named 'websockets'`:

```bash
pip install "websockets>=12.0"
```

### 2.5 Note about Python interpreters

If your machine has several Python installations (very common on Termux / Linux), make sure the interpreter you use to **install** the package is the same one you use to **run** your script:

```bash
python3 -c "import websockets; print(websockets.__version__)"   # must succeed
```

---

## 3. First connection

The entry point is `make_socket(config)` in `WAeys.Socket`. It returns a dictionary (`sock`) with everything you need.

### 3.1 Minimal QR-login example

```python
import asyncio

from WAeys.Defaults.index import default_connection_config
from WAeys.Utils.auth_utils import init_auth_creds, make_memory_key_store
from WAeys.Utils.browser_utils import Browsers
from WAeys.Socket.socket import make_socket


async def main():
    config = default_connection_config()
    config['auth'] = {'creds': init_auth_creds(), 'keys': make_memory_key_store()}
    config['browser'] = Browsers.macOS('Safari')
    config['keepAliveIntervalMs'] = 30_000
    config['logger'].level = 'info'

    sock = make_socket(config)
    ev = sock['ev']

    # Show the QR code as soon as it is generated
    async def on_connection_update(update):
        qr = update.get('qr')
        if qr:
            print('Scan this QR with WhatsApp > Linked Devices')
            print(qr)
        if update.get('connection') == 'open':
            print('Connected!')
            # from here you can send messages, see section 9
            await sock['sendMessage']('123456789@s.whatsapp.net', {'text': 'Hello from WAeys!'})
            await sock['end']()

    ev.on('connection.update', lambda u: asyncio.ensure_future(on_connection_update(u)))

    # keep the process alive
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())
```

### 3.2 What happens behind the scenes

1. `make_socket()` generates an ephemeral Curve25519 key pair and builds the Noise client.
2. It opens a WebSocket to `wss://web.whatsapp.com/ws/chat`.
3. It emits `connection.update` with `{'qr': '...'}` (repeatable until it times out) or, for an existing session, it validates credentials and emits `{'connection': 'open'}`.
4. After a successful link, it uploads prekeys and emits `{'connection': 'open'}`.

> **Important**: When linking a *new* device you should wait for the `connection: open` event before sending anything. The `registered: true` flag alone is not enough — prekeys must be uploaded first.

---

## 4. Authentication & session persistence

### 4.1 The auth state

`config['auth']` must be a dictionary with two keys:

```python
auth = {
    'creds': {...},   # plain dict, JSON-serializable credential data
    'keys': store,    # an async key store: {get, set, clear}
}
```

`init_auth_creds()` (`WAeys.Utils.auth_utils`) returns a fresh, empty credential set:

```python
from WAeys.Utils.auth_utils import init_auth_creds, make_memory_key_store
creds = init_auth_creds()
```

It contains (among others):

```python
{
  'registered': False,
  'me': None,
  'noiseKey': {'public': ..., 'private': ...},
  'signedIdentityKey': {...},
  'signedPreKey': {...},
  'registrationId': ...,
  'advSecretKey': ...,
  'nextPreKeyId': 1,
  'firstUnuploadedPreKeyId': 1,
  'serverHasPreKeys': False,
  ...
}
```

### 4.2 The key store

The `keys` store is the Signal session/sender-key/pre-key database. It must implement three **async** methods:

```python
class MyStore:
    async def get(self, type_: str, ids: list) -> dict:
        # return {id: value, ...} for the requested ids
        ...

    async def set(self, data: dict) -> None:
        # data = {type_: {id: value}}
        ...

    async def clear(self) -> None:
        ...
```

`type_` values come from `SignalTypes`: `session`, `sender-key`, `app-state-sync-key`, `app-state-sync-version`, etc.

### 4.3 A simple file-backed store

The example below is the recommended starting point for most bots. It saves every change to disk so you can restart and stay logged in.

```python
import json
import base64
import os

SESSION_DIR = os.path.join(os.getcwd(), 'wa_session')
CREDS_FILE = os.path.join(SESSION_DIR, 'creds.json')
KEYS_FILE = os.path.join(SESSION_DIR, 'keys.json')


def _encode(v):
    if isinstance(v, bytes):
        return {'__bytes__': base64.b64encode(v).decode('ascii')}
    if isinstance(v, str):
        return {'__str__': v}
    if isinstance(v, dict):
        return {k: _encode(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_encode(x) for x in v]
    return v


def _decode(v):
    if isinstance(v, dict):
        if '__bytes__' in v:
            return base64.b64decode(v['__bytes__'])
        if '__str__' in v:
            return v['__str__']
        return {k: _decode(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_decode(x) for x in v]
    return v


def save_creds(creds):
    os.makedirs(SESSION_DIR, exist_ok=True)
    with open(CREDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(_encode(creds), f, default=str, ensure_ascii=False, indent=2)


def load_creds():
    if not os.path.exists(CREDS_FILE):
        return None
    with open(CREDS_FILE, 'r', encoding='utf-8') as f:
        return _decode(json.load(f))


def make_file_key_store():
    async def get(type_, ids):
        all_keys = {}
        if os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, 'r', encoding='utf-8') as f:
                all_keys = _decode(json.load(f))
        return {i: all_keys.get(type_, {}).get(i) for i in ids if all_keys.get(type_, {}).get(i) is not None}

    async def set(data):
        existing = {}
        if os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, 'r', encoding='utf-8') as f:
                existing = _decode(json.load(f))
        for type_, entries in data.items():
            for id_, value in entries.items():
                existing.setdefault(type_, {})
                if value is None:
                    existing[type_].pop(id_, None)
                else:
                    existing[type_][id_] = value
        os.makedirs(SESSION_DIR, exist_ok=True)
        with open(KEYS_FILE, 'w', encoding='utf-8') as f:
            json.dump(_encode(existing), f, default=str, ensure_ascii=False, indent=2)

    async def clear():
        if os.path.exists(KEYS_FILE):
            os.remove(KEYS_FILE)

    return {'get': get, 'set': set, 'clear': clear}
```

### 4.4 Persisting credential updates

WAeys emits `creds.update` whenever the credentials change (after pairing, key rotation, etc.). **You must persist these**, otherwise the session will not survive a restart:

```python
async def on_creds_update(update):
    auth['creds'].update(update)
    save_creds(auth['creds'])

ev.on('creds.update', lambda u: asyncio.ensure_future(on_creds_update(u)))
```

### 4.5 Restoring a session

On startup, load the saved session and plug it in. If a valid paired session exists, WAeys will simply reconnect and emit `connection: open`:

```python
creds = load_creds()
if creds is not None:
    config['auth'] = {'creds': creds, 'keys': make_file_key_store()}
else:
    config['auth'] = {'creds': init_auth_creds(), 'keys': make_file_key_store()}
```

> **Trap**: a saved session whose prekeys were never uploaded (for example because the process was killed right after pairing) will fail with `CB:failure` / "Connection Failure". Re-link in that case. This is why waiting for `connection: open` during pairing matters.

---

## 5. Pairing with a code (alternative to QR)

Instead of scanning a QR code you can ask WhatsApp for an 8-character **pairing code** and enter it manually.

### 5.1 How it works

1. Create the socket with a fresh auth state.
2. Wait for the `connection.update` event to deliver a `qr` value (this signals WhatsApp is ready to pair).
3. Call `sock['requestPairingCode'](phone_number)`.
4. Print the code for the user, who types it in: **WhatsApp → Settings → Linked Devices → Link a Device → Link with phone number**.
5. Wait for `connection: open`.

> **Important**: use the **full international number** without `+`, e.g. `51921826291` for a Peru number.

### 5.2 Full pairing example with retry loop

```python
import asyncio
import traceback

from WAeys.Defaults.index import default_connection_config
from WAeys.Utils.auth_utils import init_auth_creds, make_memory_key_store
from WAeys.Utils.browser_utils import Browsers
from WAeys.Socket.socket import make_socket

PHONE = '51921826291'


async def pair(auth):
    config = default_connection_config()
    config['auth'] = auth
    config['browser'] = Browsers.macOS('Safari')
    config['keepAliveIntervalMs'] = 5000   # keep-alive is crucial during pairing
    config['logger'].level = 'info'

    sock = make_socket(config)
    ev = sock['ev']
    done = asyncio.Event()

    async def on_creds(update):
        auth['creds'].update(update)
        save_creds(auth['creds'])

    ev.on('creds.update', lambda u: asyncio.ensure_future(on_creds(u)))

    async def on_conn(update):
        if update.get('qr') and not sock.get('_code_requested'):
            sock['_code_requested'] = True
            try:
                code = await sock['requestPairingCode'](PHONE)
                print(f'\nPAIRING CODE: {code}\n')
            except Exception as err:
                print('pairing request failed:', err)
        if update.get('connection') == 'open':
            print('PAIRED AND OPEN')
            done.set()

    ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))

    try:
        await asyncio.wait_for(done.wait(), timeout=120)
    except asyncio.TimeoutError:
        print('timed out waiting for pairing')
    finally:
        await sock['end']()
    return done.is_set()


async def main():
    auth = {'creds': init_auth_creds(), 'keys': make_file_key_store()}
    attempt = 1
    while True:
        print(f'--- pairing attempt {attempt} ---')
        ok = await pair(auth)
        if ok:
            print('SUCCESS. Session saved.')
            return
        attempt += 1
        await asyncio.sleep(3)
        auth['creds'] = init_auth_creds()
        save_creds(auth['creds'])


asyncio.run(main())
```

### 5.3 Pairing gotchas

- **Keep the connection alive**: use a short `keepAliveIntervalMs` (5000) because WhatsApp drops unpaired connections after ~90 seconds.
- **Don't run two pairing processes at once** — they generate conflicting keys and WhatsApp may return `rate-overlimit`.
- **`rate-overlimit`** means you made too many pairing requests; wait 30–60 minutes.
- If the code is rejected ("código incorrecto"), the pairing connection may have died before you entered the code; reconnect and request a fresh code.
- After pairing, **wait for `connection: open`** before using the session, so prekeys get uploaded.

---

## 6. Configuration reference

`default_connection_config()` returns a dict you can override. Full list of options:

| Key | Default | Description |
|---|---|---|
| `version` | `[2, 3000, ...]` | WhatsApp Web protocol version sent during connect. |
| `browser` | `Browsers.macOS('Chrome')` | Browser identification. Use `Browsers.ubuntu/macOS/windows/android/baileys/appropriate`. |
| `waWebSocketUrl` | `wss://web.whatsapp.com/ws/chat` | Server URL. |
| `connectTimeoutMs` | `20000` | Timeout to establish the WebSocket. |
| `keepAliveIntervalMs` | `30000` | Ping interval. Lower to 5000 during pairing. |
| `logger` | child logger | Any `log`-style object with `.info/.warn/.error/.debug`. |
| `emitOwnEvents` | `True` | Emit events for messages you send yourself. |
| `defaultQueryTimeoutMs` | `60000` | Default timeout for IQ queries. |
| `customUploadHosts` | `[]` | Override media upload hosts. |
| `retryRequestDelayMs` | `250` | Delay before retrying failed requests. |
| `maxMsgRetryCount` | `5` | Max message resend attempts. |
| `fireInitQueries` | `True` | Run the init queries on connect. |
| `auth` | `None` | The auth state dict (required). |
| `markOnlineOnConnect` | `True` | Broadcast "online" presence. |
| `syncFullHistory` | `True` | Sync full chat history on login. |
| `patchMessageBeforeSending` | internal | Hook to mutate messages before sending. |
| `shouldSyncHistoryMessage` | internal | Filter which history sync types are processed. |
| `shouldIgnoreJid` | `lambda: False` | Skip processing for certain JIDs. |
| `linkPreviewImageThumbnailWidth` | `192` | Link-preview thumbnail width. |
| `transactionOpts` | `{maxCommitRetries:10, delayBetweenTriesMs:3000}` | Transaction retry policy for app-state. |
| `generateHighQualityLinkPreview` | `False` | Upload a high-quality thumbnail for link previews. |
| `enableAutoSessionRecreation` | `True` | Recreate signal sessions when needed. |
| `enableRecentMessageCache` | `True` | Cache recent messages. |
| `options` | `{}` | Extra HTTP options. |
| `appStateMacVerification` | `{patch:False,snapshot:False}` | Verify app-state MACs. |
| `countryCode` | `'US'` | Country code used for some queries. |
| `getMessage` | `lambda: None` | Used to resolve message content for retries. |
| `cachedGroupMetadata` | `lambda: None` | Group metadata cache hook. |
| `makeSignalRepository` | internal | How to build the libsignal repository. |
| `printQRInTerminal` | deprecated | QR auto-print; listen to events instead. |

---

## 7. The socket object

`make_socket(config)` returns a dict. Commonly used members:

```python
sock = make_socket(config)

sock['ws']              # WebSocketClient
sock['ev']              # event bus
sock['authState']       # {'creds': ..., 'keys': ...}
sock['user']            # callable -> creds.get('me')
sock['query']           # async IQ query
sock['waitForMessage']  # async low-level wait
sock['waitForSocketOpen']
sock['sendRawMessage']  # async raw noise frame
sock['sendNode']        # async send binary node
sock['logout']          # async logout
sock['end']             # async close
sock['requestPairingCode']   # async pairing code
sock['uploadPreKeys']   # async
sock['rotateSignedPreKey']   # async
sock['sendWAMBuffer']   # async
sock['executeUSyncQuery']    # async
sock['onWhatsApp']      # async phone check
sock['waitForConnectionUpdate']  # async wait helper
```

If you wrap the socket with the message layer (see `WAeys.Socket.messages_send.make_messages_socket`), you additionally get:

```python
sock['sendMessage']     # async send any message
sock['relayMessage']    # async low-level relay of a protobuf message
sock['sendReceipt']     # async ack receipts
sock['sendReceipts']
sock['readMessages']    # async mark read
sock['refreshMediaConn']
sock['getMediaHost']
sock['waUploadToServer']
sock['fetchPrivacySettings']
sock['assertSessions']
sock['issuePrivacyTokens']
sock['messageRetryManager']
sock['updateMediaMessage']
```

---

## 8. Events & event listeners

The event bus `ev` supports:

```python
ev.on(event, listener)            # subscribe
ev.off(event, listener)           # unsubscribe
ev.remove_all_listeners(event)    # remove all for event (or all if event is None)
```

Listeners are plain callables invoked with the payload. **They are synchronous** — for async work, wrap with `asyncio.ensure_future(...)`.

### 8.1 Connection events

`connection.update` payload:

```python
{'qr': '...', 'isNewLogin': True}            # during QR pairing
{'connection': 'connecting', 'qr': None}
{'receivedPendingNotifications': True}
{'connection': 'open'}                       # fully ready
{'connection': 'close',
 'lastDisconnect': {'error': <Boom error>}}  # closed/failed
{'connection': 'reconnecting'}
{'reachoutTimeLock': ...}
```

### 8.2 Credential events

`creds.update` — partial update to apply to `auth['creds']` (persist it!).

### 8.3 Message events

| Event | Payload |
|---|---|
| `messages.upsert` | `{'messages': [WAMessage, ...], 'type': 'notify'/'append'/'replace'}` |
| `messages.update` | `[{'key': ..., 'update': {...}}]` — status/edits |
| `messages.media-update` | `[event]` — media download progress/result |
| `message-capping.update` | capping info |

### 8.4 Chat/contact/group events

| Event | Payload |
|---|---|
| `chats.upsert` | list of chats |
| `contacts.upsert` | list of contacts |
| `contacts.update` | list of contact updates |
| `groups.upsert` | list of group metadata |
| `blocklist.update` | block list changes |
| `lid-mapping.update` | LID mapping updates |

### 8.5 Receiving a message example

```python
async def on_messages_upsert(data):
    for msg in data['messages']:
        key = msg.get('key', {})
        remote = key.get('remoteJid')
        content = msg.get('message') or {}
        # find the actual content type
        text = content.get('conversation') or content.get('extendedTextMessage', {}).get('text')
        print(f'[{remote}] {text}')

ev.on('messages.upsert', lambda d: asyncio.ensure_future(on_messages_upsert(d)))
```

---

## 9. Sending messages

The main API is `await sock['sendMessage'](jid, content, options)`.

### 9.1 Plain text

```python
await sock['sendMessage']('51921826291@s.whatsapp.net', {'text': 'Hello world!'})
```

### 9.2 Text with mentions

```python
await sock['sendMessage'](jid, {
    'text': 'Hi @123456789 and @987654321',
    'mentions': ['123456789@s.whatsapp.net', '987654321@s.whatsapp.net'],
})
```

### 9.3 Reply/quote another message

```python
quoted = {
    'key': {'remoteJid': jid, 'id': msg_id, 'fromMe': False},
    'message': original_message_content,
}
await sock['sendMessage'](jid, {'text': 'My reply'}, {'quoted': quoted})
```

### 9.4 Reaction

```python
await sock['sendMessage'](jid, {'react': {'text': '🔥', 'key': msg_key}})
```

### 9.5 Delete a message

```python
await sock['sendMessage'](jid, {'delete': msg_key})
```

### 9.6 Edit a message

```python
await sock['sendMessage'](jid, {'edit': msg_key, 'text': 'Edited text'})
```

### 9.7 Poll

```python
await sock['sendMessage'](jid, {
    'poll': {
        'name': 'Best programming language?',
        'values': ['Python', 'JavaScript', 'Rust'],
        'selectableCount': 1,
    }
})
```

### 9.8 Contacts

```python
await sock['sendMessage'](jid, {
    'contacts': {'contacts': [
        {'displayName': 'Jane', 'vcard': 'BEGIN:VCARD\nVERSION:3.0\nFN:Jane\nEND:VCARD'},
    ]}
})
```

### 9.9 Location

```python
await sock['sendMessage'](jid, {
    'location': {'degreesLatitude': -12.0464, 'degreesLongitude': -77.0428, 'name': 'Lima'},
})
```

### 9.10 Event (calendar)

```python
from datetime import datetime, timedelta
await sock['sendMessage'](jid, {
    'event': {
        'name': 'Meeting',
        'startDate': datetime.now() + timedelta(hours=1),
        'endDate': datetime.now() + timedelta(hours=2),
    }
})
```

### 9.11 Options common to all sends

```python
await sock['sendMessage'](jid, content, {
    'quoted': quoted_msg,          # reply to
    'timestamp': datetime.now(),   # custom timestamp
    'messageId': 'my-custom-id',   # custom message id
    'ephemeralExpiration': 7 * 86400,   # disappearing message (seconds)
    'backgroundColor': '#FF0000',  # status text background
    'font': 4,                     # status font
})
```

---

## 10. Sending media

Media is uploaded to WhatsApp's servers, encrypted, and sent automatically. Provide the bytes or a path.

### 10.1 Image

```python
with open('cat.jpg', 'rb') as f:
    await sock['sendMessage'](jid, {
        'image': f.read(),
        'caption': 'Look at this cat',
        'fileName': 'cat.jpg',
        'mimetype': 'image/jpeg',
    })
```

### 10.2 Video / audio / document / sticker

```python
# video
await sock['sendMessage'](jid, {'video': data, 'caption': 'video', 'mimetype': 'video/mp4'})
# audio
await sock['sendMessage'](jid, {'audio': data, 'mimetype': 'audio/mp4', 'ptt': False})
# voice note (push-to-talk)
await sock['sendMessage'](jid, {'audio': data, 'mimetype': 'audio/ogg; codecs=opus', 'ptt': True})
# document
await sock['sendMessage'](jid, {'document': data, 'fileName': 'report.pdf', 'mimetype': 'application/pdf', 'caption': 'Report'})
# sticker
await sock['sendMessage'](jid, {'sticker': data, 'mimetype': 'image/webp'})
```

### 10.3 GIF

```python
await sock['sendMessage'](jid, {'video': data, 'gifPlayback': True, 'mimetype': 'video/mp4'})
```

### 10.4 viewOnce media

```python
await sock['sendMessage'](jid, {'image': data, 'viewOnce': True, 'mimetype': 'image/jpeg'})
```

### 10.5 Media fields

Common fields per media type: `caption`, `mimetype`, `fileName`, `fileLength`, `viewOnce`, `ptt`, `gifPlayback`, `jpegThumbnail` (preview), `duration` (audio/video), `contextInfo`.

### 10.6 Downloading media (received)

Use the helpers in `WAeys.Utils.messages_media`:

```python
from WAeys.Utils.messages_media import download_content_from_message

buffer, mimetype = await download_content_from_message(msg, media_keys)
```

The media keys (`mediaKey`) are already on the received message; pass the message object and a store resolver. For convenience, `decrypt_media_retry_data` and `get_media_keys` help compute the keys.

---

## 11. Interactive messages (buttons, lists, templates)

WAeys does **not** ship a dict shortcut for interactive messages (same as Baileys TS). You build a **full `proto.Message`** and send it via `generate_wa_message_from_content` + `relayMessage`, or pass a raw protobuf message.

### 11.1 The general pattern

```python
from WAeys.WAProto import WAProto as proto
from WAeys.Utils.messages import generate_wa_message_from_content
from WAeys.Utils.generics import generate_message_id_v2

msg = proto.Message.from_object({
    'interactiveMessage': {
        'body': {'text': 'Pick one:'},
        'nativeFlowMessage': {
            'buttons': [
                {'name': 'quick_reply',
                 'buttonParamsJson': '{"display_text":"Option 1","id":"opt1"}'},
                {'name': 'quick_reply',
                 'buttonParamsJson': '{"display_text":"Option 2","id":"opt2"}'},
            ],
        },
    },
})

me = sock['user']()['id']
full = generate_wa_message_from_content(jid, msg, {
    'userJid': me,
    'messageId': generate_message_id_v2(me),
})
await sock['relayMessage'](jid, full['message'], {})
```

### 11.2 List message

```python
msg = proto.Message.from_object({
    'listMessage': {
        'title': 'Menu',
        'description': 'Choose a section',
        'footerText': 'Powered by WAeys',
        'buttonText': 'Options',
        'sections': [{
            'title': 'Main',
            'rows': [
                {'title': 'Pizza', 'description': 'Cheese', 'rowId': 'pizza'},
                {'title': 'Burger', 'description': 'Beef', 'rowId': 'burger'},
            ],
        }],
        'listType': 1,   # proto.Message.ListMessage.ListType.SINGLE_SELECT
    },
})
```

### 11.3 Buttons message

```python
msg = proto.Message.from_object({
    'buttonsMessage': {
        'contentText': 'Choose:',
        'footerText': 'footer',
        'buttons': [
            {'buttonId': 'yes', 'buttonText': {'displayText': 'Yes'}, 'type': 1},
            {'buttonId': 'no',  'buttonText': {'displayText': 'No'},  'type': 1},
        ],
        'headerType': 1,
    },
})
```

### 11.4 Template message

```python
msg = proto.Message.from_object({
    'templateMessage': {
        'hydratedFourRowTemplate': {
            'hydratedContentText': 'Welcome!',
            'hydratedFooterText': 'footer',
            'templateButtons': [
                {'quickReplyButton': {'displayText': 'Go', 'id': 'go'}},
            ],
        },
    },
})
```

### 11.5 Interactive with media header

```python
media_result = await prepare_wa_message_media({'image': img_bytes}, opts)
msg = proto.Message.from_object({
    'interactiveMessage': {
        'header': {'title': 'Header', 'hasMediaAttachment': True,
                   'imageMessage': media_result.imageMessage},
        'body': {'text': 'Body text'},
        'nativeFlowMessage': {'buttons': [...]},
    },
})
```

> Fields available in the proto: `buttonsMessage=42`, `listMessage=36`, `templateMessage=25`, `interactiveMessage=45`, `nativeFlowMessage` inside `interactiveMessage`.

### 11.6 Handling interactive replies

Replies to buttons/lists arrive as `messages.upsert` with content types like:

- `buttonsResponseMessage` (button replies)
- `listResponseMessage` (list replies)
- `templateButtonReplyMessage` (template replies)

```python
content = msg.get('message') or {}
if content.get('buttonsResponseMessage'):
    print('Button:', content['buttonsResponseMessage'].get('selectedButtonId'))
elif content.get('listResponseMessage'):
    print('List:', content['listResponseMessage'].get('singleSelectReply', {}).get('selectedRowId'))
```

---

## 12. Reading & reacting to incoming messages

### 12.1 Iterating over upserts

```python
async def on_upsert(data):
    for msg in data['messages']:
        if msg.get('key', {}).get('fromMe'):
            continue          # skip your own (unless emitOwnEvents)
        jid = msg['key']['remoteJid']
        content = msg.get('message') or {}
        ctype = next((k for k in content if content.get(k)), None)
        print('type:', ctype, '| from:', jid)
        if ctype == 'conversation':
            text = content['conversation']
        elif ctype == 'extendedTextMessage':
            text = content['extendedTextMessage'].get('text')
        # ... handle others

ev.on('messages.upsert', lambda d: asyncio.ensure_future(on_upsert(d)))
```

### 12.2 Command router example

```python
COMMANDS = {
    '/ping': lambda: 'pong',
    '/time': lambda: str(datetime.now()),
}

async def on_upsert(data):
    for msg in data['messages']:
        if msg.get('key', {}).get('fromMe'):
            continue
        jid = msg['key']['remoteJid']
        content = msg.get('message') or {}
        text = content.get('conversation') or content.get('extendedTextMessage', {}).get('text') or ''
        if text.startswith('/'):
            reply = COMMANDS.get(text.split()[0], lambda: 'Unknown command')()
            await sock['sendMessage'](jid, {'text': reply})
```

### 12.3 Getting chat id / jid

```python
from WAeys.Utils.process_message import get_chat_id
chat_id = get_chat_id(msg)   # jid of the chat
```

`is_real_message(msg)` tells you if the message is a real user message (not a status/system/protocol message).

---

## 13. Read receipts & presence

### 13.1 Mark messages as read

```python
await sock['readMessages']([{'remoteJid': jid, 'id': msg_id, 'fromMe': False}])
```

### 13.2 Send receipts

```python
await sock['sendReceipts'](keys, 'read')        # 'read' / 'delivered'
await sock['sendReceipt'](jid, participant, [msg_id], 'read')
```

### 13.3 Check if a phone is on WhatsApp

```python
result = await sock['onWhatsApp']('51921826291')
# [{'exists': True, 'jid': '51921826291@s.whatsapp.net'}]
```

### 13.4 Online presence

Presence is controlled by `markOnlineOnConnect` at the config level. Low-level presence control uses `sock['query']` with the appropriate presence IQ (like Baileys).

---

## 14. Session lifecycle: logout, reconnection, retries

### 14.1 Graceful shutdown

```python
await sock['end']()        # close cleanly (stops keep-alive, closes ws)
await sock['logout']()     # server-side logout (invalidates the session)
```

### 14.2 Detecting disconnects and reconnecting

```python
async def on_conn(update):
    if update.get('connection') == 'close':
        err = update.get('lastDisconnect', {}).get('error') if isinstance(update.get('lastDisconnect'), dict) else None
        print('disconnected:', err)
        # recreate the socket with the SAME auth state
        new_sock = make_socket(config)
        # re-register handlers, continue...

ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))
```

WAeys has **no automatic reconnect** built in (matching the Baileys base socket). Production bots wrap the socket in a reconnect loop, reusing the saved session.

### 14.3 Message retries

A `MessageRetryManager` is exposed at `sock['messageRetryManager']` and used automatically by `relayMessage` for failed deliveries (`maxMsgRetryCount`, `retryRequestDelayMs`).

### 14.4 Registering end-of-socket handlers

```python
sock['registerSocketEndHandler'](lambda: print('socket ended'))
```

### 14.5 Waiting for connection update

```python
update = await sock['waitForConnectionUpdate'](lambda u: u.get('connection') == 'open')
```

---

## 15. Low-level API

### 15.1 Sending a binary node

```python
from WAeys.WABinary.types import BinaryNode
node = BinaryNode(tag='iq', attrs={'type': 'get', 'to': 's.whatsapp.net', 'id': '123'}, content=None)
await sock['sendNode'](node)
```

### 15.2 IQ query

```python
result = await sock['query'](node)      # returns response BinaryNode
```

### 15.3 Raw frames

```python
await sock['sendRawMessage'](payload_bytes)
```

### 15.4 Prekeys

```python
await sock['uploadPreKeys']()                       # upload N prekeys
await sock['uploadPreKeysToServerIfRequired']()
await sock['rotateSignedPreKey']()
await sock['digestKeyBundle']()
```

### 15.5 USync

```python
from WAeys.WAUSync.index import USyncQuery, USyncUser
query = USyncQuery('interactive', [USyncUser('51921826291@s.whatsapp.net')])
await sock['executeUSyncQuery'](query)
```

---

## 16. Production tips & anti-ban

WAeys, like every unofficial WhatsApp client, can get your number **banned**. There is **no built-in anti-ban** in the library (same as Baileys). Follow these rules:

1. **Human-like behavior**: send messages with random delays (2–8 s) instead of instant bursts.
2. **Never spam**: avoid mass identical messages, group flooding, or adding contacts aggressively.
3. **Warm up**: for a new number, start with low volume and increase gradually over days.
4. **Don't reuse banned sessions**: if a number is banned, wipe its session and credentials.
5. **Keep a stable connection**: run with keep-alive; avoid killing the process repeatedly during login.
6. **Use pairing instead of repeated new logins**: repeated QR re-links can trigger `rate-overlimit`.
7. **Don't run parallel sessions** with the same number.
8. **Keep version/deps updated**: match the protocol version supported by the library.

### 16.1 Delayed-send helper

```python
import random

async def safe_send(jid, content, min_delay=2.0, max_delay=6.0):
    await asyncio.sleep(random.uniform(min_delay, max_delay))
    await sock['sendMessage'](jid, content)
```

---

## 17. Troubleshooting

### 17.1 `ModuleNotFoundError: No module named 'websockets'`
Install the dependency with the same interpreter that runs your script:
```bash
pip install "websockets>=12.0"
```

### 17.2 QR never appears / connection drops during pairing
WhatsApp drops unpaired connections after ~90 s. Use `keepAliveIntervalMs: 5000` and reconnect until paired.

### 17.3 `rate-overlimit` when requesting pairing codes
Too many attempts. Wait 30–60 minutes, and make sure you aren't running several pairing processes at once.

### 17.4 Session saved but login fails with "Connection Failure"
Prekeys were never uploaded (session was saved too early). Re-pair and wait for `connection: open`.

### 17.5 `Invalid media type`
You passed an unknown content key to `sendMessage`. Use one of: `image`, `video`, `audio`, `document`, `sticker`, `ptt`, `gif`, `ptv`, `product`.

### 17.6 `Boom` errors / `CB:failure`
Check `connection.update`'s `lastDisconnect.error` and the logs. Common causes: stale session, revoked session, or wrong pairing flow.

### 17.7 Seeing `'tb'` tracebacks in logs
If the logger prints a `tb` key, it's a real Python traceback from the internal socket — enable your logger's debug level to read it.

---

## 18. Full API reference table

### `WAeys` package

| Path | Purpose |
|---|---|
| `WAeys.WABinary` | Binary node encode/decode |
| `WAeys.Utils` | All helpers (auth, crypto, messages, media, …) |
| `WAeys.Defaults` | Defaults & constants (`default_connection_config`) |
| `WAeys.Types` | Types & enums |
| `WAeys.WAProto` | Generated protobuf classes (pure Python) |
| `WAeys.Signal` | Signal protocol implementation |
| `WAeys.Socket` | `make_socket`, websocket client, message layers |

### Key Utils functions

| Function | Module |
|---|---|
| `init_auth_creds()` | `WAeys.Utils.auth_utils` |
| `make_cacheable_signal_key_store(store, ...)` | `WAeys.Utils.auth_utils` |
| `Browsers.macOS/ubuntu/windows/android/baileys/appropriate(name)` | `WAeys.Utils.browser_utils` |
| `make_noise_handler(...)` | `WAeys.Utils.noise_handler` |
| `generate_wa_message(jid, content, options)` | `WAeys.Utils.messages` |
| `generate_wa_message_from_content(jid, msg, options)` | `WAeys.Utils.messages` |
| `prepare_wa_message_media(message, options)` | `WAeys.Utils.messages` |
| `download_content_from_message(msg, media)` | `WAeys.Utils.messages_media` |
| `get_content_type(content)` | `WAeys.Utils.messages` |
| `MessageRetryManager` | `WAeys.Utils.message_retry_manager` |
| `make_event_buffer()` | `WAeys.Utils.event_buffer` |

### Socket methods (from `make_socket`)

| Method | Returns | Description |
|---|---|---|
| `requestPairingCode(phone)` | str | Get 8-char pairing code |
| `sendMessage(jid, content, options?)` | message dict | Send any message |
| `relayMessage(jid, proto_msg, opts?)` | — | Low-level relay |
| `readMessages(keys)` | — | Mark read |
| `sendReceipts(keys, type)` | — | Send receipts |
| `onWhatsApp(phone)` | list | Check phone numbers |
| `query(node)` | BinaryNode | IQ query |
| `waitForConnectionUpdate(pred)` | update | Wait for condition |
| `uploadPreKeys()` | — | Upload prekeys |
| `logout()` | — | Server logout |
| `end()` | — | Close connection |
| `executeUSyncQuery(q)` | — | USync query |
| `sendWAMBuffer(buf)` | — | Send WAM buffer |

---

## 19. Project structure

```
WAeys/
├── __init__.py          # package init, __version__
├── Defaults/            # default config, constants, media maps
├── Types/               # auth/message/chat/event types
├── Utils/               # crypto, messages, media, auth, noise, etc.
├── WABinary/            # binary node codec
├── WAProto/             # pure-python protobuf classes + .proto
├── Signal/              # Signal protocol (sessions, prekeys)
├── Socket/              # make_socket + message send/recv layers
│   └── Client/          # websocket client
├── WAM/                 # WhatsApp Analytics Message
└── WAUSync/             # USync queries
```

---

## 20. Legal disclaimer

**WAeys is not affiliated with, endorsed by, or connected to WhatsApp or Meta Platforms, Inc.** It is an unofficial client that uses the WhatsApp Web protocol. Using it may violate WhatsApp's Terms of Service and could lead to temporary or permanent account restrictions. You are solely responsible for how you use this library.

---

*Generated for WAeys v0.1.0 — pure-Python Baileys port. See also the [Spanish](usage.es.md) and [Portuguese](usage.pt.md) versions.*
