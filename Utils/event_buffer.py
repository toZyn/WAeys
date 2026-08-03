"""Port of src/Utils/event-buffer.ts — makeEventBuffer."""

from __future__ import annotations

import asyncio
import time

from ..Types import WAMessageStatus
from .generics import trim_undefined
from .messages import update_message_with_reaction, update_message_with_receipt
from .process_message import is_real_message, should_increment_chat_unread

BUFFERABLE_EVENT = [
    'messaging-history.set',
    'chats.upsert',
    'chats.update',
    'chats.delete',
    'contacts.upsert',
    'contacts.update',
    'messages.upsert',
    'messages.update',
    'messages.delete',
    'messages.reaction',
    'message-receipt.update',
    'groups.update',
]

BUFFERABLE_EVENT_SET = set(BUFFERABLE_EVENT)


def _stringify_message_key(key: dict) -> str:
    return f"{key.get('remoteJid')},{key.get('id')},{'1' if key.get('fromMe') else '0'}"


def _make_buffer_data() -> dict:
    return {
        'historySets': {'chats': {}, 'messages': {}, 'contacts': {}, 'isLatest': False, 'empty': True},
        'chatUpserts': {},
        'chatUpdates': {},
        'chatDeletes': set(),
        'contactUpserts': {},
        'contactUpdates': {},
        'messageUpserts': {},
        'messageUpdates': {},
        'messageReactions': {},
        'messageDeletes': {},
        'messageReceipts': {},
        'groupUpdates': {},
    }


def _concat_chats(a: dict, b: dict) -> dict:
    if b.get('unreadCount') is None and a.get('unreadCount', 0) < 0:
        a['unreadCount'] = None
        b['unreadCount'] = None
    if isinstance(a.get('unreadCount'), (int, float)) and isinstance(b.get('unreadCount'), (int, float)):
        b = dict(b)
        if b['unreadCount'] >= 0:
            b['unreadCount'] = max(b['unreadCount'], 0) + max(a['unreadCount'], 0)
    a.update(b)
    return a


def _consolidate_events(data: dict) -> dict:
    map_ = {}
    if not data['historySets']['empty']:
        hs = data['historySets']
        map_['messaging-history.set'] = {
            'chats': list(hs['chats'].values()),
            'messages': list(hs['messages'].values()),
            'contacts': list(hs['contacts'].values()),
            'pastParticipants': hs.get('pastParticipants'),
            'syncType': hs.get('syncType'),
            'progress': hs.get('progress'),
            'isLatest': hs.get('isLatest'),
            'chunkOrder': hs.get('chunkOrder'),
            'peerDataRequestSessionId': hs.get('peerDataRequestSessionId'),
        }
    if data['chatUpserts']:
        map_['chats.upsert'] = list(data['chatUpserts'].values())
    if data['chatUpdates']:
        map_['chats.update'] = list(data['chatUpdates'].values())
    if data['chatDeletes']:
        map_['chats.delete'] = list(data['chatDeletes'])
    mu = list(data['messageUpserts'].values())
    if mu:
        map_['messages.upsert'] = {'messages': [m['message'] for m in mu], 'type': mu[0]['type']}
    if data['messageUpdates']:
        map_['messages.update'] = list(data['messageUpdates'].values())
    if data['messageDeletes']:
        map_['messages.delete'] = {'keys': list(data['messageDeletes'].values())}
    reactions = [r for v in data['messageReactions'].values() for r in v['reactions']]
    if reactions:
        map_['messages.reaction'] = reactions
    receipts = [r for v in data['messageReceipts'].values() for r in v['userReceipt']]
    if receipts:
        map_['message-receipt.update'] = receipts
    if data['contactUpserts']:
        map_['contacts.upsert'] = list(data['contactUpserts'].values())
    if data['contactUpdates']:
        map_['contacts.update'] = list(data['contactUpdates'].values())
    if data['groupUpdates']:
        map_['groups.update'] = list(data['groupUpdates'].values())
    return map_


