# WAeys

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PyPI - Version](https://img.shields.io/pypi/v/waeys)
![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/waeys)
![PyPI - License](https://img.shields.io/pypi/l/waeys)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/toZyn/WAeys/ci.yml?branch=main)

**Pure-Python port of [Baileys](https://github.com/WhiskeySockets/Baileys)** — a WhatsApp Web protocol client. No Node.js / node_modules dependency: all crypto is pure Python.

## Features

- WhatsApp Web protocol over WebSockets (Noise-encrypted)
- E2EE (Signal) sessions in pure Python
- Pairing code & QR login
- Messages: text, media, contacts, location, react, poll, events, and more
- Interactive messages (buttons, lists, templates) via raw protobuf
- Session persistence with a pluggable key store
- Fully typed generated protobuf classes (no `google.protobuf` dependency)
- Message retry manager for undelivered messages

## Install

```bash
pip install waeys
```

Requires **Python 3.10+**. Only runtime dependency: `websockets>=12.0`.

## Documentation

Complete guides (very detailed, in three languages):

| Language | Guide |
|---|---|
| English | [docs/usage.en.md](docs/usage.en.md) |
| Español | [docs/usage.es.md](docs/usage.es.md) |
| Português | [docs/usage.pt.md](docs/usage.pt.md) |

## Quick usage

```python
import asyncio

from WAeys.Defaults.index import default_connection_config
from WAeys.Utils.auth_utils import init_auth_creds
from WAeys.Utils.browser_utils import Browsers
from WAeys.Socket.socket import make_socket


async def main():
    config = default_connection_config()
    config['auth'] = {'creds': init_auth_creds(), 'keys': make_file_key_store()}
    config['browser'] = Browsers.macOS('Safari')
    config['logger'].level = 'info'

    sock = make_socket(config)
    ev = sock['ev']

    async def on_conn(update):
        if update.get('qr'):
            print('Scan the QR in WhatsApp > Linked Devices')
            print(update['qr'])
        if update.get('connection') == 'open':
            await sock['sendMessage']('51921826291@s.whatsapp.net', {'text': 'Hello from WAeys!'})

    ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())
```

See the full guides above for pairing codes, session persistence, media, interactive messages, events and production tips.

## Compatibility

WAeys is pure Python and runs on Linux, macOS, Windows, Android (Termux), Docker, VPS and Raspberry Pi.

## Disclaimer

This is an unofficial client for the WhatsApp Web protocol. Using it may violate WhatsApp's Terms of Service and can lead to account bans. Use at your own risk. This project is not affiliated with WhatsApp or Meta.

## License

MIT
