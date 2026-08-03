"""Port of src/Types/Message.ts — WAMessage and content types.

Python port: message shapes are dicts matching the proto-based TS types.
"""

from __future__ import annotations

import enum
from typing import Dict, List, Optional, Tuple, Union

from ..WAProto import WAProto as proto

# WAMessage and related are dicts shaped after proto.WebMessageInfo
WAMessage = Dict
WAMessageContent = Dict
WAContactMessage = Dict
WAContactsArrayMessage = Dict
WAMessageKey = Dict  # proto.IMessageKey & {remoteJidAlt?, ...}
WATextMessage = Dict
WAContextInfo = Dict
WALocationMessage = Dict
WAGenericMediaMessage = Dict
WAMediaPayloadURL = Dict
WAMediaPayloadStream = Dict
WAMediaUpload = Union[bytes, Dict]
MessageType = str

WAMessageStubType = getattr(proto.WebMessageInfo, 'StubType', None)
WAMessageStatus = getattr(proto.WebMessageInfo, 'Status', None)


class WAMessageAddressingMode(enum.Enum):
    PN = 'pn'
    LID = 'lid'


MessageWithContextInfo = Union[str, ...]

DownloadableMessage = Dict  # {mediaKey?, directPath?, url?}

MessageReceiptType = Optional[str]

MediaConnInfo = Dict  # {auth, ttl, hosts, fetchDate}

WAUrlInfo = Dict  # {canonical-url, matched-text, title, ...}

Mentionable = Dict
Contextable = Dict
ViewOnce = Dict
Editable = Dict
WithDimensions = Dict

PollMessageOptions = Dict
EventMessageOptions = Dict
AlbumMessageOptions = Dict

AnyMediaMessageContent = Dict
ButtonReplyInfo = Dict
GroupInviteInfo = Dict
WASendableProduct = Dict
AnyRegularMessageContent = Dict
AnyMessageContent = Dict

MessageRelayOptions = Dict
MiscMessageGenerationOptions = Dict
MessageGenerationOptionsFromContent = Dict
WAMediaUploadFunction = object
MediaGenerationOptions = Dict
MessageContentGenerationOptions = Dict
MessageGenerationOptions = Dict

MessageUpsertType = str  # 'append' | 'notify'

MessageUserReceipt = Dict
WAMessageUpdate = Dict
WAMessageCursor = Dict
MessageUserReceiptUpdate = Dict
MediaDecryptionKeyInfo = Dict
MinimalMessage = Dict
