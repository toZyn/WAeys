# WAeys — Guia completa de uso (Português)

> **Port puro em Python de [Baileys](https://github.com/WhiskeySockets/Baileys)** — um cliente do protocolo do WhatsApp Web que funciona **sem Node.js**. Toda a criptografia (Signal E2EE, handshake Noise, AES, Curve25519) está implementada em Python puro.

Este guia é a referência completa para instalar, configurar, conectar, parear, enviar e receber mensagens e implantar um bot construído com **WAeys**.

---

## Índice

1. [Visão geral](#1-visão-geral)
2. [Requisitos e instalação](#2-requisitos-e-instalação)
3. [Primeira conexão](#3-primeira-conexão)
4. [Autenticação e persistência de sessão](#4-autenticação-e-persistência-de-sessão)
5. [Pareamento com código (alternativa ao QR)](#5-pareamento-com-código-alternativa-ao-qr)
6. [Referência de configuração](#6-referência-de-configuração)
7. [O objeto socket](#7-o-objeto-socket)
8. [Eventos e listeners](#8-eventos-e-listeners)
9. [Envio de mensagens](#9-envio-de-mensagens)
10. [Envio de mídia](#10-envio-de-mídia)
11. [Mensagens interativas (botões, listas, modelos)](#11-mensagens-interativas-botões-listas-modelos)
12. [Ler e reagir a mensagens recebidas](#12-ler-e-reagir-a-mensagens-recebidas)
13. [Confirmações de leitura e presença](#13-confirmações-de-leitura-e-presença)
14. [Ciclo de vida da sessão: logout, reconexão, tentativas](#14-ciclo-de-vida-da-sessão-logout-reconexão-tentativas)
15. [API de baixo nível](#15-api-de-baixo-nível)
16. [Dicas de produção e anti-ban](#16-dicas-de-produção-e-anti-ban)
17. [Solução de problemas](#17-solução-de-problemas)
18. [Referência completa da API](#18-referência-completa-da-api)
19. [Estrutura do projeto](#19-estrutura-do-projeto)
20. [Aviso legal](#20-aviso-legal)

---

## 1. Visão geral

WAeys é uma tradução do Baileys escrita do zero em Python. Ele fala o mesmo protocolo binário parecido com XMPP que o WhatsApp Web usa, através de uma conexão WebSocket criptografada com Noise.

O que ele oferece:

- **Login por QR** e **login por código de pareamento** (número de telefone).
- **Criptografia de ponta a ponta** com o protocolo Signal (sessões, prekeys, signed prekeys, chaves de identidade).
- **Um barramento de eventos completo** (`ev`) que espelha o Baileys: `connection.update`, `messages.upsert`, `contacts.upsert`, `chats.upsert`, `creds.update` e mais.
- **Envio de mensagens**: texto, imagem, vídeo, áudio, sticker, documento, contatos, localização, enquetes, reações, eventos, álbuns e mensagens interativas (botões/listas/modelos via protobuf puro).
- **Pipeline de mídia**: upload, criptografia, miniaturas e utilitários de download.
- **Gerenciador de novas tentativas de mensagem** para mensagens não entregues.
- **Persistência de sessão** por meio de um key store plugável (`get`/`set`/`clear`).

### Terminologia

| Termo | Significado |
|---|---|
| `sock` | O dicionário socket retornado por `make_socket()`. Contém métodos e estado. |
| `ev` | O barramento de eventos; ouça com `ev.on('nome.evento', handler)`. |
| `auth` / `authState` | `{'creds': {...}, 'keys': store}` — credenciais + key store do Signal. |
| `creds` | O objeto de credenciais serializável em JSON (me, chaves, registration id etc.). |
| `jid` | "Jabber ID": o endereço do WhatsApp de um chat ou usuário, ex.: `123456789@s.whatsapp.net`. |
| `lid` | Identidade de longo prazo (LID) usada por contas novas do WhatsApp. |
| `código de pareamento` | Um código de 8 caracteres para vincular um telefone em vez de escanear um QR. |

---

## 2. Requisitos e instalação

### 2.1 Ambientes suportados

WAeys é **Python puro** e independente de plataforma. Funciona onde existir Python 3.10+:

- Linux (Debian/Ubuntu, Arch, Fedora, …)
- macOS
- Windows (CPython)
- Android via **Termux**
- Containers Docker, servidores VPS, Raspberry Pi

A única dependência em tempo de execução é **`websockets` (>= 12.0)**. **Não há Node.js** envolvido.

### 2.2 Instalação pelo PyPI

```bash
pip install waeys
```

### 2.3 Instalação a partir do código-fonte (desenvolvimento)

```bash
git clone https://github.com/toZyn/WAeys.git
cd WAeys
pip install -e .            # instalação editável
# ou, para gerar uma wheel:
pip install build
python -m build
pip install dist/waeys-0.1.0-py3-none-any.whl
```

### 2.4 Verificar a instalação

```python
import WAeys
print(WAeys.__version__)   # "0.1.0"
```

Se obtiver `ModuleNotFoundError: No module named 'websockets'`:

```bash
pip install "websockets>=12.0"
```

### 2.5 Nota sobre interpretadores Python

Se sua máquina tiver várias instalações de Python (muito comum em Termux/Linux), certifique-se de que o interpretador que você usa para **instalar** o pacote é o mesmo que você usa para **executar** seu script:

```bash
python3 -c "import websockets; print(websockets.__version__)"   # deve funcionar
```

---

## 3. Primeira conexão

O ponto de entrada é `make_socket(config)` em `WAeys.Socket`. Ele retorna um dicionário (`sock`) com tudo que você precisa.

### 3.1 Exemplo mínimo de login por QR

```python
import asyncio

from WAeys.Defaults.index import default_connection_config
from WAeys.Utils.auth_utils import init_auth_creds
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

    # Exibir o QR assim que for gerado
    async def on_connection_update(update):
        qr = update.get('qr')
        if qr:
            print('Escaneie este QR com WhatsApp > Dispositivos vinculados')
            print(qr)
        if update.get('connection') == 'open':
            print('Conectado!')
            # a partir daqui você já pode enviar mensagens, ver seção 9
            await sock['sendMessage']('123456789@s.whatsapp.net', {'text': 'Olá do WAeys!'})
            await sock['end']()

    ev.on('connection.update', lambda u: asyncio.ensure_future(on_connection_update(u)))

    # manter o processo vivo
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())
```

### 3.2 O que acontece por trás dos panos

1. `make_socket()` gera um par de chaves Curve25519 efêmero e constrói o cliente Noise.
2. Ele abre um WebSocket para `wss://web.whatsapp.com/ws/chat`.
3. Ele emite `connection.update` com `{'qr': '...'}` (repetível até expirar) ou, se já existir sessão, valida as credenciais e emite `{'connection': 'open'}`.
4. Após uma vinculação bem-sucedida, ele envia os prekeys e emite `{'connection': 'open'}`.

> **Importante**: ao vincular um *dispositivo novo* você deve aguardar o evento `connection: open` antes de enviar qualquer coisa. A flag `registered: true` sozinha não basta — os prekeys precisam ser enviados primeiro.

---

## 4. Autenticação e persistência de sessão

### 4.1 O estado de autenticação

`config['auth']` deve ser um dicionário com duas chaves:

```python
auth = {
    'creds': {...},   # dicionário simples, dados de credenciais serializáveis
    'keys': store,    # key store assíncrono: {get, set, clear}
}
```

`init_auth_creds()` (`WAeys.Utils.auth_utils`) retorna um conjunto de credenciais novo e vazio:

```python
from WAeys.Utils.auth_utils import init_auth_creds
creds = init_auth_creds()
```

Ele contém (entre outros):

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

### 4.2 O key store

O store `keys` é o banco de dados de sessões Signal / sender-keys / pre-keys. Ele deve implementar três métodos **assíncronos**:

```python
class MeuStore:
    async def get(self, type_: str, ids: list) -> dict:
        # retorna {id: valor, ...} para os ids pedidos
        ...

    async def set(self, data: dict) -> None:
        # data = {type_: {id: valor}}
        ...

    async def clear(self) -> None:
        ...
```

Os valores de `type_` vêm de `SignalTypes`: `session`, `sender-key`, `app-state-sync-key`, `app-state-sync-version` etc.

### 4.3 Um key store simples em arquivos

O exemplo abaixo é o ponto de partida recomendado para a maioria dos bots. Ele salva cada mudança em disco para que você possa reiniciar e continuar logado.

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

### 4.4 Persistir as atualizações de credenciais

WAeys emite `creds.update` sempre que as credenciais mudam (após o pareamento, rotação de chaves etc.). **Você deve persistir essas mudanças**, caso contrário a sessão não sobreviverá a um reinício:

```python
async def on_creds_update(update):
    auth['creds'].update(update)
    save_creds(auth['creds'])

ev.on('creds.update', lambda u: asyncio.ensure_future(on_creds_update(u)))
```

### 4.5 Restaurar uma sessão

Ao iniciar, carregue a sessão salva e conecte-a. Se houver uma sessão vinculada válida, WAeys simplesmente se reconecta e emite `connection: open`:

```python
creds = load_creds()
if creds is not None:
    config['auth'] = {'creds': creds, 'keys': make_file_key_store()}
else:
    config['auth'] = {'creds': init_auth_creds(), 'keys': make_file_key_store()}
```

> **Armadilha**: uma sessão salva cujos prekeys nunca foram enviados (por exemplo, se o processo foi morto logo após o pareamento) falhará com `CB:failure` / "Connection Failure". Nesse caso, vincule novamente. É por isso que é importante esperar `connection: open` durante o pareamento.

---

## 5. Pareamento com código (alternativa ao QR)

Em vez de escanear um QR, você pode pedir ao WhatsApp um **código de pareamento** de 8 caracteres e digitá-lo manualmente.

### 5.1 Como funciona

1. Crie o socket com um auth state novo.
2. Aguarde `connection.update` entregar um valor `qr` (indica que o WhatsApp está pronto para parear).
3. Chame `sock['requestPairingCode'](phone_number)`.
4. Imprima o código para o usuário digitar em: **WhatsApp → Configurações → Dispositivos vinculados → Vincular um dispositivo → Vincular com número de telefone**.
5. Aguarde `connection: open`.

> **Importante**: use o **número internacional completo** sem `+`, ex.: `51921826291` para um número do Peru.

### 5.2 Exemplo completo de pareamento com loop de tentativas

```python
import asyncio
import traceback

from WAeys.Defaults.index import default_connection_config
from WAeys.Utils.auth_utils import init_auth_creds
from WAeys.Utils.browser_utils import Browsers
from WAeys.Socket.socket import make_socket

PHONE = '51921826291'


async def pair(auth):
    config = default_connection_config()
    config['auth'] = auth
    config['browser'] = Browsers.macOS('Safari')
    config['keepAliveIntervalMs'] = 5000   # keep-alive é crucial durante o pareamento
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
                print(f'\nCÓDIGO DE PAREAMENTO: {code}\n')
            except Exception as err:
                print('a solicitação de pareamento falhou:', err)
        if update.get('connection') == 'open':
            print('PAREADO E ABERTO')
            done.set()

    ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))

    try:
        await asyncio.wait_for(done.wait(), timeout=120)
    except asyncio.TimeoutError:
        print('tempo esgotado durante o pareamento')
    finally:
        await sock['end']()
    return done.is_set()


async def main():
    auth = {'creds': init_auth_creds(), 'keys': make_file_key_store()}
    attempt = 1
    while True:
        print(f'--- tentativa de pareamento {attempt} ---')
        ok = await pair(auth)
        if ok:
            print('SUCESSO. Sessão salva.')
            return
        attempt += 1
        await asyncio.sleep(3)
        auth['creds'] = init_auth_creds()
        save_creds(auth['creds'])


asyncio.run(main())
```

### 5.3 Armadilhas do pareamento

- **Mantenha a conexão viva**: use um `keepAliveIntervalMs` curto (5000) porque o WhatsApp derruba conexões não vinculadas após ~90 segundos.
- **Não execute dois processos de pareamento ao mesmo tempo** — eles geram chaves em conflito e o WhatsApp pode responder `rate-overlimit`.
- **`rate-overlimit`** significa que você fez solicitações demais; aguarde 30–60 minutos.
- Se o código for rejeitado ("código incorreto"), a conexão de pareamento pode ter morrido antes de você digitar o código; reconecte e solicite um código novo.
- Após parear, **aguarde `connection: open`** antes de usar a sessão, para que os prekeys sejam enviados.

---

## 6. Referência de configuração

`default_connection_config()` retorna um dicionário que você pode sobrescrever. Lista completa de opções:

| Chave | Padrão | Descrição |
|---|---|---|
| `version` | `[2, 3000, ...]` | Versão do protocolo do WhatsApp Web enviada ao conectar. |
| `browser` | `Browsers.macOS('Chrome')` | Identificação do navegador. Use `Browsers.ubuntu/macOS/windows/android/baileys/appropriate`. |
| `waWebSocketUrl` | `wss://web.whatsapp.com/ws/chat` | URL do servidor. |
| `connectTimeoutMs` | `20000` | Tempo de espera para estabelecer o WebSocket. |
| `keepAliveIntervalMs` | `30000` | Intervalo de ping. Abaixe para 5000 durante o pareamento. |
| `logger` | logger filho | Qualquer objeto tipo `log` com `.info/.warn/.error/.debug`. |
| `emitOwnEvents` | `True` | Emite eventos para mensagens que você envia. |
| `defaultQueryTimeoutMs` | `60000` | Timeout padrão para consultas IQ. |
| `customUploadHosts` | `[]` | Sobrescreve os hosts de upload de mídia. |
| `retryRequestDelayMs` | `250` | Atraso antes de tentar novamente solicitações com falha. |
| `maxMsgRetryCount` | `5` | Nº máximo de novas tentativas de envio. |
| `fireInitQueries` | `True` | Executa as consultas de inicialização ao conectar. |
| `auth` | `None` | O estado de autenticação (obrigatório). |
| `markOnlineOnConnect` | `True` | Transmite presença "online". |
| `syncFullHistory` | `True` | Sincroniza o histórico completo ao entrar. |
| `patchMessageBeforeSending` | interno | Hook para mutar mensagens antes de enviar. |
| `shouldSyncHistoryMessage` | interno | Filtra quais tipos de sync de histórico são processados. |
| `shouldIgnoreJid` | `lambda: False` | Ignora o processamento de certos JIDs. |
| `linkPreviewImageThumbnailWidth` | `192` | Largura da miniatura de prévia de links. |
| `transactionOpts` | `{maxCommitRetries:10, delayBetweenTriesMs:3000}` | Política de tentativas de transações de app-state. |
| `generateHighQualityLinkPreview` | `False` | Envia miniatura de alta qualidade para prévias de links. |
| `enableAutoSessionRecreation` | `True` | Recria sessões Signal quando necessário. |
| `enableRecentMessageCache` | `True` | Armazena em cache mensagens recentes. |
| `options` | `{}` | Opções HTTP extras. |
| `appStateMacVerification` | `{patch:False,snapshot:False}` | Verifica os MACs do app-state. |
| `countryCode` | `'US'` | Código do país usado em algumas consultas. |
| `getMessage` | `lambda: None` | Usado para resolver conteúdo de mensagens em tentativas. |
| `cachedGroupMetadata` | `lambda: None` | Hook de cache de metadados de grupo. |
| `makeSignalRepository` | interno | Como construir o repositório libsignal. |
| `printQRInTerminal` | obsoleto | Auto-impressão de QR; ouça eventos em vez disso. |

---

## 7. O objeto socket

`make_socket(config)` retorna um dicionário. Membros de uso comum:

```python
sock = make_socket(config)

sock['ws']              # WebSocketClient
sock['ev']              # barramento de eventos
sock['authState']       # {'creds': ..., 'keys': ...}
sock['user']            # callable -> creds.get('me')
sock['query']           # consulta IQ assíncrona
sock['waitForMessage']  # espera de baixo nível assíncrona
sock['waitForSocketOpen']
sock['sendRawMessage']  # frame Noise cru assíncrono
sock['sendNode']        # envio de nó binário assíncrono
sock['logout']          # logout assíncrono
sock['end']             # fechamento assíncrono
sock['requestPairingCode']   # código de pareamento assíncrono
sock['uploadPreKeys']   # assíncrono
sock['rotateSignedPreKey']   # assíncrono
sock['sendWAMBuffer']   # assíncrono
sock['executeUSyncQuery']    # assíncrono
sock['onWhatsApp']      # verificação de telefone assíncrona
sock['waitForConnectionUpdate']  # auxiliar de espera assíncrono
```

Se você envolver o socket com a camada de mensagens (ver `WAeys.Socket.messages_send.make_messages_socket`), você também obtém:

```python
sock['sendMessage']     # enviar qualquer mensagem (assíncrono)
sock['relayMessage']    # relay de baixo nível de uma mensagem protobuf
sock['sendReceipt']     # confirmações de recebimento assíncronas
sock['sendReceipts']
sock['readMessages']    # marcar como lido
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

## 8. Eventos e listeners

O barramento de eventos `ev` suporta:

```python
ev.on(event, listener)            # assinar
ev.off(event, listener)           # cancelar assinatura
ev.remove_all_listeners(event)    # remover todos do evento (ou todos se event for None)
```

Listeners são funções simples invocadas com o payload. **Eles são síncronos** — para trabalho assíncrono, envolva com `asyncio.ensure_future(...)`.

### 8.1 Eventos de conexão

Payload de `connection.update`:

```python
{'qr': '...', 'isNewLogin': True}            # durante o pareamento por QR
{'connection': 'connecting', 'qr': None}
{'receivedPendingNotifications': True}
{'connection': 'open'}                       # totalmente pronto
{'connection': 'close',
 'lastDisconnect': {'error': <erro Boom>}}   # fechado/com falha
{'connection': 'reconnecting'}
{'reachoutTimeLock': ...}
```

### 8.2 Eventos de credenciais

`creds.update` — atualização parcial que você deve aplicar a `auth['creds']` (persista-a!).

### 8.3 Eventos de mensagens

| Evento | Payload |
|---|---|
| `messages.upsert` | `{'messages': [WAMessage, ...], 'type': 'notify'/'append'/'replace'}` |
| `messages.update` | `[{'key': ..., 'update': {...}}]` — status/edições |
| `messages.media-update` | `[event]` — progresso/resultado de download de mídia |
| `message-capping.update` | info de limite de mensagens |

### 8.4 Eventos de chats/contatos/grupos

| Evento | Payload |
|---|---|
| `chats.upsert` | lista de chats |
| `contacts.upsert` | lista de contatos |
| `contacts.update` | lista de atualizações de contatos |
| `groups.upsert` | lista de metadados de grupo |
| `blocklist.update` | mudanças na lista de bloqueados |
| `lid-mapping.update` | atualizações do mapeamento LID |

### 8.5 Exemplo de recebimento de mensagens

```python
async def on_messages_upsert(data):
    for msg in data['messages']:
        key = msg.get('key', {})
        remote = key.get('remoteJid')
        content = msg.get('message') or {}
        # encontra o tipo de conteúdo real
        text = content.get('conversation') or content.get('extendedTextMessage', {}).get('text')
        print(f'[{remote}] {text}')

ev.on('messages.upsert', lambda d: asyncio.ensure_future(on_messages_upsert(d)))
```

---

## 9. Envio de mensagens

A API principal é `await sock['sendMessage'](jid, content, options)`.

### 9.1 Texto simples

```python
await sock['sendMessage']('51921826291@s.whatsapp.net', {'text': 'Olá, mundo!'})
```

### 9.2 Texto com menções

```python
await sock['sendMessage'](jid, {
    'text': 'Olá @123456789 e @987654321',
    'mentions': ['123456789@s.whatsapp.net', '987654321@s.whatsapp.net'],
})
```

### 9.3 Responder/citar outra mensagem

```python
quoted = {
    'key': {'remoteJid': jid, 'id': msg_id, 'fromMe': False},
    'message': conteudo_da_mensagem_original,
}
await sock['sendMessage'](jid, {'text': 'Minha resposta'}, {'quoted': quoted})
```

### 9.4 Reação

```python
await sock['sendMessage'](jid, {'react': {'text': '🔥', 'key': msg_key}})
```

### 9.5 Excluir uma mensagem

```python
await sock['sendMessage'](jid, {'delete': msg_key})
```

### 9.6 Editar uma mensagem

```python
await sock['sendMessage'](jid, {'edit': msg_key, 'text': 'Texto editado'})
```

### 9.7 Enquete

```python
await sock['sendMessage'](jid, {
    'poll': {
        'name': 'Melhor linguagem de programação?',
        'values': ['Python', 'JavaScript', 'Rust'],
        'selectableCount': 1,
    }
})
```

### 9.8 Contatos

```python
await sock['sendMessage'](jid, {
    'contacts': {'contacts': [
        {'displayName': 'Joana', 'vcard': 'BEGIN:VCARD\nVERSION:3.0\nFN:Joana\nEND:VCARD'},
    ]}
})
```

### 9.9 Localização

```python
await sock['sendMessage'](jid, {
    'location': {'degreesLatitude': -12.0464, 'degreesLongitude': -77.0428, 'name': 'Lima'},
})
```

### 9.10 Evento (calendário)

```python
from datetime import datetime, timedelta
await sock['sendMessage'](jid, {
    'event': {
        'name': 'Reunião',
        'startDate': datetime.now() + timedelta(hours=1),
        'endDate': datetime.now() + timedelta(hours=2),
    }
})
```

### 9.11 Opções comuns a todos os envios

```python
await sock['sendMessage'](jid, content, {
    'quoted': quoted_msg,          # responder a
    'timestamp': datetime.now(),   # timestamp personalizado
    'messageId': 'meu-id-custom',  # id de mensagem personalizado
    'ephemeralExpiration': 7 * 86400,   # mensagem efêmera (segundos)
    'backgroundColor': '#FF0000',  # fundo do texto de status
    'font': 4,                     # fonte do status
})
```

---

## 10. Envio de mídia

A mídia é enviada para os servidores do WhatsApp, criptografada e entregue automaticamente. Forneça os bytes ou um caminho.

### 10.1 Imagem

```python
with open('gato.jpg', 'rb') as f:
    await sock['sendMessage'](jid, {
        'image': f.read(),
        'caption': 'Olha este gato',
        'fileName': 'gato.jpg',
        'mimetype': 'image/jpeg',
    })
```

### 10.2 Vídeo / áudio / documento / sticker

```python
# vídeo
await sock['sendMessage'](jid, {'video': data, 'caption': 'vídeo', 'mimetype': 'video/mp4'})
# áudio
await sock['sendMessage'](jid, {'audio': data, 'mimetype': 'audio/mp4', 'ptt': False})
# nota de voz (push-to-talk)
await sock['sendMessage'](jid, {'audio': data, 'mimetype': 'audio/ogg; codecs=opus', 'ptt': True})
# documento
await sock['sendMessage'](jid, {'document': data, 'fileName': 'relatorio.pdf', 'mimetype': 'application/pdf', 'caption': 'Relatório'})
# sticker
await sock['sendMessage'](jid, {'sticker': data, 'mimetype': 'image/webp'})
```

### 10.3 GIF

```python
await sock['sendMessage'](jid, {'video': data, 'gifPlayback': True, 'mimetype': 'video/mp4'})
```

### 10.4 Mídia viewOnce

```python
await sock['sendMessage'](jid, {'image': data, 'viewOnce': True, 'mimetype': 'image/jpeg'})
```

### 10.5 Campos de mídia

Campos comuns por tipo de mídia: `caption`, `mimetype`, `fileName`, `fileLength`, `viewOnce`, `ptt`, `gifPlayback`, `jpegThumbnail` (prévia), `duration` (áudio/vídeo), `contextInfo`.

### 10.6 Baixar mídia (recebida)

Use os utilitários de `WAeys.Utils.messages_media`:

```python
from WAeys.Utils.messages_media import download_content_from_message

buffer, mimetype = await download_content_from_message(msg, media_keys)
```

As media keys (`mediaKey`) já estão na mensagem recebida; passe o objeto da mensagem e um resolvedor do store. Para conveniência, `decrypt_media_retry_data` e `get_media_keys` ajudam a calcular as chaves.

---

## 11. Mensagens interativas (botões, listas, modelos)

WAeys **não** traz um atalho em dict para mensagens interativas (igual ao Baileys TS). Você constrói um **`proto.Message` completo** e o envia com `generate_wa_message_from_content` + `relayMessage`, ou passa uma mensagem protobuf crua.

### 11.1 O padrão geral

```python
from WAeys.WAProto import WAProto as proto
from WAeys.Utils.messages import generate_wa_message_from_content
from WAeys.Utils.generics import generate_message_id_v2

msg = proto.Message.from_object({
    'interactiveMessage': {
        'body': {'text': 'Escolha um:'},
        'nativeFlowMessage': {
            'buttons': [
                {'name': 'quick_reply',
                 'buttonParamsJson': '{"display_text":"Opção 1","id":"opt1"}'},
                {'name': 'quick_reply',
                 'buttonParamsJson': '{"display_text":"Opção 2","id":"opt2"}'},
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

### 11.2 Mensagem de lista

```python
msg = proto.Message.from_object({
    'listMessage': {
        'title': 'Menu',
        'description': 'Escolha uma seção',
        'footerText': 'Powered by WAeys',
        'buttonText': 'Opções',
        'sections': [{
            'title': 'Principal',
            'rows': [
                {'title': 'Pizza', 'description': 'Queijo', 'rowId': 'pizza'},
                {'title': 'Hambúrguer', 'description': 'Carne', 'rowId': 'burger'},
            ],
        }],
        'listType': 1,   # proto.Message.ListMessage.ListType.SINGLE_SELECT
    },
})
```

### 11.3 Mensagem de botões

```python
msg = proto.Message.from_object({
    'buttonsMessage': {
        'contentText': 'Escolha:',
        'footerText': 'rodapé',
        'buttons': [
            {'buttonId': 'sim', 'buttonText': {'displayText': 'Sim'}, 'type': 1},
            {'buttonId': 'nao', 'buttonText': {'displayText': 'Não'}, 'type': 1},
        ],
        'headerType': 1,
    },
})
```

### 11.4 Mensagem de modelo (template)

```python
msg = proto.Message.from_object({
    'templateMessage': {
        'hydratedFourRowTemplate': {
            'hydratedContentText': 'Bem-vindo!',
            'hydratedFooterText': 'rodapé',
            'templateButtons': [
                {'quickReplyButton': {'displayText': 'Ir', 'id': 'go'}},
            ],
        },
    },
})
```

### 11.5 Interativo com cabeçalho de mídia

```python
media_result = await prepare_wa_message_media({'image': img_bytes}, opts)
msg = proto.Message.from_object({
    'interactiveMessage': {
        'header': {'title': 'Cabeçalho', 'hasMediaAttachment': True,
                   'imageMessage': media_result.imageMessage},
        'body': {'text': 'Texto do corpo'},
        'nativeFlowMessage': {'buttons': [...]},
    },
})
```

> Campos disponíveis no proto: `buttonsMessage=42`, `listMessage=36`, `templateMessage=25`, `interactiveMessage=45`, `nativeFlowMessage` dentro de `interactiveMessage`.

### 11.6 Lidar com respostas interativas

As respostas a botões/listas chegam como `messages.upsert` com tipos de conteúdo como:

- `buttonsResponseMessage` (respostas a botões)
- `listResponseMessage` (respostas a listas)
- `templateButtonReplyMessage` (respostas a modelos)

```python
content = msg.get('message') or {}
if content.get('buttonsResponseMessage'):
    print('Botão:', content['buttonsResponseMessage'].get('selectedButtonId'))
elif content.get('listResponseMessage'):
    print('Lista:', content['listResponseMessage'].get('singleSelectReply', {}).get('selectedRowId'))
```

---

## 12. Ler e reagir a mensagens recebidas

### 12.1 Iterar sobre os upserts

```python
async def on_upsert(data):
    for msg in data['messages']:
        if msg.get('key', {}).get('fromMe'):
            continue          # ignora as suas (exceto emitOwnEvents)
        jid = msg['key']['remoteJid']
        content = msg.get('message') or {}
        ctype = next((k for k in content if content.get(k)), None)
        print('tipo:', ctype, '| de:', jid)
        if ctype == 'conversation':
            text = content['conversation']
        elif ctype == 'extendedTextMessage':
            text = content['extendedTextMessage'].get('text')
        # ... trate o restante

ev.on('messages.upsert', lambda d: asyncio.ensure_future(on_upsert(d)))
```

### 12.2 Exemplo de roteador de comandos

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
            reply = COMMANDS.get(text.split()[0], lambda: 'Comando desconhecido')()
            await sock['sendMessage'](jid, {'text': reply})
```

### 12.3 Obter chat id / jid

```python
from WAeys.Utils.process_message import get_chat_id
chat_id = get_chat_id(msg)   # jid do chat
```

`is_real_message(msg)` informa se a mensagem é real de usuário (não de status/sistema/protocolo).

---

## 13. Confirmações de leitura e presença

### 13.1 Marcar mensagens como lidas

```python
await sock['readMessages']([{'remoteJid': jid, 'id': msg_id, 'fromMe': False}])
```

### 13.2 Enviar confirmações de recebimento

```python
await sock['sendReceipts'](keys, 'read')        # 'read' / 'delivered'
await sock['sendReceipt'](jid, participant, [msg_id], 'read')
```

### 13.3 Verificar se um telefone está no WhatsApp

```python
result = await sock['onWhatsApp']('51921826291')
# [{'exists': True, 'jid': '51921826291@s.whatsapp.net'}]
```

### 13.4 Presença online

A presença é controlada por `markOnlineOnConnect` no nível de configuração. O controle de baixo nível de presença usa `sock['query']` com o IQ de presença apropriado (como no Baileys).

---

## 14. Ciclo de vida da sessão: logout, reconexão, tentativas

### 14.1 Encerramento correto

```python
await sock['end']()        # fecha limpo (para keep-alive, fecha ws)
await sock['logout']()     # logout no servidor (invalida a sessão)
```

### 14.2 Detectar desconexões e reconectar

```python
async def on_conn(update):
    if update.get('connection') == 'close':
        err = update.get('lastDisconnect', {}).get('error') if isinstance(update.get('lastDisconnect'), dict) else None
        print('desconectado:', err)
        # recria o socket com O MESMO auth state
        new_sock = make_socket(config)
        # registra os handlers novamente, continua...

ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))
```

WAeys **não traz reconexão automática** (igual ao socket base do Baileys). Bots de produção envolvem o socket em um loop de reconexão reutilizando a sessão salva.

### 14.3 Novas tentativas de mensagem

Um `MessageRetryManager` é exposto em `sock['messageRetryManager']` e usado automaticamente pelo `relayMessage` para entregas com falha (`maxMsgRetryCount`, `retryRequestDelayMs`).

### 14.4 Registrar handlers de fim de socket

```python
sock['registerSocketEndHandler'](lambda: print('socket encerrado'))
```

### 14.5 Aguardar uma atualização de conexão

```python
update = await sock['waitForConnectionUpdate'](lambda u: u.get('connection') == 'open')
```

---

## 15. API de baixo nível

### 15.1 Enviar um nó binário

```python
from WAeys.WABinary.types import BinaryNode
node = BinaryNode(tag='iq', attrs={'type': 'get', 'to': 's.whatsapp.net', 'id': '123'}, content=None)
await sock['sendNode'](node)
```

### 15.2 Consulta IQ

```python
result = await sock['query'](node)      # retorna o BinaryNode de resposta
```

### 15.3 Frames crus

```python
await sock['sendRawMessage'](payload_bytes)
```

### 15.4 Prekeys

```python
await sock['uploadPreKeys']()                       # envia N prekeys
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

## 16. Dicas de produção e anti-ban

WAeys, como todo cliente não oficial do WhatsApp, pode fazer seu número ser **banido**. **Não há anti-ban incorporado** na biblioteca (igual ao Baileys). Siga estas regras:

1. **Comportamento humano**: envie mensagens com atrasos aleatórios (2–8 s) em vez de rajadas instantâneas.
2. **Nunca faça spam**: evite mensagens em massa idênticas, inundar grupos ou adicionar contatos agressivamente.
3. **Aqueça o número**: para um número novo, comece com volume baixo e aumente gradualmente ao longo de dias.
4. **Não reutilize sessões banidas**: se banirem um número, apague sua sessão e credenciais.
5. **Mantenha uma conexão estável**: execute com keep-alive; evite matar o processo repetidamente durante o login.
6. **Use pareamento em vez de novos logins repetidos**: re-vinculações por QR repetidas podem causar `rate-overlimit`.
7. **Não execute sessões paralelas** com o mesmo número.
8. **Mantenha versão/dependências atualizadas**: use a versão do protocolo suportada pela biblioteca.

### 16.1 Auxiliar de envio com atraso

```python
import random

async def safe_send(jid, content, min_delay=2.0, max_delay=6.0):
    await asyncio.sleep(random.uniform(min_delay, max_delay))
    await sock['sendMessage'](jid, content)
```

---

## 17. Solução de problemas

### 17.1 `ModuleNotFoundError: No module named 'websockets'`
Instale a dependência com o mesmo interpretador que executa seu script:
```bash
pip install "websockets>=12.0"
```

### 17.2 O QR nunca aparece / a conexão cai durante o pareamento
O WhatsApp derruba conexões não vinculadas após ~90 s. Use `keepAliveIntervalMs: 5000` e reconecte até parear.

### 17.3 `rate-overlimit` ao solicitar códigos de pareamento
Solicitações demais. Aguarde 30–60 minutos e garanta que não esteja executando vários processos de pareamento ao mesmo tempo.

### 17.4 Sessão salva, mas o login falha com "Connection Failure"
Os prekeys nunca foram enviados (a sessão foi salva cedo demais). Pareie novamente e aguarde `connection: open`.

### 17.5 `Invalid media type`
Você passou uma chave de conteúdo desconhecida para `sendMessage`. Use uma de: `image`, `video`, `audio`, `document`, `sticker`, `ptt`, `gif`, `ptv`, `product`.

### 17.6 Erros `Boom` / `CB:failure`
Verifique `connection.update` e seu `lastDisconnect.error`, e os logs. Causas comuns: sessão expirada, sessão revogada ou fluxo de pareamento incorreto.

### 17.7 Ver `'tb'` nos logs
Se o logger imprimir uma chave `tb`, é um traceback real de Python do socket interno — habilite o nível de debug do seu logger para lê-lo.

---

## 18. Referência completa da API

### Pacote `WAeys`

| Caminho | Propósito |
|---|---|
| `WAeys.WABinary` | Codificação/decodificação de nós binários |
| `WAeys.Utils` | Todos os utilitários (auth, crypto, mensagens, mídia, …) |
| `WAeys.Defaults` | Padrões e constantes (`default_connection_config`) |
| `WAeys.Types` | Tipos e enums |
| `WAeys.WAProto` | Classes protobuf geradas (Python puro) |
| `WAeys.Signal` | Implementação do protocolo Signal |
| `WAeys.Socket` | `make_socket`, cliente websocket, camadas de mensagens |

### Funções Utils principais

| Função | Módulo |
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

### Métodos do socket (de `make_socket`)

| Método | Retorna | Descrição |
|---|---|---|
| `requestPairingCode(phone)` | str | Obtém o código de pareamento de 8 caracteres |
| `sendMessage(jid, content, options?)` | dict mensagem | Envia qualquer mensagem |
| `relayMessage(jid, proto_msg, opts?)` | — | Relay de baixo nível |
| `readMessages(keys)` | — | Marcar como lido |
| `sendReceipts(keys, type)` | — | Enviar confirmações |
| `onWhatsApp(phone)` | list | Verifica números de telefone |
| `query(node)` | BinaryNode | Consulta IQ |
| `waitForConnectionUpdate(pred)` | update | Aguarda uma condição |
| `uploadPreKeys()` | — | Envia prekeys |
| `logout()` | — | Logout no servidor |
| `end()` | — | Fecha a conexão |
| `executeUSyncQuery(q)` | — | Consulta USync |
| `sendWAMBuffer(buf)` | — | Envia buffer WAM |

---

## 19. Estrutura do projeto

```
WAeys/
├── __init__.py          # init do pacote, __version__
├── Defaults/            # configuração padrão, constantes, mapas de mídia
├── Types/               # tipos de auth/mensagem/chat/evento
├── Utils/               # crypto, mensagens, mídia, auth, noise etc.
├── WABinary/            # codec de nós binários
├── WAProto/             # classes protobuf em python puro + .proto
├── Signal/              # protocolo Signal (sessões, prekeys)
├── Socket/              # make_socket + camadas de envio/recebimento
│   └── Client/          # cliente websocket
├── WAM/                 # WhatsApp Analytics Message
└── WAUSync/             # consultas USync
```

---

## 20. Aviso legal

**WAeys não é afiliado, endossado ou conectado ao WhatsApp ou à Meta Platforms, Inc.** É um cliente não oficial que usa o protocolo do WhatsApp Web. O uso pode violar os Termos de Serviço do WhatsApp e pode levar a restrições temporárias ou permanentes da conta. Você é o único responsável pelo uso desta biblioteca.

---

*Gerado para WAeys v0.1.0 — port do Baileys em Python puro. Consulte também as versões em [inglês](usage.en.md) e [espanhol](usage.es.md).*
