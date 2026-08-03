"""Port of src/Types/Call.ts — call event types."""

from __future__ import annotations

from typing import Dict

WACallUpdateType = str  # 'offer' | 'ringing' | ... | 'terminate'

WACallEvent = Dict  # {chatId, from, callerPn?, isGroup?, groupJid?, id, date, isVideo?, status, offline, latencyMs?}
