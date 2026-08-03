"""Port of src/Types/Chat.ts — privacy values, presence, chat mutations."""

from __future__ import annotations

from typing import Dict, List, Union

from ..WAProto import WAProto as proto

WAPrivacyValue = str  # 'all' | 'contacts' | 'contact_blacklist' | 'none'
WAPrivacyOnlineValue = str  # 'all' | 'match_last_seen'
WAPrivacyGroupAddValue = str  # 'all' | 'contacts' | 'contact_blacklist'
WAReadReceiptsValue = str  # 'all' | 'none'
WAPrivacyCallValue = str  # 'all' | 'known'
WAPrivacyMessagesValue = str  # 'all' | 'contacts'

WAPresence = str  # 'unavailable' | 'available' | 'composing' | 'recording' | 'paused'

ALL_WA_PATCH_NAMES = ('critical_block', 'critical_unblock_low', 'regular_high', 'regular_low', 'regular')

WAPatchName = str

PresenceData = Dict  # {lastKnownPresence, lastSeen?, groupOnlineCount?}

BotListInfo = Dict

ChatMutation = Dict

WAPatchCreate = Dict

Chat = Dict  # proto.IConversation & {lastMessageRecvTimestamp?}

ChatUpdate = Dict  # Partial<Chat> & {conditional?, timestamp?}

LastMessageList = Union[List[Dict], Dict]

ChatModification = Dict

InitialReceivedChatsState = Dict

InitialAppStateSyncOptions = Dict
