# WAeys — Guía de uso completa (Español)

> **Port puro de Python de [Baileys](https://github.com/WhiskeySockets/Baileys)** — un cliente del protocolo de WhatsApp Web que funciona **sin Node.js**. Toda la criptografía (Signal E2EE, handshake Noise, AES, Curve25519) está implementada en Python puro.

Esta guía es la referencia completa para instalar, configurar, conectar, emparejar, enviar y recibir mensajes, y desplegar un bot construido con **WAeys**.

---

## Índice

1. [Resumen](#1-resumen)
2. [Requisitos e instalación](#2-requisitos-e-instalación)
3. [Primera conexión](#3-primera-conexión)
4. [Autenticación y persistencia de sesión](#4-autenticación-y-persistencia-de-sesión)
5. [Emparejamiento con código (alternativa al QR)](#5-emparejamiento-con-código-alternativa-al-qr)
6. [Referencia de configuración](#6-referencia-de-configuración)
7. [El objeto socket](#7-el-objeto-socket)
8. [Eventos y listeners](#8-eventos-y-listeners)
9. [Envío de mensajes](#9-envío-de-mensajes)
10. [Envío de multimedia](#10-envío-de-multimedia)
11. [Mensajes interactivos (botones, listas, plantillas)](#11-mensajes-interactivos-botones-listas-plantillas)
12. [Leer y reaccionar a mensajes entrantes](#12-leer-y-reaccionar-a-mensajes-entrantes)
13. [Confirmaciones de lectura y presencia](#13-confirmaciones-de-lectura-y-presencia)
14. [Ciclo de vida de la sesión: logout, reconexión, reintentos](#14-ciclo-de-vida-de-la-sesión-logout-reconexión-reintentos)
15. [API de bajo nivel](#15-api-de-bajo-nivel)
16. [Consejos de producción y anti-ban](#16-consejos-de-producción-y-anti-ban)
17. [Solución de problemas](#17-solución-de-problemas)
18. [Referencia completa de la API](#18-referencia-completa-de-la-api)
19. [Estructura del proyecto](#19-estructura-del-proyecto)
20. [Aviso legal](#20-aviso-legal)

---

## 1. Resumen

WAeys es una traducción de Baileys escrita desde cero en Python. Habla el mismo protocolo binario tipo XMPP que usa WhatsApp Web, a través de una conexión WebSocket cifrada con Noise.

Qué te ofrece:

- **Login por QR** y **login por código de emparejamiento** (número de teléfono).
- **Cifrado de extremo a extremo** con el protocolo Signal (sesiones, prekeys, signed prekeys, claves de identidad).
- **Un bus de eventos completo** (`ev`) que replica a Baileys: `connection.update`, `messages.upsert`, `contacts.upsert`, `chats.upsert`, `creds.update` y más.
- **Envío de mensajes**: texto, imagen, vídeo, audio, sticker, documento, contactos, ubicación, encuestas, reacciones, eventos, álbumes y mensajes interactivos (botones/listas/plantillas vía protobuf crudo).
- **Pipeline multimedia**: subida, cifrado, miniaturas y ayudantes de descarga.
- **Gestor de reintentos de mensajes** para mensajes no entregados.
- **Persistencia de sesión** mediante un key store enchufable (`get`/`set`/`clear`).

### Terminología

| Término | Significado |
|---|---|
| `sock` | El diccionario socket devuelto por `make_socket()`. Contiene métodos y estado. |
| `ev` | El bus de eventos; escucha con `ev.on('nombre.evento', handler)`. |
| `auth` / `authState` | `{'creds': {...}, 'keys': store}` — credenciales + key store de Signal. |
| `creds` | El objeto de credenciales serializable a JSON (me, claves, registration id, etc.). |
| `jid` | "Jabber ID": la dirección de WhatsApp de un chat o usuario, p. ej. `123456789@s.whatsapp.net`. |
| `lid` | Identidad de largo plazo (LID) usada por cuentas nuevas de WhatsApp. |
| `código de emparejamiento` | Un código de 8 caracteres para vincular un teléfono en lugar de escanear un QR. |

---

## 2. Requisitos e instalación

### 2.1 Entornos soportados

WAeys es **Python puro** e independiente de la plataforma. Funciona donde exista Python 3.10+:

- Linux (Debian/Ubuntu, Arch, Fedora, …)
- macOS
- Windows (CPython)
- Android vía **Termux**
- Contenedores Docker, servidores VPS, Raspberry Pi

La única dependencia en runtime es **`websockets` (>= 12.0)**. **No hay Node.js** involucrado.

### 2.2 Instalación desde PyPI

```bash
pip install waeys
```

### 2.3 Instalación desde el código fuente (desarrollo)

```bash
git clone https://github.com/toZyn/WAeys.git
cd WAeys
pip install -e .            # instalación editable
# o, para construir una rueda:
pip install build
python -m build
pip install dist/waeys-0.1.0-py3-none-any.whl
```

### 2.4 Verificar la instalación

```python
import WAeys
print(WAeys.__version__)   # "0.1.0"
```

Si obtienes `ModuleNotFoundError: No module named 'websockets'`:

```bash
pip install "websockets>=12.0"
```

### 2.5 Nota sobre intérpretes de Python

Si tu máquina tiene varias instalaciones de Python (muy común en Termux/Linux), asegúrate de que el intérprete que usas para **instalar** el paquete es el mismo con el que **ejecutas** tu script:

```bash
python3 -c "import websockets; print(websockets.__version__)"   # debe funcionar
```

---

## 3. Primera conexión

El punto de entrada es `make_socket(config)` en `WAeys.Socket`. Devuelve un diccionario (`sock`) con todo lo que necesitas.

### 3.1 Ejemplo mínimo de login con QR

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

    # Mostrar el QR en cuanto se genera
    async def on_connection_update(update):
        qr = update.get('qr')
        if qr:
            print('Escanea este QR con WhatsApp > Dispositivos vinculados')
            print(qr)
        if update.get('connection') == 'open':
            print('¡Conectado!')
            # desde aquí ya puedes enviar mensajes, ver sección 9
            await sock['sendMessage']('123456789@s.whatsapp.net', {'text': '¡Hola desde WAeys!'})
            await sock['end']()

    ev.on('connection.update', lambda u: asyncio.ensure_future(on_connection_update(u)))

    # mantener vivo el proceso
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())
```

### 3.2 Qué ocurre entre bambalinas

1. `make_socket()` genera un par de claves Curve25519 efímero y construye el cliente Noise.
2. Abre un WebSocket hacia `wss://web.whatsapp.com/ws/chat`.
3. Emite `connection.update` con `{'qr': '...'}` (repetible hasta que caduque) o, si ya existe sesión, valida credenciales y emite `{'connection': 'open'}`.
4. Tras un vínculo correcto, sube los prekeys y emite `{'connection': 'open'}`.

> **Importante**: al vincular un *dispositivo nuevo* debes esperar al evento `connection: open` antes de enviar nada. El flag `registered: true` por sí solo no basta — primero deben subirse los prekeys.

---

## 4. Autenticación y persistencia de sesión

### 4.1 El estado de autenticación

`config['auth']` debe ser un diccionario con dos claves:

```python
auth = {
    'creds': {...},   # diccionario plano, datos de credenciales serializables
    'keys': store,    # key store asíncrono: {get, set, clear}
}
```

`init_auth_creds()` (`WAeys.Utils.auth_utils`) devuelve un conjunto de credenciales nuevo y vacío:

```python
from WAeys.Utils.auth_utils import init_auth_creds, make_memory_key_store
creds = init_auth_creds()
```

Contiene (entre otros):

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

### 4.2 El key store

El store `keys` es la base de datos de sesiones Signal / sender-keys / pre-keys. Debe implementar tres métodos **asíncronos**:

```python
class MiStore:
    async def get(self, type_: str, ids: list) -> dict:
        # devuelve {id: valor, ...} para los ids pedidos
        ...

    async def set(self, data: dict) -> None:
        # data = {type_: {id: valor}}
        ...

    async def clear(self) -> None:
        ...
```

Los valores de `type_` provienen de `SignalTypes`: `session`, `sender-key`, `app-state-sync-key`, `app-state-sync-version`, etc.

### 4.3 Un key store simple respaldado en ficheros

El ejemplo siguiente es el punto de partida recomendado para la mayoría de bots. Guarda cada cambio en disco para que puedas reiniciar y seguir con la sesión iniciada.

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

### 4.4 Persistir las actualizaciones de credenciales

WAeys emite `creds.update` siempre que cambian las credenciales (tras el emparejamiento, rotación de claves, etc.). **Debes persistirlas**, o la sesión no sobrevivirá a un reinicio:

```python
async def on_creds_update(update):
    auth['creds'].update(update)
    save_creds(auth['creds'])

ev.on('creds.update', lambda u: asyncio.ensure_future(on_creds_update(u)))
```

### 4.5 Restaurar una sesión

Al arrancar, carga la sesión guardada y conéctala. Si existe una sesión vinculada válida, WAeys simplemente se reconecta y emite `connection: open`:

```python
creds = load_creds()
if creds is not None:
    config['auth'] = {'creds': creds, 'keys': make_file_key_store()}
else:
    config['auth'] = {'creds': init_auth_creds(), 'keys': make_file_key_store()}
```

> **Trampa**: una sesión guardada cuyos prekeys nunca se subieron (por ejemplo si el proceso se mató justo tras el emparejamiento) fallará con `CB:failure` / "Connection Failure". En ese caso vuelve a vincular. Por eso es importante esperar a `connection: open` durante el emparejamiento.

---

## 5. Emparejamiento con código (alternativa al QR)

En lugar de escanear un QR puedes pedir a WhatsApp un **código de emparejamiento** de 8 caracteres e introducirlo manualmente.

### 5.1 Cómo funciona

1. Crea el socket con un auth state nuevo.
2. Espera a que `connection.update` entregue un valor `qr` (indica que WhatsApp está listo para emparejar).
3. Llama a `sock['requestPairingCode'](phone_number)`.
4. Imprime el código para que el usuario lo teclee en: **WhatsApp → Ajustes → Dispositivos vinculados → Vincular un dispositivo → Vincular con número de teléfono**.
5. Espera a `connection: open`.

> **Importante**: usa el **número internacional completo** sin `+`, p. ej. `51921826291` para un número de Perú.

### 5.2 Ejemplo completo de emparejamiento con bucle de reintentos

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
    config['keepAliveIntervalMs'] = 5000   # el keep-alive es crucial durante el emparejamiento
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
                print(f'\nCÓDIGO DE EMPAREJAMIENTO: {code}\n')
            except Exception as err:
                print('la petición de emparejamiento falló:', err)
        if update.get('connection') == 'open':
            print('EMPAREJADO Y ABIERTO')
            done.set()

    ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))

    try:
        await asyncio.wait_for(done.wait(), timeout=120)
    except asyncio.TimeoutError:
        print('tiempo de espera agotado durante el emparejamiento')
    finally:
        await sock['end']()
    return done.is_set()


async def main():
    auth = {'creds': init_auth_creds(), 'keys': make_file_key_store()}
    attempt = 1
    while True:
        print(f'--- intento de emparejamiento {attempt} ---')
        ok = await pair(auth)
        if ok:
            print('ÉXITO. Sesión guardada.')
            return
        attempt += 1
        await asyncio.sleep(3)
        auth['creds'] = init_auth_creds()
        save_creds(auth['creds'])


asyncio.run(main())
```

### 5.3 Trampas del emparejamiento

- **Mantén viva la conexión**: usa un `keepAliveIntervalMs` corto (5000) porque WhatsApp corta las conexiones sin vincular tras ~90 segundos.
- **No ejecutes dos procesos de emparejamiento a la vez** — generan claves en conflicto y WhatsApp puede responder `rate-overlimit`.
- **`rate-overlimit`** significa que hiciste demasiadas peticiones; espera 30–60 minutos.
- Si el código es rechazado ("código incorrecto"), la conexión de emparejamiento pudo morir antes de que introdujeras el código; reconecta y pide un código nuevo.
- Tras emparejar, **espera a `connection: open`** antes de usar la sesión, para que se suban los prekeys.

---

## 6. Referencia de configuración

`default_connection_config()` devuelve un diccionario que puedes sobrescribir. Lista completa de opciones:

| Clave | Valor por defecto | Descripción |
|---|---|---|
| `version` | `[2, 3000, ...]` | Versión del protocolo WhatsApp Web enviada al conectar. |
| `browser` | `Browsers.macOS('Chrome')` | Identificación de navegador. Usa `Browsers.ubuntu/macOS/windows/android/baileys/appropriate`. |
| `waWebSocketUrl` | `wss://web.whatsapp.com/ws/chat` | URL del servidor. |
| `connectTimeoutMs` | `20000` | Tiempo de espera para establecer el WebSocket. |
| `keepAliveIntervalMs` | `30000` | Intervalo de ping. Bájalo a 5000 durante el emparejamiento. |
| `logger` | logger hijo | Cualquier objeto tipo `log` con `.info/.warn/.error/.debug`. |
| `emitOwnEvents` | `True` | Emite eventos para los mensajes que envías tú. |
| `defaultQueryTimeoutMs` | `60000` | Timeout por defecto para consultas IQ. |
| `customUploadHosts` | `[]` | Sobrescribe los hosts de subida de multimedia. |
| `retryRequestDelayMs` | `250` | Retardo antes de reintentar peticiones fallidas. |
| `maxMsgRetryCount` | `5` | Nº máximo de reintentos de envío. |
| `fireInitQueries` | `True` | Ejecuta las consultas de inicialización al conectar. |
| `auth` | `None` | El estado de autenticación (obligatorio). |
| `markOnlineOnConnect` | `True` | Transmite presencia "en línea". |
| `syncFullHistory` | `True` | Sincroniza el historial completo al iniciar sesión. |
| `patchMessageBeforeSending` | interno | Hook para mutar mensajes antes de enviarlos. |
| `shouldSyncHistoryMessage` | interno | Filtra qué tipos de sync de historial se procesan. |
| `shouldIgnoreJid` | `lambda: False` | Omite el procesamiento de ciertos JIDs. |
| `linkPreviewImageThumbnailWidth` | `192` | Ancho de la miniatura de vista previa de enlaces. |
| `transactionOpts` | `{maxCommitRetries:10, delayBetweenTriesMs:3000}` | Política de reintentos de transacciones de app-state. |
| `generateHighQualityLinkPreview` | `False` | Sube una miniatura de alta calidad para vistas previas. |
| `enableAutoSessionRecreation` | `True` | Recrea sesiones Signal cuando es necesario. |
| `enableRecentMessageCache` | `True` | Cachea mensajes recientes. |
| `options` | `{}` | Opciones HTTP extra. |
| `appStateMacVerification` | `{patch:False,snapshot:False}` | Verifica los MAC del app-state. |
| `countryCode` | `'US'` | Código de país usado en algunas consultas. |
| `getMessage` | `lambda: None` | Se usa para resolver contenido de mensajes en reintentos. |
| `cachedGroupMetadata` | `lambda: None` | Hook de caché de metadatos de grupo. |
| `makeSignalRepository` | interno | Cómo construir el repositorio libsignal. |
| `printQRInTerminal` | obsoleto | Auto-impresión de QR; escucha eventos en su lugar. |

---

## 7. El objeto socket

`make_socket(config)` devuelve un diccionario. Miembros de uso común:

```python
sock = make_socket(config)

sock['ws']              # WebSocketClient
sock['ev']              # bus de eventos
sock['authState']       # {'creds': ..., 'keys': ...}
sock['user']            # callable -> creds.get('me')
sock['query']           # consulta IQ asíncrona
sock['waitForMessage']  # espera de bajo nivel asíncrona
sock['waitForSocketOpen']
sock['sendRawMessage']  # frame noise crudo asíncrono
sock['sendNode']        # envío de nodo binario asíncrono
sock['logout']          # logout asíncrono
sock['end']             # cierre asíncrono
sock['requestPairingCode']   # código de emparejamiento asíncrono
sock['uploadPreKeys']   # asíncrono
sock['rotateSignedPreKey']   # asíncrono
sock['sendWAMBuffer']   # asíncrono
sock['executeUSyncQuery']    # asíncrono
sock['onWhatsApp']      # comprobación de teléfono asíncrona
sock['waitForConnectionUpdate']  # ayudante de espera asíncrono
```

Si envuelves el socket con la capa de mensajes (ver `WAeys.Socket.messages_send.make_messages_socket`), además obtienes:

```python
sock['sendMessage']     # enviar cualquier mensaje (asíncrono)
sock['relayMessage']    # relay de bajo nivel de un mensaje protobuf
sock['sendReceipt']     # acuses de recibo asíncronos
sock['sendReceipts']
sock['readMessages']    # marcar como leído
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

## 8. Eventos y listeners

El bus de eventos `ev` soporta:

```python
ev.on(event, listener)            # suscribirse
ev.off(event, listener)           # darse de baja
ev.remove_all_listeners(event)    # eliminar todos los del evento (o todos si event es None)
```

Los listeners son funciones normales invocadas con el payload. **Son síncronas** — para trabajo asíncrono, envuélvelas con `asyncio.ensure_future(...)`.

### 8.1 Eventos de conexión

Payload de `connection.update`:

```python
{'qr': '...', 'isNewLogin': True}            # durante el emparejamiento por QR
{'connection': 'connecting', 'qr': None}
{'receivedPendingNotifications': True}
{'connection': 'open'}                       # completamente listo
{'connection': 'close',
 'lastDisconnect': {'error': <error Boom>}}  # cerrado/fallido
{'connection': 'reconnecting'}
{'reachoutTimeLock': ...}
```

### 8.2 Eventos de credenciales

`creds.update` — actualización parcial que debes aplicar a `auth['creds']` (¡persístela!).

### 8.3 Eventos de mensajes

| Evento | Payload |
|---|---|
| `messages.upsert` | `{'messages': [WAMessage, ...], 'type': 'notify'/'append'/'replace'}` |
| `messages.update` | `[{'key': ..., 'update': {...}}]` — estado/ediciones |
| `messages.media-update` | `[event]` — progreso/resultado de descarga de multimedia |
| `message-capping.update` | info de limitación de mensajes |

### 8.4 Eventos de chats/contactos/grupos

| Evento | Payload |
|---|---|
| `chats.upsert` | lista de chats |
| `contacts.upsert` | lista de contactos |
| `contacts.update` | lista de actualizaciones de contactos |
| `groups.upsert` | lista de metadatos de grupo |
| `blocklist.update` | cambios en la lista de bloqueados |
| `lid-mapping.update` | actualizaciones del mapeo LID |

### 8.5 Ejemplo de recepción de mensajes

```python
async def on_messages_upsert(data):
    for msg in data['messages']:
        key = msg.get('key', {})
        remote = key.get('remoteJid')
        content = msg.get('message') or {}
        # encuentra el tipo de contenido real
        text = content.get('conversation') or content.get('extendedTextMessage', {}).get('text')
        print(f'[{remote}] {text}')

ev.on('messages.upsert', lambda d: asyncio.ensure_future(on_messages_upsert(d)))
```

---

## 9. Envío de mensajes

La API principal es `await sock['sendMessage'](jid, content, options)`.

### 9.1 Texto plano

```python
await sock['sendMessage']('51921826291@s.whatsapp.net', {'text': '¡Hola mundo!'})
```

### 9.2 Texto con menciones

```python
await sock['sendMessage'](jid, {
    'text': 'Hola @123456789 y @987654321',
    'mentions': ['123456789@s.whatsapp.net', '987654321@s.whatsapp.net'],
})
```

### 9.3 Responder/citar otro mensaje

```python
quoted = {
    'key': {'remoteJid': jid, 'id': msg_id, 'fromMe': False},
    'message': contenido_del_mensaje_original,
}
await sock['sendMessage'](jid, {'text': 'Mi respuesta'}, {'quoted': quoted})
```

### 9.4 Reacción

```python
await sock['sendMessage'](jid, {'react': {'text': '🔥', 'key': msg_key}})
```

### 9.5 Borrar un mensaje

```python
await sock['sendMessage'](jid, {'delete': msg_key})
```

### 9.6 Editar un mensaje

```python
await sock['sendMessage'](jid, {'edit': msg_key, 'text': 'Texto editado'})
```

### 9.7 Encuesta

```python
await sock['sendMessage'](jid, {
    'poll': {
        'name': '¿Mejor lenguaje de programación?',
        'values': ['Python', 'JavaScript', 'Rust'],
        'selectableCount': 1,
    }
})
```

### 9.8 Contactos

```python
await sock['sendMessage'](jid, {
    'contacts': {'contacts': [
        {'displayName': 'Juana', 'vcard': 'BEGIN:VCARD\nVERSION:3.0\nFN:Juana\nEND:VCARD'},
    ]}
})
```

### 9.9 Ubicación

```python
await sock['sendMessage'](jid, {
    'location': {'degreesLatitude': -12.0464, 'degreesLongitude': -77.0428, 'name': 'Lima'},
})
```

### 9.10 Evento (calendario)

```python
from datetime import datetime, timedelta
await sock['sendMessage'](jid, {
    'event': {
        'name': 'Reunión',
        'startDate': datetime.now() + timedelta(hours=1),
        'endDate': datetime.now() + timedelta(hours=2),
    }
})
```

### 9.11 Opciones comunes a todos los envíos

```python
await sock['sendMessage'](jid, content, {
    'quoted': quoted_msg,          # responder a
    'timestamp': datetime.now(),   # timestamp personalizado
    'messageId': 'mi-id-custom',   # id de mensaje personalizado
    'ephemeralExpiration': 7 * 86400,   # mensaje efímero (segundos)
    'backgroundColor': '#FF0000',  # fondo del texto de estado
    'font': 4,                     # fuente del estado
})
```

---

## 10. Envío de multimedia

La multimedia se sube a los servidores de WhatsApp, se cifra y se envía automáticamente. Proporciona los bytes o una ruta.

### 10.1 Imagen

```python
with open('gato.jpg', 'rb') as f:
    await sock['sendMessage'](jid, {
        'image': f.read(),
        'caption': 'Mira este gato',
        'fileName': 'gato.jpg',
        'mimetype': 'image/jpeg',
    })
```

### 10.2 Vídeo / audio / documento / sticker

```python
# vídeo
await sock['sendMessage'](jid, {'video': data, 'caption': 'vídeo', 'mimetype': 'video/mp4'})
# audio
await sock['sendMessage'](jid, {'audio': data, 'mimetype': 'audio/mp4', 'ptt': False})
# nota de voz (push-to-talk)
await sock['sendMessage'](jid, {'audio': data, 'mimetype': 'audio/ogg; codecs=opus', 'ptt': True})
# documento
await sock['sendMessage'](jid, {'document': data, 'fileName': 'informe.pdf', 'mimetype': 'application/pdf', 'caption': 'Informe'})
# sticker
await sock['sendMessage'](jid, {'sticker': data, 'mimetype': 'image/webp'})
```

### 10.3 GIF

```python
await sock['sendMessage'](jid, {'video': data, 'gifPlayback': True, 'mimetype': 'video/mp4'})
```

### 10.4 Multimedia viewOnce

```python
await sock['sendMessage'](jid, {'image': data, 'viewOnce': True, 'mimetype': 'image/jpeg'})
```

### 10.5 Campos de multimedia

Campos comunes por tipo de medio: `caption`, `mimetype`, `fileName`, `fileLength`, `viewOnce`, `ptt`, `gifPlayback`, `jpegThumbnail` (vista previa), `duration` (audio/vídeo), `contextInfo`.

### 10.6 Descargar multimedia (recibida)

Usa los ayudantes de `WAeys.Utils.messages_media`:

```python
from WAeys.Utils.messages_media import download_content_from_message

buffer, mimetype = await download_content_from_message(msg, media_keys)
```

Las media keys (`mediaKey`) ya están en el mensaje recibido; pasa el objeto del mensaje y un resolvedor del store. Para mayor comodidad, `decrypt_media_retry_data` y `get_media_keys` ayudan a calcular las claves.

---

## 11. Mensajes interactivos (botones, listas, plantillas)

WAeys **no** trae un atajo en dict para mensajes interactivos (igual que Baileys TS). Construyes un **`proto.Message` completo** y lo envías con `generate_wa_message_from_content` + `relayMessage`, o pasas un mensaje protobuf crudo.

### 11.1 El patrón general

```python
from WAeys.WAProto import WAProto as proto
from WAeys.Utils.messages import generate_wa_message_from_content
from WAeys.Utils.generics import generate_message_id_v2

msg = proto.Message.from_object({
    'interactiveMessage': {
        'body': {'text': 'Elige uno:'},
        'nativeFlowMessage': {
            'buttons': [
                {'name': 'quick_reply',
                 'buttonParamsJson': '{"display_text":"Opción 1","id":"opt1"}'},
                {'name': 'quick_reply',
                 'buttonParamsJson': '{"display_text":"Opción 2","id":"opt2"}'},
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

### 11.2 Mensaje de lista

```python
msg = proto.Message.from_object({
    'listMessage': {
        'title': 'Menú',
        'description': 'Elige una sección',
        'footerText': 'Powered by WAeys',
        'buttonText': 'Opciones',
        'sections': [{
            'title': 'Principal',
            'rows': [
                {'title': 'Pizza', 'description': 'Queso', 'rowId': 'pizza'},
                {'title': 'Hamburguesa', 'description': 'Res', 'rowId': 'burger'},
            ],
        }],
        'listType': 1,   # proto.Message.ListMessage.ListType.SINGLE_SELECT
    },
})
```

### 11.3 Mensaje de botones

```python
msg = proto.Message.from_object({
    'buttonsMessage': {
        'contentText': 'Elige:',
        'footerText': 'pie',
        'buttons': [
            {'buttonId': 'si', 'buttonText': {'displayText': 'Sí'}, 'type': 1},
            {'buttonId': 'no', 'buttonText': {'displayText': 'No'},  'type': 1},
        ],
        'headerType': 1,
    },
})
```

### 11.4 Mensaje de plantilla

```python
msg = proto.Message.from_object({
    'templateMessage': {
        'hydratedFourRowTemplate': {
            'hydratedContentText': '¡Bienvenido!',
            'hydratedFooterText': 'pie',
            'templateButtons': [
                {'quickReplyButton': {'displayText': 'Ir', 'id': 'go'}},
            ],
        },
    },
})
```

### 11.5 Interactivo con cabecera multimedia

```python
media_result = await prepare_wa_message_media({'image': img_bytes}, opts)
msg = proto.Message.from_object({
    'interactiveMessage': {
        'header': {'title': 'Cabecera', 'hasMediaAttachment': True,
                   'imageMessage': media_result.imageMessage},
        'body': {'text': 'Texto del cuerpo'},
        'nativeFlowMessage': {'buttons': [...]},
    },
})
```

> Campos disponibles en el proto: `buttonsMessage=42`, `listMessage=36`, `templateMessage=25`, `interactiveMessage=45`, `nativeFlowMessage` dentro de `interactiveMessage`.

### 11.6 Gestionar respuestas interactivas

Las respuestas a botones/listas llegan como `messages.upsert` con tipos de contenido como:

- `buttonsResponseMessage` (respuestas a botones)
- `listResponseMessage` (respuestas a listas)
- `templateButtonReplyMessage` (respuestas a plantillas)

```python
content = msg.get('message') or {}
if content.get('buttonsResponseMessage'):
    print('Botón:', content['buttonsResponseMessage'].get('selectedButtonId'))
elif content.get('listResponseMessage'):
    print('Lista:', content['listResponseMessage'].get('singleSelectReply', {}).get('selectedRowId'))
```

---

## 12. Leer y reaccionar a mensajes entrantes

### 12.1 Iterar sobre los upserts

```python
async def on_upsert(data):
    for msg in data['messages']:
        if msg.get('key', {}).get('fromMe'):
            continue          # omite los tuyos (salvo emitOwnEvents)
        jid = msg['key']['remoteJid']
        content = msg.get('message') or {}
        ctype = next((k for k in content if content.get(k)), None)
        print('tipo:', ctype, '| de:', jid)
        if ctype == 'conversation':
            text = content['conversation']
        elif ctype == 'extendedTextMessage':
            text = content['extendedTextMessage'].get('text')
        # ... gestiona el resto

ev.on('messages.upsert', lambda d: asyncio.ensure_future(on_upsert(d)))
```

### 12.2 Ejemplo de router de comandos

```python
COMMANDS = {
    '/ping': lambda: 'pong',
    '/hora': lambda: str(datetime.now()),
}

async def on_upsert(data):
    for msg in data['messages']:
        if msg.get('key', {}).get('fromMe'):
            continue
        jid = msg['key']['remoteJid']
        content = msg.get('message') or {}
        text = content.get('conversation') or content.get('extendedTextMessage', {}).get('text') or ''
        if text.startswith('/'):
            reply = COMMANDS.get(text.split()[0], lambda: 'Comando desconocido')()
            await sock['sendMessage'](jid, {'text': reply})
```

### 12.3 Obtener chat id / jid

```python
from WAeys.Utils.process_message import get_chat_id
chat_id = get_chat_id(msg)   # jid del chat
```

`is_real_message(msg)` te dice si el mensaje es real de usuario (no de estado/sistema/protocolo).

---

## 13. Confirmaciones de lectura y presencia

### 13.1 Marcar mensajes como leídos

```python
await sock['readMessages']([{'remoteJid': jid, 'id': msg_id, 'fromMe': False}])
```

### 13.2 Enviar acuses de recibo

```python
await sock['sendReceipts'](keys, 'read')        # 'read' / 'delivered'
await sock['sendReceipt'](jid, participant, [msg_id], 'read')
```

### 13.3 Comprobar si un teléfono está en WhatsApp

```python
result = await sock['onWhatsApp']('51921826291')
# [{'exists': True, 'jid': '51921826291@s.whatsapp.net'}]
```

### 13.4 Presencia en línea

La presencia se controla con `markOnlineOnConnect` a nivel de configuración. El control de bajo nivel de presencia usa `sock['query']` con el IQ de presencia apropiado (como en Baileys).

---

## 14. Ciclo de vida de la sesión: logout, reconexión, reintentos

### 14.1 Apagado correcto

```python
await sock['end']()        # cierra limpio (detiene keep-alive, cierra ws)
await sock['logout']()     # logout del lado del servidor (invalida la sesión)
```

### 14.2 Detectar desconexiones y reconectar

```python
async def on_conn(update):
    if update.get('connection') == 'close':
        err = update.get('lastDisconnect', {}).get('error') if isinstance(update.get('lastDisconnect'), dict) else None
        print('desconectado:', err)
        # recrea el socket con EL MISMO auth state
        new_sock = make_socket(config)
        # vuelve a registrar handlers, continúa...

ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))
```

WAeys **no trae reconexión automática** (igual que el socket base de Baileys). Los bots de producción envuelven el socket en un bucle de reconexión reutilizando la sesión guardada.

### 14.3 Reintentos de mensajes

Un `MessageRetryManager` se expone en `sock['messageRetryManager']` y lo usa `relayMessage` automáticamente para entregas fallidas (`maxMsgRetryCount`, `retryRequestDelayMs`).

### 14.4 Registrar handlers de fin de socket

```python
sock['registerSocketEndHandler'](lambda: print('socket terminado'))
```

### 14.5 Esperar una actualización de conexión

```python
update = await sock['waitForConnectionUpdate'](lambda u: u.get('connection') == 'open')
```

---

## 15. API de bajo nivel

### 15.1 Enviar un nodo binario

```python
from WAeys.WABinary.types import BinaryNode
node = BinaryNode(tag='iq', attrs={'type': 'get', 'to': 's.whatsapp.net', 'id': '123'}, content=None)
await sock['sendNode'](node)
```

### 15.2 Consulta IQ

```python
result = await sock['query'](node)      # devuelve el BinaryNode de respuesta
```

### 15.3 Frames crudos

```python
await sock['sendRawMessage'](payload_bytes)
```

### 15.4 Prekeys

```python
await sock['uploadPreKeys']()                       # sube N prekeys
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

## 16. Consejos de producción y anti-ban

WAeys, como todo cliente no oficial de WhatsApp, puede hacer que te **baneen** el número. **No hay anti-ban incorporado** en la librería (igual que Baileys). Sigue estas reglas:

1. **Comportamiento humano**: envía mensajes con retardos aleatorios (2–8 s) en lugar de ráfagas instantáneas.
2. **Nunca hagas spam**: evita mensajes masivos idénticos, inundar grupos o añadir contactos agresivamente.
3. **Calienta el número**: para un número nuevo, empieza con volumen bajo y aumenta gradualmente en días.
4. **No reutilices sesiones baneadas**: si banean un número, borra su sesión y credenciales.
5. **Mantén una conexión estable**: ejecuta con keep-alive; evita matar el proceso repetidamente durante el login.
6. **Usa emparejamiento en lugar de nuevos logins repetidos**: los re-vínculos por QR repetidos pueden provocar `rate-overlimit`.
7. **No ejecutes sesiones paralelas** con el mismo número.
8. **Mantén la versión/dependencias actualizadas**: usa la versión del protocolo que soporta la librería.

### 16.1 Ayudante de envío con retardo

```python
import random

async def safe_send(jid, content, min_delay=2.0, max_delay=6.0):
    await asyncio.sleep(random.uniform(min_delay, max_delay))
    await sock['sendMessage'](jid, content)
```

---

## 17. Solución de problemas

### 17.1 `ModuleNotFoundError: No module named 'websockets'`
Instala la dependencia con el mismo intérprete que ejecuta tu script:
```bash
pip install "websockets>=12.0"
```

### 17.2 El QR nunca aparece / la conexión cae durante el emparejamiento
WhatsApp corta las conexiones sin vincular tras ~90 s. Usa `keepAliveIntervalMs: 5000` y reconecta hasta emparejar.

### 17.3 `rate-overlimit` al pedir códigos de emparejamiento
Demasiados intentos. Espera 30–60 minutos, y asegúrate de no ejecutar varios procesos de emparejamiento a la vez.

### 17.4 Sesión guardada pero el login falla con "Connection Failure"
Los prekeys nunca se subieron (la sesión se guardó demasiado pronto). Vuelve a emparejar y espera a `connection: open`.

### 17.5 `Invalid media type`
Pasaste una clave de contenido desconocida a `sendMessage`. Usa una de: `image`, `video`, `audio`, `document`, `sticker`, `ptt`, `gif`, `ptv`, `product`.

### 17.6 Errores `Boom` / `CB:failure`
Revisa `connection.update` y su `lastDisconnect.error`, y los logs. Causas comunes: sesión caducada, sesión revocada o flujo de emparejamiento incorrecto.

### 17.7 Ver `'tb'` en los logs
Si el logger imprime una clave `tb`, es un traceback real de Python del socket interno — activa el nivel de debug de tu logger para leerlo.

---

## 18. Referencia completa de la API

### Paquete `WAeys`

| Ruta | Propósito |
|---|---|
| `WAeys.WABinary` | Codificación/decodificación de nodos binarios |
| `WAeys.Utils` | Todos los ayudantes (auth, crypto, mensajes, multimedia, …) |
| `WAeys.Defaults` | Valores por defecto y constantes (`default_connection_config`) |
| `WAeys.Types` | Tipos y enums |
| `WAeys.WAProto` | Clases protobuf generadas (Python puro) |
| `WAeys.Signal` | Implementación del protocolo Signal |
| `WAeys.Socket` | `make_socket`, cliente websocket, capas de mensajes |

### Funciones Utils clave

| Función | Módulo |
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

### Métodos del socket (de `make_socket`)

| Método | Devuelve | Descripción |
|---|---|---|
| `requestPairingCode(phone)` | str | Obtiene el código de emparejamiento de 8 caracteres |
| `sendMessage(jid, content, options?)` | dict mensaje | Envía cualquier mensaje |
| `relayMessage(jid, proto_msg, opts?)` | — | Relay de bajo nivel |
| `readMessages(keys)` | — | Marcar como leído |
| `sendReceipts(keys, type)` | — | Enviar acuses |
| `onWhatsApp(phone)` | list | Comprueba números de teléfono |
| `query(node)` | BinaryNode | Consulta IQ |
| `waitForConnectionUpdate(pred)` | update | Espera una condición |
| `uploadPreKeys()` | — | Sube prekeys |
| `logout()` | — | Logout del servidor |
| `end()` | — | Cierra la conexión |
| `executeUSyncQuery(q)` | — | Consulta USync |
| `sendWAMBuffer(buf)` | — | Envía buffer WAM |

---

## 19. Estructura del proyecto

```
WAeys/
├── __init__.py          # init del paquete, __version__
├── Defaults/            # config por defecto, constantes, mapas de medios
├── Types/               # tipos de auth/mensaje/chat/evento
├── Utils/               # crypto, mensajes, multimedia, auth, noise, etc.
├── WABinary/            # códec de nodos binarios
├── WAProto/             # clases protobuf en python puro + .proto
├── Signal/              # protocolo Signal (sesiones, prekeys)
├── Socket/              # make_socket + capas de envío/recepción
│   └── Client/          # cliente websocket
├── WAM/                 # WhatsApp Analytics Message
└── WAUSync/             # consultas USync
```

---

## 20. Aviso legal

**WAeys no está afiliado, respaldado ni conectado con WhatsApp o Meta Platforms, Inc.** Es un cliente no oficial que usa el protocolo de WhatsApp Web. Su uso puede violar los Términos de Servicio de WhatsApp y podría conllevar restricciones temporales o permanentes de la cuenta. Eres el único responsable del uso que le des a esta librería.

---

*Generado para WAeys v0.1.0 — port de Baileys en Python puro. Consulta también las versiones en [inglés](usage.en.md) y [portugués](usage.pt.md).*