def make_event_buffer(logger):
    """Returns an event buffer object with the same API as Baileys' makeEventBuffer."""

    class _EventBuffer:
        def __init__(self):
            self._listeners = {}
            self.data = _make_buffer_data()
            self.is_buffering = False
            self.buffer_timeout = None
            self.flush_pending_timeout = None
            self.buffer_count = 0
            self.history_cache = set()
            self.MAX_HISTORY_CACHE_SIZE = 10000
            self.BUFFER_TIMEOUT_MS = 30000
            self._destroyed = False
            # re-dispatch consolidated events to per-event channels (TS: ev.on('event', ...))
            self._listeners['event'] = [self._dispatch_event_map]

        def _dispatch_event_map(self, ev_map):
            for event, ev_data in (ev_map or {}).items():
                self.emit_event(event, ev_data)

        # --- emitter primitives ---
        def on(self, event, listener):
            self._listeners.setdefault(event, []).append(listener)

        def off(self, event, listener):
            lst = self._listeners.get(event)
            if lst is not None:
                try:
                    lst.remove(listener)
                except ValueError:
                    pass

        def remove_all_listeners(self, event=None):
            if event is None:
                self._listeners.clear()
            else:
                self._listeners.pop(event, None)

        def emit(self, event, ev_data):
            # messages.upsert type mismatch handling
            if event == 'messages.upsert':
                type_ = ev_data.get('type')
                existing_upserts = list(self.data['messageUpserts'].values())
                if existing_upserts:
                    buffered_type = existing_upserts[0]['type']
                    if buffered_type != type_:
                        logger.debug({}, 'messages.upsert type mismatch, emitting buffered messages')
                        self.emit('event', {
                            'messages.upsert': {
                                'messages': [m['message'] for m in existing_upserts],
                                'type': buffered_type,
                            }
                        })
                        self.data['messageUpserts'] = {}

            if self.is_buffering and event in BUFFERABLE_EVENT_SET:
                self._append(event, ev_data)
                return True
            return self.emit_event('event', {event: ev_data})

        def emit_event(self, event, ev_data):
            lst = self._listeners.get(event)
            if not lst:
                return False
            for listener in list(lst):
                listener(ev_data)
            return True

        def is_buffering(self):
            return self.is_buffering

        def buffer(self):
            if not self.is_buffering:
                logger.debug('Event buffer activated')
                self.is_buffering = True
                self.buffer_count = 0
                if self.buffer_timeout:
                    self.buffer_timeout.cancel()
                self.buffer_timeout = asyncio.get_event_loop().call_later(
                    self.BUFFER_TIMEOUT_MS / 1000.0, self._auto_flush
                )
            self.buffer_count += 1

        def _auto_flush(self):
            if self.is_buffering:
                logger.warn('Buffer timeout reached, auto-flushing')
                self.flush()

        def flush(self):
            if not self.is_buffering:
                return False
            logger.debug({'bufferCount': self.buffer_count}, 'Flushing event buffer')
            self.is_buffering = False
            self.buffer_count = 0
            if self.buffer_timeout:
                self.buffer_timeout.cancel()
                self.buffer_timeout = None
            if self.flush_pending_timeout:
                self.flush_pending_timeout.cancel()
                self.flush_pending_timeout = None

            if len(self.history_cache) > self.MAX_HISTORY_CACHE_SIZE:
                logger.debug({'cacheSize': len(self.history_cache)}, 'Clearing history cache')
                self.history_cache.clear()

            new_data = _make_buffer_data()
            conditional_left = 0
            for update in list(self.data['chatUpdates'].values()):
                if update.get('conditional'):
                    conditional_left += 1
                    new_data['chatUpdates'][update.get('id')] = update
                    del self.data['chatUpdates'][update.get('id')]

            consolidated = _consolidate_events(self.data)
            if consolidated:
                self.emit_event('event', consolidated)

            self.data = new_data
            logger.trace({'conditionalChatUpdatesLeft': conditional_left}, 'released buffered events')
            return True

        def process(self, handler):
            async def listener(ev_map):
                await handler(ev_map)

            self.on('event', listener)
            return lambda: self.off('event', listener)

        def create_buffered_function(self, work):
            async def wrapper(*args):
                self.buffer()
                try:
                    result = await work(*args)
                    if self.buffer_count == 1:
                        loop = asyncio.get_event_loop()
                        loop.call_later(0.1, lambda: self.flush() if (self.is_buffering and self.buffer_count == 1) else None)
                    return result
                except Exception:
                    raise
                finally:
                    self.buffer_count = max(0, self.buffer_count - 1)
                    if self.buffer_count == 0 and not self.flush_pending_timeout:
                        self.flush_pending_timeout = asyncio.get_event_loop().call_later(0.1, self._flush_pending)

            return wrapper

        def _flush_pending(self):
            self.flush_pending_timeout = None
            self.flush()

        def destroy(self):
            if self.buffer_timeout:
                self.buffer_timeout.cancel()
                self.buffer_timeout = None
            if self.flush_pending_timeout:
                self.flush_pending_timeout.cancel()
                self.flush_pending_timeout = None
            self.history_cache.clear()
            self.data = _make_buffer_data()
            self.is_buffering = False
            self.buffer_count = 0
            self._listeners.clear()
            logger.debug('Event buffer destroyed')

        # --- appending buffered events ---
        def _absorbing_chat_update(self, existing: dict):
            chat_id = existing.get('id') or ''
            update = self.data['chatUpdates'].get(chat_id)
            if update:
                condition_matches = update.get('conditional')(self.data) if update.get('conditional') else True
                if condition_matches:
                    update.pop('conditional', None)
                    logger.debug({'chatId': chat_id}, 'absorbed chat update in existing chat')
                    existing.update(_concat_chats(update, existing))
                    del self.data['chatUpdates'][chat_id]
                elif condition_matches is False:
                    logger.debug({'chatId': chat_id}, 'chat update condition fail, removing')
                    del self.data['chatUpdates'][chat_id]

        def _decrement_chat_read_counter(self, message: dict):
            chat_id = message.get('key', {}).get('remoteJid')
            chat = self.data['chatUpdates'].get(chat_id) or self.data['chatUpserts'].get(chat_id)
            if (
                is_real_message(message)
                and should_increment_chat_unread(message)
                and isinstance(chat.get('unreadCount'), (int, float))
                and chat['unreadCount'] > 0
            ):
                logger.debug({'chatId': chat.get('id')}, 'decrementing chat counter')
                chat['unreadCount'] -= 1
                if chat['unreadCount'] == 0:
                    chat.pop('unreadCount', None)

        def _append(self, event: str, event_data):
            data = self.data
            if event == 'messaging-history.set':
                for chat in event_data.get('chats') or []:
                    chat_id = chat.get('id') or ''
                    existing = data['historySets']['chats'].get(chat_id)
                    if existing:
                        existing['endOfHistoryTransferType'] = chat.get('endOfHistoryTransferType')
                    if not existing and chat_id not in self.history_cache:
                        data['historySets']['chats'][chat_id] = chat
                        self.history_cache.add(chat_id)
                        self._absorbing_chat_update(chat)

                for contact in event_data.get('contacts') or []:
                    existing = data['historySets']['contacts'].get(contact.get('id'))
                    if existing:
                        existing.update(trim_undefined(contact))
                    else:
                        history_id = f"c:{contact.get('id')}"
                        has_any_name = contact.get('notify') or contact.get('name') or contact.get('verifiedName')
                        if history_id not in self.history_cache or has_any_name:
                            data['historySets']['contacts'][contact.get('id')] = contact
                            self.history_cache.add(history_id)

                for message in event_data.get('messages') or []:
                    key = _stringify_message_key(message.get('key'))
                    if key not in data['historySets']['messages'] and key not in self.history_cache:
                        data['historySets']['messages'][key] = message
                        self.history_cache.add(key)

                hs = data['historySets']
                hs['empty'] = False
                hs['syncType'] = event_data.get('syncType')
                past = event_data.get('pastParticipants')
                if past:
                    merged = {}
                    def sig_of(p):
                        return f"{p.get('userJid') or ''}:{p.get('leaveTs') or ''}:{p.get('leaveReason') or ''}"
                    def ingest(entry):
                        key = entry.get('groupJid') or str(entry)
                        existing = merged.get(key)
                        if not existing:
                            merged[key] = {**entry, 'pastParticipants': list(entry.get('pastParticipants') or [])}
                            return
                        seen = {sig_of(p) for p in existing.get('pastParticipants') or []}
                        for p in entry.get('pastParticipants') or []:
                            sig = sig_of(p)
                            if sig not in seen:
                                existing['pastParticipants'].append(p)
                                seen.add(sig)
                    for entry in hs.get('pastParticipants') or []:
                        ingest(entry)
                    for entry in past:
                        ingest(entry)
                    hs['pastParticipants'] = list(merged.values())

                hs['progress'] = event_data.get('progress')
                hs['chunkOrder'] = event_data.get('chunkOrder')
                hs['peerDataRequestSessionId'] = event_data.get('peerDataRequestSessionId')
                hs['isLatest'] = event_data.get('isLatest') or hs.get('isLatest')

            elif event == 'chats.upsert':
                for chat in event_data:
                    chat_id = chat.get('id') or ''
                    upsert = data['chatUpserts'].get(chat_id)
                    if chat_id and not upsert:
                        upsert = data['historySets']['chats'].get(chat_id)
                        if upsert:
                            logger.debug({'chatId': chat_id}, 'absorbed chat upsert in chat set')
                    if upsert:
                        upsert = _concat_chats(upsert, chat)
                    else:
                        upsert = chat
                        data['chatUpserts'][chat_id] = upsert
                    self._absorbing_chat_update(upsert)
                    if chat_id in data['chatDeletes']:
                        data['chatDeletes'].discard(chat_id)

            elif event == 'chats.update':
                for update in event_data:
                    chat_id = update.get('id')
                    condition_matches = update.get('conditional')(data) if update.get('conditional') else True
                    if condition_matches:
                        update.pop('conditional', None)
                        upsert = data['historySets']['chats'].get(chat_id) or data['chatUpserts'].get(chat_id)
                        if upsert:
                            _concat_chats(upsert, update)
                        else:
                            chat_update = data['chatUpdates'].get(chat_id) or {}
                            data['chatUpdates'][chat_id] = _concat_chats(chat_update, update)
                    elif condition_matches is None:
                        data['chatUpdates'][chat_id] = update
                    if chat_id in data['chatDeletes']:
                        data['chatDeletes'].discard(chat_id)

            elif event == 'chats.delete':
                for chat_id in event_data:
                    if chat_id not in data['chatDeletes']:
                        data['chatDeletes'].add(chat_id)
                    data['chatUpdates'].pop(chat_id, None)
                    data['chatUpserts'].pop(chat_id, None)
                    data['historySets']['chats'].pop(chat_id, None)

            elif event == 'contacts.upsert':
                for contact in event_data:
                    upsert = data['contactUpserts'].get(contact.get('id'))
                    if not upsert:
                        upsert = data['historySets']['contacts'].get(contact.get('id'))
                        if upsert:
                            logger.debug({'contactId': contact.get('id')}, 'absorbed contact upsert in contact set')
                    if upsert:
                        upsert.update(trim_undefined(contact))
                    else:
                        upsert = contact
                        data['contactUpserts'][contact.get('id')] = upsert
                    if contact.get('id') in data['contactUpdates']:
                        upsert = data['contactUpdates'][contact.get('id')]
                        upsert.update(trim_undefined(contact))
                        del data['contactUpdates'][contact.get('id')]

            elif event == 'contacts.update':
                for update in event_data:
                    cid = update.get('id')
                    upsert = data['historySets']['contacts'].get(cid) or data['contactUpserts'].get(cid)
                    if upsert:
                        upsert.update(update)
                    else:
                        contact_update = data['contactUpdates'].get(cid) or {}
                        contact_update.update(update)
                        data['contactUpdates'][cid] = contact_update

            elif event == 'messages.upsert':
                messages = event_data.get('messages') or []
                type_ = event_data.get('type')
                for message in messages:
                    key = _stringify_message_key(message.get('key'))
                    existing = data['messageUpserts'].get(key, {}).get('message')
                    if not existing:
                        existing = data['historySets']['messages'].get(key)
                        if existing:
                            logger.debug({'messageId': key}, 'absorbed message upsert in message set')
                    if existing:
                        message['messageTimestamp'] = existing.get('messageTimestamp')
                    if key in data['messageUpdates']:
                        logger.debug('absorbed prior message update in message upsert')
                        message.update(data['messageUpdates'][key].get('update'))
                        del data['messageUpdates'][key]
                    if key in data['historySets']['messages']:
                        data['historySets']['messages'][key] = message
                    else:
                        prev = data['messageUpserts'].get(key)
                        data['messageUpserts'][key] = {
                            'message': message,
                            'type': 'notify' if (type_ == 'notify' or (prev and prev['type'] == 'notify')) else type_,
                        }

            elif event == 'messages.update':
                for item in event_data:
                    key = _stringify_message_key(item.get('key'))
                    update = item.get('update') or {}
                    existing = data['historySets']['messages'].get(key) or data['messageUpserts'].get(key, {}).get('message')
                    if existing:
                        existing.update(update)
                        if update.get('status') == WAMessageStatus.READ and not item.get('key', {}).get('fromMe'):
                            self._decrement_chat_read_counter(existing)
                    else:
                        msg_update = data['messageUpdates'].get(key) or {'key': item.get('key'), 'update': {}}
                        msg_update['update'].update(update)
                        data['messageUpdates'][key] = msg_update

            elif event == 'messages.delete':
                delete_data = event_data
                if 'keys' in delete_data:
                    for key in delete_data['keys']:
                        key_str = _stringify_message_key(key)
                        if key_str not in data['messageDeletes']:
                            data['messageDeletes'][key_str] = key
                        data['messageUpserts'].pop(key_str, None)
                        data['messageUpdates'].pop(key_str, None)

            elif event == 'messages.reaction':
                for item in event_data:
                    key = _stringify_message_key(item.get('key'))
                    existing = data['messageUpserts'].get(key)
                    if existing:
                        update_message_with_reaction(existing['message'], item.get('reaction'))
                    else:
                        entry = data['messageReactions'].get(key) or {'key': item.get('key'), 'reactions': []}
                        update_message_with_reaction(entry, item.get('reaction'))
                        data['messageReactions'][key] = entry

            elif event == 'message-receipt.update':
                for item in event_data:
                    key = _stringify_message_key(item.get('key'))
                    existing = data['messageUpserts'].get(key)
                    if existing:
                        update_message_with_receipt(existing['message'], item.get('receipt'))
                    else:
                        entry = data['messageReceipts'].get(key) or {'key': item.get('key'), 'userReceipt': []}
                        update_message_with_receipt(entry, item.get('receipt'))
                        data['messageReceipts'][key] = entry

            elif event == 'groups.update':
                for update in event_data:
                    gid = update.get('id')
                    if gid not in data['groupUpdates']:
                        data['groupUpdates'][gid] = update

            else:
                raise ValueError(f'"{event}" cannot be buffered')

    return _EventBuffer()
