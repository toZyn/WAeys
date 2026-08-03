"""Port of src/Types/index.ts — shared types and re-exports.

Python port: types are dicts/enums with the same shapes as the TS originals.
"""

from __future__ import annotations

import enum
from typing import Dict, List, Optional, Tuple, Union

from . import Auth as Auth
from . import Signal as Signal
from . import Message as Message
from . import Events as Events
from . import Chat as Chat
from . import Contact as Contact
from . import GroupMetadata as GroupMetadata
from . import Label as Label
from . import LabelAssociation as LabelAssociation
from . import Call as Call
from . import Product as Product
from . import Bussines as Bussines
from . import Mex as Mex
from . import State as State
from . import Socket as Socket
from . import USync as USync
from .Auth import (
    AuthenticationState,
    AuthenticationCreds,
    LIDMapping,
    SignalAuthState,
    SignalCreds,
    SignalDataSet,
    SignalKeyStore,
    SignalKeyStoreWithTransaction,
    SignalDataTypeMap,
)
from .Message import WAMessageAddressingMode, WAMessageStubType, WAMessageStatus, MessageUpsertType
from .Events import BaileysEventEmitter, BufferedEventData
from .Chat import ALL_WA_PATCH_NAMES, WAPresence, PresenceData
from .Contact import Contact as _Contact
from .GroupMetadata import GroupMetadata as _GroupMetadata, ParticipantAction, GroupParticipant
from .Label import LabelColor, Label as _Label
from .LabelAssociation import LabelAssociationType
from .Call import WACallEvent, WACallUpdateType
from .Mex import XWAPaths, QueryIds
from .State import SyncState, ConnectionState, ReachoutTimelockEnforcementType
from .Socket import SocketConfig as _SocketConfig, WAVersion, WABrowserDescription

# Re-export module references for convenience
from .Signal import SignalRepository


class DisconnectReason(enum.IntEnum):
    connectionClosed = 428
    connectionLost = 408
    connectionReplaced = 440
    timedOut = 408
    loggedOut = 401
    badSession = 500
    restartRequired = 515
    multideviceMismatch = 411
    forbidden = 403
    unavailableService = 503


WAInitResponse = Dict  # {ref, ttl, status}

SocketConfig = Dict  # full config dict (see src/Types/Socket.ts)

UserFacingSocketConfig = Dict  # Partial<SocketConfig> & {auth: AuthenticationState}

Contact = Dict
WAMessage = Dict
Chat = Dict
GroupMetadata = Dict
EventMap = Dict

DisconnectReason = DisconnectReason  # noqa: F811
