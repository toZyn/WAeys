"""Port of src/Types/LabelAssociation.ts — chat/message label associations."""

from __future__ import annotations

import enum

from typing import Dict


class LabelAssociationType(enum.Enum):
    Chat = 'label_jid'
    Message = 'label_message'


LabelAssociationTypes = str

ChatLabelAssociation = Dict  # {type: 'label_jid', chatId, labelId}
MessageLabelAssociation = Dict  # {type: 'label_message', chatId, messageId, labelId}
LabelAssociation = Dict

ChatLabelAssociationActionBody = Dict  # {labelId}
MessageLabelAssociationActionBody = Dict  # {labelId, messageId}
