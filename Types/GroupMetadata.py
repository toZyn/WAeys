"""Port of src/Types/GroupMetadata.ts — group metadata and participant shapes."""

from __future__ import annotations

from typing import Dict, List, Optional

GroupParticipant = Dict  # Contact & {isAdmin?, isSuperAdmin?, admin?}

ParticipantAction = str  # 'add' | 'remove' | 'promote' | 'demote' | 'modify'

RequestJoinAction = str  # 'created' | 'revoked' | 'rejected'

RequestJoinMethod = Optional[str]  # 'invite_link' | 'linked_group_join' | 'non_admin_add'

GroupMetadata = Dict  # see TS for the full field list

WAGroupCreateResponse = Dict

GroupModificationResponse = Dict
