"""Generated from WAProto.proto — do not edit by hand.

Pure-Python protobuf classes (see runtime.py). Enums are enum.IntEnum.
The base is aliased as MessageBase so the proto's own `Message` type
cannot shadow it in the module namespace.
"""
import enum

from .runtime import Message as MessageBase, FieldDescriptor

class ADVEncryptionType(enum.IntEnum):
    E2EE = 0
    HOSTED = 1

class AIRichResponseMessageType(enum.IntEnum):
    AI_RICH_RESPONSE_TYPE_UNKNOWN = 0
    AI_RICH_RESPONSE_TYPE_STANDARD = 1

class AIRichResponseSubMessageType(enum.IntEnum):
    AI_RICH_RESPONSE_UNKNOWN = 0
    AI_RICH_RESPONSE_GRID_IMAGE = 1
    AI_RICH_RESPONSE_TEXT = 2
    AI_RICH_RESPONSE_INLINE_IMAGE = 3
    AI_RICH_RESPONSE_TABLE = 4
    AI_RICH_RESPONSE_CODE = 5
    AI_RICH_RESPONSE_DYNAMIC = 6
    AI_RICH_RESPONSE_MAP = 7
    AI_RICH_RESPONSE_LATEX = 8
    AI_RICH_RESPONSE_CONTENT_ITEMS = 9

class BotMetricsEntryPoint(enum.IntEnum):
    UNDEFINED_ENTRY_POINT = 0
    FAVICON = 1
    CHATLIST = 2
    AISEARCH_NULL_STATE_PAPER_PLANE = 3
    AISEARCH_NULL_STATE_SUGGESTION = 4
    AISEARCH_TYPE_AHEAD_SUGGESTION = 5
    AISEARCH_TYPE_AHEAD_PAPER_PLANE = 6
    AISEARCH_TYPE_AHEAD_RESULT_CHATLIST = 7
    AISEARCH_TYPE_AHEAD_RESULT_MESSAGES = 8
    AIVOICE_SEARCH_BAR = 9
    AIVOICE_FAVICON = 10
    AISTUDIO = 11
    DEEPLINK = 12
    NOTIFICATION = 13
    PROFILE_MESSAGE_BUTTON = 14
    FORWARD = 15
    APP_SHORTCUT = 16
    FF_FAMILY = 17
    AI_TAB = 18
    AI_HOME = 19
    AI_DEEPLINK_IMMERSIVE = 20
    AI_DEEPLINK = 21
    META_AI_CHAT_SHORTCUT_AI_STUDIO = 22
    UGC_CHAT_SHORTCUT_AI_STUDIO = 23
    NEW_CHAT_AI_STUDIO = 24
    AIVOICE_FAVICON_CALL_HISTORY = 25
    ASK_META_AI_CONTEXT_MENU = 26
    ASK_META_AI_CONTEXT_MENU_1ON1 = 27
    ASK_META_AI_CONTEXT_MENU_GROUP = 28
    INVOKE_META_AI_1ON1 = 29
    INVOKE_META_AI_GROUP = 30
    META_AI_FORWARD = 31
    NEW_CHAT_AI_CONTACT = 32
    MESSAGE_QUICK_ACTION_1_ON_1_CHAT = 33
    MESSAGE_QUICK_ACTION_GROUP_CHAT = 34
    ATTACHMENT_TRAY_1_ON_1_CHAT = 35
    ATTACHMENT_TRAY_GROUP_CHAT = 36
    ASK_META_AI_MEDIA_VIEWER_1ON1 = 37
    ASK_META_AI_MEDIA_VIEWER_GROUP = 38

class BotMetricsThreadEntryPoint(enum.IntEnum):
    AI_TAB_THREAD = 1
    AI_HOME_THREAD = 2
    AI_DEEPLINK_IMMERSIVE_THREAD = 3
    AI_DEEPLINK_THREAD = 4
    ASK_META_AI_CONTEXT_MENU_THREAD = 5

class BotSessionSource(enum.IntEnum):
    NONE = 0
    NULL_STATE = 1
    TYPEAHEAD = 2
    USER_INPUT = 3
    EMU_FLASH = 4
    EMU_FLASH_FOLLOWUP = 5
    VOICE = 6

class CollectionName(enum.IntEnum):
    COLLECTION_NAME_UNKNOWN = 0
    REGULAR = 1
    REGULAR_LOW = 2
    REGULAR_HIGH = 3
    CRITICAL_BLOCK = 4
    CRITICAL_UNBLOCK_LOW = 5

class KeepType(enum.IntEnum):
    UNKNOWN = 0
    KEEP_FOR_ALL = 1
    UNDO_KEEP_FOR_ALL = 2

class MediaVisibility(enum.IntEnum):
    DEFAULT = 0
    OFF = 1
    ON = 2

class MutationProps(enum.IntEnum):
    STAR_ACTION = 2
    CONTACT_ACTION = 3
    MUTE_ACTION = 4
    PIN_ACTION = 5
    SECURITY_NOTIFICATION_SETTING = 6
    PUSH_NAME_SETTING = 7
    QUICK_REPLY_ACTION = 8
    RECENT_EMOJI_WEIGHTS_ACTION = 11
    LABEL_MESSAGE_ACTION = 13
    LABEL_EDIT_ACTION = 14
    LABEL_ASSOCIATION_ACTION = 15
    LOCALE_SETTING = 16
    ARCHIVE_CHAT_ACTION = 17
    DELETE_MESSAGE_FOR_ME_ACTION = 18
    KEY_EXPIRATION = 19
    MARK_CHAT_AS_READ_ACTION = 20
    CLEAR_CHAT_ACTION = 21
    DELETE_CHAT_ACTION = 22
    UNARCHIVE_CHATS_SETTING = 23
    PRIMARY_FEATURE = 24
    ANDROID_UNSUPPORTED_ACTIONS = 26
    AGENT_ACTION = 27
    SUBSCRIPTION_ACTION = 28
    USER_STATUS_MUTE_ACTION = 29
    TIME_FORMAT_ACTION = 30
    NUX_ACTION = 31
    PRIMARY_VERSION_ACTION = 32
    STICKER_ACTION = 33
    REMOVE_RECENT_STICKER_ACTION = 34
    CHAT_ASSIGNMENT = 35
    CHAT_ASSIGNMENT_OPENED_STATUS = 36
    PN_FOR_LID_CHAT_ACTION = 37
    MARKETING_MESSAGE_ACTION = 38
    MARKETING_MESSAGE_BROADCAST_ACTION = 39
    EXTERNAL_WEB_BETA_ACTION = 40
    PRIVACY_SETTING_RELAY_ALL_CALLS = 41
    CALL_LOG_ACTION = 42
    UGC_BOT = 43
    STATUS_PRIVACY = 44
    BOT_WELCOME_REQUEST_ACTION = 45
    DELETE_INDIVIDUAL_CALL_LOG = 46
    LABEL_REORDERING_ACTION = 47
    PAYMENT_INFO_ACTION = 48
    CUSTOM_PAYMENT_METHODS_ACTION = 49
    LOCK_CHAT_ACTION = 50
    CHAT_LOCK_SETTINGS = 51
    WAMO_USER_IDENTIFIER_ACTION = 52
    PRIVACY_SETTING_DISABLE_LINK_PREVIEWS_ACTION = 53
    DEVICE_CAPABILITIES = 54
    NOTE_EDIT_ACTION = 55
    FAVORITES_ACTION = 56
    MERCHANT_PAYMENT_PARTNER_ACTION = 57
    WAFFLE_ACCOUNT_LINK_STATE_ACTION = 58
    USERNAME_CHAT_START_MODE = 59
    NOTIFICATION_ACTIVITY_SETTING_ACTION = 60
    LID_CONTACT_ACTION = 61
    CTWA_PER_CUSTOMER_DATA_SHARING_ACTION = 62
    PAYMENT_TOS_ACTION = 63
    PRIVACY_SETTING_CHANNELS_PERSONALISED_RECOMMENDATION_ACTION = 64
    BUSINESS_BROADCAST_ASSOCIATION_ACTION = 65
    DETECTED_OUTCOMES_STATUS_ACTION = 66
    MAIBA_AI_FEATURES_CONTROL_ACTION = 68
    BUSINESS_BROADCAST_LIST_ACTION = 69
    MUSIC_USER_ID_ACTION = 70
    STATUS_POST_OPT_IN_NOTIFICATION_PREFERENCES_ACTION = 71
    AVATAR_UPDATED_ACTION = 72
    GALAXY_FLOW_ACTION = 73
    PRIVATE_PROCESSING_SETTING_ACTION = 74
    NEWSLETTER_SAVED_INTERESTS_ACTION = 75
    AI_THREAD_RENAME_ACTION = 76
    INTERACTIVE_MESSAGE_ACTION = 77
    SHARE_OWN_PN = 10001
    BUSINESS_BROADCAST_ACTION = 10002

class PrivacySystemMessage(enum.IntEnum):
    E2EE_MSG = 1
    NE2EE_SELF = 2
    NE2EE_OTHER = 3

class SessionTransparencyType(enum.IntEnum):
    UNKNOWN_TYPE = 0
    NY_AI_SAFETY_DISCLAIMER = 1

class WebLinkRenderConfig(enum.IntEnum):
    WEBVIEW = 0
    SYSTEM = 1

class ADVDeviceIdentity(MessageBase):
    FIELDS = {
        'rawId': FieldDescriptor('rawId', 1, 'uint32', repeated=False, packed=False),
        'timestamp': FieldDescriptor('timestamp', 2, 'uint64', repeated=False, packed=False),
        'keyIndex': FieldDescriptor('keyIndex', 3, 'uint32', repeated=False, packed=False),
        'accountType': FieldDescriptor('accountType', 4, "enum", repeated=False, packed=False, _enum_path='ADVEncryptionType'),
        'deviceType': FieldDescriptor('deviceType', 5, "enum", repeated=False, packed=False, _enum_path='ADVEncryptionType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ADVKeyIndexList(MessageBase):
    FIELDS = {
        'rawId': FieldDescriptor('rawId', 1, 'uint32', repeated=False, packed=False),
        'timestamp': FieldDescriptor('timestamp', 2, 'uint64', repeated=False, packed=False),
        'currentIndex': FieldDescriptor('currentIndex', 3, 'uint32', repeated=False, packed=False),
        'validIndexes': FieldDescriptor('validIndexes', 4, 'uint32', repeated=True, packed=True),
        'accountType': FieldDescriptor('accountType', 5, "enum", repeated=False, packed=False, _enum_path='ADVEncryptionType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ADVSignedDeviceIdentity(MessageBase):
    FIELDS = {
        'details': FieldDescriptor('details', 1, 'bytes', repeated=False, packed=False),
        'accountSignatureKey': FieldDescriptor('accountSignatureKey', 2, 'bytes', repeated=False, packed=False),
        'accountSignature': FieldDescriptor('accountSignature', 3, 'bytes', repeated=False, packed=False),
        'deviceSignature': FieldDescriptor('deviceSignature', 4, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ADVSignedDeviceIdentityHMAC(MessageBase):
    FIELDS = {
        'details': FieldDescriptor('details', 1, 'bytes', repeated=False, packed=False),
        'hmac': FieldDescriptor('hmac', 2, 'bytes', repeated=False, packed=False),
        'accountType': FieldDescriptor('accountType', 3, "enum", repeated=False, packed=False, _enum_path='ADVEncryptionType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ADVSignedKeyIndexList(MessageBase):
    FIELDS = {
        'details': FieldDescriptor('details', 1, 'bytes', repeated=False, packed=False),
        'accountSignature': FieldDescriptor('accountSignature', 2, 'bytes', repeated=False, packed=False),
        'accountSignatureKey': FieldDescriptor('accountSignatureKey', 3, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIHomeState(MessageBase):
    class AIHomeOption(MessageBase):
        class AIHomeActionType(enum.IntEnum):
            PROMPT = 0
            CREATE_IMAGE = 1
            ANIMATE_PHOTO = 2
            ANALYZE_FILE = 3
        FIELDS = {
            'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='AIHomeState.AIHomeOption.AIHomeActionType'),
            'title': FieldDescriptor('title', 2, 'string', repeated=False, packed=False),
            'promptText': FieldDescriptor('promptText', 3, 'string', repeated=False, packed=False),
            'sessionId': FieldDescriptor('sessionId', 4, 'string', repeated=False, packed=False),
            'imageWdsIdentifier': FieldDescriptor('imageWdsIdentifier', 5, 'string', repeated=False, packed=False),
            'imageTintColor': FieldDescriptor('imageTintColor', 6, 'string', repeated=False, packed=False),
            'imageBackgroundColor': FieldDescriptor('imageBackgroundColor', 7, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'lastFetchTime': FieldDescriptor('lastFetchTime', 1, 'int64', repeated=False, packed=False),
        'capabilityOptions': FieldDescriptor('capabilityOptions', 2, "message", repeated=True, packed=False, _msg_path='AIHomeState.AIHomeOption'),
        'conversationOptions': FieldDescriptor('conversationOptions', 3, "message", repeated=True, packed=False, _msg_path='AIHomeState.AIHomeOption'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIQueryFanout(MessageBase):
    FIELDS = {
        'messageKey': FieldDescriptor('messageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'message': FieldDescriptor('message', 2, "message", repeated=False, packed=False, _msg_path='Message'),
        'timestamp': FieldDescriptor('timestamp', 3, 'int64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRegenerateMetadata(MessageBase):
    FIELDS = {
        'messageKey': FieldDescriptor('messageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'responseTimestampMs': FieldDescriptor('responseTimestampMs', 2, 'int64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseCodeMetadata(MessageBase):
    class AIRichResponseCodeHighlightType(enum.IntEnum):
        AI_RICH_RESPONSE_CODE_HIGHLIGHT_DEFAULT = 0
        AI_RICH_RESPONSE_CODE_HIGHLIGHT_KEYWORD = 1
        AI_RICH_RESPONSE_CODE_HIGHLIGHT_METHOD = 2
        AI_RICH_RESPONSE_CODE_HIGHLIGHT_STRING = 3
        AI_RICH_RESPONSE_CODE_HIGHLIGHT_NUMBER = 4
        AI_RICH_RESPONSE_CODE_HIGHLIGHT_COMMENT = 5
    class AIRichResponseCodeBlock(MessageBase):
        FIELDS = {
            'highlightType': FieldDescriptor('highlightType', 1, "enum", repeated=False, packed=False, _enum_path='AIRichResponseCodeMetadata.AIRichResponseCodeHighlightType'),
            'codeContent': FieldDescriptor('codeContent', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'codeLanguage': FieldDescriptor('codeLanguage', 1, 'string', repeated=False, packed=False),
        'codeBlocks': FieldDescriptor('codeBlocks', 2, "message", repeated=True, packed=False, _msg_path='AIRichResponseCodeMetadata.AIRichResponseCodeBlock'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseContentItemsMetadata(MessageBase):
    class ContentType(enum.IntEnum):
        DEFAULT = 0
        CAROUSEL = 1
    class AIRichResponseContentItemMetadata(MessageBase):
        FIELDS = {
            'reelItem': FieldDescriptor('reelItem', 1, "message", repeated=False, packed=False, _msg_path='AIRichResponseContentItemsMetadata.AIRichResponseReelItem'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AIRichResponseReelItem(MessageBase):
        FIELDS = {
            'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
            'profileIconUrl': FieldDescriptor('profileIconUrl', 2, 'string', repeated=False, packed=False),
            'thumbnailUrl': FieldDescriptor('thumbnailUrl', 3, 'string', repeated=False, packed=False),
            'videoUrl': FieldDescriptor('videoUrl', 4, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'itemsMetadata': FieldDescriptor('itemsMetadata', 1, "message", repeated=True, packed=False, _msg_path='AIRichResponseContentItemsMetadata.AIRichResponseContentItemMetadata'),
        'contentType': FieldDescriptor('contentType', 2, "enum", repeated=False, packed=False, _enum_path='AIRichResponseContentItemsMetadata.ContentType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseDynamicMetadata(MessageBase):
    class AIRichResponseDynamicMetadataType(enum.IntEnum):
        AI_RICH_RESPONSE_DYNAMIC_METADATA_TYPE_UNKNOWN = 0
        AI_RICH_RESPONSE_DYNAMIC_METADATA_TYPE_IMAGE = 1
        AI_RICH_RESPONSE_DYNAMIC_METADATA_TYPE_GIF = 2
    FIELDS = {
        'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='AIRichResponseDynamicMetadata.AIRichResponseDynamicMetadataType'),
        'version': FieldDescriptor('version', 2, 'uint64', repeated=False, packed=False),
        'url': FieldDescriptor('url', 3, 'string', repeated=False, packed=False),
        'loopCount': FieldDescriptor('loopCount', 4, 'uint32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseGridImageMetadata(MessageBase):
    FIELDS = {
        'gridImageUrl': FieldDescriptor('gridImageUrl', 1, "message", repeated=False, packed=False, _msg_path='AIRichResponseImageURL'),
        'imageUrls': FieldDescriptor('imageUrls', 2, "message", repeated=True, packed=False, _msg_path='AIRichResponseImageURL'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseImageURL(MessageBase):
    FIELDS = {
        'imagePreviewUrl': FieldDescriptor('imagePreviewUrl', 1, 'string', repeated=False, packed=False),
        'imageHighResUrl': FieldDescriptor('imageHighResUrl', 2, 'string', repeated=False, packed=False),
        'sourceUrl': FieldDescriptor('sourceUrl', 3, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseInlineImageMetadata(MessageBase):
    class AIRichResponseImageAlignment(enum.IntEnum):
        AI_RICH_RESPONSE_IMAGE_LAYOUT_LEADING_ALIGNED = 0
        AI_RICH_RESPONSE_IMAGE_LAYOUT_TRAILING_ALIGNED = 1
        AI_RICH_RESPONSE_IMAGE_LAYOUT_CENTER_ALIGNED = 2
    FIELDS = {
        'imageUrl': FieldDescriptor('imageUrl', 1, "message", repeated=False, packed=False, _msg_path='AIRichResponseImageURL'),
        'imageText': FieldDescriptor('imageText', 2, 'string', repeated=False, packed=False),
        'alignment': FieldDescriptor('alignment', 3, "enum", repeated=False, packed=False, _enum_path='AIRichResponseInlineImageMetadata.AIRichResponseImageAlignment'),
        'tapLinkUrl': FieldDescriptor('tapLinkUrl', 4, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseLatexMetadata(MessageBase):
    class AIRichResponseLatexExpression(MessageBase):
        FIELDS = {
            'latexExpression': FieldDescriptor('latexExpression', 1, 'string', repeated=False, packed=False),
            'url': FieldDescriptor('url', 2, 'string', repeated=False, packed=False),
            'width': FieldDescriptor('width', 3, 'double', repeated=False, packed=False),
            'height': FieldDescriptor('height', 4, 'double', repeated=False, packed=False),
            'fontHeight': FieldDescriptor('fontHeight', 5, 'double', repeated=False, packed=False),
            'imageTopPadding': FieldDescriptor('imageTopPadding', 6, 'double', repeated=False, packed=False),
            'imageLeadingPadding': FieldDescriptor('imageLeadingPadding', 7, 'double', repeated=False, packed=False),
            'imageBottomPadding': FieldDescriptor('imageBottomPadding', 8, 'double', repeated=False, packed=False),
            'imageTrailingPadding': FieldDescriptor('imageTrailingPadding', 9, 'double', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'text': FieldDescriptor('text', 1, 'string', repeated=False, packed=False),
        'expressions': FieldDescriptor('expressions', 2, "message", repeated=True, packed=False, _msg_path='AIRichResponseLatexMetadata.AIRichResponseLatexExpression'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseMapMetadata(MessageBase):
    class AIRichResponseMapAnnotation(MessageBase):
        FIELDS = {
            'annotationNumber': FieldDescriptor('annotationNumber', 1, 'uint32', repeated=False, packed=False),
            'latitude': FieldDescriptor('latitude', 2, 'double', repeated=False, packed=False),
            'longitude': FieldDescriptor('longitude', 3, 'double', repeated=False, packed=False),
            'title': FieldDescriptor('title', 4, 'string', repeated=False, packed=False),
            'body': FieldDescriptor('body', 5, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'centerLatitude': FieldDescriptor('centerLatitude', 1, 'double', repeated=False, packed=False),
        'centerLongitude': FieldDescriptor('centerLongitude', 2, 'double', repeated=False, packed=False),
        'latitudeDelta': FieldDescriptor('latitudeDelta', 3, 'double', repeated=False, packed=False),
        'longitudeDelta': FieldDescriptor('longitudeDelta', 4, 'double', repeated=False, packed=False),
        'annotations': FieldDescriptor('annotations', 5, "message", repeated=True, packed=False, _msg_path='AIRichResponseMapMetadata.AIRichResponseMapAnnotation'),
        'showInfoList': FieldDescriptor('showInfoList', 6, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseMessage(MessageBase):
    FIELDS = {
        'messageType': FieldDescriptor('messageType', 1, "enum", repeated=False, packed=False, _enum_path='AIRichResponseMessageType'),
        'submessages': FieldDescriptor('submessages', 2, "message", repeated=True, packed=False, _msg_path='AIRichResponseSubMessage'),
        'unifiedResponse': FieldDescriptor('unifiedResponse', 3, "message", repeated=False, packed=False, _msg_path='AIRichResponseUnifiedResponse'),
        'contextInfo': FieldDescriptor('contextInfo', 4, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseSubMessage(MessageBase):
    FIELDS = {
        'messageType': FieldDescriptor('messageType', 1, "enum", repeated=False, packed=False, _enum_path='AIRichResponseSubMessageType'),
        'gridImageMetadata': FieldDescriptor('gridImageMetadata', 2, "message", repeated=False, packed=False, _msg_path='AIRichResponseGridImageMetadata'),
        'messageText': FieldDescriptor('messageText', 3, 'string', repeated=False, packed=False),
        'imageMetadata': FieldDescriptor('imageMetadata', 4, "message", repeated=False, packed=False, _msg_path='AIRichResponseInlineImageMetadata'),
        'codeMetadata': FieldDescriptor('codeMetadata', 5, "message", repeated=False, packed=False, _msg_path='AIRichResponseCodeMetadata'),
        'tableMetadata': FieldDescriptor('tableMetadata', 6, "message", repeated=False, packed=False, _msg_path='AIRichResponseTableMetadata'),
        'dynamicMetadata': FieldDescriptor('dynamicMetadata', 7, "message", repeated=False, packed=False, _msg_path='AIRichResponseDynamicMetadata'),
        'latexMetadata': FieldDescriptor('latexMetadata', 8, "message", repeated=False, packed=False, _msg_path='AIRichResponseLatexMetadata'),
        'mapMetadata': FieldDescriptor('mapMetadata', 9, "message", repeated=False, packed=False, _msg_path='AIRichResponseMapMetadata'),
        'contentItemsMetadata': FieldDescriptor('contentItemsMetadata', 10, "message", repeated=False, packed=False, _msg_path='AIRichResponseContentItemsMetadata'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseTableMetadata(MessageBase):
    class AIRichResponseTableRow(MessageBase):
        FIELDS = {
            'items': FieldDescriptor('items', 1, 'string', repeated=True, packed=False),
            'isHeading': FieldDescriptor('isHeading', 2, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'rows': FieldDescriptor('rows', 1, "message", repeated=True, packed=False, _msg_path='AIRichResponseTableMetadata.AIRichResponseTableRow'),
        'title': FieldDescriptor('title', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIRichResponseUnifiedResponse(MessageBase):
    FIELDS = {
        'data': FieldDescriptor('data', 1, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AIThreadInfo(MessageBase):
    class AIThreadClientInfo(MessageBase):
        class AIThreadType(enum.IntEnum):
            UNKNOWN = 0
            DEFAULT = 1
            INCOGNITO = 2
        FIELDS = {
            'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='AIThreadInfo.AIThreadClientInfo.AIThreadType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AIThreadServerInfo(MessageBase):
        FIELDS = {
            'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'serverInfo': FieldDescriptor('serverInfo', 1, "message", repeated=False, packed=False, _msg_path='AIThreadInfo.AIThreadServerInfo'),
        'clientInfo': FieldDescriptor('clientInfo', 2, "message", repeated=False, packed=False, _msg_path='AIThreadInfo.AIThreadClientInfo'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Account(MessageBase):
    FIELDS = {
        'lid': FieldDescriptor('lid', 1, 'string', repeated=False, packed=False),
        'username': FieldDescriptor('username', 2, 'string', repeated=False, packed=False),
        'countryCode': FieldDescriptor('countryCode', 3, 'string', repeated=False, packed=False),
        'isUsernameDeleted': FieldDescriptor('isUsernameDeleted', 4, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ActionLink(MessageBase):
    FIELDS = {
        'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
        'buttonTitle': FieldDescriptor('buttonTitle', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AutoDownloadSettings(MessageBase):
    FIELDS = {
        'downloadImages': FieldDescriptor('downloadImages', 1, 'bool', repeated=False, packed=False),
        'downloadAudio': FieldDescriptor('downloadAudio', 2, 'bool', repeated=False, packed=False),
        'downloadVideo': FieldDescriptor('downloadVideo', 3, 'bool', repeated=False, packed=False),
        'downloadDocuments': FieldDescriptor('downloadDocuments', 4, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class AvatarUserSettings(MessageBase):
    FIELDS = {
        'fbid': FieldDescriptor('fbid', 1, 'string', repeated=False, packed=False),
        'password': FieldDescriptor('password', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BizAccountLinkInfo(MessageBase):
    class AccountType(enum.IntEnum):
        ENTERPRISE = 0
    class HostStorageType(enum.IntEnum):
        ON_PREMISE = 0
        FACEBOOK = 1
    FIELDS = {
        'whatsappBizAcctFbid': FieldDescriptor('whatsappBizAcctFbid', 1, 'uint64', repeated=False, packed=False),
        'whatsappAcctNumber': FieldDescriptor('whatsappAcctNumber', 2, 'string', repeated=False, packed=False),
        'issueTime': FieldDescriptor('issueTime', 3, 'uint64', repeated=False, packed=False),
        'hostStorage': FieldDescriptor('hostStorage', 4, "enum", repeated=False, packed=False, _enum_path='BizAccountLinkInfo.HostStorageType'),
        'accountType': FieldDescriptor('accountType', 5, "enum", repeated=False, packed=False, _enum_path='BizAccountLinkInfo.AccountType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BizAccountPayload(MessageBase):
    FIELDS = {
        'vnameCert': FieldDescriptor('vnameCert', 1, "message", repeated=False, packed=False, _msg_path='VerifiedNameCertificate'),
        'bizAcctLinkInfo': FieldDescriptor('bizAcctLinkInfo', 2, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BizIdentityInfo(MessageBase):
    class ActualActorsType(enum.IntEnum):
        SELF = 0
        BSP = 1
    class HostStorageType(enum.IntEnum):
        ON_PREMISE = 0
        FACEBOOK = 1
    class VerifiedLevelValue(enum.IntEnum):
        UNKNOWN = 0
        LOW = 1
        HIGH = 2
    FIELDS = {
        'vlevel': FieldDescriptor('vlevel', 1, "enum", repeated=False, packed=False, _enum_path='BizIdentityInfo.VerifiedLevelValue'),
        'vnameCert': FieldDescriptor('vnameCert', 2, "message", repeated=False, packed=False, _msg_path='VerifiedNameCertificate'),
        'signed': FieldDescriptor('signed', 3, 'bool', repeated=False, packed=False),
        'revoked': FieldDescriptor('revoked', 4, 'bool', repeated=False, packed=False),
        'hostStorage': FieldDescriptor('hostStorage', 5, "enum", repeated=False, packed=False, _enum_path='BizIdentityInfo.HostStorageType'),
        'actualActors': FieldDescriptor('actualActors', 6, "enum", repeated=False, packed=False, _enum_path='BizIdentityInfo.ActualActorsType'),
        'privacyModeTs': FieldDescriptor('privacyModeTs', 7, 'uint64', repeated=False, packed=False),
        'featureControls': FieldDescriptor('featureControls', 8, 'uint64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotAgeCollectionMetadata(MessageBase):
    class AgeCollectionType(enum.IntEnum):
        O18_BINARY = 0
        WAFFLE = 1
    FIELDS = {
        'ageCollectionEligible': FieldDescriptor('ageCollectionEligible', 1, 'bool', repeated=False, packed=False),
        'shouldTriggerAgeCollectionOnClient': FieldDescriptor('shouldTriggerAgeCollectionOnClient', 2, 'bool', repeated=False, packed=False),
        'ageCollectionType': FieldDescriptor('ageCollectionType', 3, "enum", repeated=False, packed=False, _enum_path='BotAgeCollectionMetadata.AgeCollectionType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotAvatarMetadata(MessageBase):
    FIELDS = {
        'sentiment': FieldDescriptor('sentiment', 1, 'uint32', repeated=False, packed=False),
        'behaviorGraph': FieldDescriptor('behaviorGraph', 2, 'string', repeated=False, packed=False),
        'action': FieldDescriptor('action', 3, 'uint32', repeated=False, packed=False),
        'intensity': FieldDescriptor('intensity', 4, 'uint32', repeated=False, packed=False),
        'wordCount': FieldDescriptor('wordCount', 5, 'uint32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotCapabilityMetadata(MessageBase):
    class BotCapabilityType(enum.IntEnum):
        UNKNOWN = 0
        PROGRESS_INDICATOR = 1
        RICH_RESPONSE_HEADING = 2
        RICH_RESPONSE_NESTED_LIST = 3
        AI_MEMORY = 4
        RICH_RESPONSE_THREAD_SURFING = 5
        RICH_RESPONSE_TABLE = 6
        RICH_RESPONSE_CODE = 7
        RICH_RESPONSE_STRUCTURED_RESPONSE = 8
        RICH_RESPONSE_INLINE_IMAGE = 9
        WA_IG_1P_PLUGIN_RANKING_CONTROL = 10
        WA_IG_1P_PLUGIN_RANKING_UPDATE_1 = 11
        WA_IG_1P_PLUGIN_RANKING_UPDATE_2 = 12
        WA_IG_1P_PLUGIN_RANKING_UPDATE_3 = 13
        WA_IG_1P_PLUGIN_RANKING_UPDATE_4 = 14
        WA_IG_1P_PLUGIN_RANKING_UPDATE_5 = 15
        WA_IG_1P_PLUGIN_RANKING_UPDATE_6 = 16
        WA_IG_1P_PLUGIN_RANKING_UPDATE_7 = 17
        WA_IG_1P_PLUGIN_RANKING_UPDATE_8 = 18
        WA_IG_1P_PLUGIN_RANKING_UPDATE_9 = 19
        WA_IG_1P_PLUGIN_RANKING_UPDATE_10 = 20
        RICH_RESPONSE_SUB_HEADING = 21
        RICH_RESPONSE_GRID_IMAGE = 22
        AI_STUDIO_UGC_MEMORY = 23
        RICH_RESPONSE_LATEX = 24
        RICH_RESPONSE_MAPS = 25
        RICH_RESPONSE_INLINE_REELS = 26
        AGENTIC_PLANNING = 27
        ACCOUNT_LINKING = 28
        STREAMING_DISAGGREGATION = 29
        RICH_RESPONSE_GRID_IMAGE_3P = 30
        RICH_RESPONSE_LATEX_INLINE = 31
        QUERY_PLAN = 32
        PROACTIVE_MESSAGE = 33
        RICH_RESPONSE_UNIFIED_RESPONSE = 34
        PROMOTION_MESSAGE = 35
        SIMPLIFIED_PROFILE_PAGE = 36
        RICH_RESPONSE_SOURCES_IN_MESSAGE = 37
        RICH_RESPONSE_SIDE_BY_SIDE_SURVEY = 38
        RICH_RESPONSE_UNIFIED_TEXT_COMPONENT = 39
        AI_SHARED_MEMORY = 40
        RICH_RESPONSE_UNIFIED_SOURCES = 41
        RICH_RESPONSE_UNIFIED_DOMAIN_CITATIONS = 42
        RICH_RESPONSE_UR_INLINE_REELS_ENABLED = 43
        RICH_RESPONSE_UR_MEDIA_GRID_ENABLED = 44
        RICH_RESPONSE_UR_TIMESTAMP_PLACEHOLDER = 45
        RICH_RESPONSE_IN_APP_SURVEY = 46
        AI_RESPONSE_MODEL_BRANDING = 47
        SESSION_TRANSPARENCY_SYSTEM_MESSAGE = 48
        RICH_RESPONSE_UR_REASONING = 49
    FIELDS = {
        'capabilities': FieldDescriptor('capabilities', 1, "enum", repeated=True, packed=False, _enum_path='BotCapabilityMetadata.BotCapabilityType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotFeedbackMessage(MessageBase):
    class BotFeedbackKind(enum.IntEnum):
        BOT_FEEDBACK_POSITIVE = 0
        BOT_FEEDBACK_NEGATIVE_GENERIC = 1
        BOT_FEEDBACK_NEGATIVE_HELPFUL = 2
        BOT_FEEDBACK_NEGATIVE_INTERESTING = 3
        BOT_FEEDBACK_NEGATIVE_ACCURATE = 4
        BOT_FEEDBACK_NEGATIVE_SAFE = 5
        BOT_FEEDBACK_NEGATIVE_OTHER = 6
        BOT_FEEDBACK_NEGATIVE_REFUSED = 7
        BOT_FEEDBACK_NEGATIVE_NOT_VISUALLY_APPEALING = 8
        BOT_FEEDBACK_NEGATIVE_NOT_RELEVANT_TO_TEXT = 9
        BOT_FEEDBACK_NEGATIVE_PERSONALIZED = 10
        BOT_FEEDBACK_NEGATIVE_CLARITY = 11
        BOT_FEEDBACK_NEGATIVE_DOESNT_LOOK_LIKE_THE_PERSON = 12
        BOT_FEEDBACK_NEGATIVE_HALLUCINATION_INTERNAL_ONLY = 13
        BOT_FEEDBACK_NEGATIVE = 14
    class BotFeedbackKindMultipleNegative(enum.IntEnum):
        BOT_FEEDBACK_MULTIPLE_NEGATIVE_GENERIC = 1
        BOT_FEEDBACK_MULTIPLE_NEGATIVE_HELPFUL = 2
        BOT_FEEDBACK_MULTIPLE_NEGATIVE_INTERESTING = 4
        BOT_FEEDBACK_MULTIPLE_NEGATIVE_ACCURATE = 8
        BOT_FEEDBACK_MULTIPLE_NEGATIVE_SAFE = 16
        BOT_FEEDBACK_MULTIPLE_NEGATIVE_OTHER = 32
        BOT_FEEDBACK_MULTIPLE_NEGATIVE_REFUSED = 64
        BOT_FEEDBACK_MULTIPLE_NEGATIVE_NOT_VISUALLY_APPEALING = 128
        BOT_FEEDBACK_MULTIPLE_NEGATIVE_NOT_RELEVANT_TO_TEXT = 256
    class BotFeedbackKindMultiplePositive(enum.IntEnum):
        BOT_FEEDBACK_MULTIPLE_POSITIVE_GENERIC = 1
    class ReportKind(enum.IntEnum):
        NONE = 0
        GENERIC = 1
    class SideBySideSurveyMetadata(MessageBase):
        class SideBySideSurveyAnalyticsData(MessageBase):
            FIELDS = {
                'tessaEvent': FieldDescriptor('tessaEvent', 1, 'string', repeated=False, packed=False),
                'tessaSessionFbid': FieldDescriptor('tessaSessionFbid', 2, 'string', repeated=False, packed=False),
                'simonSessionFbid': FieldDescriptor('simonSessionFbid', 3, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class SidebySideSurveyMetaAiAnalyticsData(MessageBase):
            class SideBySideSurveyAbandonEventData(MessageBase):
                FIELDS = {
                    'abandonDwellTimeMsString': FieldDescriptor('abandonDwellTimeMsString', 1, 'string', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class SideBySideSurveyCTAClickEventData(MessageBase):
                FIELDS = {
                    'isSurveyExpired': FieldDescriptor('isSurveyExpired', 1, 'bool', repeated=False, packed=False),
                    'clickDwellTimeMsString': FieldDescriptor('clickDwellTimeMsString', 2, 'string', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class SideBySideSurveyCTAImpressionEventData(MessageBase):
                FIELDS = {
                    'isSurveyExpired': FieldDescriptor('isSurveyExpired', 1, 'bool', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class SideBySideSurveyCardImpressionEventData(MessageBase):
                FIELDS = {
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class SideBySideSurveyResponseEventData(MessageBase):
                FIELDS = {
                    'responseDwellTimeMsString': FieldDescriptor('responseDwellTimeMsString', 1, 'string', repeated=False, packed=False),
                    'selectedResponseId': FieldDescriptor('selectedResponseId', 2, 'string', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            FIELDS = {
                'surveyId': FieldDescriptor('surveyId', 1, 'uint32', repeated=False, packed=False),
                'primaryResponseId': FieldDescriptor('primaryResponseId', 2, 'string', repeated=False, packed=False),
                'testArmName': FieldDescriptor('testArmName', 3, 'string', repeated=False, packed=False),
                'timestampMsString': FieldDescriptor('timestampMsString', 4, 'string', repeated=False, packed=False),
                'ctaImpressionEvent': FieldDescriptor('ctaImpressionEvent', 5, "message", repeated=False, packed=False, _msg_path='BotFeedbackMessage.SideBySideSurveyMetadata.SidebySideSurveyMetaAiAnalyticsData.SideBySideSurveyCTAImpressionEventData'),
                'ctaClickEvent': FieldDescriptor('ctaClickEvent', 6, "message", repeated=False, packed=False, _msg_path='BotFeedbackMessage.SideBySideSurveyMetadata.SidebySideSurveyMetaAiAnalyticsData.SideBySideSurveyCTAClickEventData'),
                'cardImpressionEvent': FieldDescriptor('cardImpressionEvent', 7, "message", repeated=False, packed=False, _msg_path='BotFeedbackMessage.SideBySideSurveyMetadata.SidebySideSurveyMetaAiAnalyticsData.SideBySideSurveyCardImpressionEventData'),
                'responseEvent': FieldDescriptor('responseEvent', 8, "message", repeated=False, packed=False, _msg_path='BotFeedbackMessage.SideBySideSurveyMetadata.SidebySideSurveyMetaAiAnalyticsData.SideBySideSurveyResponseEventData'),
                'abandonEvent': FieldDescriptor('abandonEvent', 9, "message", repeated=False, packed=False, _msg_path='BotFeedbackMessage.SideBySideSurveyMetadata.SidebySideSurveyMetaAiAnalyticsData.SideBySideSurveyAbandonEventData'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'selectedRequestId': FieldDescriptor('selectedRequestId', 1, 'string', repeated=False, packed=False),
            'surveyId': FieldDescriptor('surveyId', 2, 'uint32', repeated=False, packed=False),
            'simonSessionFbid': FieldDescriptor('simonSessionFbid', 3, 'string', repeated=False, packed=False),
            'responseOtid': FieldDescriptor('responseOtid', 4, 'string', repeated=False, packed=False),
            'responseTimestampMsString': FieldDescriptor('responseTimestampMsString', 5, 'string', repeated=False, packed=False),
            'isSelectedResponsePrimary': FieldDescriptor('isSelectedResponsePrimary', 6, 'bool', repeated=False, packed=False),
            'messageIdToEdit': FieldDescriptor('messageIdToEdit', 7, 'string', repeated=False, packed=False),
            'analyticsData': FieldDescriptor('analyticsData', 8, "message", repeated=False, packed=False, _msg_path='BotFeedbackMessage.SideBySideSurveyMetadata.SideBySideSurveyAnalyticsData'),
            'metaAiAnalyticsData': FieldDescriptor('metaAiAnalyticsData', 9, "message", repeated=False, packed=False, _msg_path='BotFeedbackMessage.SideBySideSurveyMetadata.SidebySideSurveyMetaAiAnalyticsData'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'messageKey': FieldDescriptor('messageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'kind': FieldDescriptor('kind', 2, "enum", repeated=False, packed=False, _enum_path='BotFeedbackMessage.BotFeedbackKind'),
        'text': FieldDescriptor('text', 3, 'string', repeated=False, packed=False),
        'kindNegative': FieldDescriptor('kindNegative', 4, 'uint64', repeated=False, packed=False),
        'kindPositive': FieldDescriptor('kindPositive', 5, 'uint64', repeated=False, packed=False),
        'kindReport': FieldDescriptor('kindReport', 6, "enum", repeated=False, packed=False, _enum_path='BotFeedbackMessage.ReportKind'),
        'sideBySideSurveyMetadata': FieldDescriptor('sideBySideSurveyMetadata', 7, "message", repeated=False, packed=False, _msg_path='BotFeedbackMessage.SideBySideSurveyMetadata'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotImagineMetadata(MessageBase):
    class ImagineType(enum.IntEnum):
        UNKNOWN = 0
        IMAGINE = 1
        MEMU = 2
        FLASH = 3
        EDIT = 4
    FIELDS = {
        'imagineType': FieldDescriptor('imagineType', 1, "enum", repeated=False, packed=False, _enum_path='BotImagineMetadata.ImagineType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotLinkedAccount(MessageBase):
    class BotLinkedAccountType(enum.IntEnum):
        BOT_LINKED_ACCOUNT_TYPE_1P = 0
    FIELDS = {
        'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='BotLinkedAccount.BotLinkedAccountType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotLinkedAccountsMetadata(MessageBase):
    FIELDS = {
        'accounts': FieldDescriptor('accounts', 1, "message", repeated=True, packed=False, _msg_path='BotLinkedAccount'),
        'acAuthTokens': FieldDescriptor('acAuthTokens', 2, 'bytes', repeated=False, packed=False),
        'acErrorCode': FieldDescriptor('acErrorCode', 3, 'int32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotMediaMetadata(MessageBase):
    class OrientationType(enum.IntEnum):
        CENTER = 1
        LEFT = 2
        RIGHT = 3
    FIELDS = {
        'fileSha256': FieldDescriptor('fileSha256', 1, 'string', repeated=False, packed=False),
        'mediaKey': FieldDescriptor('mediaKey', 2, 'string', repeated=False, packed=False),
        'fileEncSha256': FieldDescriptor('fileEncSha256', 3, 'string', repeated=False, packed=False),
        'directPath': FieldDescriptor('directPath', 4, 'string', repeated=False, packed=False),
        'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 5, 'int64', repeated=False, packed=False),
        'mimetype': FieldDescriptor('mimetype', 6, 'string', repeated=False, packed=False),
        'orientationType': FieldDescriptor('orientationType', 7, "enum", repeated=False, packed=False, _enum_path='BotMediaMetadata.OrientationType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotMemoryFact(MessageBase):
    FIELDS = {
        'fact': FieldDescriptor('fact', 1, 'string', repeated=False, packed=False),
        'factId': FieldDescriptor('factId', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotMemoryMetadata(MessageBase):
    FIELDS = {
        'addedFacts': FieldDescriptor('addedFacts', 1, "message", repeated=True, packed=False, _msg_path='BotMemoryFact'),
        'removedFacts': FieldDescriptor('removedFacts', 2, "message", repeated=True, packed=False, _msg_path='BotMemoryFact'),
        'disclaimer': FieldDescriptor('disclaimer', 3, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotMemuMetadata(MessageBase):
    FIELDS = {
        'faceImages': FieldDescriptor('faceImages', 1, "message", repeated=True, packed=False, _msg_path='BotMediaMetadata'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotMessageOrigin(MessageBase):
    class BotMessageOriginType(enum.IntEnum):
        BOT_MESSAGE_ORIGIN_TYPE_AI_INITIATED = 0
    FIELDS = {
        'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='BotMessageOrigin.BotMessageOriginType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotMessageOriginMetadata(MessageBase):
    FIELDS = {
        'origins': FieldDescriptor('origins', 1, "message", repeated=True, packed=False, _msg_path='BotMessageOrigin'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotMessageSharingInfo(MessageBase):
    FIELDS = {
        'botEntryPointOrigin': FieldDescriptor('botEntryPointOrigin', 1, "enum", repeated=False, packed=False, _enum_path='BotMetricsEntryPoint'),
        'forwardScore': FieldDescriptor('forwardScore', 2, 'uint32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotMetadata(MessageBase):
    FIELDS = {
        'avatarMetadata': FieldDescriptor('avatarMetadata', 1, "message", repeated=False, packed=False, _msg_path='BotAvatarMetadata'),
        'personaId': FieldDescriptor('personaId', 2, 'string', repeated=False, packed=False),
        'pluginMetadata': FieldDescriptor('pluginMetadata', 3, "message", repeated=False, packed=False, _msg_path='BotPluginMetadata'),
        'suggestedPromptMetadata': FieldDescriptor('suggestedPromptMetadata', 4, "message", repeated=False, packed=False, _msg_path='BotSuggestedPromptMetadata'),
        'invokerJid': FieldDescriptor('invokerJid', 5, 'string', repeated=False, packed=False),
        'sessionMetadata': FieldDescriptor('sessionMetadata', 6, "message", repeated=False, packed=False, _msg_path='BotSessionMetadata'),
        'memuMetadata': FieldDescriptor('memuMetadata', 7, "message", repeated=False, packed=False, _msg_path='BotMemuMetadata'),
        'timezone': FieldDescriptor('timezone', 8, 'string', repeated=False, packed=False),
        'reminderMetadata': FieldDescriptor('reminderMetadata', 9, "message", repeated=False, packed=False, _msg_path='BotReminderMetadata'),
        'modelMetadata': FieldDescriptor('modelMetadata', 10, "message", repeated=False, packed=False, _msg_path='BotModelMetadata'),
        'messageDisclaimerText': FieldDescriptor('messageDisclaimerText', 11, 'string', repeated=False, packed=False),
        'progressIndicatorMetadata': FieldDescriptor('progressIndicatorMetadata', 12, "message", repeated=False, packed=False, _msg_path='BotProgressIndicatorMetadata'),
        'capabilityMetadata': FieldDescriptor('capabilityMetadata', 13, "message", repeated=False, packed=False, _msg_path='BotCapabilityMetadata'),
        'imagineMetadata': FieldDescriptor('imagineMetadata', 14, "message", repeated=False, packed=False, _msg_path='BotImagineMetadata'),
        'memoryMetadata': FieldDescriptor('memoryMetadata', 15, "message", repeated=False, packed=False, _msg_path='BotMemoryMetadata'),
        'renderingMetadata': FieldDescriptor('renderingMetadata', 16, "message", repeated=False, packed=False, _msg_path='BotRenderingMetadata'),
        'botMetricsMetadata': FieldDescriptor('botMetricsMetadata', 17, "message", repeated=False, packed=False, _msg_path='BotMetricsMetadata'),
        'botLinkedAccountsMetadata': FieldDescriptor('botLinkedAccountsMetadata', 18, "message", repeated=False, packed=False, _msg_path='BotLinkedAccountsMetadata'),
        'richResponseSourcesMetadata': FieldDescriptor('richResponseSourcesMetadata', 19, "message", repeated=False, packed=False, _msg_path='BotSourcesMetadata'),
        'aiConversationContext': FieldDescriptor('aiConversationContext', 20, 'bytes', repeated=False, packed=False),
        'botPromotionMessageMetadata': FieldDescriptor('botPromotionMessageMetadata', 21, "message", repeated=False, packed=False, _msg_path='BotPromotionMessageMetadata'),
        'botModeSelectionMetadata': FieldDescriptor('botModeSelectionMetadata', 22, "message", repeated=False, packed=False, _msg_path='BotModeSelectionMetadata'),
        'botQuotaMetadata': FieldDescriptor('botQuotaMetadata', 23, "message", repeated=False, packed=False, _msg_path='BotQuotaMetadata'),
        'botAgeCollectionMetadata': FieldDescriptor('botAgeCollectionMetadata', 24, "message", repeated=False, packed=False, _msg_path='BotAgeCollectionMetadata'),
        'conversationStarterPromptId': FieldDescriptor('conversationStarterPromptId', 25, 'string', repeated=False, packed=False),
        'botResponseId': FieldDescriptor('botResponseId', 26, 'string', repeated=False, packed=False),
        'verificationMetadata': FieldDescriptor('verificationMetadata', 27, "message", repeated=False, packed=False, _msg_path='BotSignatureVerificationMetadata'),
        'unifiedResponseMutation': FieldDescriptor('unifiedResponseMutation', 28, "message", repeated=False, packed=False, _msg_path='BotUnifiedResponseMutation'),
        'botMessageOriginMetadata': FieldDescriptor('botMessageOriginMetadata', 29, "message", repeated=False, packed=False, _msg_path='BotMessageOriginMetadata'),
        'inThreadSurveyMetadata': FieldDescriptor('inThreadSurveyMetadata', 30, "message", repeated=False, packed=False, _msg_path='InThreadSurveyMetadata'),
        'botThreadInfo': FieldDescriptor('botThreadInfo', 31, "message", repeated=False, packed=False, _msg_path='AIThreadInfo'),
        'regenerateMetadata': FieldDescriptor('regenerateMetadata', 32, "message", repeated=False, packed=False, _msg_path='AIRegenerateMetadata'),
        'sessionTransparencyMetadata': FieldDescriptor('sessionTransparencyMetadata', 33, "message", repeated=False, packed=False, _msg_path='SessionTransparencyMetadata'),
        'internalMetadata': FieldDescriptor('internalMetadata', 999, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotMetricsMetadata(MessageBase):
    FIELDS = {
        'destinationId': FieldDescriptor('destinationId', 1, 'string', repeated=False, packed=False),
        'destinationEntryPoint': FieldDescriptor('destinationEntryPoint', 2, "enum", repeated=False, packed=False, _enum_path='BotMetricsEntryPoint'),
        'threadOrigin': FieldDescriptor('threadOrigin', 3, "enum", repeated=False, packed=False, _enum_path='BotMetricsThreadEntryPoint'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotModeSelectionMetadata(MessageBase):
    class BotUserSelectionMode(enum.IntEnum):
        UNKNOWN_MODE = 0
        REASONING_MODE = 1
    FIELDS = {
        'mode': FieldDescriptor('mode', 1, "enum", repeated=True, packed=False, _enum_path='BotModeSelectionMetadata.BotUserSelectionMode'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotModelMetadata(MessageBase):
    class ModelType(enum.IntEnum):
        UNKNOWN_TYPE = 0
        LLAMA_PROD = 1
        LLAMA_PROD_PREMIUM = 2
    class PremiumModelStatus(enum.IntEnum):
        UNKNOWN_STATUS = 0
        AVAILABLE = 1
        QUOTA_EXCEED_LIMIT = 2
    FIELDS = {
        'modelType': FieldDescriptor('modelType', 1, "enum", repeated=False, packed=False, _enum_path='BotModelMetadata.ModelType'),
        'premiumModelStatus': FieldDescriptor('premiumModelStatus', 2, "enum", repeated=False, packed=False, _enum_path='BotModelMetadata.PremiumModelStatus'),
        'modelNameOverride': FieldDescriptor('modelNameOverride', 3, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotPluginMetadata(MessageBase):
    class PluginType(enum.IntEnum):
        UNKNOWN_PLUGIN = 0
        REELS = 1
        SEARCH = 2
    class SearchProvider(enum.IntEnum):
        UNKNOWN = 0
        BING = 1
        GOOGLE = 2
        SUPPORT = 3
    FIELDS = {
        'provider': FieldDescriptor('provider', 1, "enum", repeated=False, packed=False, _enum_path='BotPluginMetadata.SearchProvider'),
        'pluginType': FieldDescriptor('pluginType', 2, "enum", repeated=False, packed=False, _enum_path='BotPluginMetadata.PluginType'),
        'thumbnailCdnUrl': FieldDescriptor('thumbnailCdnUrl', 3, 'string', repeated=False, packed=False),
        'profilePhotoCdnUrl': FieldDescriptor('profilePhotoCdnUrl', 4, 'string', repeated=False, packed=False),
        'searchProviderUrl': FieldDescriptor('searchProviderUrl', 5, 'string', repeated=False, packed=False),
        'referenceIndex': FieldDescriptor('referenceIndex', 6, 'uint32', repeated=False, packed=False),
        'expectedLinksCount': FieldDescriptor('expectedLinksCount', 7, 'uint32', repeated=False, packed=False),
        'searchQuery': FieldDescriptor('searchQuery', 9, 'string', repeated=False, packed=False),
        'parentPluginMessageKey': FieldDescriptor('parentPluginMessageKey', 10, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'deprecatedField': FieldDescriptor('deprecatedField', 11, "enum", repeated=False, packed=False, _enum_path='BotPluginMetadata.PluginType'),
        'parentPluginType': FieldDescriptor('parentPluginType', 12, "enum", repeated=False, packed=False, _enum_path='BotPluginMetadata.PluginType'),
        'faviconCdnUrl': FieldDescriptor('faviconCdnUrl', 13, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotProgressIndicatorMetadata(MessageBase):
    class BotPlanningStepMetadata(MessageBase):
        class BotSearchSourceProvider(enum.IntEnum):
            UNKNOWN_PROVIDER = 0
            OTHER = 1
            GOOGLE = 2
            BING = 3
        class PlanningStepStatus(enum.IntEnum):
            UNKNOWN = 0
            PLANNED = 1
            EXECUTING = 2
            FINISHED = 3
        class BotPlanningSearchSourceMetadata(MessageBase):
            FIELDS = {
                'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
                'provider': FieldDescriptor('provider', 2, "enum", repeated=False, packed=False, _enum_path='BotProgressIndicatorMetadata.BotPlanningStepMetadata.BotSearchSourceProvider'),
                'sourceUrl': FieldDescriptor('sourceUrl', 3, 'string', repeated=False, packed=False),
                'favIconUrl': FieldDescriptor('favIconUrl', 4, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class BotPlanningSearchSourcesMetadata(MessageBase):
            class BotPlanningSearchSourceProvider(enum.IntEnum):
                UNKNOWN = 0
                OTHER = 1
                GOOGLE = 2
                BING = 3
            FIELDS = {
                'sourceTitle': FieldDescriptor('sourceTitle', 1, 'string', repeated=False, packed=False),
                'provider': FieldDescriptor('provider', 2, "enum", repeated=False, packed=False, _enum_path='BotProgressIndicatorMetadata.BotPlanningStepMetadata.BotPlanningSearchSourcesMetadata.BotPlanningSearchSourceProvider'),
                'sourceUrl': FieldDescriptor('sourceUrl', 3, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class BotPlanningStepSectionMetadata(MessageBase):
            FIELDS = {
                'sectionTitle': FieldDescriptor('sectionTitle', 1, 'string', repeated=False, packed=False),
                'sectionBody': FieldDescriptor('sectionBody', 2, 'string', repeated=False, packed=False),
                'sourcesMetadata': FieldDescriptor('sourcesMetadata', 3, "message", repeated=True, packed=False, _msg_path='BotProgressIndicatorMetadata.BotPlanningStepMetadata.BotPlanningSearchSourceMetadata'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'statusTitle': FieldDescriptor('statusTitle', 1, 'string', repeated=False, packed=False),
            'statusBody': FieldDescriptor('statusBody', 2, 'string', repeated=False, packed=False),
            'sourcesMetadata': FieldDescriptor('sourcesMetadata', 3, "message", repeated=True, packed=False, _msg_path='BotProgressIndicatorMetadata.BotPlanningStepMetadata.BotPlanningSearchSourcesMetadata'),
            'status': FieldDescriptor('status', 4, "enum", repeated=False, packed=False, _enum_path='BotProgressIndicatorMetadata.BotPlanningStepMetadata.PlanningStepStatus'),
            'isReasoning': FieldDescriptor('isReasoning', 5, 'bool', repeated=False, packed=False),
            'isEnhancedSearch': FieldDescriptor('isEnhancedSearch', 6, 'bool', repeated=False, packed=False),
            'sections': FieldDescriptor('sections', 7, "message", repeated=True, packed=False, _msg_path='BotProgressIndicatorMetadata.BotPlanningStepMetadata.BotPlanningStepSectionMetadata'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'progressDescription': FieldDescriptor('progressDescription', 1, 'string', repeated=False, packed=False),
        'stepsMetadata': FieldDescriptor('stepsMetadata', 2, "message", repeated=True, packed=False, _msg_path='BotProgressIndicatorMetadata.BotPlanningStepMetadata'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotPromotionMessageMetadata(MessageBase):
    class BotPromotionType(enum.IntEnum):
        UNKNOWN_TYPE = 0
        C50 = 1
        SURVEY_PLATFORM = 2
    FIELDS = {
        'promotionType': FieldDescriptor('promotionType', 1, "enum", repeated=False, packed=False, _enum_path='BotPromotionMessageMetadata.BotPromotionType'),
        'buttonTitle': FieldDescriptor('buttonTitle', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotPromptSuggestion(MessageBase):
    FIELDS = {
        'prompt': FieldDescriptor('prompt', 1, 'string', repeated=False, packed=False),
        'promptId': FieldDescriptor('promptId', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotPromptSuggestions(MessageBase):
    FIELDS = {
        'suggestions': FieldDescriptor('suggestions', 1, "message", repeated=True, packed=False, _msg_path='BotPromptSuggestion'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotQuotaMetadata(MessageBase):
    class BotFeatureQuotaMetadata(MessageBase):
        class BotFeatureType(enum.IntEnum):
            UNKNOWN_FEATURE = 0
            REASONING_FEATURE = 1
        FIELDS = {
            'featureType': FieldDescriptor('featureType', 1, "enum", repeated=False, packed=False, _enum_path='BotQuotaMetadata.BotFeatureQuotaMetadata.BotFeatureType'),
            'remainingQuota': FieldDescriptor('remainingQuota', 2, 'uint32', repeated=False, packed=False),
            'expirationTimestamp': FieldDescriptor('expirationTimestamp', 3, 'uint64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'botFeatureQuotaMetadata': FieldDescriptor('botFeatureQuotaMetadata', 1, "message", repeated=True, packed=False, _msg_path='BotQuotaMetadata.BotFeatureQuotaMetadata'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotReminderMetadata(MessageBase):
    class ReminderAction(enum.IntEnum):
        NOTIFY = 1
        CREATE = 2
        DELETE = 3
        UPDATE = 4
    class ReminderFrequency(enum.IntEnum):
        ONCE = 1
        DAILY = 2
        WEEKLY = 3
        BIWEEKLY = 4
        MONTHLY = 5
    FIELDS = {
        'requestMessageKey': FieldDescriptor('requestMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'action': FieldDescriptor('action', 2, "enum", repeated=False, packed=False, _enum_path='BotReminderMetadata.ReminderAction'),
        'name': FieldDescriptor('name', 3, 'string', repeated=False, packed=False),
        'nextTriggerTimestamp': FieldDescriptor('nextTriggerTimestamp', 4, 'uint64', repeated=False, packed=False),
        'frequency': FieldDescriptor('frequency', 5, "enum", repeated=False, packed=False, _enum_path='BotReminderMetadata.ReminderFrequency'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotRenderingMetadata(MessageBase):
    class Keyword(MessageBase):
        FIELDS = {
            'value': FieldDescriptor('value', 1, 'string', repeated=False, packed=False),
            'associatedPrompts': FieldDescriptor('associatedPrompts', 2, 'string', repeated=True, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'keywords': FieldDescriptor('keywords', 1, "message", repeated=True, packed=False, _msg_path='BotRenderingMetadata.Keyword'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotSessionMetadata(MessageBase):
    FIELDS = {
        'sessionId': FieldDescriptor('sessionId', 1, 'string', repeated=False, packed=False),
        'sessionSource': FieldDescriptor('sessionSource', 2, "enum", repeated=False, packed=False, _enum_path='BotSessionSource'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotSignatureVerificationMetadata(MessageBase):
    FIELDS = {
        'proofs': FieldDescriptor('proofs', 1, "message", repeated=True, packed=False, _msg_path='BotSignatureVerificationUseCaseProof'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotSignatureVerificationUseCaseProof(MessageBase):
    class BotSignatureUseCase(enum.IntEnum):
        UNSPECIFIED = 0
        WA_BOT_MSG = 1
    FIELDS = {
        'version': FieldDescriptor('version', 1, 'int32', repeated=False, packed=False),
        'useCase': FieldDescriptor('useCase', 2, "enum", repeated=False, packed=False, _enum_path='BotSignatureVerificationUseCaseProof.BotSignatureUseCase'),
        'signature': FieldDescriptor('signature', 3, 'bytes', repeated=False, packed=False),
        'certificateChain': FieldDescriptor('certificateChain', 4, 'bytes', repeated=True, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotSourcesMetadata(MessageBase):
    class BotSourceItem(MessageBase):
        class SourceProvider(enum.IntEnum):
            UNKNOWN = 0
            BING = 1
            GOOGLE = 2
            SUPPORT = 3
            OTHER = 4
        FIELDS = {
            'provider': FieldDescriptor('provider', 1, "enum", repeated=False, packed=False, _enum_path='BotSourcesMetadata.BotSourceItem.SourceProvider'),
            'thumbnailCdnUrl': FieldDescriptor('thumbnailCdnUrl', 2, 'string', repeated=False, packed=False),
            'sourceProviderUrl': FieldDescriptor('sourceProviderUrl', 3, 'string', repeated=False, packed=False),
            'sourceQuery': FieldDescriptor('sourceQuery', 4, 'string', repeated=False, packed=False),
            'faviconCdnUrl': FieldDescriptor('faviconCdnUrl', 5, 'string', repeated=False, packed=False),
            'citationNumber': FieldDescriptor('citationNumber', 6, 'uint32', repeated=False, packed=False),
            'sourceTitle': FieldDescriptor('sourceTitle', 7, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'sources': FieldDescriptor('sources', 1, "message", repeated=True, packed=False, _msg_path='BotSourcesMetadata.BotSourceItem'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotSuggestedPromptMetadata(MessageBase):
    FIELDS = {
        'suggestedPrompts': FieldDescriptor('suggestedPrompts', 1, 'string', repeated=True, packed=False),
        'selectedPromptIndex': FieldDescriptor('selectedPromptIndex', 2, 'uint32', repeated=False, packed=False),
        'promptSuggestions': FieldDescriptor('promptSuggestions', 3, "message", repeated=False, packed=False, _msg_path='BotPromptSuggestions'),
        'selectedPromptId': FieldDescriptor('selectedPromptId', 4, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class BotUnifiedResponseMutation(MessageBase):
    class MediaDetailsMetadata(MessageBase):
        FIELDS = {
            'id': FieldDescriptor('id', 1, 'string', repeated=False, packed=False),
            'highResMedia': FieldDescriptor('highResMedia', 2, "message", repeated=False, packed=False, _msg_path='BotMediaMetadata'),
            'previewMedia': FieldDescriptor('previewMedia', 3, "message", repeated=False, packed=False, _msg_path='BotMediaMetadata'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class SideBySideMetadata(MessageBase):
        FIELDS = {
            'primaryResponseId': FieldDescriptor('primaryResponseId', 1, 'string', repeated=False, packed=False),
            'surveyCtaHasRendered': FieldDescriptor('surveyCtaHasRendered', 2, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'sbsMetadata': FieldDescriptor('sbsMetadata', 1, "message", repeated=False, packed=False, _msg_path='BotUnifiedResponseMutation.SideBySideMetadata'),
        'mediaDetailsMetadataList': FieldDescriptor('mediaDetailsMetadataList', 2, "message", repeated=True, packed=False, _msg_path='BotUnifiedResponseMutation.MediaDetailsMetadata'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class CallLogRecord(MessageBase):
    class CallResult(enum.IntEnum):
        CONNECTED = 0
        REJECTED = 1
        CANCELLED = 2
        ACCEPTEDELSEWHERE = 3
        MISSED = 4
        INVALID = 5
        UNAVAILABLE = 6
        UPCOMING = 7
        FAILED = 8
        ABANDONED = 9
        ONGOING = 10
    class CallType(enum.IntEnum):
        REGULAR = 0
        SCHEDULED_CALL = 1
        VOICE_CHAT = 2
    class SilenceReason(enum.IntEnum):
        NONE = 0
        SCHEDULED = 1
        PRIVACY = 2
        LIGHTWEIGHT = 3
    class ParticipantInfo(MessageBase):
        FIELDS = {
            'userJid': FieldDescriptor('userJid', 1, 'string', repeated=False, packed=False),
            'callResult': FieldDescriptor('callResult', 2, "enum", repeated=False, packed=False, _enum_path='CallLogRecord.CallResult'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'callResult': FieldDescriptor('callResult', 1, "enum", repeated=False, packed=False, _enum_path='CallLogRecord.CallResult'),
        'isDndMode': FieldDescriptor('isDndMode', 2, 'bool', repeated=False, packed=False),
        'silenceReason': FieldDescriptor('silenceReason', 3, "enum", repeated=False, packed=False, _enum_path='CallLogRecord.SilenceReason'),
        'duration': FieldDescriptor('duration', 4, 'int64', repeated=False, packed=False),
        'startTime': FieldDescriptor('startTime', 5, 'int64', repeated=False, packed=False),
        'isIncoming': FieldDescriptor('isIncoming', 6, 'bool', repeated=False, packed=False),
        'isVideo': FieldDescriptor('isVideo', 7, 'bool', repeated=False, packed=False),
        'isCallLink': FieldDescriptor('isCallLink', 8, 'bool', repeated=False, packed=False),
        'callLinkToken': FieldDescriptor('callLinkToken', 9, 'string', repeated=False, packed=False),
        'scheduledCallId': FieldDescriptor('scheduledCallId', 10, 'string', repeated=False, packed=False),
        'callId': FieldDescriptor('callId', 11, 'string', repeated=False, packed=False),
        'callCreatorJid': FieldDescriptor('callCreatorJid', 12, 'string', repeated=False, packed=False),
        'groupJid': FieldDescriptor('groupJid', 13, 'string', repeated=False, packed=False),
        'participants': FieldDescriptor('participants', 14, "message", repeated=True, packed=False, _msg_path='CallLogRecord.ParticipantInfo'),
        'callType': FieldDescriptor('callType', 15, "enum", repeated=False, packed=False, _enum_path='CallLogRecord.CallType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class CertChain(MessageBase):
    class NoiseCertificate(MessageBase):
        class Details(MessageBase):
            FIELDS = {
                'serial': FieldDescriptor('serial', 1, 'uint32', repeated=False, packed=False),
                'issuerSerial': FieldDescriptor('issuerSerial', 2, 'uint32', repeated=False, packed=False),
                'key': FieldDescriptor('key', 3, 'bytes', repeated=False, packed=False),
                'notBefore': FieldDescriptor('notBefore', 4, 'uint64', repeated=False, packed=False),
                'notAfter': FieldDescriptor('notAfter', 5, 'uint64', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'details': FieldDescriptor('details', 1, 'bytes', repeated=False, packed=False),
            'signature': FieldDescriptor('signature', 2, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'leaf': FieldDescriptor('leaf', 1, "message", repeated=False, packed=False, _msg_path='CertChain.NoiseCertificate'),
        'intermediate': FieldDescriptor('intermediate', 2, "message", repeated=False, packed=False, _msg_path='CertChain.NoiseCertificate'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ChatLockSettings(MessageBase):
    FIELDS = {
        'hideLockedChats': FieldDescriptor('hideLockedChats', 1, 'bool', repeated=False, packed=False),
        'secretCode': FieldDescriptor('secretCode', 2, "message", repeated=False, packed=False, _msg_path='UserPassword'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ChatRowOpaqueData(MessageBase):
    class DraftMessage(MessageBase):
        class CtwaContextData(MessageBase):
            class ContextInfoExternalAdReplyInfoMediaType(enum.IntEnum):
                NONE = 0
                IMAGE = 1
                VIDEO = 2
            FIELDS = {
                'conversionSource': FieldDescriptor('conversionSource', 1, 'string', repeated=False, packed=False),
                'conversionData': FieldDescriptor('conversionData', 2, 'bytes', repeated=False, packed=False),
                'sourceUrl': FieldDescriptor('sourceUrl', 3, 'string', repeated=False, packed=False),
                'sourceId': FieldDescriptor('sourceId', 4, 'string', repeated=False, packed=False),
                'sourceType': FieldDescriptor('sourceType', 5, 'string', repeated=False, packed=False),
                'title': FieldDescriptor('title', 6, 'string', repeated=False, packed=False),
                'description': FieldDescriptor('description', 7, 'string', repeated=False, packed=False),
                'thumbnail': FieldDescriptor('thumbnail', 8, 'string', repeated=False, packed=False),
                'thumbnailUrl': FieldDescriptor('thumbnailUrl', 9, 'string', repeated=False, packed=False),
                'mediaType': FieldDescriptor('mediaType', 10, "enum", repeated=False, packed=False, _enum_path='ChatRowOpaqueData.DraftMessage.CtwaContextData.ContextInfoExternalAdReplyInfoMediaType'),
                'mediaUrl': FieldDescriptor('mediaUrl', 11, 'string', repeated=False, packed=False),
                'isSuspiciousLink': FieldDescriptor('isSuspiciousLink', 12, 'bool', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class CtwaContextLinkData(MessageBase):
            FIELDS = {
                'context': FieldDescriptor('context', 1, 'string', repeated=False, packed=False),
                'sourceUrl': FieldDescriptor('sourceUrl', 2, 'string', repeated=False, packed=False),
                'icebreaker': FieldDescriptor('icebreaker', 3, 'string', repeated=False, packed=False),
                'phone': FieldDescriptor('phone', 4, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'text': FieldDescriptor('text', 1, 'string', repeated=False, packed=False),
            'omittedUrl': FieldDescriptor('omittedUrl', 2, 'string', repeated=False, packed=False),
            'ctwaContextLinkData': FieldDescriptor('ctwaContextLinkData', 3, "message", repeated=False, packed=False, _msg_path='ChatRowOpaqueData.DraftMessage.CtwaContextLinkData'),
            'ctwaContext': FieldDescriptor('ctwaContext', 4, "message", repeated=False, packed=False, _msg_path='ChatRowOpaqueData.DraftMessage.CtwaContextData'),
            'timestamp': FieldDescriptor('timestamp', 5, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'draftMessage': FieldDescriptor('draftMessage', 1, "message", repeated=False, packed=False, _msg_path='ChatRowOpaqueData.DraftMessage'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Citation(MessageBase):
    FIELDS = {
        'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
        'subtitle': FieldDescriptor('subtitle', 2, 'string', repeated=False, packed=False),
        'cmsId': FieldDescriptor('cmsId', 3, 'string', repeated=False, packed=False),
        'imageUrl': FieldDescriptor('imageUrl', 4, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ClientPairingProps(MessageBase):
    FIELDS = {
        'isChatDbLidMigrated': FieldDescriptor('isChatDbLidMigrated', 1, 'bool', repeated=False, packed=False),
        'isSyncdPureLidSession': FieldDescriptor('isSyncdPureLidSession', 2, 'bool', repeated=False, packed=False),
        'isSyncdSnapshotRecoveryEnabled': FieldDescriptor('isSyncdSnapshotRecoveryEnabled', 3, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ClientPayload(MessageBase):
    class AccountType(enum.IntEnum):
        DEFAULT = 0
        GUEST = 1
    class ConnectReason(enum.IntEnum):
        PUSH = 0
        USER_ACTIVATED = 1
        SCHEDULED = 2
        ERROR_RECONNECT = 3
        NETWORK_SWITCH = 4
        PING_RECONNECT = 5
        UNKNOWN = 6
    class ConnectType(enum.IntEnum):
        CELLULAR_UNKNOWN = 0
        WIFI_UNKNOWN = 1
        CELLULAR_EDGE = 100
        CELLULAR_IDEN = 101
        CELLULAR_UMTS = 102
        CELLULAR_EVDO = 103
        CELLULAR_GPRS = 104
        CELLULAR_HSDPA = 105
        CELLULAR_HSUPA = 106
        CELLULAR_HSPA = 107
        CELLULAR_CDMA = 108
        CELLULAR_1XRTT = 109
        CELLULAR_EHRPD = 110
        CELLULAR_LTE = 111
        CELLULAR_HSPAP = 112
    class IOSAppExtension(enum.IntEnum):
        SHARE_EXTENSION = 0
        SERVICE_EXTENSION = 1
        INTENTS_EXTENSION = 2
    class Product(enum.IntEnum):
        WHATSAPP = 0
        MESSENGER = 1
        INTEROP = 2
        INTEROP_MSGR = 3
        WHATSAPP_LID = 4
    class TrafficAnonymization(enum.IntEnum):
        OFF = 0
        STANDARD = 1
    class DNSSource(MessageBase):
        class DNSResolutionMethod(enum.IntEnum):
            SYSTEM = 0
            GOOGLE = 1
            HARDCODED = 2
            OVERRIDE = 3
            FALLBACK = 4
            MNS = 5
        FIELDS = {
            'dnsMethod': FieldDescriptor('dnsMethod', 15, "enum", repeated=False, packed=False, _enum_path='ClientPayload.DNSSource.DNSResolutionMethod'),
            'appCached': FieldDescriptor('appCached', 16, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class DevicePairingRegistrationData(MessageBase):
        FIELDS = {
            'eRegid': FieldDescriptor('eRegid', 1, 'bytes', repeated=False, packed=False),
            'eKeytype': FieldDescriptor('eKeytype', 2, 'bytes', repeated=False, packed=False),
            'eIdent': FieldDescriptor('eIdent', 3, 'bytes', repeated=False, packed=False),
            'eSkeyId': FieldDescriptor('eSkeyId', 4, 'bytes', repeated=False, packed=False),
            'eSkeyVal': FieldDescriptor('eSkeyVal', 5, 'bytes', repeated=False, packed=False),
            'eSkeySig': FieldDescriptor('eSkeySig', 6, 'bytes', repeated=False, packed=False),
            'buildHash': FieldDescriptor('buildHash', 7, 'bytes', repeated=False, packed=False),
            'deviceProps': FieldDescriptor('deviceProps', 8, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class InteropData(MessageBase):
        FIELDS = {
            'accountId': FieldDescriptor('accountId', 1, 'uint64', repeated=False, packed=False),
            'token': FieldDescriptor('token', 2, 'bytes', repeated=False, packed=False),
            'enableReadReceipts': FieldDescriptor('enableReadReceipts', 3, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class UserAgent(MessageBase):
        class DeviceType(enum.IntEnum):
            PHONE = 0
            TABLET = 1
            DESKTOP = 2
            WEARABLE = 3
            VR = 4
        class Platform(enum.IntEnum):
            ANDROID = 0
            IOS = 1
            WINDOWS_PHONE = 2
            BLACKBERRY = 3
            BLACKBERRYX = 4
            S40 = 5
            S60 = 6
            PYTHON_CLIENT = 7
            TIZEN = 8
            ENTERPRISE = 9
            SMB_ANDROID = 10
            KAIOS = 11
            SMB_IOS = 12
            WINDOWS = 13
            WEB = 14
            PORTAL = 15
            GREEN_ANDROID = 16
            GREEN_IPHONE = 17
            BLUE_ANDROID = 18
            BLUE_IPHONE = 19
            FBLITE_ANDROID = 20
            MLITE_ANDROID = 21
            IGLITE_ANDROID = 22
            PAGE = 23
            MACOS = 24
            OCULUS_MSG = 25
            OCULUS_CALL = 26
            MILAN = 27
            CAPI = 28
            WEAROS = 29
            ARDEVICE = 30
            VRDEVICE = 31
            BLUE_WEB = 32
            IPAD = 33
            TEST = 34
            SMART_GLASSES = 35
            BLUE_VR = 36
            AR_WRIST = 37
        class ReleaseChannel(enum.IntEnum):
            RELEASE = 0
            BETA = 1
            ALPHA = 2
            DEBUG = 3
        class AppVersion(MessageBase):
            FIELDS = {
                'primary': FieldDescriptor('primary', 1, 'uint32', repeated=False, packed=False),
                'secondary': FieldDescriptor('secondary', 2, 'uint32', repeated=False, packed=False),
                'tertiary': FieldDescriptor('tertiary', 3, 'uint32', repeated=False, packed=False),
                'quaternary': FieldDescriptor('quaternary', 4, 'uint32', repeated=False, packed=False),
                'quinary': FieldDescriptor('quinary', 5, 'uint32', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'platform': FieldDescriptor('platform', 1, "enum", repeated=False, packed=False, _enum_path='ClientPayload.UserAgent.Platform'),
            'appVersion': FieldDescriptor('appVersion', 2, "message", repeated=False, packed=False, _msg_path='ClientPayload.UserAgent.AppVersion'),
            'mcc': FieldDescriptor('mcc', 3, 'string', repeated=False, packed=False),
            'mnc': FieldDescriptor('mnc', 4, 'string', repeated=False, packed=False),
            'osVersion': FieldDescriptor('osVersion', 5, 'string', repeated=False, packed=False),
            'manufacturer': FieldDescriptor('manufacturer', 6, 'string', repeated=False, packed=False),
            'device': FieldDescriptor('device', 7, 'string', repeated=False, packed=False),
            'osBuildNumber': FieldDescriptor('osBuildNumber', 8, 'string', repeated=False, packed=False),
            'phoneId': FieldDescriptor('phoneId', 9, 'string', repeated=False, packed=False),
            'releaseChannel': FieldDescriptor('releaseChannel', 10, "enum", repeated=False, packed=False, _enum_path='ClientPayload.UserAgent.ReleaseChannel'),
            'localeLanguageIso6391': FieldDescriptor('localeLanguageIso6391', 11, 'string', repeated=False, packed=False),
            'localeCountryIso31661Alpha2': FieldDescriptor('localeCountryIso31661Alpha2', 12, 'string', repeated=False, packed=False),
            'deviceBoard': FieldDescriptor('deviceBoard', 13, 'string', repeated=False, packed=False),
            'deviceExpId': FieldDescriptor('deviceExpId', 14, 'string', repeated=False, packed=False),
            'deviceType': FieldDescriptor('deviceType', 15, "enum", repeated=False, packed=False, _enum_path='ClientPayload.UserAgent.DeviceType'),
            'deviceModelType': FieldDescriptor('deviceModelType', 16, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class WebInfo(MessageBase):
        class WebSubPlatform(enum.IntEnum):
            WEB_BROWSER = 0
            APP_STORE = 1
            WIN_STORE = 2
            DARWIN = 3
            WIN32 = 4
            WIN_HYBRID = 5
        class WebdPayload(MessageBase):
            FIELDS = {
                'usesParticipantInKey': FieldDescriptor('usesParticipantInKey', 1, 'bool', repeated=False, packed=False),
                'supportsStarredMessages': FieldDescriptor('supportsStarredMessages', 2, 'bool', repeated=False, packed=False),
                'supportsDocumentMessages': FieldDescriptor('supportsDocumentMessages', 3, 'bool', repeated=False, packed=False),
                'supportsUrlMessages': FieldDescriptor('supportsUrlMessages', 4, 'bool', repeated=False, packed=False),
                'supportsMediaRetry': FieldDescriptor('supportsMediaRetry', 5, 'bool', repeated=False, packed=False),
                'supportsE2EImage': FieldDescriptor('supportsE2EImage', 6, 'bool', repeated=False, packed=False),
                'supportsE2EVideo': FieldDescriptor('supportsE2EVideo', 7, 'bool', repeated=False, packed=False),
                'supportsE2EAudio': FieldDescriptor('supportsE2EAudio', 8, 'bool', repeated=False, packed=False),
                'supportsE2EDocument': FieldDescriptor('supportsE2EDocument', 9, 'bool', repeated=False, packed=False),
                'documentTypes': FieldDescriptor('documentTypes', 10, 'string', repeated=False, packed=False),
                'features': FieldDescriptor('features', 11, 'bytes', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'refToken': FieldDescriptor('refToken', 1, 'string', repeated=False, packed=False),
            'version': FieldDescriptor('version', 2, 'string', repeated=False, packed=False),
            'webdPayload': FieldDescriptor('webdPayload', 3, "message", repeated=False, packed=False, _msg_path='ClientPayload.WebInfo.WebdPayload'),
            'webSubPlatform': FieldDescriptor('webSubPlatform', 4, "enum", repeated=False, packed=False, _enum_path='ClientPayload.WebInfo.WebSubPlatform'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'username': FieldDescriptor('username', 1, 'uint64', repeated=False, packed=False),
        'passive': FieldDescriptor('passive', 3, 'bool', repeated=False, packed=False),
        'userAgent': FieldDescriptor('userAgent', 5, "message", repeated=False, packed=False, _msg_path='ClientPayload.UserAgent'),
        'webInfo': FieldDescriptor('webInfo', 6, "message", repeated=False, packed=False, _msg_path='ClientPayload.WebInfo'),
        'pushName': FieldDescriptor('pushName', 7, 'string', repeated=False, packed=False),
        'sessionId': FieldDescriptor('sessionId', 9, 'sfixed32', repeated=False, packed=False),
        'shortConnect': FieldDescriptor('shortConnect', 10, 'bool', repeated=False, packed=False),
        'connectType': FieldDescriptor('connectType', 12, "enum", repeated=False, packed=False, _enum_path='ClientPayload.ConnectType'),
        'connectReason': FieldDescriptor('connectReason', 13, "enum", repeated=False, packed=False, _enum_path='ClientPayload.ConnectReason'),
        'shards': FieldDescriptor('shards', 14, 'int32', repeated=True, packed=False),
        'dnsSource': FieldDescriptor('dnsSource', 15, "message", repeated=False, packed=False, _msg_path='ClientPayload.DNSSource'),
        'connectAttemptCount': FieldDescriptor('connectAttemptCount', 16, 'uint32', repeated=False, packed=False),
        'device': FieldDescriptor('device', 18, 'uint32', repeated=False, packed=False),
        'devicePairingData': FieldDescriptor('devicePairingData', 19, "message", repeated=False, packed=False, _msg_path='ClientPayload.DevicePairingRegistrationData'),
        'product': FieldDescriptor('product', 20, "enum", repeated=False, packed=False, _enum_path='ClientPayload.Product'),
        'fbCat': FieldDescriptor('fbCat', 21, 'bytes', repeated=False, packed=False),
        'fbUserAgent': FieldDescriptor('fbUserAgent', 22, 'bytes', repeated=False, packed=False),
        'oc': FieldDescriptor('oc', 23, 'bool', repeated=False, packed=False),
        'lc': FieldDescriptor('lc', 24, 'int32', repeated=False, packed=False),
        'iosAppExtension': FieldDescriptor('iosAppExtension', 30, "enum", repeated=False, packed=False, _enum_path='ClientPayload.IOSAppExtension'),
        'fbAppId': FieldDescriptor('fbAppId', 31, 'uint64', repeated=False, packed=False),
        'fbDeviceId': FieldDescriptor('fbDeviceId', 32, 'bytes', repeated=False, packed=False),
        'pull': FieldDescriptor('pull', 33, 'bool', repeated=False, packed=False),
        'paddingBytes': FieldDescriptor('paddingBytes', 34, 'bytes', repeated=False, packed=False),
        'yearClass': FieldDescriptor('yearClass', 36, 'int32', repeated=False, packed=False),
        'memClass': FieldDescriptor('memClass', 37, 'int32', repeated=False, packed=False),
        'interopData': FieldDescriptor('interopData', 38, "message", repeated=False, packed=False, _msg_path='ClientPayload.InteropData'),
        'trafficAnonymization': FieldDescriptor('trafficAnonymization', 40, "enum", repeated=False, packed=False, _enum_path='ClientPayload.TrafficAnonymization'),
        'lidDbMigrated': FieldDescriptor('lidDbMigrated', 41, 'bool', repeated=False, packed=False),
        'accountType': FieldDescriptor('accountType', 42, "enum", repeated=False, packed=False, _enum_path='ClientPayload.AccountType'),
        'connectionSequenceInfo': FieldDescriptor('connectionSequenceInfo', 43, 'sfixed32', repeated=False, packed=False),
        'paaLink': FieldDescriptor('paaLink', 44, 'bool', repeated=False, packed=False),
        'preacksCount': FieldDescriptor('preacksCount', 45, 'int32', repeated=False, packed=False),
        'processingQueueSize': FieldDescriptor('processingQueueSize', 46, 'int32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class CommentMetadata(MessageBase):
    FIELDS = {
        'commentParentKey': FieldDescriptor('commentParentKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'replyCount': FieldDescriptor('replyCount', 2, 'uint32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class CompanionCommitment(MessageBase):
    FIELDS = {
        'hash': FieldDescriptor('hash', 1, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class CompanionEphemeralIdentity(MessageBase):
    FIELDS = {
        'publicKey': FieldDescriptor('publicKey', 1, 'bytes', repeated=False, packed=False),
        'deviceType': FieldDescriptor('deviceType', 2, "enum", repeated=False, packed=False, _enum_path='DeviceProps.PlatformType'),
        'ref': FieldDescriptor('ref', 3, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Config(MessageBase):
    FIELDS = {
        'field': FieldDescriptor('field', 1, "map", repeated=True, map_key_type='uint32', map_value=FieldDescriptor("value", 2, "message", _msg_path='Field')),
        'version': FieldDescriptor('version', 2, 'uint32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ContextInfo(MessageBase):
    class ForwardOrigin(enum.IntEnum):
        UNKNOWN = 0
        CHAT = 1
        STATUS = 2
        CHANNELS = 3
        META_AI = 4
        UGC = 5
    class PairedMediaType(enum.IntEnum):
        NOT_PAIRED_MEDIA = 0
        SD_VIDEO_PARENT = 1
        HD_VIDEO_CHILD = 2
        SD_IMAGE_PARENT = 3
        HD_IMAGE_CHILD = 4
        MOTION_PHOTO_PARENT = 5
        MOTION_PHOTO_CHILD = 6
        HEVC_VIDEO_PARENT = 7
        HEVC_VIDEO_CHILD = 8
    class QuotedType(enum.IntEnum):
        EXPLICIT = 0
        AUTO = 1
    class StatusAttributionType(enum.IntEnum):
        NONE = 0
        RESHARED_FROM_MENTION = 1
        RESHARED_FROM_POST = 2
        RESHARED_FROM_POST_MANY_TIMES = 3
        FORWARDED_FROM_STATUS = 4
    class StatusSourceType(enum.IntEnum):
        IMAGE = 0
        VIDEO = 1
        GIF = 2
        AUDIO = 3
        TEXT = 4
        MUSIC_STANDALONE = 5
    class AdReplyInfo(MessageBase):
        class MediaType(enum.IntEnum):
            NONE = 0
            IMAGE = 1
            VIDEO = 2
        FIELDS = {
            'advertiserName': FieldDescriptor('advertiserName', 1, 'string', repeated=False, packed=False),
            'mediaType': FieldDescriptor('mediaType', 2, "enum", repeated=False, packed=False, _enum_path='ContextInfo.AdReplyInfo.MediaType'),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 16, 'bytes', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 17, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class BusinessMessageForwardInfo(MessageBase):
        FIELDS = {
            'businessOwnerJid': FieldDescriptor('businessOwnerJid', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class DataSharingContext(MessageBase):
        class DataSharingFlags(enum.IntEnum):
            SHOW_MM_DISCLOSURE_ON_CLICK = 1
            SHOW_MM_DISCLOSURE_ON_READ = 2
        class Parameters(MessageBase):
            FIELDS = {
                'key': FieldDescriptor('key', 1, 'string', repeated=False, packed=False),
                'stringData': FieldDescriptor('stringData', 2, 'string', repeated=False, packed=False),
                'intData': FieldDescriptor('intData', 3, 'int64', repeated=False, packed=False),
                'floatData': FieldDescriptor('floatData', 4, 'float', repeated=False, packed=False),
                'contents': FieldDescriptor('contents', 5, "message", repeated=False, packed=False, _msg_path='ContextInfo.DataSharingContext.Parameters'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'showMmDisclosure': FieldDescriptor('showMmDisclosure', 1, 'bool', repeated=False, packed=False),
            'encryptedSignalTokenConsented': FieldDescriptor('encryptedSignalTokenConsented', 2, 'string', repeated=False, packed=False),
            'parameters': FieldDescriptor('parameters', 3, "message", repeated=True, packed=False, _msg_path='ContextInfo.DataSharingContext.Parameters'),
            'dataSharingFlags': FieldDescriptor('dataSharingFlags', 4, 'int32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ExternalAdReplyInfo(MessageBase):
        class AdType(enum.IntEnum):
            CTWA = 0
            CAWC = 1
        class MediaType(enum.IntEnum):
            NONE = 0
            IMAGE = 1
            VIDEO = 2
        FIELDS = {
            'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
            'body': FieldDescriptor('body', 2, 'string', repeated=False, packed=False),
            'mediaType': FieldDescriptor('mediaType', 3, "enum", repeated=False, packed=False, _enum_path='ContextInfo.ExternalAdReplyInfo.MediaType'),
            'thumbnailUrl': FieldDescriptor('thumbnailUrl', 4, 'string', repeated=False, packed=False),
            'mediaUrl': FieldDescriptor('mediaUrl', 5, 'string', repeated=False, packed=False),
            'thumbnail': FieldDescriptor('thumbnail', 6, 'bytes', repeated=False, packed=False),
            'sourceType': FieldDescriptor('sourceType', 7, 'string', repeated=False, packed=False),
            'sourceId': FieldDescriptor('sourceId', 8, 'string', repeated=False, packed=False),
            'sourceUrl': FieldDescriptor('sourceUrl', 9, 'string', repeated=False, packed=False),
            'containsAutoReply': FieldDescriptor('containsAutoReply', 10, 'bool', repeated=False, packed=False),
            'renderLargerThumbnail': FieldDescriptor('renderLargerThumbnail', 11, 'bool', repeated=False, packed=False),
            'showAdAttribution': FieldDescriptor('showAdAttribution', 12, 'bool', repeated=False, packed=False),
            'ctwaClid': FieldDescriptor('ctwaClid', 13, 'string', repeated=False, packed=False),
            'ref': FieldDescriptor('ref', 14, 'string', repeated=False, packed=False),
            'clickToWhatsappCall': FieldDescriptor('clickToWhatsappCall', 15, 'bool', repeated=False, packed=False),
            'adContextPreviewDismissed': FieldDescriptor('adContextPreviewDismissed', 16, 'bool', repeated=False, packed=False),
            'sourceApp': FieldDescriptor('sourceApp', 17, 'string', repeated=False, packed=False),
            'automatedGreetingMessageShown': FieldDescriptor('automatedGreetingMessageShown', 18, 'bool', repeated=False, packed=False),
            'greetingMessageBody': FieldDescriptor('greetingMessageBody', 19, 'string', repeated=False, packed=False),
            'ctaPayload': FieldDescriptor('ctaPayload', 20, 'string', repeated=False, packed=False),
            'disableNudge': FieldDescriptor('disableNudge', 21, 'bool', repeated=False, packed=False),
            'originalImageUrl': FieldDescriptor('originalImageUrl', 22, 'string', repeated=False, packed=False),
            'automatedGreetingMessageCtaType': FieldDescriptor('automatedGreetingMessageCtaType', 23, 'string', repeated=False, packed=False),
            'wtwaAdFormat': FieldDescriptor('wtwaAdFormat', 24, 'bool', repeated=False, packed=False),
            'adType': FieldDescriptor('adType', 25, "enum", repeated=False, packed=False, _enum_path='ContextInfo.ExternalAdReplyInfo.AdType'),
            'wtwaWebsiteUrl': FieldDescriptor('wtwaWebsiteUrl', 26, 'string', repeated=False, packed=False),
            'adPreviewUrl': FieldDescriptor('adPreviewUrl', 27, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class FeatureEligibilities(MessageBase):
        FIELDS = {
            'cannotBeReactedTo': FieldDescriptor('cannotBeReactedTo', 1, 'bool', repeated=False, packed=False),
            'cannotBeRanked': FieldDescriptor('cannotBeRanked', 2, 'bool', repeated=False, packed=False),
            'canRequestFeedback': FieldDescriptor('canRequestFeedback', 3, 'bool', repeated=False, packed=False),
            'canBeReshared': FieldDescriptor('canBeReshared', 4, 'bool', repeated=False, packed=False),
            'canReceiveMultiReact': FieldDescriptor('canReceiveMultiReact', 5, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ForwardedNewsletterMessageInfo(MessageBase):
        class ContentType(enum.IntEnum):
            UPDATE = 1
            UPDATE_CARD = 2
            LINK_CARD = 3
        FIELDS = {
            'newsletterJid': FieldDescriptor('newsletterJid', 1, 'string', repeated=False, packed=False),
            'serverMessageId': FieldDescriptor('serverMessageId', 2, 'int32', repeated=False, packed=False),
            'newsletterName': FieldDescriptor('newsletterName', 3, 'string', repeated=False, packed=False),
            'contentType': FieldDescriptor('contentType', 4, "enum", repeated=False, packed=False, _enum_path='ContextInfo.ForwardedNewsletterMessageInfo.ContentType'),
            'accessibilityText': FieldDescriptor('accessibilityText', 5, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class QuestionReplyQuotedMessage(MessageBase):
        FIELDS = {
            'serverQuestionId': FieldDescriptor('serverQuestionId', 1, 'int32', repeated=False, packed=False),
            'quotedQuestion': FieldDescriptor('quotedQuestion', 2, "message", repeated=False, packed=False, _msg_path='Message'),
            'quotedResponse': FieldDescriptor('quotedResponse', 3, "message", repeated=False, packed=False, _msg_path='Message'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StatusAudienceMetadata(MessageBase):
        class AudienceType(enum.IntEnum):
            UNKNOWN = 0
            CLOSE_FRIENDS = 1
        FIELDS = {
            'audienceType': FieldDescriptor('audienceType', 1, "enum", repeated=False, packed=False, _enum_path='ContextInfo.StatusAudienceMetadata.AudienceType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class UTMInfo(MessageBase):
        FIELDS = {
            'utmSource': FieldDescriptor('utmSource', 1, 'string', repeated=False, packed=False),
            'utmCampaign': FieldDescriptor('utmCampaign', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'stanzaId': FieldDescriptor('stanzaId', 1, 'string', repeated=False, packed=False),
        'participant': FieldDescriptor('participant', 2, 'string', repeated=False, packed=False),
        'quotedMessage': FieldDescriptor('quotedMessage', 3, "message", repeated=False, packed=False, _msg_path='Message'),
        'remoteJid': FieldDescriptor('remoteJid', 4, 'string', repeated=False, packed=False),
        'mentionedJid': FieldDescriptor('mentionedJid', 15, 'string', repeated=True, packed=False),
        'conversionSource': FieldDescriptor('conversionSource', 18, 'string', repeated=False, packed=False),
        'conversionData': FieldDescriptor('conversionData', 19, 'bytes', repeated=False, packed=False),
        'conversionDelaySeconds': FieldDescriptor('conversionDelaySeconds', 20, 'uint32', repeated=False, packed=False),
        'forwardingScore': FieldDescriptor('forwardingScore', 21, 'uint32', repeated=False, packed=False),
        'isForwarded': FieldDescriptor('isForwarded', 22, 'bool', repeated=False, packed=False),
        'quotedAd': FieldDescriptor('quotedAd', 23, "message", repeated=False, packed=False, _msg_path='ContextInfo.AdReplyInfo'),
        'placeholderKey': FieldDescriptor('placeholderKey', 24, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'expiration': FieldDescriptor('expiration', 25, 'uint32', repeated=False, packed=False),
        'ephemeralSettingTimestamp': FieldDescriptor('ephemeralSettingTimestamp', 26, 'int64', repeated=False, packed=False),
        'ephemeralSharedSecret': FieldDescriptor('ephemeralSharedSecret', 27, 'bytes', repeated=False, packed=False),
        'externalAdReply': FieldDescriptor('externalAdReply', 28, "message", repeated=False, packed=False, _msg_path='ContextInfo.ExternalAdReplyInfo'),
        'entryPointConversionSource': FieldDescriptor('entryPointConversionSource', 29, 'string', repeated=False, packed=False),
        'entryPointConversionApp': FieldDescriptor('entryPointConversionApp', 30, 'string', repeated=False, packed=False),
        'entryPointConversionDelaySeconds': FieldDescriptor('entryPointConversionDelaySeconds', 31, 'uint32', repeated=False, packed=False),
        'disappearingMode': FieldDescriptor('disappearingMode', 32, "message", repeated=False, packed=False, _msg_path='DisappearingMode'),
        'actionLink': FieldDescriptor('actionLink', 33, "message", repeated=False, packed=False, _msg_path='ActionLink'),
        'groupSubject': FieldDescriptor('groupSubject', 34, 'string', repeated=False, packed=False),
        'parentGroupJid': FieldDescriptor('parentGroupJid', 35, 'string', repeated=False, packed=False),
        'trustBannerType': FieldDescriptor('trustBannerType', 37, 'string', repeated=False, packed=False),
        'trustBannerAction': FieldDescriptor('trustBannerAction', 38, 'uint32', repeated=False, packed=False),
        'isSampled': FieldDescriptor('isSampled', 39, 'bool', repeated=False, packed=False),
        'groupMentions': FieldDescriptor('groupMentions', 40, "message", repeated=True, packed=False, _msg_path='GroupMention'),
        'utm': FieldDescriptor('utm', 41, "message", repeated=False, packed=False, _msg_path='ContextInfo.UTMInfo'),
        'forwardedNewsletterMessageInfo': FieldDescriptor('forwardedNewsletterMessageInfo', 43, "message", repeated=False, packed=False, _msg_path='ContextInfo.ForwardedNewsletterMessageInfo'),
        'businessMessageForwardInfo': FieldDescriptor('businessMessageForwardInfo', 44, "message", repeated=False, packed=False, _msg_path='ContextInfo.BusinessMessageForwardInfo'),
        'smbClientCampaignId': FieldDescriptor('smbClientCampaignId', 45, 'string', repeated=False, packed=False),
        'smbServerCampaignId': FieldDescriptor('smbServerCampaignId', 46, 'string', repeated=False, packed=False),
        'dataSharingContext': FieldDescriptor('dataSharingContext', 47, "message", repeated=False, packed=False, _msg_path='ContextInfo.DataSharingContext'),
        'alwaysShowAdAttribution': FieldDescriptor('alwaysShowAdAttribution', 48, 'bool', repeated=False, packed=False),
        'featureEligibilities': FieldDescriptor('featureEligibilities', 49, "message", repeated=False, packed=False, _msg_path='ContextInfo.FeatureEligibilities'),
        'entryPointConversionExternalSource': FieldDescriptor('entryPointConversionExternalSource', 50, 'string', repeated=False, packed=False),
        'entryPointConversionExternalMedium': FieldDescriptor('entryPointConversionExternalMedium', 51, 'string', repeated=False, packed=False),
        'ctwaSignals': FieldDescriptor('ctwaSignals', 54, 'string', repeated=False, packed=False),
        'ctwaPayload': FieldDescriptor('ctwaPayload', 55, 'bytes', repeated=False, packed=False),
        'forwardedAiBotMessageInfo': FieldDescriptor('forwardedAiBotMessageInfo', 56, "message", repeated=False, packed=False, _msg_path='ForwardedAIBotMessageInfo'),
        'statusAttributionType': FieldDescriptor('statusAttributionType', 57, "enum", repeated=False, packed=False, _enum_path='ContextInfo.StatusAttributionType'),
        'urlTrackingMap': FieldDescriptor('urlTrackingMap', 58, "message", repeated=False, packed=False, _msg_path='UrlTrackingMap'),
        'pairedMediaType': FieldDescriptor('pairedMediaType', 59, "enum", repeated=False, packed=False, _enum_path='ContextInfo.PairedMediaType'),
        'rankingVersion': FieldDescriptor('rankingVersion', 60, 'uint32', repeated=False, packed=False),
        'memberLabel': FieldDescriptor('memberLabel', 62, "message", repeated=False, packed=False, _msg_path='MemberLabel'),
        'isQuestion': FieldDescriptor('isQuestion', 63, 'bool', repeated=False, packed=False),
        'statusSourceType': FieldDescriptor('statusSourceType', 64, "enum", repeated=False, packed=False, _enum_path='ContextInfo.StatusSourceType'),
        'statusAttributions': FieldDescriptor('statusAttributions', 65, "message", repeated=True, packed=False, _msg_path='StatusAttribution'),
        'isGroupStatus': FieldDescriptor('isGroupStatus', 66, 'bool', repeated=False, packed=False),
        'forwardOrigin': FieldDescriptor('forwardOrigin', 67, "enum", repeated=False, packed=False, _enum_path='ContextInfo.ForwardOrigin'),
        'questionReplyQuotedMessage': FieldDescriptor('questionReplyQuotedMessage', 68, "message", repeated=False, packed=False, _msg_path='ContextInfo.QuestionReplyQuotedMessage'),
        'statusAudienceMetadata': FieldDescriptor('statusAudienceMetadata', 69, "message", repeated=False, packed=False, _msg_path='ContextInfo.StatusAudienceMetadata'),
        'nonJidMentions': FieldDescriptor('nonJidMentions', 70, 'uint32', repeated=False, packed=False),
        'quotedType': FieldDescriptor('quotedType', 71, "enum", repeated=False, packed=False, _enum_path='ContextInfo.QuotedType'),
        'botMessageSharingInfo': FieldDescriptor('botMessageSharingInfo', 72, "message", repeated=False, packed=False, _msg_path='BotMessageSharingInfo'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Conversation(MessageBase):
    class EndOfHistoryTransferType(enum.IntEnum):
        COMPLETE_BUT_MORE_MESSAGES_REMAIN_ON_PRIMARY = 0
        COMPLETE_AND_NO_MORE_MESSAGE_REMAIN_ON_PRIMARY = 1
        COMPLETE_ON_DEMAND_SYNC_BUT_MORE_MSG_REMAIN_ON_PRIMARY = 2
    FIELDS = {
        'id': FieldDescriptor('id', 1, 'string', repeated=False, packed=False),
        'messages': FieldDescriptor('messages', 2, "message", repeated=True, packed=False, _msg_path='HistorySyncMsg'),
        'newJid': FieldDescriptor('newJid', 3, 'string', repeated=False, packed=False),
        'oldJid': FieldDescriptor('oldJid', 4, 'string', repeated=False, packed=False),
        'lastMsgTimestamp': FieldDescriptor('lastMsgTimestamp', 5, 'uint64', repeated=False, packed=False),
        'unreadCount': FieldDescriptor('unreadCount', 6, 'uint32', repeated=False, packed=False),
        'readOnly': FieldDescriptor('readOnly', 7, 'bool', repeated=False, packed=False),
        'endOfHistoryTransfer': FieldDescriptor('endOfHistoryTransfer', 8, 'bool', repeated=False, packed=False),
        'ephemeralExpiration': FieldDescriptor('ephemeralExpiration', 9, 'uint32', repeated=False, packed=False),
        'ephemeralSettingTimestamp': FieldDescriptor('ephemeralSettingTimestamp', 10, 'int64', repeated=False, packed=False),
        'endOfHistoryTransferType': FieldDescriptor('endOfHistoryTransferType', 11, "enum", repeated=False, packed=False, _enum_path='Conversation.EndOfHistoryTransferType'),
        'conversationTimestamp': FieldDescriptor('conversationTimestamp', 12, 'uint64', repeated=False, packed=False),
        'name': FieldDescriptor('name', 13, 'string', repeated=False, packed=False),
        'pHash': FieldDescriptor('pHash', 14, 'string', repeated=False, packed=False),
        'notSpam': FieldDescriptor('notSpam', 15, 'bool', repeated=False, packed=False),
        'archived': FieldDescriptor('archived', 16, 'bool', repeated=False, packed=False),
        'disappearingMode': FieldDescriptor('disappearingMode', 17, "message", repeated=False, packed=False, _msg_path='DisappearingMode'),
        'unreadMentionCount': FieldDescriptor('unreadMentionCount', 18, 'uint32', repeated=False, packed=False),
        'markedAsUnread': FieldDescriptor('markedAsUnread', 19, 'bool', repeated=False, packed=False),
        'participant': FieldDescriptor('participant', 20, "message", repeated=True, packed=False, _msg_path='GroupParticipant'),
        'tcToken': FieldDescriptor('tcToken', 21, 'bytes', repeated=False, packed=False),
        'tcTokenTimestamp': FieldDescriptor('tcTokenTimestamp', 22, 'uint64', repeated=False, packed=False),
        'contactPrimaryIdentityKey': FieldDescriptor('contactPrimaryIdentityKey', 23, 'bytes', repeated=False, packed=False),
        'pinned': FieldDescriptor('pinned', 24, 'uint32', repeated=False, packed=False),
        'muteEndTime': FieldDescriptor('muteEndTime', 25, 'uint64', repeated=False, packed=False),
        'wallpaper': FieldDescriptor('wallpaper', 26, "message", repeated=False, packed=False, _msg_path='WallpaperSettings'),
        'mediaVisibility': FieldDescriptor('mediaVisibility', 27, "enum", repeated=False, packed=False, _enum_path='MediaVisibility'),
        'tcTokenSenderTimestamp': FieldDescriptor('tcTokenSenderTimestamp', 28, 'uint64', repeated=False, packed=False),
        'suspended': FieldDescriptor('suspended', 29, 'bool', repeated=False, packed=False),
        'terminated': FieldDescriptor('terminated', 30, 'bool', repeated=False, packed=False),
        'createdAt': FieldDescriptor('createdAt', 31, 'uint64', repeated=False, packed=False),
        'createdBy': FieldDescriptor('createdBy', 32, 'string', repeated=False, packed=False),
        'description': FieldDescriptor('description', 33, 'string', repeated=False, packed=False),
        'support': FieldDescriptor('support', 34, 'bool', repeated=False, packed=False),
        'isParentGroup': FieldDescriptor('isParentGroup', 35, 'bool', repeated=False, packed=False),
        'parentGroupId': FieldDescriptor('parentGroupId', 37, 'string', repeated=False, packed=False),
        'isDefaultSubgroup': FieldDescriptor('isDefaultSubgroup', 36, 'bool', repeated=False, packed=False),
        'displayName': FieldDescriptor('displayName', 38, 'string', repeated=False, packed=False),
        'pnJid': FieldDescriptor('pnJid', 39, 'string', repeated=False, packed=False),
        'shareOwnPn': FieldDescriptor('shareOwnPn', 40, 'bool', repeated=False, packed=False),
        'pnhDuplicateLidThread': FieldDescriptor('pnhDuplicateLidThread', 41, 'bool', repeated=False, packed=False),
        'lidJid': FieldDescriptor('lidJid', 42, 'string', repeated=False, packed=False),
        'username': FieldDescriptor('username', 43, 'string', repeated=False, packed=False),
        'lidOriginType': FieldDescriptor('lidOriginType', 44, 'string', repeated=False, packed=False),
        'commentsCount': FieldDescriptor('commentsCount', 45, 'uint32', repeated=False, packed=False),
        'locked': FieldDescriptor('locked', 46, 'bool', repeated=False, packed=False),
        'systemMessageToInsert': FieldDescriptor('systemMessageToInsert', 47, "enum", repeated=False, packed=False, _enum_path='PrivacySystemMessage'),
        'capiCreatedGroup': FieldDescriptor('capiCreatedGroup', 48, 'bool', repeated=False, packed=False),
        'accountLid': FieldDescriptor('accountLid', 49, 'string', repeated=False, packed=False),
        'limitSharing': FieldDescriptor('limitSharing', 50, 'bool', repeated=False, packed=False),
        'limitSharingSettingTimestamp': FieldDescriptor('limitSharingSettingTimestamp', 51, 'int64', repeated=False, packed=False),
        'limitSharingTrigger': FieldDescriptor('limitSharingTrigger', 52, "enum", repeated=False, packed=False, _enum_path='LimitSharing.TriggerType'),
        'limitSharingInitiatedByMe': FieldDescriptor('limitSharingInitiatedByMe', 53, 'bool', repeated=False, packed=False),
        'maibaAiThreadEnabled': FieldDescriptor('maibaAiThreadEnabled', 54, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class DeviceCapabilities(MessageBase):
    class ChatLockSupportLevel(enum.IntEnum):
        NONE = 0
        MINIMAL = 1
        FULL = 2
    class MemberNameTagPrimarySupport(enum.IntEnum):
        DISABLED = 0
        RECEIVER_ENABLED = 1
        SENDER_ENABLED = 2
    class BusinessBroadcast(MessageBase):
        FIELDS = {
            'importListEnabled': FieldDescriptor('importListEnabled', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LIDMigration(MessageBase):
        FIELDS = {
            'chatDbMigrationTimestamp': FieldDescriptor('chatDbMigrationTimestamp', 1, 'uint64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class UserHasAvatar(MessageBase):
        FIELDS = {
            'userHasAvatar': FieldDescriptor('userHasAvatar', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'chatLockSupportLevel': FieldDescriptor('chatLockSupportLevel', 1, "enum", repeated=False, packed=False, _enum_path='DeviceCapabilities.ChatLockSupportLevel'),
        'lidMigration': FieldDescriptor('lidMigration', 2, "message", repeated=False, packed=False, _msg_path='DeviceCapabilities.LIDMigration'),
        'businessBroadcast': FieldDescriptor('businessBroadcast', 3, "message", repeated=False, packed=False, _msg_path='DeviceCapabilities.BusinessBroadcast'),
        'userHasAvatar': FieldDescriptor('userHasAvatar', 4, "message", repeated=False, packed=False, _msg_path='DeviceCapabilities.UserHasAvatar'),
        'memberNameTagPrimarySupport': FieldDescriptor('memberNameTagPrimarySupport', 5, "enum", repeated=False, packed=False, _enum_path='DeviceCapabilities.MemberNameTagPrimarySupport'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class DeviceConsistencyCodeMessage(MessageBase):
    FIELDS = {
        'generation': FieldDescriptor('generation', 1, 'uint32', repeated=False, packed=False),
        'signature': FieldDescriptor('signature', 2, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class DeviceListMetadata(MessageBase):
    FIELDS = {
        'senderKeyHash': FieldDescriptor('senderKeyHash', 1, 'bytes', repeated=False, packed=False),
        'senderTimestamp': FieldDescriptor('senderTimestamp', 2, 'uint64', repeated=False, packed=False),
        'senderKeyIndexes': FieldDescriptor('senderKeyIndexes', 3, 'uint32', repeated=True, packed=True),
        'senderAccountType': FieldDescriptor('senderAccountType', 4, "enum", repeated=False, packed=False, _enum_path='ADVEncryptionType'),
        'receiverAccountType': FieldDescriptor('receiverAccountType', 5, "enum", repeated=False, packed=False, _enum_path='ADVEncryptionType'),
        'recipientKeyHash': FieldDescriptor('recipientKeyHash', 8, 'bytes', repeated=False, packed=False),
        'recipientTimestamp': FieldDescriptor('recipientTimestamp', 9, 'uint64', repeated=False, packed=False),
        'recipientKeyIndexes': FieldDescriptor('recipientKeyIndexes', 10, 'uint32', repeated=True, packed=True),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class DeviceProps(MessageBase):
    class PlatformType(enum.IntEnum):
        UNKNOWN = 0
        CHROME = 1
        FIREFOX = 2
        IE = 3
        OPERA = 4
        SAFARI = 5
        EDGE = 6
        DESKTOP = 7
        IPAD = 8
        ANDROID_TABLET = 9
        OHANA = 10
        ALOHA = 11
        CATALINA = 12
        TCL_TV = 13
        IOS_PHONE = 14
        IOS_CATALYST = 15
        ANDROID_PHONE = 16
        ANDROID_AMBIGUOUS = 17
        WEAR_OS = 18
        AR_WRIST = 19
        AR_DEVICE = 20
        UWP = 21
        VR = 22
        CLOUD_API = 23
        SMARTGLASSES = 24
    class AppVersion(MessageBase):
        FIELDS = {
            'primary': FieldDescriptor('primary', 1, 'uint32', repeated=False, packed=False),
            'secondary': FieldDescriptor('secondary', 2, 'uint32', repeated=False, packed=False),
            'tertiary': FieldDescriptor('tertiary', 3, 'uint32', repeated=False, packed=False),
            'quaternary': FieldDescriptor('quaternary', 4, 'uint32', repeated=False, packed=False),
            'quinary': FieldDescriptor('quinary', 5, 'uint32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class HistorySyncConfig(MessageBase):
        FIELDS = {
            'fullSyncDaysLimit': FieldDescriptor('fullSyncDaysLimit', 1, 'uint32', repeated=False, packed=False),
            'fullSyncSizeMbLimit': FieldDescriptor('fullSyncSizeMbLimit', 2, 'uint32', repeated=False, packed=False),
            'storageQuotaMb': FieldDescriptor('storageQuotaMb', 3, 'uint32', repeated=False, packed=False),
            'inlineInitialPayloadInE2EeMsg': FieldDescriptor('inlineInitialPayloadInE2EeMsg', 4, 'bool', repeated=False, packed=False),
            'recentSyncDaysLimit': FieldDescriptor('recentSyncDaysLimit', 5, 'uint32', repeated=False, packed=False),
            'supportCallLogHistory': FieldDescriptor('supportCallLogHistory', 6, 'bool', repeated=False, packed=False),
            'supportBotUserAgentChatHistory': FieldDescriptor('supportBotUserAgentChatHistory', 7, 'bool', repeated=False, packed=False),
            'supportCagReactionsAndPolls': FieldDescriptor('supportCagReactionsAndPolls', 8, 'bool', repeated=False, packed=False),
            'supportBizHostedMsg': FieldDescriptor('supportBizHostedMsg', 9, 'bool', repeated=False, packed=False),
            'supportRecentSyncChunkMessageCountTuning': FieldDescriptor('supportRecentSyncChunkMessageCountTuning', 10, 'bool', repeated=False, packed=False),
            'supportHostedGroupMsg': FieldDescriptor('supportHostedGroupMsg', 11, 'bool', repeated=False, packed=False),
            'supportFbidBotChatHistory': FieldDescriptor('supportFbidBotChatHistory', 12, 'bool', repeated=False, packed=False),
            'supportAddOnHistorySyncMigration': FieldDescriptor('supportAddOnHistorySyncMigration', 13, 'bool', repeated=False, packed=False),
            'supportMessageAssociation': FieldDescriptor('supportMessageAssociation', 14, 'bool', repeated=False, packed=False),
            'supportGroupHistory': FieldDescriptor('supportGroupHistory', 15, 'bool', repeated=False, packed=False),
            'onDemandReady': FieldDescriptor('onDemandReady', 16, 'bool', repeated=False, packed=False),
            'supportGuestChat': FieldDescriptor('supportGuestChat', 17, 'bool', repeated=False, packed=False),
            'completeOnDemandReady': FieldDescriptor('completeOnDemandReady', 18, 'bool', repeated=False, packed=False),
            'thumbnailSyncDaysLimit': FieldDescriptor('thumbnailSyncDaysLimit', 19, 'uint32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'os': FieldDescriptor('os', 1, 'string', repeated=False, packed=False),
        'version': FieldDescriptor('version', 2, "message", repeated=False, packed=False, _msg_path='DeviceProps.AppVersion'),
        'platformType': FieldDescriptor('platformType', 3, "enum", repeated=False, packed=False, _enum_path='DeviceProps.PlatformType'),
        'requireFullSync': FieldDescriptor('requireFullSync', 4, 'bool', repeated=False, packed=False),
        'historySyncConfig': FieldDescriptor('historySyncConfig', 5, "message", repeated=False, packed=False, _msg_path='DeviceProps.HistorySyncConfig'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class DisappearingMode(MessageBase):
    class Initiator(enum.IntEnum):
        CHANGED_IN_CHAT = 0
        INITIATED_BY_ME = 1
        INITIATED_BY_OTHER = 2
        BIZ_UPGRADE_FB_HOSTING = 3
    class Trigger(enum.IntEnum):
        UNKNOWN = 0
        CHAT_SETTING = 1
        ACCOUNT_SETTING = 2
        BULK_CHANGE = 3
        BIZ_SUPPORTS_FB_HOSTING = 4
        UNKNOWN_GROUPS = 5
    FIELDS = {
        'initiator': FieldDescriptor('initiator', 1, "enum", repeated=False, packed=False, _enum_path='DisappearingMode.Initiator'),
        'trigger': FieldDescriptor('trigger', 2, "enum", repeated=False, packed=False, _enum_path='DisappearingMode.Trigger'),
        'initiatorDeviceJid': FieldDescriptor('initiatorDeviceJid', 3, 'string', repeated=False, packed=False),
        'initiatedByMe': FieldDescriptor('initiatedByMe', 4, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class EmbeddedContent(MessageBase):
    FIELDS = {
        'embeddedMessage': FieldDescriptor('embeddedMessage', 1, "message", repeated=False, packed=False, _msg_path='EmbeddedMessage'),
        'embeddedMusic': FieldDescriptor('embeddedMusic', 2, "message", repeated=False, packed=False, _msg_path='EmbeddedMusic'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class EmbeddedMessage(MessageBase):
    FIELDS = {
        'stanzaId': FieldDescriptor('stanzaId', 1, 'string', repeated=False, packed=False),
        'message': FieldDescriptor('message', 2, "message", repeated=False, packed=False, _msg_path='Message'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class EmbeddedMusic(MessageBase):
    FIELDS = {
        'musicContentMediaId': FieldDescriptor('musicContentMediaId', 1, 'string', repeated=False, packed=False),
        'songId': FieldDescriptor('songId', 2, 'string', repeated=False, packed=False),
        'author': FieldDescriptor('author', 3, 'string', repeated=False, packed=False),
        'title': FieldDescriptor('title', 4, 'string', repeated=False, packed=False),
        'artworkDirectPath': FieldDescriptor('artworkDirectPath', 5, 'string', repeated=False, packed=False),
        'artworkSha256': FieldDescriptor('artworkSha256', 6, 'bytes', repeated=False, packed=False),
        'artworkEncSha256': FieldDescriptor('artworkEncSha256', 7, 'bytes', repeated=False, packed=False),
        'artistAttribution': FieldDescriptor('artistAttribution', 8, 'string', repeated=False, packed=False),
        'countryBlocklist': FieldDescriptor('countryBlocklist', 9, 'bytes', repeated=False, packed=False),
        'isExplicit': FieldDescriptor('isExplicit', 10, 'bool', repeated=False, packed=False),
        'artworkMediaKey': FieldDescriptor('artworkMediaKey', 11, 'bytes', repeated=False, packed=False),
        'musicSongStartTimeInMs': FieldDescriptor('musicSongStartTimeInMs', 12, 'int64', repeated=False, packed=False),
        'derivedContentStartTimeInMs': FieldDescriptor('derivedContentStartTimeInMs', 13, 'int64', repeated=False, packed=False),
        'overlapDurationInMs': FieldDescriptor('overlapDurationInMs', 14, 'int64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class EncryptedPairingRequest(MessageBase):
    FIELDS = {
        'encryptedPayload': FieldDescriptor('encryptedPayload', 1, 'bytes', repeated=False, packed=False),
        'iv': FieldDescriptor('iv', 2, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class EphemeralSetting(MessageBase):
    FIELDS = {
        'duration': FieldDescriptor('duration', 1, 'sfixed32', repeated=False, packed=False),
        'timestamp': FieldDescriptor('timestamp', 2, 'sfixed64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class EventAdditionalMetadata(MessageBase):
    FIELDS = {
        'isStale': FieldDescriptor('isStale', 1, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class EventResponse(MessageBase):
    FIELDS = {
        'eventResponseMessageKey': FieldDescriptor('eventResponseMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'timestampMs': FieldDescriptor('timestampMs', 2, 'int64', repeated=False, packed=False),
        'eventResponseMessage': FieldDescriptor('eventResponseMessage', 3, "message", repeated=False, packed=False, _msg_path='Message.EventResponseMessage'),
        'unread': FieldDescriptor('unread', 4, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ExitCode(MessageBase):
    FIELDS = {
        'code': FieldDescriptor('code', 1, 'uint64', repeated=False, packed=False),
        'text': FieldDescriptor('text', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ExternalBlobReference(MessageBase):
    FIELDS = {
        'mediaKey': FieldDescriptor('mediaKey', 1, 'bytes', repeated=False, packed=False),
        'directPath': FieldDescriptor('directPath', 2, 'string', repeated=False, packed=False),
        'handle': FieldDescriptor('handle', 3, 'string', repeated=False, packed=False),
        'fileSizeBytes': FieldDescriptor('fileSizeBytes', 4, 'uint64', repeated=False, packed=False),
        'fileSha256': FieldDescriptor('fileSha256', 5, 'bytes', repeated=False, packed=False),
        'fileEncSha256': FieldDescriptor('fileEncSha256', 6, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Field(MessageBase):
    FIELDS = {
        'minVersion': FieldDescriptor('minVersion', 1, 'uint32', repeated=False, packed=False),
        'maxVersion': FieldDescriptor('maxVersion', 2, 'uint32', repeated=False, packed=False),
        'notReportableMinVersion': FieldDescriptor('notReportableMinVersion', 3, 'uint32', repeated=False, packed=False),
        'isMessage': FieldDescriptor('isMessage', 4, 'bool', repeated=False, packed=False),
        'subfield': FieldDescriptor('subfield', 5, "map", repeated=True, map_key_type='uint32', map_value=FieldDescriptor("value", 2, "message", _msg_path='Field')),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ForwardedAIBotMessageInfo(MessageBase):
    FIELDS = {
        'botName': FieldDescriptor('botName', 1, 'string', repeated=False, packed=False),
        'botJid': FieldDescriptor('botJid', 2, 'string', repeated=False, packed=False),
        'creatorName': FieldDescriptor('creatorName', 3, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class GlobalSettings(MessageBase):
    FIELDS = {
        'lightThemeWallpaper': FieldDescriptor('lightThemeWallpaper', 1, "message", repeated=False, packed=False, _msg_path='WallpaperSettings'),
        'mediaVisibility': FieldDescriptor('mediaVisibility', 2, "enum", repeated=False, packed=False, _enum_path='MediaVisibility'),
        'darkThemeWallpaper': FieldDescriptor('darkThemeWallpaper', 3, "message", repeated=False, packed=False, _msg_path='WallpaperSettings'),
        'autoDownloadWiFi': FieldDescriptor('autoDownloadWiFi', 4, "message", repeated=False, packed=False, _msg_path='AutoDownloadSettings'),
        'autoDownloadCellular': FieldDescriptor('autoDownloadCellular', 5, "message", repeated=False, packed=False, _msg_path='AutoDownloadSettings'),
        'autoDownloadRoaming': FieldDescriptor('autoDownloadRoaming', 6, "message", repeated=False, packed=False, _msg_path='AutoDownloadSettings'),
        'showIndividualNotificationsPreview': FieldDescriptor('showIndividualNotificationsPreview', 7, 'bool', repeated=False, packed=False),
        'showGroupNotificationsPreview': FieldDescriptor('showGroupNotificationsPreview', 8, 'bool', repeated=False, packed=False),
        'disappearingModeDuration': FieldDescriptor('disappearingModeDuration', 9, 'int32', repeated=False, packed=False),
        'disappearingModeTimestamp': FieldDescriptor('disappearingModeTimestamp', 10, 'int64', repeated=False, packed=False),
        'avatarUserSettings': FieldDescriptor('avatarUserSettings', 11, "message", repeated=False, packed=False, _msg_path='AvatarUserSettings'),
        'fontSize': FieldDescriptor('fontSize', 12, 'int32', repeated=False, packed=False),
        'securityNotifications': FieldDescriptor('securityNotifications', 13, 'bool', repeated=False, packed=False),
        'autoUnarchiveChats': FieldDescriptor('autoUnarchiveChats', 14, 'bool', repeated=False, packed=False),
        'videoQualityMode': FieldDescriptor('videoQualityMode', 15, 'int32', repeated=False, packed=False),
        'photoQualityMode': FieldDescriptor('photoQualityMode', 16, 'int32', repeated=False, packed=False),
        'individualNotificationSettings': FieldDescriptor('individualNotificationSettings', 17, "message", repeated=False, packed=False, _msg_path='NotificationSettings'),
        'groupNotificationSettings': FieldDescriptor('groupNotificationSettings', 18, "message", repeated=False, packed=False, _msg_path='NotificationSettings'),
        'chatLockSettings': FieldDescriptor('chatLockSettings', 19, "message", repeated=False, packed=False, _msg_path='ChatLockSettings'),
        'chatDbLidMigrationTimestamp': FieldDescriptor('chatDbLidMigrationTimestamp', 20, 'int64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class GroupHistoryBundleInfo(MessageBase):
    class ProcessState(enum.IntEnum):
        NOT_INJECTED = 0
        INJECTED = 1
        INJECTED_PARTIAL = 2
        INJECTION_FAILED = 3
        INJECTION_FAILED_NO_RETRY = 4
    FIELDS = {
        'deprecatedMessageHistoryBundle': FieldDescriptor('deprecatedMessageHistoryBundle', 1, "message", repeated=False, packed=False, _msg_path='Message.MessageHistoryBundle'),
        'processState': FieldDescriptor('processState', 2, "enum", repeated=False, packed=False, _enum_path='GroupHistoryBundleInfo.ProcessState'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class GroupHistoryIndividualMessageInfo(MessageBase):
    FIELDS = {
        'bundleMessageKey': FieldDescriptor('bundleMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'editedAfterReceivedAsHistory': FieldDescriptor('editedAfterReceivedAsHistory', 2, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class GroupMention(MessageBase):
    FIELDS = {
        'groupJid': FieldDescriptor('groupJid', 1, 'string', repeated=False, packed=False),
        'groupSubject': FieldDescriptor('groupSubject', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class GroupParticipant(MessageBase):
    class Rank(enum.IntEnum):
        REGULAR = 0
        ADMIN = 1
        SUPERADMIN = 2
    FIELDS = {
        'userJid': FieldDescriptor('userJid', 1, 'string', repeated=False, packed=False),
        'rank': FieldDescriptor('rank', 2, "enum", repeated=False, packed=False, _enum_path='GroupParticipant.Rank'),
        'memberLabel': FieldDescriptor('memberLabel', 3, "message", repeated=False, packed=False, _msg_path='MemberLabel'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class HandshakeMessage(MessageBase):
    class ClientFinish(MessageBase):
        FIELDS = {
            'static': FieldDescriptor('static', 1, 'bytes', repeated=False, packed=False),
            'payload': FieldDescriptor('payload', 2, 'bytes', repeated=False, packed=False),
            'extendedCiphertext': FieldDescriptor('extendedCiphertext', 3, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ClientHello(MessageBase):
        FIELDS = {
            'ephemeral': FieldDescriptor('ephemeral', 1, 'bytes', repeated=False, packed=False),
            'static': FieldDescriptor('static', 2, 'bytes', repeated=False, packed=False),
            'payload': FieldDescriptor('payload', 3, 'bytes', repeated=False, packed=False),
            'useExtended': FieldDescriptor('useExtended', 4, 'bool', repeated=False, packed=False),
            'extendedCiphertext': FieldDescriptor('extendedCiphertext', 5, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ServerHello(MessageBase):
        FIELDS = {
            'ephemeral': FieldDescriptor('ephemeral', 1, 'bytes', repeated=False, packed=False),
            'static': FieldDescriptor('static', 2, 'bytes', repeated=False, packed=False),
            'payload': FieldDescriptor('payload', 3, 'bytes', repeated=False, packed=False),
            'extendedStatic': FieldDescriptor('extendedStatic', 4, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'clientHello': FieldDescriptor('clientHello', 2, "message", repeated=False, packed=False, _msg_path='HandshakeMessage.ClientHello'),
        'serverHello': FieldDescriptor('serverHello', 3, "message", repeated=False, packed=False, _msg_path='HandshakeMessage.ServerHello'),
        'clientFinish': FieldDescriptor('clientFinish', 4, "message", repeated=False, packed=False, _msg_path='HandshakeMessage.ClientFinish'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class HistorySync(MessageBase):
    class BotAIWaitListState(enum.IntEnum):
        IN_WAITLIST = 0
        AI_AVAILABLE = 1
    class HistorySyncType(enum.IntEnum):
        INITIAL_BOOTSTRAP = 0
        INITIAL_STATUS_V3 = 1
        FULL = 2
        RECENT = 3
        PUSH_NAME = 4
        NON_BLOCKING_DATA = 5
        ON_DEMAND = 6
    FIELDS = {
        'syncType': FieldDescriptor('syncType', 1, "enum", repeated=False, packed=False, _enum_path='HistorySync.HistorySyncType'),
        'conversations': FieldDescriptor('conversations', 2, "message", repeated=True, packed=False, _msg_path='Conversation'),
        'statusV3Messages': FieldDescriptor('statusV3Messages', 3, "message", repeated=True, packed=False, _msg_path='WebMessageInfo'),
        'chunkOrder': FieldDescriptor('chunkOrder', 5, 'uint32', repeated=False, packed=False),
        'progress': FieldDescriptor('progress', 6, 'uint32', repeated=False, packed=False),
        'pushnames': FieldDescriptor('pushnames', 7, "message", repeated=True, packed=False, _msg_path='Pushname'),
        'globalSettings': FieldDescriptor('globalSettings', 8, "message", repeated=False, packed=False, _msg_path='GlobalSettings'),
        'threadIdUserSecret': FieldDescriptor('threadIdUserSecret', 9, 'bytes', repeated=False, packed=False),
        'threadDsTimeframeOffset': FieldDescriptor('threadDsTimeframeOffset', 10, 'uint32', repeated=False, packed=False),
        'recentStickers': FieldDescriptor('recentStickers', 11, "message", repeated=True, packed=False, _msg_path='StickerMetadata'),
        'pastParticipants': FieldDescriptor('pastParticipants', 12, "message", repeated=True, packed=False, _msg_path='PastParticipants'),
        'callLogRecords': FieldDescriptor('callLogRecords', 13, "message", repeated=True, packed=False, _msg_path='CallLogRecord'),
        'aiWaitListState': FieldDescriptor('aiWaitListState', 14, "enum", repeated=False, packed=False, _enum_path='HistorySync.BotAIWaitListState'),
        'phoneNumberToLidMappings': FieldDescriptor('phoneNumberToLidMappings', 15, "message", repeated=True, packed=False, _msg_path='PhoneNumberToLIDMapping'),
        'companionMetaNonce': FieldDescriptor('companionMetaNonce', 16, 'string', repeated=False, packed=False),
        'shareableChatIdentifierEncryptionKey': FieldDescriptor('shareableChatIdentifierEncryptionKey', 17, 'bytes', repeated=False, packed=False),
        'accounts': FieldDescriptor('accounts', 18, "message", repeated=True, packed=False, _msg_path='Account'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class HistorySyncMsg(MessageBase):
    FIELDS = {
        'message': FieldDescriptor('message', 1, "message", repeated=False, packed=False, _msg_path='WebMessageInfo'),
        'msgOrderId': FieldDescriptor('msgOrderId', 2, 'uint64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class HydratedTemplateButton(MessageBase):
    class HydratedCallButton(MessageBase):
        FIELDS = {
            'displayText': FieldDescriptor('displayText', 1, 'string', repeated=False, packed=False),
            'phoneNumber': FieldDescriptor('phoneNumber', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class HydratedQuickReplyButton(MessageBase):
        FIELDS = {
            'displayText': FieldDescriptor('displayText', 1, 'string', repeated=False, packed=False),
            'id': FieldDescriptor('id', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class HydratedURLButton(MessageBase):
        class WebviewPresentationType(enum.IntEnum):
            FULL = 1
            TALL = 2
            COMPACT = 3
        FIELDS = {
            'displayText': FieldDescriptor('displayText', 1, 'string', repeated=False, packed=False),
            'url': FieldDescriptor('url', 2, 'string', repeated=False, packed=False),
            'consentedUsersUrl': FieldDescriptor('consentedUsersUrl', 3, 'string', repeated=False, packed=False),
            'webviewPresentation': FieldDescriptor('webviewPresentation', 4, "enum", repeated=False, packed=False, _enum_path='HydratedTemplateButton.HydratedURLButton.WebviewPresentationType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'index': FieldDescriptor('index', 4, 'uint32', repeated=False, packed=False),
        'quickReplyButton': FieldDescriptor('quickReplyButton', 1, "message", repeated=False, packed=False, _msg_path='HydratedTemplateButton.HydratedQuickReplyButton'),
        'urlButton': FieldDescriptor('urlButton', 2, "message", repeated=False, packed=False, _msg_path='HydratedTemplateButton.HydratedURLButton'),
        'callButton': FieldDescriptor('callButton', 3, "message", repeated=False, packed=False, _msg_path='HydratedTemplateButton.HydratedCallButton'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class IdentityKeyPairStructure(MessageBase):
    FIELDS = {
        'publicKey': FieldDescriptor('publicKey', 1, 'bytes', repeated=False, packed=False),
        'privateKey': FieldDescriptor('privateKey', 2, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class InThreadSurveyMetadata(MessageBase):
    class InThreadSurveyOption(MessageBase):
        FIELDS = {
            'stringValue': FieldDescriptor('stringValue', 1, 'string', repeated=False, packed=False),
            'numericValue': FieldDescriptor('numericValue', 2, 'uint32', repeated=False, packed=False),
            'textTranslated': FieldDescriptor('textTranslated', 3, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class InThreadSurveyPrivacyStatementPart(MessageBase):
        FIELDS = {
            'text': FieldDescriptor('text', 1, 'string', repeated=False, packed=False),
            'url': FieldDescriptor('url', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class InThreadSurveyQuestion(MessageBase):
        FIELDS = {
            'questionText': FieldDescriptor('questionText', 1, 'string', repeated=False, packed=False),
            'questionId': FieldDescriptor('questionId', 2, 'string', repeated=False, packed=False),
            'questionOptions': FieldDescriptor('questionOptions', 3, "message", repeated=True, packed=False, _msg_path='InThreadSurveyMetadata.InThreadSurveyOption'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'tessaSessionId': FieldDescriptor('tessaSessionId', 1, 'string', repeated=False, packed=False),
        'simonSessionId': FieldDescriptor('simonSessionId', 2, 'string', repeated=False, packed=False),
        'simonSurveyId': FieldDescriptor('simonSurveyId', 3, 'string', repeated=False, packed=False),
        'tessaRootId': FieldDescriptor('tessaRootId', 4, 'string', repeated=False, packed=False),
        'requestId': FieldDescriptor('requestId', 5, 'string', repeated=False, packed=False),
        'tessaEvent': FieldDescriptor('tessaEvent', 6, 'string', repeated=False, packed=False),
        'invitationHeaderText': FieldDescriptor('invitationHeaderText', 7, 'string', repeated=False, packed=False),
        'invitationBodyText': FieldDescriptor('invitationBodyText', 8, 'string', repeated=False, packed=False),
        'invitationCtaText': FieldDescriptor('invitationCtaText', 9, 'string', repeated=False, packed=False),
        'invitationCtaUrl': FieldDescriptor('invitationCtaUrl', 10, 'string', repeated=False, packed=False),
        'surveyTitle': FieldDescriptor('surveyTitle', 11, 'string', repeated=False, packed=False),
        'questions': FieldDescriptor('questions', 12, "message", repeated=True, packed=False, _msg_path='InThreadSurveyMetadata.InThreadSurveyQuestion'),
        'surveyContinueButtonText': FieldDescriptor('surveyContinueButtonText', 13, 'string', repeated=False, packed=False),
        'surveySubmitButtonText': FieldDescriptor('surveySubmitButtonText', 14, 'string', repeated=False, packed=False),
        'privacyStatementFull': FieldDescriptor('privacyStatementFull', 15, 'string', repeated=False, packed=False),
        'privacyStatementParts': FieldDescriptor('privacyStatementParts', 16, "message", repeated=True, packed=False, _msg_path='InThreadSurveyMetadata.InThreadSurveyPrivacyStatementPart'),
        'feedbackToastText': FieldDescriptor('feedbackToastText', 17, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class InteractiveAnnotation(MessageBase):
    class StatusLinkType(enum.IntEnum):
        RASTERIZED_LINK_PREVIEW = 1
        RASTERIZED_LINK_TRUNCATED = 2
        RASTERIZED_LINK_FULL_URL = 3
    FIELDS = {
        'polygonVertices': FieldDescriptor('polygonVertices', 1, "message", repeated=True, packed=False, _msg_path='Point'),
        'shouldSkipConfirmation': FieldDescriptor('shouldSkipConfirmation', 4, 'bool', repeated=False, packed=False),
        'embeddedContent': FieldDescriptor('embeddedContent', 5, "message", repeated=False, packed=False, _msg_path='EmbeddedContent'),
        'statusLinkType': FieldDescriptor('statusLinkType', 8, "enum", repeated=False, packed=False, _enum_path='InteractiveAnnotation.StatusLinkType'),
        'location': FieldDescriptor('location', 2, "message", repeated=False, packed=False, _msg_path='Location'),
        'newsletter': FieldDescriptor('newsletter', 3, "message", repeated=False, packed=False, _msg_path='ContextInfo.ForwardedNewsletterMessageInfo'),
        'embeddedAction': FieldDescriptor('embeddedAction', 6, 'bool', repeated=False, packed=False),
        'tapAction': FieldDescriptor('tapAction', 7, "message", repeated=False, packed=False, _msg_path='TapLinkAction'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class InteractiveMessageAdditionalMetadata(MessageBase):
    FIELDS = {
        'isGalaxyFlowCompleted': FieldDescriptor('isGalaxyFlowCompleted', 1, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class KeepInChat(MessageBase):
    FIELDS = {
        'keepType': FieldDescriptor('keepType', 1, "enum", repeated=False, packed=False, _enum_path='KeepType'),
        'serverTimestamp': FieldDescriptor('serverTimestamp', 2, 'int64', repeated=False, packed=False),
        'key': FieldDescriptor('key', 3, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'deviceJid': FieldDescriptor('deviceJid', 4, 'string', repeated=False, packed=False),
        'clientTimestampMs': FieldDescriptor('clientTimestampMs', 5, 'int64', repeated=False, packed=False),
        'serverTimestampMs': FieldDescriptor('serverTimestampMs', 6, 'int64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class KeyExchangeMessage(MessageBase):
    FIELDS = {
        'id': FieldDescriptor('id', 1, 'uint32', repeated=False, packed=False),
        'baseKey': FieldDescriptor('baseKey', 2, 'bytes', repeated=False, packed=False),
        'ratchetKey': FieldDescriptor('ratchetKey', 3, 'bytes', repeated=False, packed=False),
        'identityKey': FieldDescriptor('identityKey', 4, 'bytes', repeated=False, packed=False),
        'baseKeySignature': FieldDescriptor('baseKeySignature', 5, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class KeyId(MessageBase):
    FIELDS = {
        'id': FieldDescriptor('id', 1, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class LIDMigrationMapping(MessageBase):
    FIELDS = {
        'pn': FieldDescriptor('pn', 1, 'uint64', repeated=False, packed=False),
        'assignedLid': FieldDescriptor('assignedLid', 2, 'uint64', repeated=False, packed=False),
        'latestLid': FieldDescriptor('latestLid', 3, 'uint64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class LIDMigrationMappingSyncMessage(MessageBase):
    FIELDS = {
        'encodedMappingPayload': FieldDescriptor('encodedMappingPayload', 1, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class LIDMigrationMappingSyncPayload(MessageBase):
    FIELDS = {
        'pnToLidMappings': FieldDescriptor('pnToLidMappings', 1, "message", repeated=True, packed=False, _msg_path='LIDMigrationMapping'),
        'chatDbMigrationTimestamp': FieldDescriptor('chatDbMigrationTimestamp', 2, 'uint64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class LegacyMessage(MessageBase):
    FIELDS = {
        'eventResponseMessage': FieldDescriptor('eventResponseMessage', 1, "message", repeated=False, packed=False, _msg_path='Message.EventResponseMessage'),
        'pollVote': FieldDescriptor('pollVote', 2, "message", repeated=False, packed=False, _msg_path='Message.PollVoteMessage'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class LimitSharing(MessageBase):
    class TriggerType(enum.IntEnum):
        UNKNOWN = 0
        CHAT_SETTING = 1
        BIZ_SUPPORTS_FB_HOSTING = 2
        UNKNOWN_GROUP = 3
    FIELDS = {
        'sharingLimited': FieldDescriptor('sharingLimited', 1, 'bool', repeated=False, packed=False),
        'trigger': FieldDescriptor('trigger', 2, "enum", repeated=False, packed=False, _enum_path='LimitSharing.TriggerType'),
        'limitSharingSettingTimestamp': FieldDescriptor('limitSharingSettingTimestamp', 3, 'int64', repeated=False, packed=False),
        'initiatedByMe': FieldDescriptor('initiatedByMe', 4, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class LocalizedName(MessageBase):
    FIELDS = {
        'lg': FieldDescriptor('lg', 1, 'string', repeated=False, packed=False),
        'lc': FieldDescriptor('lc', 2, 'string', repeated=False, packed=False),
        'verifiedName': FieldDescriptor('verifiedName', 3, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Location(MessageBase):
    FIELDS = {
        'degreesLatitude': FieldDescriptor('degreesLatitude', 1, 'double', repeated=False, packed=False),
        'degreesLongitude': FieldDescriptor('degreesLongitude', 2, 'double', repeated=False, packed=False),
        'name': FieldDescriptor('name', 3, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MediaData(MessageBase):
    FIELDS = {
        'localPath': FieldDescriptor('localPath', 1, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MediaNotifyMessage(MessageBase):
    FIELDS = {
        'expressPathUrl': FieldDescriptor('expressPathUrl', 1, 'string', repeated=False, packed=False),
        'fileEncSha256': FieldDescriptor('fileEncSha256', 2, 'bytes', repeated=False, packed=False),
        'fileLength': FieldDescriptor('fileLength', 3, 'uint64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MediaRetryNotification(MessageBase):
    class ResultType(enum.IntEnum):
        GENERAL_ERROR = 0
        SUCCESS = 1
        NOT_FOUND = 2
        DECRYPTION_ERROR = 3
    FIELDS = {
        'stanzaId': FieldDescriptor('stanzaId', 1, 'string', repeated=False, packed=False),
        'directPath': FieldDescriptor('directPath', 2, 'string', repeated=False, packed=False),
        'result': FieldDescriptor('result', 3, "enum", repeated=False, packed=False, _enum_path='MediaRetryNotification.ResultType'),
        'messageSecret': FieldDescriptor('messageSecret', 4, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MemberLabel(MessageBase):
    FIELDS = {
        'label': FieldDescriptor('label', 1, 'string', repeated=False, packed=False),
        'labelTimestamp': FieldDescriptor('labelTimestamp', 2, 'int64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Message(MessageBase):
    class HistorySyncType(enum.IntEnum):
        INITIAL_BOOTSTRAP = 0
        INITIAL_STATUS_V3 = 1
        FULL = 2
        RECENT = 3
        PUSH_NAME = 4
        NON_BLOCKING_DATA = 5
        ON_DEMAND = 6
        NO_HISTORY = 7
        MESSAGE_ACCESS_STATUS = 8
    class MediaKeyDomain(enum.IntEnum):
        UNSET = 0
        E2EE_CHAT = 1
        STATUS = 2
        CAPI = 3
        BOT = 4
    class PeerDataOperationRequestType(enum.IntEnum):
        UPLOAD_STICKER = 0
        SEND_RECENT_STICKER_BOOTSTRAP = 1
        GENERATE_LINK_PREVIEW = 2
        HISTORY_SYNC_ON_DEMAND = 3
        PLACEHOLDER_MESSAGE_RESEND = 4
        WAFFLE_LINKING_NONCE_FETCH = 5
        FULL_HISTORY_SYNC_ON_DEMAND = 6
        COMPANION_META_NONCE_FETCH = 7
        COMPANION_SYNCD_SNAPSHOT_FATAL_RECOVERY = 8
        COMPANION_CANONICAL_USER_NONCE_FETCH = 9
        HISTORY_SYNC_CHUNK_RETRY = 10
        GALAXY_FLOW_ACTION = 11
    class PollContentType(enum.IntEnum):
        UNKNOWN = 0
        TEXT = 1
        IMAGE = 2
    class PollType(enum.IntEnum):
        POLL = 0
        QUIZ = 1
    class AlbumMessage(MessageBase):
        FIELDS = {
            'expectedImageCount': FieldDescriptor('expectedImageCount', 2, 'uint32', repeated=False, packed=False),
            'expectedVideoCount': FieldDescriptor('expectedVideoCount', 3, 'uint32', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AppStateFatalExceptionNotification(MessageBase):
        FIELDS = {
            'collectionNames': FieldDescriptor('collectionNames', 1, 'string', repeated=True, packed=False),
            'timestamp': FieldDescriptor('timestamp', 2, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AppStateSyncKey(MessageBase):
        FIELDS = {
            'keyId': FieldDescriptor('keyId', 1, "message", repeated=False, packed=False, _msg_path='Message.AppStateSyncKeyId'),
            'keyData': FieldDescriptor('keyData', 2, "message", repeated=False, packed=False, _msg_path='Message.AppStateSyncKeyData'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AppStateSyncKeyData(MessageBase):
        FIELDS = {
            'keyData': FieldDescriptor('keyData', 1, 'bytes', repeated=False, packed=False),
            'fingerprint': FieldDescriptor('fingerprint', 2, "message", repeated=False, packed=False, _msg_path='Message.AppStateSyncKeyFingerprint'),
            'timestamp': FieldDescriptor('timestamp', 3, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AppStateSyncKeyFingerprint(MessageBase):
        FIELDS = {
            'rawId': FieldDescriptor('rawId', 1, 'uint32', repeated=False, packed=False),
            'currentIndex': FieldDescriptor('currentIndex', 2, 'uint32', repeated=False, packed=False),
            'deviceIndexes': FieldDescriptor('deviceIndexes', 3, 'uint32', repeated=True, packed=True),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AppStateSyncKeyId(MessageBase):
        FIELDS = {
            'keyId': FieldDescriptor('keyId', 1, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AppStateSyncKeyRequest(MessageBase):
        FIELDS = {
            'keyIds': FieldDescriptor('keyIds', 1, "message", repeated=True, packed=False, _msg_path='Message.AppStateSyncKeyId'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AppStateSyncKeyShare(MessageBase):
        FIELDS = {
            'keys': FieldDescriptor('keys', 1, "message", repeated=True, packed=False, _msg_path='Message.AppStateSyncKey'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AudioMessage(MessageBase):
        FIELDS = {
            'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
            'mimetype': FieldDescriptor('mimetype', 2, 'string', repeated=False, packed=False),
            'fileSha256': FieldDescriptor('fileSha256', 3, 'bytes', repeated=False, packed=False),
            'fileLength': FieldDescriptor('fileLength', 4, 'uint64', repeated=False, packed=False),
            'seconds': FieldDescriptor('seconds', 5, 'uint32', repeated=False, packed=False),
            'ptt': FieldDescriptor('ptt', 6, 'bool', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 7, 'bytes', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 8, 'bytes', repeated=False, packed=False),
            'directPath': FieldDescriptor('directPath', 9, 'string', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 10, 'int64', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'streamingSidecar': FieldDescriptor('streamingSidecar', 18, 'bytes', repeated=False, packed=False),
            'waveform': FieldDescriptor('waveform', 19, 'bytes', repeated=False, packed=False),
            'backgroundArgb': FieldDescriptor('backgroundArgb', 20, 'fixed32', repeated=False, packed=False),
            'viewOnce': FieldDescriptor('viewOnce', 21, 'bool', repeated=False, packed=False),
            'accessibilityLabel': FieldDescriptor('accessibilityLabel', 22, 'string', repeated=False, packed=False),
            'mediaKeyDomain': FieldDescriptor('mediaKeyDomain', 23, "enum", repeated=False, packed=False, _enum_path='Message.MediaKeyDomain'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class BCallMessage(MessageBase):
        class MediaType(enum.IntEnum):
            UNKNOWN = 0
            AUDIO = 1
            VIDEO = 2
        FIELDS = {
            'sessionId': FieldDescriptor('sessionId', 1, 'string', repeated=False, packed=False),
            'mediaType': FieldDescriptor('mediaType', 2, "enum", repeated=False, packed=False, _enum_path='Message.BCallMessage.MediaType'),
            'masterKey': FieldDescriptor('masterKey', 3, 'bytes', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 4, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ButtonsMessage(MessageBase):
        class HeaderType(enum.IntEnum):
            UNKNOWN = 0
            EMPTY = 1
            TEXT = 2
            DOCUMENT = 3
            IMAGE = 4
            VIDEO = 5
            LOCATION = 6
        class Button(MessageBase):
            class Type(enum.IntEnum):
                UNKNOWN = 0
                RESPONSE = 1
                NATIVE_FLOW = 2
            class ButtonText(MessageBase):
                FIELDS = {
                    'displayText': FieldDescriptor('displayText', 1, 'string', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class NativeFlowInfo(MessageBase):
                FIELDS = {
                    'name': FieldDescriptor('name', 1, 'string', repeated=False, packed=False),
                    'paramsJson': FieldDescriptor('paramsJson', 2, 'string', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            FIELDS = {
                'buttonId': FieldDescriptor('buttonId', 1, 'string', repeated=False, packed=False),
                'buttonText': FieldDescriptor('buttonText', 2, "message", repeated=False, packed=False, _msg_path='Message.ButtonsMessage.Button.ButtonText'),
                'type': FieldDescriptor('type', 3, "enum", repeated=False, packed=False, _enum_path='Message.ButtonsMessage.Button.Type'),
                'nativeFlowInfo': FieldDescriptor('nativeFlowInfo', 4, "message", repeated=False, packed=False, _msg_path='Message.ButtonsMessage.Button.NativeFlowInfo'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'contentText': FieldDescriptor('contentText', 6, 'string', repeated=False, packed=False),
            'footerText': FieldDescriptor('footerText', 7, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 8, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'buttons': FieldDescriptor('buttons', 9, "message", repeated=True, packed=False, _msg_path='Message.ButtonsMessage.Button'),
            'headerType': FieldDescriptor('headerType', 10, "enum", repeated=False, packed=False, _enum_path='Message.ButtonsMessage.HeaderType'),
            'text': FieldDescriptor('text', 1, 'string', repeated=False, packed=False),
            'documentMessage': FieldDescriptor('documentMessage', 2, "message", repeated=False, packed=False, _msg_path='Message.DocumentMessage'),
            'imageMessage': FieldDescriptor('imageMessage', 3, "message", repeated=False, packed=False, _msg_path='Message.ImageMessage'),
            'videoMessage': FieldDescriptor('videoMessage', 4, "message", repeated=False, packed=False, _msg_path='Message.VideoMessage'),
            'locationMessage': FieldDescriptor('locationMessage', 5, "message", repeated=False, packed=False, _msg_path='Message.LocationMessage'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ButtonsResponseMessage(MessageBase):
        class Type(enum.IntEnum):
            UNKNOWN = 0
            DISPLAY_TEXT = 1
        FIELDS = {
            'selectedButtonId': FieldDescriptor('selectedButtonId', 1, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 3, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'type': FieldDescriptor('type', 4, "enum", repeated=False, packed=False, _enum_path='Message.ButtonsResponseMessage.Type'),
            'selectedDisplayText': FieldDescriptor('selectedDisplayText', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class Call(MessageBase):
        FIELDS = {
            'callKey': FieldDescriptor('callKey', 1, 'bytes', repeated=False, packed=False),
            'conversionSource': FieldDescriptor('conversionSource', 2, 'string', repeated=False, packed=False),
            'conversionData': FieldDescriptor('conversionData', 3, 'bytes', repeated=False, packed=False),
            'conversionDelaySeconds': FieldDescriptor('conversionDelaySeconds', 4, 'uint32', repeated=False, packed=False),
            'ctwaSignals': FieldDescriptor('ctwaSignals', 5, 'string', repeated=False, packed=False),
            'ctwaPayload': FieldDescriptor('ctwaPayload', 6, 'bytes', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 7, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'nativeFlowCallButtonPayload': FieldDescriptor('nativeFlowCallButtonPayload', 8, 'string', repeated=False, packed=False),
            'deeplinkPayload': FieldDescriptor('deeplinkPayload', 9, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class CallLogMessage(MessageBase):
        class CallOutcome(enum.IntEnum):
            CONNECTED = 0
            MISSED = 1
            FAILED = 2
            REJECTED = 3
            ACCEPTED_ELSEWHERE = 4
            ONGOING = 5
            SILENCED_BY_DND = 6
            SILENCED_UNKNOWN_CALLER = 7
        class CallType(enum.IntEnum):
            REGULAR = 0
            SCHEDULED_CALL = 1
            VOICE_CHAT = 2
        class CallParticipant(MessageBase):
            FIELDS = {
                'jid': FieldDescriptor('jid', 1, 'string', repeated=False, packed=False),
                'callOutcome': FieldDescriptor('callOutcome', 2, "enum", repeated=False, packed=False, _enum_path='Message.CallLogMessage.CallOutcome'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'isVideo': FieldDescriptor('isVideo', 1, 'bool', repeated=False, packed=False),
            'callOutcome': FieldDescriptor('callOutcome', 2, "enum", repeated=False, packed=False, _enum_path='Message.CallLogMessage.CallOutcome'),
            'durationSecs': FieldDescriptor('durationSecs', 3, 'int64', repeated=False, packed=False),
            'callType': FieldDescriptor('callType', 4, "enum", repeated=False, packed=False, _enum_path='Message.CallLogMessage.CallType'),
            'participants': FieldDescriptor('participants', 5, "message", repeated=True, packed=False, _msg_path='Message.CallLogMessage.CallParticipant'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class CancelPaymentRequestMessage(MessageBase):
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class Chat(MessageBase):
        FIELDS = {
            'displayName': FieldDescriptor('displayName', 1, 'string', repeated=False, packed=False),
            'id': FieldDescriptor('id', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class CloudAPIThreadControlNotification(MessageBase):
        class CloudAPIThreadControl(enum.IntEnum):
            UNKNOWN = 0
            CONTROL_PASSED = 1
            CONTROL_TAKEN = 2
        class CloudAPIThreadControlNotificationContent(MessageBase):
            FIELDS = {
                'handoffNotificationText': FieldDescriptor('handoffNotificationText', 1, 'string', repeated=False, packed=False),
                'extraJson': FieldDescriptor('extraJson', 2, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'status': FieldDescriptor('status', 1, "enum", repeated=False, packed=False, _enum_path='Message.CloudAPIThreadControlNotification.CloudAPIThreadControl'),
            'senderNotificationTimestampMs': FieldDescriptor('senderNotificationTimestampMs', 2, 'int64', repeated=False, packed=False),
            'consumerLid': FieldDescriptor('consumerLid', 3, 'string', repeated=False, packed=False),
            'consumerPhoneNumber': FieldDescriptor('consumerPhoneNumber', 4, 'string', repeated=False, packed=False),
            'notificationContent': FieldDescriptor('notificationContent', 5, "message", repeated=False, packed=False, _msg_path='Message.CloudAPIThreadControlNotification.CloudAPIThreadControlNotificationContent'),
            'shouldSuppressNotification': FieldDescriptor('shouldSuppressNotification', 6, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class CommentMessage(MessageBase):
        FIELDS = {
            'message': FieldDescriptor('message', 1, "message", repeated=False, packed=False, _msg_path='Message'),
            'targetMessageKey': FieldDescriptor('targetMessageKey', 2, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ContactMessage(MessageBase):
        FIELDS = {
            'displayName': FieldDescriptor('displayName', 1, 'string', repeated=False, packed=False),
            'vcard': FieldDescriptor('vcard', 16, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ContactsArrayMessage(MessageBase):
        FIELDS = {
            'displayName': FieldDescriptor('displayName', 1, 'string', repeated=False, packed=False),
            'contacts': FieldDescriptor('contacts', 2, "message", repeated=True, packed=False, _msg_path='Message.ContactMessage'),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class DeclinePaymentRequestMessage(MessageBase):
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class DeviceSentMessage(MessageBase):
        FIELDS = {
            'destinationJid': FieldDescriptor('destinationJid', 1, 'string', repeated=False, packed=False),
            'message': FieldDescriptor('message', 2, "message", repeated=False, packed=False, _msg_path='Message'),
            'phash': FieldDescriptor('phash', 3, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class DocumentMessage(MessageBase):
        FIELDS = {
            'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
            'mimetype': FieldDescriptor('mimetype', 2, 'string', repeated=False, packed=False),
            'title': FieldDescriptor('title', 3, 'string', repeated=False, packed=False),
            'fileSha256': FieldDescriptor('fileSha256', 4, 'bytes', repeated=False, packed=False),
            'fileLength': FieldDescriptor('fileLength', 5, 'uint64', repeated=False, packed=False),
            'pageCount': FieldDescriptor('pageCount', 6, 'uint32', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 7, 'bytes', repeated=False, packed=False),
            'fileName': FieldDescriptor('fileName', 8, 'string', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 9, 'bytes', repeated=False, packed=False),
            'directPath': FieldDescriptor('directPath', 10, 'string', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 11, 'int64', repeated=False, packed=False),
            'contactVcard': FieldDescriptor('contactVcard', 12, 'bool', repeated=False, packed=False),
            'thumbnailDirectPath': FieldDescriptor('thumbnailDirectPath', 13, 'string', repeated=False, packed=False),
            'thumbnailSha256': FieldDescriptor('thumbnailSha256', 14, 'bytes', repeated=False, packed=False),
            'thumbnailEncSha256': FieldDescriptor('thumbnailEncSha256', 15, 'bytes', repeated=False, packed=False),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 16, 'bytes', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'thumbnailHeight': FieldDescriptor('thumbnailHeight', 18, 'uint32', repeated=False, packed=False),
            'thumbnailWidth': FieldDescriptor('thumbnailWidth', 19, 'uint32', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 20, 'string', repeated=False, packed=False),
            'accessibilityLabel': FieldDescriptor('accessibilityLabel', 21, 'string', repeated=False, packed=False),
            'mediaKeyDomain': FieldDescriptor('mediaKeyDomain', 22, "enum", repeated=False, packed=False, _enum_path='Message.MediaKeyDomain'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class EncCommentMessage(MessageBase):
        FIELDS = {
            'targetMessageKey': FieldDescriptor('targetMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'encPayload': FieldDescriptor('encPayload', 2, 'bytes', repeated=False, packed=False),
            'encIv': FieldDescriptor('encIv', 3, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class EncEventResponseMessage(MessageBase):
        FIELDS = {
            'eventCreationMessageKey': FieldDescriptor('eventCreationMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'encPayload': FieldDescriptor('encPayload', 2, 'bytes', repeated=False, packed=False),
            'encIv': FieldDescriptor('encIv', 3, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class EncReactionMessage(MessageBase):
        FIELDS = {
            'targetMessageKey': FieldDescriptor('targetMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'encPayload': FieldDescriptor('encPayload', 2, 'bytes', repeated=False, packed=False),
            'encIv': FieldDescriptor('encIv', 3, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class EventMessage(MessageBase):
        FIELDS = {
            'contextInfo': FieldDescriptor('contextInfo', 1, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'isCanceled': FieldDescriptor('isCanceled', 2, 'bool', repeated=False, packed=False),
            'name': FieldDescriptor('name', 3, 'string', repeated=False, packed=False),
            'description': FieldDescriptor('description', 4, 'string', repeated=False, packed=False),
            'location': FieldDescriptor('location', 5, "message", repeated=False, packed=False, _msg_path='Message.LocationMessage'),
            'joinLink': FieldDescriptor('joinLink', 6, 'string', repeated=False, packed=False),
            'startTime': FieldDescriptor('startTime', 7, 'int64', repeated=False, packed=False),
            'endTime': FieldDescriptor('endTime', 8, 'int64', repeated=False, packed=False),
            'extraGuestsAllowed': FieldDescriptor('extraGuestsAllowed', 9, 'bool', repeated=False, packed=False),
            'isScheduleCall': FieldDescriptor('isScheduleCall', 10, 'bool', repeated=False, packed=False),
            'hasReminder': FieldDescriptor('hasReminder', 11, 'bool', repeated=False, packed=False),
            'reminderOffsetSec': FieldDescriptor('reminderOffsetSec', 12, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class EventResponseMessage(MessageBase):
        class EventResponseType(enum.IntEnum):
            UNKNOWN = 0
            GOING = 1
            NOT_GOING = 2
            MAYBE = 3
        FIELDS = {
            'response': FieldDescriptor('response', 1, "enum", repeated=False, packed=False, _enum_path='Message.EventResponseMessage.EventResponseType'),
            'timestampMs': FieldDescriptor('timestampMs', 2, 'int64', repeated=False, packed=False),
            'extraGuestCount': FieldDescriptor('extraGuestCount', 3, 'int32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ExtendedTextMessage(MessageBase):
        class FontType(enum.IntEnum):
            SYSTEM = 0
            SYSTEM_TEXT = 1
            FB_SCRIPT = 2
            SYSTEM_BOLD = 6
            MORNINGBREEZE_REGULAR = 7
            CALISTOGA_REGULAR = 8
            EXO2_EXTRABOLD = 9
            COURIERPRIME_BOLD = 10
        class InviteLinkGroupType(enum.IntEnum):
            DEFAULT = 0
            PARENT = 1
            SUB = 2
            DEFAULT_SUB = 3
        class PreviewType(enum.IntEnum):
            NONE = 0
            VIDEO = 1
            PLACEHOLDER = 4
            IMAGE = 5
            PAYMENT_LINKS = 6
            PROFILE = 7
        FIELDS = {
            'text': FieldDescriptor('text', 1, 'string', repeated=False, packed=False),
            'matchedText': FieldDescriptor('matchedText', 2, 'string', repeated=False, packed=False),
            'description': FieldDescriptor('description', 5, 'string', repeated=False, packed=False),
            'title': FieldDescriptor('title', 6, 'string', repeated=False, packed=False),
            'textArgb': FieldDescriptor('textArgb', 7, 'fixed32', repeated=False, packed=False),
            'backgroundArgb': FieldDescriptor('backgroundArgb', 8, 'fixed32', repeated=False, packed=False),
            'font': FieldDescriptor('font', 9, "enum", repeated=False, packed=False, _enum_path='Message.ExtendedTextMessage.FontType'),
            'previewType': FieldDescriptor('previewType', 10, "enum", repeated=False, packed=False, _enum_path='Message.ExtendedTextMessage.PreviewType'),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 16, 'bytes', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'doNotPlayInline': FieldDescriptor('doNotPlayInline', 18, 'bool', repeated=False, packed=False),
            'thumbnailDirectPath': FieldDescriptor('thumbnailDirectPath', 19, 'string', repeated=False, packed=False),
            'thumbnailSha256': FieldDescriptor('thumbnailSha256', 20, 'bytes', repeated=False, packed=False),
            'thumbnailEncSha256': FieldDescriptor('thumbnailEncSha256', 21, 'bytes', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 22, 'bytes', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 23, 'int64', repeated=False, packed=False),
            'thumbnailHeight': FieldDescriptor('thumbnailHeight', 24, 'uint32', repeated=False, packed=False),
            'thumbnailWidth': FieldDescriptor('thumbnailWidth', 25, 'uint32', repeated=False, packed=False),
            'inviteLinkGroupType': FieldDescriptor('inviteLinkGroupType', 26, "enum", repeated=False, packed=False, _enum_path='Message.ExtendedTextMessage.InviteLinkGroupType'),
            'inviteLinkParentGroupSubjectV2': FieldDescriptor('inviteLinkParentGroupSubjectV2', 27, 'string', repeated=False, packed=False),
            'inviteLinkParentGroupThumbnailV2': FieldDescriptor('inviteLinkParentGroupThumbnailV2', 28, 'bytes', repeated=False, packed=False),
            'inviteLinkGroupTypeV2': FieldDescriptor('inviteLinkGroupTypeV2', 29, "enum", repeated=False, packed=False, _enum_path='Message.ExtendedTextMessage.InviteLinkGroupType'),
            'viewOnce': FieldDescriptor('viewOnce', 30, 'bool', repeated=False, packed=False),
            'videoHeight': FieldDescriptor('videoHeight', 31, 'uint32', repeated=False, packed=False),
            'videoWidth': FieldDescriptor('videoWidth', 32, 'uint32', repeated=False, packed=False),
            'faviconMMSMetadata': FieldDescriptor('faviconMMSMetadata', 33, "message", repeated=False, packed=False, _msg_path='Message.MMSThumbnailMetadata'),
            'linkPreviewMetadata': FieldDescriptor('linkPreviewMetadata', 34, "message", repeated=False, packed=False, _msg_path='Message.LinkPreviewMetadata'),
            'paymentLinkMetadata': FieldDescriptor('paymentLinkMetadata', 35, "message", repeated=False, packed=False, _msg_path='Message.PaymentLinkMetadata'),
            'endCardTiles': FieldDescriptor('endCardTiles', 36, "message", repeated=True, packed=False, _msg_path='Message.VideoEndCard'),
            'videoContentUrl': FieldDescriptor('videoContentUrl', 37, 'string', repeated=False, packed=False),
            'musicMetadata': FieldDescriptor('musicMetadata', 38, "message", repeated=False, packed=False, _msg_path='EmbeddedMusic'),
            'paymentExtendedMetadata': FieldDescriptor('paymentExtendedMetadata', 39, "message", repeated=False, packed=False, _msg_path='Message.PaymentExtendedMetadata'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class FullHistorySyncOnDemandRequestMetadata(MessageBase):
        FIELDS = {
            'requestId': FieldDescriptor('requestId', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class FutureProofMessage(MessageBase):
        FIELDS = {
            'message': FieldDescriptor('message', 1, "message", repeated=False, packed=False, _msg_path='Message'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class GroupInviteMessage(MessageBase):
        class GroupType(enum.IntEnum):
            DEFAULT = 0
            PARENT = 1
        FIELDS = {
            'groupJid': FieldDescriptor('groupJid', 1, 'string', repeated=False, packed=False),
            'inviteCode': FieldDescriptor('inviteCode', 2, 'string', repeated=False, packed=False),
            'inviteExpiration': FieldDescriptor('inviteExpiration', 3, 'int64', repeated=False, packed=False),
            'groupName': FieldDescriptor('groupName', 4, 'string', repeated=False, packed=False),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 5, 'bytes', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 6, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 7, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'groupType': FieldDescriptor('groupType', 8, "enum", repeated=False, packed=False, _enum_path='Message.GroupInviteMessage.GroupType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class HighlyStructuredMessage(MessageBase):
        class HSMLocalizableParameter(MessageBase):
            class HSMCurrency(MessageBase):
                FIELDS = {
                    'currencyCode': FieldDescriptor('currencyCode', 1, 'string', repeated=False, packed=False),
                    'amount1000': FieldDescriptor('amount1000', 2, 'int64', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class HSMDateTime(MessageBase):
                class HSMDateTimeComponent(MessageBase):
                    class CalendarType(enum.IntEnum):
                        GREGORIAN = 1
                        SOLAR_HIJRI = 2
                    class DayOfWeekType(enum.IntEnum):
                        MONDAY = 1
                        TUESDAY = 2
                        WEDNESDAY = 3
                        THURSDAY = 4
                        FRIDAY = 5
                        SATURDAY = 6
                        SUNDAY = 7
                    FIELDS = {
                        'dayOfWeek': FieldDescriptor('dayOfWeek', 1, "enum", repeated=False, packed=False, _enum_path='Message.HighlyStructuredMessage.HSMLocalizableParameter.HSMDateTime.HSMDateTimeComponent.DayOfWeekType'),
                        'year': FieldDescriptor('year', 2, 'uint32', repeated=False, packed=False),
                        'month': FieldDescriptor('month', 3, 'uint32', repeated=False, packed=False),
                        'dayOfMonth': FieldDescriptor('dayOfMonth', 4, 'uint32', repeated=False, packed=False),
                        'hour': FieldDescriptor('hour', 5, 'uint32', repeated=False, packed=False),
                        'minute': FieldDescriptor('minute', 6, 'uint32', repeated=False, packed=False),
                        'calendar': FieldDescriptor('calendar', 7, "enum", repeated=False, packed=False, _enum_path='Message.HighlyStructuredMessage.HSMLocalizableParameter.HSMDateTime.HSMDateTimeComponent.CalendarType'),
                    }
                    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
                class HSMDateTimeUnixEpoch(MessageBase):
                    FIELDS = {
                        'timestamp': FieldDescriptor('timestamp', 1, 'int64', repeated=False, packed=False),
                    }
                    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
                FIELDS = {
                    'component': FieldDescriptor('component', 1, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage.HSMLocalizableParameter.HSMDateTime.HSMDateTimeComponent'),
                    'unixEpoch': FieldDescriptor('unixEpoch', 2, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage.HSMLocalizableParameter.HSMDateTime.HSMDateTimeUnixEpoch'),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            FIELDS = {
                'default': FieldDescriptor('default', 1, 'string', repeated=False, packed=False),
                'currency': FieldDescriptor('currency', 2, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage.HSMLocalizableParameter.HSMCurrency'),
                'dateTime': FieldDescriptor('dateTime', 3, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage.HSMLocalizableParameter.HSMDateTime'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'namespace': FieldDescriptor('namespace', 1, 'string', repeated=False, packed=False),
            'elementName': FieldDescriptor('elementName', 2, 'string', repeated=False, packed=False),
            'params': FieldDescriptor('params', 3, 'string', repeated=True, packed=False),
            'fallbackLg': FieldDescriptor('fallbackLg', 4, 'string', repeated=False, packed=False),
            'fallbackLc': FieldDescriptor('fallbackLc', 5, 'string', repeated=False, packed=False),
            'localizableParams': FieldDescriptor('localizableParams', 6, "message", repeated=True, packed=False, _msg_path='Message.HighlyStructuredMessage.HSMLocalizableParameter'),
            'deterministicLg': FieldDescriptor('deterministicLg', 7, 'string', repeated=False, packed=False),
            'deterministicLc': FieldDescriptor('deterministicLc', 8, 'string', repeated=False, packed=False),
            'hydratedHsm': FieldDescriptor('hydratedHsm', 9, "message", repeated=False, packed=False, _msg_path='Message.TemplateMessage'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class HistorySyncMessageAccessStatus(MessageBase):
        FIELDS = {
            'completeAccessGranted': FieldDescriptor('completeAccessGranted', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class HistorySyncNotification(MessageBase):
        FIELDS = {
            'fileSha256': FieldDescriptor('fileSha256', 1, 'bytes', repeated=False, packed=False),
            'fileLength': FieldDescriptor('fileLength', 2, 'uint64', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 3, 'bytes', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 4, 'bytes', repeated=False, packed=False),
            'directPath': FieldDescriptor('directPath', 5, 'string', repeated=False, packed=False),
            'syncType': FieldDescriptor('syncType', 6, "enum", repeated=False, packed=False, _enum_path='Message.HistorySyncType'),
            'chunkOrder': FieldDescriptor('chunkOrder', 7, 'uint32', repeated=False, packed=False),
            'originalMessageId': FieldDescriptor('originalMessageId', 8, 'string', repeated=False, packed=False),
            'progress': FieldDescriptor('progress', 9, 'uint32', repeated=False, packed=False),
            'oldestMsgInChunkTimestampSec': FieldDescriptor('oldestMsgInChunkTimestampSec', 10, 'int64', repeated=False, packed=False),
            'initialHistBootstrapInlinePayload': FieldDescriptor('initialHistBootstrapInlinePayload', 11, 'bytes', repeated=False, packed=False),
            'peerDataRequestSessionId': FieldDescriptor('peerDataRequestSessionId', 12, 'string', repeated=False, packed=False),
            'fullHistorySyncOnDemandRequestMetadata': FieldDescriptor('fullHistorySyncOnDemandRequestMetadata', 13, "message", repeated=False, packed=False, _msg_path='Message.FullHistorySyncOnDemandRequestMetadata'),
            'encHandle': FieldDescriptor('encHandle', 14, 'string', repeated=False, packed=False),
            'messageAccessStatus': FieldDescriptor('messageAccessStatus', 15, "message", repeated=False, packed=False, _msg_path='Message.HistorySyncMessageAccessStatus'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ImageMessage(MessageBase):
        class ImageSourceType(enum.IntEnum):
            USER_IMAGE = 0
            AI_GENERATED = 1
            AI_MODIFIED = 2
            RASTERIZED_TEXT_STATUS = 3
        FIELDS = {
            'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
            'mimetype': FieldDescriptor('mimetype', 2, 'string', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 3, 'string', repeated=False, packed=False),
            'fileSha256': FieldDescriptor('fileSha256', 4, 'bytes', repeated=False, packed=False),
            'fileLength': FieldDescriptor('fileLength', 5, 'uint64', repeated=False, packed=False),
            'height': FieldDescriptor('height', 6, 'uint32', repeated=False, packed=False),
            'width': FieldDescriptor('width', 7, 'uint32', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 8, 'bytes', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 9, 'bytes', repeated=False, packed=False),
            'interactiveAnnotations': FieldDescriptor('interactiveAnnotations', 10, "message", repeated=True, packed=False, _msg_path='InteractiveAnnotation'),
            'directPath': FieldDescriptor('directPath', 11, 'string', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 12, 'int64', repeated=False, packed=False),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 16, 'bytes', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'firstScanSidecar': FieldDescriptor('firstScanSidecar', 18, 'bytes', repeated=False, packed=False),
            'firstScanLength': FieldDescriptor('firstScanLength', 19, 'uint32', repeated=False, packed=False),
            'experimentGroupId': FieldDescriptor('experimentGroupId', 20, 'uint32', repeated=False, packed=False),
            'scansSidecar': FieldDescriptor('scansSidecar', 21, 'bytes', repeated=False, packed=False),
            'scanLengths': FieldDescriptor('scanLengths', 22, 'uint32', repeated=True, packed=False),
            'midQualityFileSha256': FieldDescriptor('midQualityFileSha256', 23, 'bytes', repeated=False, packed=False),
            'midQualityFileEncSha256': FieldDescriptor('midQualityFileEncSha256', 24, 'bytes', repeated=False, packed=False),
            'viewOnce': FieldDescriptor('viewOnce', 25, 'bool', repeated=False, packed=False),
            'thumbnailDirectPath': FieldDescriptor('thumbnailDirectPath', 26, 'string', repeated=False, packed=False),
            'thumbnailSha256': FieldDescriptor('thumbnailSha256', 27, 'bytes', repeated=False, packed=False),
            'thumbnailEncSha256': FieldDescriptor('thumbnailEncSha256', 28, 'bytes', repeated=False, packed=False),
            'staticUrl': FieldDescriptor('staticUrl', 29, 'string', repeated=False, packed=False),
            'annotations': FieldDescriptor('annotations', 30, "message", repeated=True, packed=False, _msg_path='InteractiveAnnotation'),
            'imageSourceType': FieldDescriptor('imageSourceType', 31, "enum", repeated=False, packed=False, _enum_path='Message.ImageMessage.ImageSourceType'),
            'accessibilityLabel': FieldDescriptor('accessibilityLabel', 32, 'string', repeated=False, packed=False),
            'mediaKeyDomain': FieldDescriptor('mediaKeyDomain', 33, "enum", repeated=False, packed=False, _enum_path='Message.MediaKeyDomain'),
            'qrUrl': FieldDescriptor('qrUrl', 34, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class InitialSecurityNotificationSettingSync(MessageBase):
        FIELDS = {
            'securityNotificationEnabled': FieldDescriptor('securityNotificationEnabled', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class InteractiveMessage(MessageBase):
        class Body(MessageBase):
            FIELDS = {
                'text': FieldDescriptor('text', 1, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class CarouselMessage(MessageBase):
            class CarouselCardType(enum.IntEnum):
                UNKNOWN = 0
                HSCROLL_CARDS = 1
                ALBUM_IMAGE = 2
            FIELDS = {
                'cards': FieldDescriptor('cards', 1, "message", repeated=True, packed=False, _msg_path='Message.InteractiveMessage'),
                'messageVersion': FieldDescriptor('messageVersion', 2, 'int32', repeated=False, packed=False),
                'carouselCardType': FieldDescriptor('carouselCardType', 3, "enum", repeated=False, packed=False, _enum_path='Message.InteractiveMessage.CarouselMessage.CarouselCardType'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class CollectionMessage(MessageBase):
            FIELDS = {
                'bizJid': FieldDescriptor('bizJid', 1, 'string', repeated=False, packed=False),
                'id': FieldDescriptor('id', 2, 'string', repeated=False, packed=False),
                'messageVersion': FieldDescriptor('messageVersion', 3, 'int32', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class Footer(MessageBase):
            FIELDS = {
                'text': FieldDescriptor('text', 1, 'string', repeated=False, packed=False),
                'hasMediaAttachment': FieldDescriptor('hasMediaAttachment', 3, 'bool', repeated=False, packed=False),
                'audioMessage': FieldDescriptor('audioMessage', 2, "message", repeated=False, packed=False, _msg_path='Message.AudioMessage'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class Header(MessageBase):
            FIELDS = {
                'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
                'subtitle': FieldDescriptor('subtitle', 2, 'string', repeated=False, packed=False),
                'hasMediaAttachment': FieldDescriptor('hasMediaAttachment', 5, 'bool', repeated=False, packed=False),
                'documentMessage': FieldDescriptor('documentMessage', 3, "message", repeated=False, packed=False, _msg_path='Message.DocumentMessage'),
                'imageMessage': FieldDescriptor('imageMessage', 4, "message", repeated=False, packed=False, _msg_path='Message.ImageMessage'),
                'jpegThumbnail': FieldDescriptor('jpegThumbnail', 6, 'bytes', repeated=False, packed=False),
                'videoMessage': FieldDescriptor('videoMessage', 7, "message", repeated=False, packed=False, _msg_path='Message.VideoMessage'),
                'locationMessage': FieldDescriptor('locationMessage', 8, "message", repeated=False, packed=False, _msg_path='Message.LocationMessage'),
                'productMessage': FieldDescriptor('productMessage', 9, "message", repeated=False, packed=False, _msg_path='Message.ProductMessage'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class NativeFlowMessage(MessageBase):
            class NativeFlowButton(MessageBase):
                FIELDS = {
                    'name': FieldDescriptor('name', 1, 'string', repeated=False, packed=False),
                    'buttonParamsJson': FieldDescriptor('buttonParamsJson', 2, 'string', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            FIELDS = {
                'buttons': FieldDescriptor('buttons', 1, "message", repeated=True, packed=False, _msg_path='Message.InteractiveMessage.NativeFlowMessage.NativeFlowButton'),
                'messageParamsJson': FieldDescriptor('messageParamsJson', 2, 'string', repeated=False, packed=False),
                'messageVersion': FieldDescriptor('messageVersion', 3, 'int32', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class ShopMessage(MessageBase):
            class Surface(enum.IntEnum):
                UNKNOWN_SURFACE = 0
                FB = 1
                IG = 2
                WA = 3
            FIELDS = {
                'id': FieldDescriptor('id', 1, 'string', repeated=False, packed=False),
                'surface': FieldDescriptor('surface', 2, "enum", repeated=False, packed=False, _enum_path='Message.InteractiveMessage.ShopMessage.Surface'),
                'messageVersion': FieldDescriptor('messageVersion', 3, 'int32', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'header': FieldDescriptor('header', 1, "message", repeated=False, packed=False, _msg_path='Message.InteractiveMessage.Header'),
            'body': FieldDescriptor('body', 2, "message", repeated=False, packed=False, _msg_path='Message.InteractiveMessage.Body'),
            'footer': FieldDescriptor('footer', 3, "message", repeated=False, packed=False, _msg_path='Message.InteractiveMessage.Footer'),
            'contextInfo': FieldDescriptor('contextInfo', 15, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'urlTrackingMap': FieldDescriptor('urlTrackingMap', 16, "message", repeated=False, packed=False, _msg_path='UrlTrackingMap'),
            'shopStorefrontMessage': FieldDescriptor('shopStorefrontMessage', 4, "message", repeated=False, packed=False, _msg_path='Message.InteractiveMessage.ShopMessage'),
            'collectionMessage': FieldDescriptor('collectionMessage', 5, "message", repeated=False, packed=False, _msg_path='Message.InteractiveMessage.CollectionMessage'),
            'nativeFlowMessage': FieldDescriptor('nativeFlowMessage', 6, "message", repeated=False, packed=False, _msg_path='Message.InteractiveMessage.NativeFlowMessage'),
            'carouselMessage': FieldDescriptor('carouselMessage', 7, "message", repeated=False, packed=False, _msg_path='Message.InteractiveMessage.CarouselMessage'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class InteractiveResponseMessage(MessageBase):
        class Body(MessageBase):
            class Format(enum.IntEnum):
                DEFAULT = 0
                EXTENSIONS_1 = 1
            FIELDS = {
                'text': FieldDescriptor('text', 1, 'string', repeated=False, packed=False),
                'format': FieldDescriptor('format', 2, "enum", repeated=False, packed=False, _enum_path='Message.InteractiveResponseMessage.Body.Format'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class NativeFlowResponseMessage(MessageBase):
            FIELDS = {
                'name': FieldDescriptor('name', 1, 'string', repeated=False, packed=False),
                'paramsJson': FieldDescriptor('paramsJson', 2, 'string', repeated=False, packed=False),
                'version': FieldDescriptor('version', 3, 'int32', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'body': FieldDescriptor('body', 1, "message", repeated=False, packed=False, _msg_path='Message.InteractiveResponseMessage.Body'),
            'contextInfo': FieldDescriptor('contextInfo', 15, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'nativeFlowResponseMessage': FieldDescriptor('nativeFlowResponseMessage', 2, "message", repeated=False, packed=False, _msg_path='Message.InteractiveResponseMessage.NativeFlowResponseMessage'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class InvoiceMessage(MessageBase):
        class AttachmentType(enum.IntEnum):
            IMAGE = 0
            PDF = 1
        FIELDS = {
            'note': FieldDescriptor('note', 1, 'string', repeated=False, packed=False),
            'token': FieldDescriptor('token', 2, 'string', repeated=False, packed=False),
            'attachmentType': FieldDescriptor('attachmentType', 3, "enum", repeated=False, packed=False, _enum_path='Message.InvoiceMessage.AttachmentType'),
            'attachmentMimetype': FieldDescriptor('attachmentMimetype', 4, 'string', repeated=False, packed=False),
            'attachmentMediaKey': FieldDescriptor('attachmentMediaKey', 5, 'bytes', repeated=False, packed=False),
            'attachmentMediaKeyTimestamp': FieldDescriptor('attachmentMediaKeyTimestamp', 6, 'int64', repeated=False, packed=False),
            'attachmentFileSha256': FieldDescriptor('attachmentFileSha256', 7, 'bytes', repeated=False, packed=False),
            'attachmentFileEncSha256': FieldDescriptor('attachmentFileEncSha256', 8, 'bytes', repeated=False, packed=False),
            'attachmentDirectPath': FieldDescriptor('attachmentDirectPath', 9, 'string', repeated=False, packed=False),
            'attachmentJpegThumbnail': FieldDescriptor('attachmentJpegThumbnail', 10, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class KeepInChatMessage(MessageBase):
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'keepType': FieldDescriptor('keepType', 2, "enum", repeated=False, packed=False, _enum_path='KeepType'),
            'timestampMs': FieldDescriptor('timestampMs', 3, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LinkPreviewMetadata(MessageBase):
        class SocialMediaPostType(enum.IntEnum):
            NONE = 0
            REEL = 1
            LIVE_VIDEO = 2
            LONG_VIDEO = 3
            SINGLE_IMAGE = 4
            CAROUSEL = 5
        FIELDS = {
            'paymentLinkMetadata': FieldDescriptor('paymentLinkMetadata', 1, "message", repeated=False, packed=False, _msg_path='Message.PaymentLinkMetadata'),
            'urlMetadata': FieldDescriptor('urlMetadata', 2, "message", repeated=False, packed=False, _msg_path='Message.URLMetadata'),
            'fbExperimentId': FieldDescriptor('fbExperimentId', 3, 'uint32', repeated=False, packed=False),
            'linkMediaDuration': FieldDescriptor('linkMediaDuration', 4, 'uint32', repeated=False, packed=False),
            'socialMediaPostType': FieldDescriptor('socialMediaPostType', 5, "enum", repeated=False, packed=False, _enum_path='Message.LinkPreviewMetadata.SocialMediaPostType'),
            'linkInlineVideoMuted': FieldDescriptor('linkInlineVideoMuted', 6, 'bool', repeated=False, packed=False),
            'videoContentUrl': FieldDescriptor('videoContentUrl', 7, 'string', repeated=False, packed=False),
            'musicMetadata': FieldDescriptor('musicMetadata', 8, "message", repeated=False, packed=False, _msg_path='EmbeddedMusic'),
            'videoContentCaption': FieldDescriptor('videoContentCaption', 9, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ListMessage(MessageBase):
        class ListType(enum.IntEnum):
            UNKNOWN = 0
            SINGLE_SELECT = 1
            PRODUCT_LIST = 2
        class Product(MessageBase):
            FIELDS = {
                'productId': FieldDescriptor('productId', 1, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class ProductListHeaderImage(MessageBase):
            FIELDS = {
                'productId': FieldDescriptor('productId', 1, 'string', repeated=False, packed=False),
                'jpegThumbnail': FieldDescriptor('jpegThumbnail', 2, 'bytes', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class ProductListInfo(MessageBase):
            FIELDS = {
                'productSections': FieldDescriptor('productSections', 1, "message", repeated=True, packed=False, _msg_path='Message.ListMessage.ProductSection'),
                'headerImage': FieldDescriptor('headerImage', 2, "message", repeated=False, packed=False, _msg_path='Message.ListMessage.ProductListHeaderImage'),
                'businessOwnerJid': FieldDescriptor('businessOwnerJid', 3, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class ProductSection(MessageBase):
            FIELDS = {
                'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
                'products': FieldDescriptor('products', 2, "message", repeated=True, packed=False, _msg_path='Message.ListMessage.Product'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class Row(MessageBase):
            FIELDS = {
                'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
                'description': FieldDescriptor('description', 2, 'string', repeated=False, packed=False),
                'rowId': FieldDescriptor('rowId', 3, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class Section(MessageBase):
            FIELDS = {
                'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
                'rows': FieldDescriptor('rows', 2, "message", repeated=True, packed=False, _msg_path='Message.ListMessage.Row'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
            'description': FieldDescriptor('description', 2, 'string', repeated=False, packed=False),
            'buttonText': FieldDescriptor('buttonText', 3, 'string', repeated=False, packed=False),
            'listType': FieldDescriptor('listType', 4, "enum", repeated=False, packed=False, _enum_path='Message.ListMessage.ListType'),
            'sections': FieldDescriptor('sections', 5, "message", repeated=True, packed=False, _msg_path='Message.ListMessage.Section'),
            'productListInfo': FieldDescriptor('productListInfo', 6, "message", repeated=False, packed=False, _msg_path='Message.ListMessage.ProductListInfo'),
            'footerText': FieldDescriptor('footerText', 7, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 8, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ListResponseMessage(MessageBase):
        class ListType(enum.IntEnum):
            UNKNOWN = 0
            SINGLE_SELECT = 1
        class SingleSelectReply(MessageBase):
            FIELDS = {
                'selectedRowId': FieldDescriptor('selectedRowId', 1, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
            'listType': FieldDescriptor('listType', 2, "enum", repeated=False, packed=False, _enum_path='Message.ListResponseMessage.ListType'),
            'singleSelectReply': FieldDescriptor('singleSelectReply', 3, "message", repeated=False, packed=False, _msg_path='Message.ListResponseMessage.SingleSelectReply'),
            'contextInfo': FieldDescriptor('contextInfo', 4, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'description': FieldDescriptor('description', 5, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LiveLocationMessage(MessageBase):
        FIELDS = {
            'degreesLatitude': FieldDescriptor('degreesLatitude', 1, 'double', repeated=False, packed=False),
            'degreesLongitude': FieldDescriptor('degreesLongitude', 2, 'double', repeated=False, packed=False),
            'accuracyInMeters': FieldDescriptor('accuracyInMeters', 3, 'uint32', repeated=False, packed=False),
            'speedInMps': FieldDescriptor('speedInMps', 4, 'float', repeated=False, packed=False),
            'degreesClockwiseFromMagneticNorth': FieldDescriptor('degreesClockwiseFromMagneticNorth', 5, 'uint32', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 6, 'string', repeated=False, packed=False),
            'sequenceNumber': FieldDescriptor('sequenceNumber', 7, 'int64', repeated=False, packed=False),
            'timeOffset': FieldDescriptor('timeOffset', 8, 'uint32', repeated=False, packed=False),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 16, 'bytes', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LocationMessage(MessageBase):
        FIELDS = {
            'degreesLatitude': FieldDescriptor('degreesLatitude', 1, 'double', repeated=False, packed=False),
            'degreesLongitude': FieldDescriptor('degreesLongitude', 2, 'double', repeated=False, packed=False),
            'name': FieldDescriptor('name', 3, 'string', repeated=False, packed=False),
            'address': FieldDescriptor('address', 4, 'string', repeated=False, packed=False),
            'url': FieldDescriptor('url', 5, 'string', repeated=False, packed=False),
            'isLive': FieldDescriptor('isLive', 6, 'bool', repeated=False, packed=False),
            'accuracyInMeters': FieldDescriptor('accuracyInMeters', 7, 'uint32', repeated=False, packed=False),
            'speedInMps': FieldDescriptor('speedInMps', 8, 'float', repeated=False, packed=False),
            'degreesClockwiseFromMagneticNorth': FieldDescriptor('degreesClockwiseFromMagneticNorth', 9, 'uint32', repeated=False, packed=False),
            'comment': FieldDescriptor('comment', 11, 'string', repeated=False, packed=False),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 16, 'bytes', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MMSThumbnailMetadata(MessageBase):
        FIELDS = {
            'thumbnailDirectPath': FieldDescriptor('thumbnailDirectPath', 1, 'string', repeated=False, packed=False),
            'thumbnailSha256': FieldDescriptor('thumbnailSha256', 2, 'bytes', repeated=False, packed=False),
            'thumbnailEncSha256': FieldDescriptor('thumbnailEncSha256', 3, 'bytes', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 4, 'bytes', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 5, 'int64', repeated=False, packed=False),
            'thumbnailHeight': FieldDescriptor('thumbnailHeight', 6, 'uint32', repeated=False, packed=False),
            'thumbnailWidth': FieldDescriptor('thumbnailWidth', 7, 'uint32', repeated=False, packed=False),
            'mediaKeyDomain': FieldDescriptor('mediaKeyDomain', 8, "enum", repeated=False, packed=False, _enum_path='Message.MediaKeyDomain'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MessageHistoryBundle(MessageBase):
        FIELDS = {
            'mimetype': FieldDescriptor('mimetype', 1, 'string', repeated=False, packed=False),
            'fileSha256': FieldDescriptor('fileSha256', 2, 'bytes', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 3, 'bytes', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 4, 'bytes', repeated=False, packed=False),
            'directPath': FieldDescriptor('directPath', 5, 'string', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 6, 'int64', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 7, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'messageHistoryMetadata': FieldDescriptor('messageHistoryMetadata', 8, "message", repeated=False, packed=False, _msg_path='Message.MessageHistoryMetadata'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MessageHistoryMetadata(MessageBase):
        FIELDS = {
            'historyReceivers': FieldDescriptor('historyReceivers', 1, 'string', repeated=True, packed=False),
            'oldestMessageTimestamp': FieldDescriptor('oldestMessageTimestamp', 2, 'int64', repeated=False, packed=False),
            'messageCount': FieldDescriptor('messageCount', 3, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MessageHistoryNotice(MessageBase):
        FIELDS = {
            'contextInfo': FieldDescriptor('contextInfo', 1, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'messageHistoryMetadata': FieldDescriptor('messageHistoryMetadata', 2, "message", repeated=False, packed=False, _msg_path='Message.MessageHistoryMetadata'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class NewsletterAdminInviteMessage(MessageBase):
        FIELDS = {
            'newsletterJid': FieldDescriptor('newsletterJid', 1, 'string', repeated=False, packed=False),
            'newsletterName': FieldDescriptor('newsletterName', 2, 'string', repeated=False, packed=False),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 3, 'bytes', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 4, 'string', repeated=False, packed=False),
            'inviteExpiration': FieldDescriptor('inviteExpiration', 5, 'int64', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 6, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class NewsletterFollowerInviteMessage(MessageBase):
        FIELDS = {
            'newsletterJid': FieldDescriptor('newsletterJid', 1, 'string', repeated=False, packed=False),
            'newsletterName': FieldDescriptor('newsletterName', 2, 'string', repeated=False, packed=False),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 3, 'bytes', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 4, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 5, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class OrderMessage(MessageBase):
        class OrderStatus(enum.IntEnum):
            INQUIRY = 1
            ACCEPTED = 2
            DECLINED = 3
        class OrderSurface(enum.IntEnum):
            CATALOG = 1
        FIELDS = {
            'orderId': FieldDescriptor('orderId', 1, 'string', repeated=False, packed=False),
            'thumbnail': FieldDescriptor('thumbnail', 2, 'bytes', repeated=False, packed=False),
            'itemCount': FieldDescriptor('itemCount', 3, 'int32', repeated=False, packed=False),
            'status': FieldDescriptor('status', 4, "enum", repeated=False, packed=False, _enum_path='Message.OrderMessage.OrderStatus'),
            'surface': FieldDescriptor('surface', 5, "enum", repeated=False, packed=False, _enum_path='Message.OrderMessage.OrderSurface'),
            'message': FieldDescriptor('message', 6, 'string', repeated=False, packed=False),
            'orderTitle': FieldDescriptor('orderTitle', 7, 'string', repeated=False, packed=False),
            'sellerJid': FieldDescriptor('sellerJid', 8, 'string', repeated=False, packed=False),
            'token': FieldDescriptor('token', 9, 'string', repeated=False, packed=False),
            'totalAmount1000': FieldDescriptor('totalAmount1000', 10, 'int64', repeated=False, packed=False),
            'totalCurrencyCode': FieldDescriptor('totalCurrencyCode', 11, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'messageVersion': FieldDescriptor('messageVersion', 12, 'int32', repeated=False, packed=False),
            'orderRequestMessageId': FieldDescriptor('orderRequestMessageId', 13, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'catalogType': FieldDescriptor('catalogType', 15, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PaymentExtendedMetadata(MessageBase):
        FIELDS = {
            'type': FieldDescriptor('type', 1, 'uint32', repeated=False, packed=False),
            'platform': FieldDescriptor('platform', 2, 'string', repeated=False, packed=False),
            'messageParamsJson': FieldDescriptor('messageParamsJson', 3, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PaymentInviteMessage(MessageBase):
        class ServiceType(enum.IntEnum):
            UNKNOWN = 0
            FBPAY = 1
            NOVI = 2
            UPI = 3
        FIELDS = {
            'serviceType': FieldDescriptor('serviceType', 1, "enum", repeated=False, packed=False, _enum_path='Message.PaymentInviteMessage.ServiceType'),
            'expiryTimestamp': FieldDescriptor('expiryTimestamp', 2, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PaymentLinkMetadata(MessageBase):
        class PaymentLinkButton(MessageBase):
            FIELDS = {
                'displayText': FieldDescriptor('displayText', 1, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class PaymentLinkHeader(MessageBase):
            class PaymentLinkHeaderType(enum.IntEnum):
                LINK_PREVIEW = 0
                ORDER = 1
            FIELDS = {
                'headerType': FieldDescriptor('headerType', 1, "enum", repeated=False, packed=False, _enum_path='Message.PaymentLinkMetadata.PaymentLinkHeader.PaymentLinkHeaderType'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class PaymentLinkProvider(MessageBase):
            FIELDS = {
                'paramsJson': FieldDescriptor('paramsJson', 1, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'button': FieldDescriptor('button', 1, "message", repeated=False, packed=False, _msg_path='Message.PaymentLinkMetadata.PaymentLinkButton'),
            'header': FieldDescriptor('header', 2, "message", repeated=False, packed=False, _msg_path='Message.PaymentLinkMetadata.PaymentLinkHeader'),
            'provider': FieldDescriptor('provider', 3, "message", repeated=False, packed=False, _msg_path='Message.PaymentLinkMetadata.PaymentLinkProvider'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PeerDataOperationRequestMessage(MessageBase):
        class FullHistorySyncOnDemandRequest(MessageBase):
            FIELDS = {
                'requestMetadata': FieldDescriptor('requestMetadata', 1, "message", repeated=False, packed=False, _msg_path='Message.FullHistorySyncOnDemandRequestMetadata'),
                'historySyncConfig': FieldDescriptor('historySyncConfig', 2, "message", repeated=False, packed=False, _msg_path='DeviceProps.HistorySyncConfig'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class GalaxyFlowAction(MessageBase):
            class GalaxyFlowActionType(enum.IntEnum):
                NOTIFY_LAUNCH = 1
            FIELDS = {
                'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='Message.PeerDataOperationRequestMessage.GalaxyFlowAction.GalaxyFlowActionType'),
                'flowId': FieldDescriptor('flowId', 2, 'string', repeated=False, packed=False),
                'stanzaId': FieldDescriptor('stanzaId', 3, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class HistorySyncChunkRetryRequest(MessageBase):
            FIELDS = {
                'syncType': FieldDescriptor('syncType', 1, "enum", repeated=False, packed=False, _enum_path='Message.HistorySyncType'),
                'chunkOrder': FieldDescriptor('chunkOrder', 2, 'uint32', repeated=False, packed=False),
                'chunkNotificationId': FieldDescriptor('chunkNotificationId', 3, 'string', repeated=False, packed=False),
                'regenerateChunk': FieldDescriptor('regenerateChunk', 4, 'bool', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class HistorySyncOnDemandRequest(MessageBase):
            FIELDS = {
                'chatJid': FieldDescriptor('chatJid', 1, 'string', repeated=False, packed=False),
                'oldestMsgId': FieldDescriptor('oldestMsgId', 2, 'string', repeated=False, packed=False),
                'oldestMsgFromMe': FieldDescriptor('oldestMsgFromMe', 3, 'bool', repeated=False, packed=False),
                'onDemandMsgCount': FieldDescriptor('onDemandMsgCount', 4, 'int32', repeated=False, packed=False),
                'oldestMsgTimestampMs': FieldDescriptor('oldestMsgTimestampMs', 5, 'int64', repeated=False, packed=False),
                'accountLid': FieldDescriptor('accountLid', 6, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class PlaceholderMessageResendRequest(MessageBase):
            FIELDS = {
                'messageKey': FieldDescriptor('messageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class RequestStickerReupload(MessageBase):
            FIELDS = {
                'fileSha256': FieldDescriptor('fileSha256', 1, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class RequestUrlPreview(MessageBase):
            FIELDS = {
                'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
                'includeHqThumbnail': FieldDescriptor('includeHqThumbnail', 2, 'bool', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class SyncDCollectionFatalRecoveryRequest(MessageBase):
            FIELDS = {
                'collectionName': FieldDescriptor('collectionName', 1, 'string', repeated=False, packed=False),
                'timestamp': FieldDescriptor('timestamp', 2, 'int64', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'peerDataOperationRequestType': FieldDescriptor('peerDataOperationRequestType', 1, "enum", repeated=False, packed=False, _enum_path='Message.PeerDataOperationRequestType'),
            'requestStickerReupload': FieldDescriptor('requestStickerReupload', 2, "message", repeated=True, packed=False, _msg_path='Message.PeerDataOperationRequestMessage.RequestStickerReupload'),
            'requestUrlPreview': FieldDescriptor('requestUrlPreview', 3, "message", repeated=True, packed=False, _msg_path='Message.PeerDataOperationRequestMessage.RequestUrlPreview'),
            'historySyncOnDemandRequest': FieldDescriptor('historySyncOnDemandRequest', 4, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestMessage.HistorySyncOnDemandRequest'),
            'placeholderMessageResendRequest': FieldDescriptor('placeholderMessageResendRequest', 5, "message", repeated=True, packed=False, _msg_path='Message.PeerDataOperationRequestMessage.PlaceholderMessageResendRequest'),
            'fullHistorySyncOnDemandRequest': FieldDescriptor('fullHistorySyncOnDemandRequest', 6, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestMessage.FullHistorySyncOnDemandRequest'),
            'syncdCollectionFatalRecoveryRequest': FieldDescriptor('syncdCollectionFatalRecoveryRequest', 7, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestMessage.SyncDCollectionFatalRecoveryRequest'),
            'historySyncChunkRetryRequest': FieldDescriptor('historySyncChunkRetryRequest', 8, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestMessage.HistorySyncChunkRetryRequest'),
            'galaxyFlowAction': FieldDescriptor('galaxyFlowAction', 9, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestMessage.GalaxyFlowAction'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PeerDataOperationRequestResponseMessage(MessageBase):
        class PeerDataOperationResult(MessageBase):
            class FullHistorySyncOnDemandResponseCode(enum.IntEnum):
                REQUEST_SUCCESS = 0
                REQUEST_TIME_EXPIRED = 1
                DECLINED_SHARING_HISTORY = 2
                GENERIC_ERROR = 3
                ERROR_REQUEST_ON_NON_SMB_PRIMARY = 4
                ERROR_HOSTED_DEVICE_NOT_CONNECTED = 5
                ERROR_HOSTED_DEVICE_LOGIN_TIME_NOT_SET = 6
            class HistorySyncChunkRetryResponseCode(enum.IntEnum):
                GENERATION_ERROR = 1
                CHUNK_CONSUMED = 2
                TIMEOUT = 3
                SESSION_EXHAUSTED = 4
                CHUNK_EXHAUSTED = 5
                DUPLICATED_REQUEST = 6
            class CompanionCanonicalUserNonceFetchResponse(MessageBase):
                FIELDS = {
                    'nonce': FieldDescriptor('nonce', 1, 'string', repeated=False, packed=False),
                    'waFbid': FieldDescriptor('waFbid', 2, 'string', repeated=False, packed=False),
                    'forceRefresh': FieldDescriptor('forceRefresh', 3, 'bool', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class CompanionMetaNonceFetchResponse(MessageBase):
                FIELDS = {
                    'nonce': FieldDescriptor('nonce', 1, 'string', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class FullHistorySyncOnDemandRequestResponse(MessageBase):
                FIELDS = {
                    'requestMetadata': FieldDescriptor('requestMetadata', 1, "message", repeated=False, packed=False, _msg_path='Message.FullHistorySyncOnDemandRequestMetadata'),
                    'responseCode': FieldDescriptor('responseCode', 2, "enum", repeated=False, packed=False, _enum_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.FullHistorySyncOnDemandResponseCode'),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class HistorySyncChunkRetryResponse(MessageBase):
                FIELDS = {
                    'syncType': FieldDescriptor('syncType', 1, "enum", repeated=False, packed=False, _enum_path='Message.HistorySyncType'),
                    'chunkOrder': FieldDescriptor('chunkOrder', 2, 'uint32', repeated=False, packed=False),
                    'requestId': FieldDescriptor('requestId', 3, 'string', repeated=False, packed=False),
                    'responseCode': FieldDescriptor('responseCode', 4, "enum", repeated=False, packed=False, _enum_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.HistorySyncChunkRetryResponseCode'),
                    'canRecover': FieldDescriptor('canRecover', 5, 'bool', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class LinkPreviewResponse(MessageBase):
                class LinkPreviewHighQualityThumbnail(MessageBase):
                    FIELDS = {
                        'directPath': FieldDescriptor('directPath', 1, 'string', repeated=False, packed=False),
                        'thumbHash': FieldDescriptor('thumbHash', 2, 'string', repeated=False, packed=False),
                        'encThumbHash': FieldDescriptor('encThumbHash', 3, 'string', repeated=False, packed=False),
                        'mediaKey': FieldDescriptor('mediaKey', 4, 'bytes', repeated=False, packed=False),
                        'mediaKeyTimestampMs': FieldDescriptor('mediaKeyTimestampMs', 5, 'int64', repeated=False, packed=False),
                        'thumbWidth': FieldDescriptor('thumbWidth', 6, 'int32', repeated=False, packed=False),
                        'thumbHeight': FieldDescriptor('thumbHeight', 7, 'int32', repeated=False, packed=False),
                    }
                    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
                class PaymentLinkPreviewMetadata(MessageBase):
                    FIELDS = {
                        'isBusinessVerified': FieldDescriptor('isBusinessVerified', 1, 'bool', repeated=False, packed=False),
                        'providerName': FieldDescriptor('providerName', 2, 'string', repeated=False, packed=False),
                    }
                    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
                FIELDS = {
                    'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
                    'title': FieldDescriptor('title', 2, 'string', repeated=False, packed=False),
                    'description': FieldDescriptor('description', 3, 'string', repeated=False, packed=False),
                    'thumbData': FieldDescriptor('thumbData', 4, 'bytes', repeated=False, packed=False),
                    'matchText': FieldDescriptor('matchText', 6, 'string', repeated=False, packed=False),
                    'previewType': FieldDescriptor('previewType', 7, 'string', repeated=False, packed=False),
                    'hqThumbnail': FieldDescriptor('hqThumbnail', 8, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.LinkPreviewResponse.LinkPreviewHighQualityThumbnail'),
                    'previewMetadata': FieldDescriptor('previewMetadata', 9, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.LinkPreviewResponse.PaymentLinkPreviewMetadata'),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class PlaceholderMessageResendResponse(MessageBase):
                FIELDS = {
                    'webMessageInfoBytes': FieldDescriptor('webMessageInfoBytes', 1, 'bytes', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class SyncDSnapshotFatalRecoveryResponse(MessageBase):
                FIELDS = {
                    'collectionSnapshot': FieldDescriptor('collectionSnapshot', 1, 'bytes', repeated=False, packed=False),
                    'isCompressed': FieldDescriptor('isCompressed', 2, 'bool', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            class WaffleNonceFetchResponse(MessageBase):
                FIELDS = {
                    'nonce': FieldDescriptor('nonce', 1, 'string', repeated=False, packed=False),
                    'waEntFbid': FieldDescriptor('waEntFbid', 2, 'string', repeated=False, packed=False),
                }
                _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
            FIELDS = {
                'mediaUploadResult': FieldDescriptor('mediaUploadResult', 1, "enum", repeated=False, packed=False, _enum_path='MediaRetryNotification.ResultType'),
                'stickerMessage': FieldDescriptor('stickerMessage', 2, "message", repeated=False, packed=False, _msg_path='Message.StickerMessage'),
                'linkPreviewResponse': FieldDescriptor('linkPreviewResponse', 3, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.LinkPreviewResponse'),
                'placeholderMessageResendResponse': FieldDescriptor('placeholderMessageResendResponse', 4, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.PlaceholderMessageResendResponse'),
                'waffleNonceFetchRequestResponse': FieldDescriptor('waffleNonceFetchRequestResponse', 5, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.WaffleNonceFetchResponse'),
                'fullHistorySyncOnDemandRequestResponse': FieldDescriptor('fullHistorySyncOnDemandRequestResponse', 6, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.FullHistorySyncOnDemandRequestResponse'),
                'companionMetaNonceFetchRequestResponse': FieldDescriptor('companionMetaNonceFetchRequestResponse', 7, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.CompanionMetaNonceFetchResponse'),
                'syncdSnapshotFatalRecoveryResponse': FieldDescriptor('syncdSnapshotFatalRecoveryResponse', 8, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.SyncDSnapshotFatalRecoveryResponse'),
                'companionCanonicalUserNonceFetchRequestResponse': FieldDescriptor('companionCanonicalUserNonceFetchRequestResponse', 9, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.CompanionCanonicalUserNonceFetchResponse'),
                'historySyncChunkRetryResponse': FieldDescriptor('historySyncChunkRetryResponse', 10, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult.HistorySyncChunkRetryResponse'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'peerDataOperationRequestType': FieldDescriptor('peerDataOperationRequestType', 1, "enum", repeated=False, packed=False, _enum_path='Message.PeerDataOperationRequestType'),
            'stanzaId': FieldDescriptor('stanzaId', 2, 'string', repeated=False, packed=False),
            'peerDataOperationResult': FieldDescriptor('peerDataOperationResult', 3, "message", repeated=True, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage.PeerDataOperationResult'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PinInChatMessage(MessageBase):
        class Type(enum.IntEnum):
            UNKNOWN_TYPE = 0
            PIN_FOR_ALL = 1
            UNPIN_FOR_ALL = 2
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'type': FieldDescriptor('type', 2, "enum", repeated=False, packed=False, _enum_path='Message.PinInChatMessage.Type'),
            'senderTimestampMs': FieldDescriptor('senderTimestampMs', 3, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PlaceholderMessage(MessageBase):
        class PlaceholderType(enum.IntEnum):
            MASK_LINKED_DEVICES = 0
        FIELDS = {
            'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='Message.PlaceholderMessage.PlaceholderType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PollCreationMessage(MessageBase):
        class Option(MessageBase):
            FIELDS = {
                'optionName': FieldDescriptor('optionName', 1, 'string', repeated=False, packed=False),
                'optionHash': FieldDescriptor('optionHash', 2, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'encKey': FieldDescriptor('encKey', 1, 'bytes', repeated=False, packed=False),
            'name': FieldDescriptor('name', 2, 'string', repeated=False, packed=False),
            'options': FieldDescriptor('options', 3, "message", repeated=True, packed=False, _msg_path='Message.PollCreationMessage.Option'),
            'selectableOptionsCount': FieldDescriptor('selectableOptionsCount', 4, 'uint32', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 5, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'pollContentType': FieldDescriptor('pollContentType', 6, "enum", repeated=False, packed=False, _enum_path='Message.PollContentType'),
            'pollType': FieldDescriptor('pollType', 7, "enum", repeated=False, packed=False, _enum_path='Message.PollType'),
            'correctAnswer': FieldDescriptor('correctAnswer', 8, "message", repeated=False, packed=False, _msg_path='Message.PollCreationMessage.Option'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PollEncValue(MessageBase):
        FIELDS = {
            'encPayload': FieldDescriptor('encPayload', 1, 'bytes', repeated=False, packed=False),
            'encIv': FieldDescriptor('encIv', 2, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PollResultSnapshotMessage(MessageBase):
        class PollVote(MessageBase):
            FIELDS = {
                'optionName': FieldDescriptor('optionName', 1, 'string', repeated=False, packed=False),
                'optionVoteCount': FieldDescriptor('optionVoteCount', 2, 'int64', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'name': FieldDescriptor('name', 1, 'string', repeated=False, packed=False),
            'pollVotes': FieldDescriptor('pollVotes', 2, "message", repeated=True, packed=False, _msg_path='Message.PollResultSnapshotMessage.PollVote'),
            'contextInfo': FieldDescriptor('contextInfo', 3, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'pollType': FieldDescriptor('pollType', 4, "enum", repeated=False, packed=False, _enum_path='Message.PollType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PollUpdateMessage(MessageBase):
        FIELDS = {
            'pollCreationMessageKey': FieldDescriptor('pollCreationMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'vote': FieldDescriptor('vote', 2, "message", repeated=False, packed=False, _msg_path='Message.PollEncValue'),
            'metadata': FieldDescriptor('metadata', 3, "message", repeated=False, packed=False, _msg_path='Message.PollUpdateMessageMetadata'),
            'senderTimestampMs': FieldDescriptor('senderTimestampMs', 4, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PollUpdateMessageMetadata(MessageBase):
        FIELDS = {
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PollVoteMessage(MessageBase):
        FIELDS = {
            'selectedOptions': FieldDescriptor('selectedOptions', 1, 'bytes', repeated=True, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ProductMessage(MessageBase):
        class CatalogSnapshot(MessageBase):
            FIELDS = {
                'catalogImage': FieldDescriptor('catalogImage', 1, "message", repeated=False, packed=False, _msg_path='Message.ImageMessage'),
                'title': FieldDescriptor('title', 2, 'string', repeated=False, packed=False),
                'description': FieldDescriptor('description', 3, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class ProductSnapshot(MessageBase):
            FIELDS = {
                'productImage': FieldDescriptor('productImage', 1, "message", repeated=False, packed=False, _msg_path='Message.ImageMessage'),
                'productId': FieldDescriptor('productId', 2, 'string', repeated=False, packed=False),
                'title': FieldDescriptor('title', 3, 'string', repeated=False, packed=False),
                'description': FieldDescriptor('description', 4, 'string', repeated=False, packed=False),
                'currencyCode': FieldDescriptor('currencyCode', 5, 'string', repeated=False, packed=False),
                'priceAmount1000': FieldDescriptor('priceAmount1000', 6, 'int64', repeated=False, packed=False),
                'retailerId': FieldDescriptor('retailerId', 7, 'string', repeated=False, packed=False),
                'url': FieldDescriptor('url', 8, 'string', repeated=False, packed=False),
                'productImageCount': FieldDescriptor('productImageCount', 9, 'uint32', repeated=False, packed=False),
                'firstImageId': FieldDescriptor('firstImageId', 11, 'string', repeated=False, packed=False),
                'salePriceAmount1000': FieldDescriptor('salePriceAmount1000', 12, 'int64', repeated=False, packed=False),
                'signedUrl': FieldDescriptor('signedUrl', 13, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'product': FieldDescriptor('product', 1, "message", repeated=False, packed=False, _msg_path='Message.ProductMessage.ProductSnapshot'),
            'businessOwnerJid': FieldDescriptor('businessOwnerJid', 2, 'string', repeated=False, packed=False),
            'catalog': FieldDescriptor('catalog', 4, "message", repeated=False, packed=False, _msg_path='Message.ProductMessage.CatalogSnapshot'),
            'body': FieldDescriptor('body', 5, 'string', repeated=False, packed=False),
            'footer': FieldDescriptor('footer', 6, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ProtocolMessage(MessageBase):
        class Type(enum.IntEnum):
            REVOKE = 0
            EPHEMERAL_SETTING = 3
            EPHEMERAL_SYNC_RESPONSE = 4
            HISTORY_SYNC_NOTIFICATION = 5
            APP_STATE_SYNC_KEY_SHARE = 6
            APP_STATE_SYNC_KEY_REQUEST = 7
            MSG_FANOUT_BACKFILL_REQUEST = 8
            INITIAL_SECURITY_NOTIFICATION_SETTING_SYNC = 9
            APP_STATE_FATAL_EXCEPTION_NOTIFICATION = 10
            SHARE_PHONE_NUMBER = 11
            MESSAGE_EDIT = 14
            PEER_DATA_OPERATION_REQUEST_MESSAGE = 16
            PEER_DATA_OPERATION_REQUEST_RESPONSE_MESSAGE = 17
            REQUEST_WELCOME_MESSAGE = 18
            BOT_FEEDBACK_MESSAGE = 19
            MEDIA_NOTIFY_MESSAGE = 20
            CLOUD_API_THREAD_CONTROL_NOTIFICATION = 21
            LID_MIGRATION_MAPPING_SYNC = 22
            REMINDER_MESSAGE = 23
            BOT_MEMU_ONBOARDING_MESSAGE = 24
            STATUS_MENTION_MESSAGE = 25
            STOP_GENERATION_MESSAGE = 26
            LIMIT_SHARING = 27
            AI_PSI_METADATA = 28
            AI_QUERY_FANOUT = 29
            GROUP_MEMBER_LABEL_CHANGE = 30
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'type': FieldDescriptor('type', 2, "enum", repeated=False, packed=False, _enum_path='Message.ProtocolMessage.Type'),
            'ephemeralExpiration': FieldDescriptor('ephemeralExpiration', 4, 'uint32', repeated=False, packed=False),
            'ephemeralSettingTimestamp': FieldDescriptor('ephemeralSettingTimestamp', 5, 'int64', repeated=False, packed=False),
            'historySyncNotification': FieldDescriptor('historySyncNotification', 6, "message", repeated=False, packed=False, _msg_path='Message.HistorySyncNotification'),
            'appStateSyncKeyShare': FieldDescriptor('appStateSyncKeyShare', 7, "message", repeated=False, packed=False, _msg_path='Message.AppStateSyncKeyShare'),
            'appStateSyncKeyRequest': FieldDescriptor('appStateSyncKeyRequest', 8, "message", repeated=False, packed=False, _msg_path='Message.AppStateSyncKeyRequest'),
            'initialSecurityNotificationSettingSync': FieldDescriptor('initialSecurityNotificationSettingSync', 9, "message", repeated=False, packed=False, _msg_path='Message.InitialSecurityNotificationSettingSync'),
            'appStateFatalExceptionNotification': FieldDescriptor('appStateFatalExceptionNotification', 10, "message", repeated=False, packed=False, _msg_path='Message.AppStateFatalExceptionNotification'),
            'disappearingMode': FieldDescriptor('disappearingMode', 11, "message", repeated=False, packed=False, _msg_path='DisappearingMode'),
            'editedMessage': FieldDescriptor('editedMessage', 14, "message", repeated=False, packed=False, _msg_path='Message'),
            'timestampMs': FieldDescriptor('timestampMs', 15, 'int64', repeated=False, packed=False),
            'peerDataOperationRequestMessage': FieldDescriptor('peerDataOperationRequestMessage', 16, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestMessage'),
            'peerDataOperationRequestResponseMessage': FieldDescriptor('peerDataOperationRequestResponseMessage', 17, "message", repeated=False, packed=False, _msg_path='Message.PeerDataOperationRequestResponseMessage'),
            'botFeedbackMessage': FieldDescriptor('botFeedbackMessage', 18, "message", repeated=False, packed=False, _msg_path='BotFeedbackMessage'),
            'invokerJid': FieldDescriptor('invokerJid', 19, 'string', repeated=False, packed=False),
            'requestWelcomeMessageMetadata': FieldDescriptor('requestWelcomeMessageMetadata', 20, "message", repeated=False, packed=False, _msg_path='Message.RequestWelcomeMessageMetadata'),
            'mediaNotifyMessage': FieldDescriptor('mediaNotifyMessage', 21, "message", repeated=False, packed=False, _msg_path='MediaNotifyMessage'),
            'cloudApiThreadControlNotification': FieldDescriptor('cloudApiThreadControlNotification', 22, "message", repeated=False, packed=False, _msg_path='Message.CloudAPIThreadControlNotification'),
            'lidMigrationMappingSyncMessage': FieldDescriptor('lidMigrationMappingSyncMessage', 23, "message", repeated=False, packed=False, _msg_path='LIDMigrationMappingSyncMessage'),
            'limitSharing': FieldDescriptor('limitSharing', 24, "message", repeated=False, packed=False, _msg_path='LimitSharing'),
            'aiPsiMetadata': FieldDescriptor('aiPsiMetadata', 25, 'bytes', repeated=False, packed=False),
            'aiQueryFanout': FieldDescriptor('aiQueryFanout', 26, "message", repeated=False, packed=False, _msg_path='AIQueryFanout'),
            'memberLabel': FieldDescriptor('memberLabel', 27, "message", repeated=False, packed=False, _msg_path='MemberLabel'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class QuestionResponseMessage(MessageBase):
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'text': FieldDescriptor('text', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ReactionMessage(MessageBase):
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'text': FieldDescriptor('text', 2, 'string', repeated=False, packed=False),
            'groupingKey': FieldDescriptor('groupingKey', 3, 'string', repeated=False, packed=False),
            'senderTimestampMs': FieldDescriptor('senderTimestampMs', 4, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class RequestPaymentMessage(MessageBase):
        FIELDS = {
            'noteMessage': FieldDescriptor('noteMessage', 4, "message", repeated=False, packed=False, _msg_path='Message'),
            'currencyCodeIso4217': FieldDescriptor('currencyCodeIso4217', 1, 'string', repeated=False, packed=False),
            'amount1000': FieldDescriptor('amount1000', 2, 'uint64', repeated=False, packed=False),
            'requestFrom': FieldDescriptor('requestFrom', 3, 'string', repeated=False, packed=False),
            'expiryTimestamp': FieldDescriptor('expiryTimestamp', 5, 'int64', repeated=False, packed=False),
            'amount': FieldDescriptor('amount', 6, "message", repeated=False, packed=False, _msg_path='Money'),
            'background': FieldDescriptor('background', 7, "message", repeated=False, packed=False, _msg_path='PaymentBackground'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class RequestPhoneNumberMessage(MessageBase):
        FIELDS = {
            'contextInfo': FieldDescriptor('contextInfo', 1, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class RequestWelcomeMessageMetadata(MessageBase):
        class LocalChatState(enum.IntEnum):
            EMPTY = 0
            NON_EMPTY = 1
        FIELDS = {
            'localChatState': FieldDescriptor('localChatState', 1, "enum", repeated=False, packed=False, _enum_path='Message.RequestWelcomeMessageMetadata.LocalChatState'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ScheduledCallCreationMessage(MessageBase):
        class CallType(enum.IntEnum):
            UNKNOWN = 0
            VOICE = 1
            VIDEO = 2
        FIELDS = {
            'scheduledTimestampMs': FieldDescriptor('scheduledTimestampMs', 1, 'int64', repeated=False, packed=False),
            'callType': FieldDescriptor('callType', 2, "enum", repeated=False, packed=False, _enum_path='Message.ScheduledCallCreationMessage.CallType'),
            'title': FieldDescriptor('title', 3, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ScheduledCallEditMessage(MessageBase):
        class EditType(enum.IntEnum):
            UNKNOWN = 0
            CANCEL = 1
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'editType': FieldDescriptor('editType', 2, "enum", repeated=False, packed=False, _enum_path='Message.ScheduledCallEditMessage.EditType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class SecretEncryptedMessage(MessageBase):
        class SecretEncType(enum.IntEnum):
            UNKNOWN = 0
            EVENT_EDIT = 1
            MESSAGE_EDIT = 2
        FIELDS = {
            'targetMessageKey': FieldDescriptor('targetMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'encPayload': FieldDescriptor('encPayload', 2, 'bytes', repeated=False, packed=False),
            'encIv': FieldDescriptor('encIv', 3, 'bytes', repeated=False, packed=False),
            'secretEncType': FieldDescriptor('secretEncType', 4, "enum", repeated=False, packed=False, _enum_path='Message.SecretEncryptedMessage.SecretEncType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class SendPaymentMessage(MessageBase):
        FIELDS = {
            'noteMessage': FieldDescriptor('noteMessage', 2, "message", repeated=False, packed=False, _msg_path='Message'),
            'requestMessageKey': FieldDescriptor('requestMessageKey', 3, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'background': FieldDescriptor('background', 4, "message", repeated=False, packed=False, _msg_path='PaymentBackground'),
            'transactionData': FieldDescriptor('transactionData', 5, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class SenderKeyDistributionMessage(MessageBase):
        FIELDS = {
            'groupId': FieldDescriptor('groupId', 1, 'string', repeated=False, packed=False),
            'axolotlSenderKeyDistributionMessage': FieldDescriptor('axolotlSenderKeyDistributionMessage', 2, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StatusNotificationMessage(MessageBase):
        class StatusNotificationType(enum.IntEnum):
            UNKNOWN = 0
            STATUS_ADD_YOURS = 1
            STATUS_RESHARE = 2
            STATUS_QUESTION_ANSWER_RESHARE = 3
        FIELDS = {
            'responseMessageKey': FieldDescriptor('responseMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'originalMessageKey': FieldDescriptor('originalMessageKey', 2, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'type': FieldDescriptor('type', 3, "enum", repeated=False, packed=False, _enum_path='Message.StatusNotificationMessage.StatusNotificationType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StatusQuestionAnswerMessage(MessageBase):
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'text': FieldDescriptor('text', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StatusQuotedMessage(MessageBase):
        class StatusQuotedMessageType(enum.IntEnum):
            QUESTION_ANSWER = 1
        FIELDS = {
            'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='Message.StatusQuotedMessage.StatusQuotedMessageType'),
            'text': FieldDescriptor('text', 2, 'string', repeated=False, packed=False),
            'thumbnail': FieldDescriptor('thumbnail', 3, 'bytes', repeated=False, packed=False),
            'originalStatusId': FieldDescriptor('originalStatusId', 4, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StatusStickerInteractionMessage(MessageBase):
        class StatusStickerType(enum.IntEnum):
            UNKNOWN = 0
            REACTION = 1
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'stickerKey': FieldDescriptor('stickerKey', 2, 'string', repeated=False, packed=False),
            'type': FieldDescriptor('type', 3, "enum", repeated=False, packed=False, _enum_path='Message.StatusStickerInteractionMessage.StatusStickerType'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StickerMessage(MessageBase):
        FIELDS = {
            'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
            'fileSha256': FieldDescriptor('fileSha256', 2, 'bytes', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 3, 'bytes', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 4, 'bytes', repeated=False, packed=False),
            'mimetype': FieldDescriptor('mimetype', 5, 'string', repeated=False, packed=False),
            'height': FieldDescriptor('height', 6, 'uint32', repeated=False, packed=False),
            'width': FieldDescriptor('width', 7, 'uint32', repeated=False, packed=False),
            'directPath': FieldDescriptor('directPath', 8, 'string', repeated=False, packed=False),
            'fileLength': FieldDescriptor('fileLength', 9, 'uint64', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 10, 'int64', repeated=False, packed=False),
            'firstFrameLength': FieldDescriptor('firstFrameLength', 11, 'uint32', repeated=False, packed=False),
            'firstFrameSidecar': FieldDescriptor('firstFrameSidecar', 12, 'bytes', repeated=False, packed=False),
            'isAnimated': FieldDescriptor('isAnimated', 13, 'bool', repeated=False, packed=False),
            'pngThumbnail': FieldDescriptor('pngThumbnail', 16, 'bytes', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'stickerSentTs': FieldDescriptor('stickerSentTs', 18, 'int64', repeated=False, packed=False),
            'isAvatar': FieldDescriptor('isAvatar', 19, 'bool', repeated=False, packed=False),
            'isAiSticker': FieldDescriptor('isAiSticker', 20, 'bool', repeated=False, packed=False),
            'isLottie': FieldDescriptor('isLottie', 21, 'bool', repeated=False, packed=False),
            'accessibilityLabel': FieldDescriptor('accessibilityLabel', 22, 'string', repeated=False, packed=False),
            'mediaKeyDomain': FieldDescriptor('mediaKeyDomain', 23, "enum", repeated=False, packed=False, _enum_path='Message.MediaKeyDomain'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StickerPackMessage(MessageBase):
        class StickerPackOrigin(enum.IntEnum):
            FIRST_PARTY = 0
            THIRD_PARTY = 1
            USER_CREATED = 2
        class Sticker(MessageBase):
            FIELDS = {
                'fileName': FieldDescriptor('fileName', 1, 'string', repeated=False, packed=False),
                'isAnimated': FieldDescriptor('isAnimated', 2, 'bool', repeated=False, packed=False),
                'emojis': FieldDescriptor('emojis', 3, 'string', repeated=True, packed=False),
                'accessibilityLabel': FieldDescriptor('accessibilityLabel', 4, 'string', repeated=False, packed=False),
                'isLottie': FieldDescriptor('isLottie', 5, 'bool', repeated=False, packed=False),
                'mimetype': FieldDescriptor('mimetype', 6, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'stickerPackId': FieldDescriptor('stickerPackId', 1, 'string', repeated=False, packed=False),
            'name': FieldDescriptor('name', 2, 'string', repeated=False, packed=False),
            'publisher': FieldDescriptor('publisher', 3, 'string', repeated=False, packed=False),
            'stickers': FieldDescriptor('stickers', 4, "message", repeated=True, packed=False, _msg_path='Message.StickerPackMessage.Sticker'),
            'fileLength': FieldDescriptor('fileLength', 5, 'uint64', repeated=False, packed=False),
            'fileSha256': FieldDescriptor('fileSha256', 6, 'bytes', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 7, 'bytes', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 8, 'bytes', repeated=False, packed=False),
            'directPath': FieldDescriptor('directPath', 9, 'string', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 10, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 11, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'packDescription': FieldDescriptor('packDescription', 12, 'string', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 13, 'int64', repeated=False, packed=False),
            'trayIconFileName': FieldDescriptor('trayIconFileName', 14, 'string', repeated=False, packed=False),
            'thumbnailDirectPath': FieldDescriptor('thumbnailDirectPath', 15, 'string', repeated=False, packed=False),
            'thumbnailSha256': FieldDescriptor('thumbnailSha256', 16, 'bytes', repeated=False, packed=False),
            'thumbnailEncSha256': FieldDescriptor('thumbnailEncSha256', 17, 'bytes', repeated=False, packed=False),
            'thumbnailHeight': FieldDescriptor('thumbnailHeight', 18, 'uint32', repeated=False, packed=False),
            'thumbnailWidth': FieldDescriptor('thumbnailWidth', 19, 'uint32', repeated=False, packed=False),
            'imageDataHash': FieldDescriptor('imageDataHash', 20, 'string', repeated=False, packed=False),
            'stickerPackSize': FieldDescriptor('stickerPackSize', 21, 'uint64', repeated=False, packed=False),
            'stickerPackOrigin': FieldDescriptor('stickerPackOrigin', 22, "enum", repeated=False, packed=False, _enum_path='Message.StickerPackMessage.StickerPackOrigin'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StickerSyncRMRMessage(MessageBase):
        FIELDS = {
            'filehash': FieldDescriptor('filehash', 1, 'string', repeated=True, packed=False),
            'rmrSource': FieldDescriptor('rmrSource', 2, 'string', repeated=False, packed=False),
            'requestTimestamp': FieldDescriptor('requestTimestamp', 3, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class TemplateButtonReplyMessage(MessageBase):
        FIELDS = {
            'selectedId': FieldDescriptor('selectedId', 1, 'string', repeated=False, packed=False),
            'selectedDisplayText': FieldDescriptor('selectedDisplayText', 2, 'string', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 3, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'selectedIndex': FieldDescriptor('selectedIndex', 4, 'uint32', repeated=False, packed=False),
            'selectedCarouselCardIndex': FieldDescriptor('selectedCarouselCardIndex', 5, 'uint32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class TemplateMessage(MessageBase):
        class FourRowTemplate(MessageBase):
            FIELDS = {
                'content': FieldDescriptor('content', 6, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage'),
                'footer': FieldDescriptor('footer', 7, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage'),
                'buttons': FieldDescriptor('buttons', 8, "message", repeated=True, packed=False, _msg_path='TemplateButton'),
                'documentMessage': FieldDescriptor('documentMessage', 1, "message", repeated=False, packed=False, _msg_path='Message.DocumentMessage'),
                'highlyStructuredMessage': FieldDescriptor('highlyStructuredMessage', 2, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage'),
                'imageMessage': FieldDescriptor('imageMessage', 3, "message", repeated=False, packed=False, _msg_path='Message.ImageMessage'),
                'videoMessage': FieldDescriptor('videoMessage', 4, "message", repeated=False, packed=False, _msg_path='Message.VideoMessage'),
                'locationMessage': FieldDescriptor('locationMessage', 5, "message", repeated=False, packed=False, _msg_path='Message.LocationMessage'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class HydratedFourRowTemplate(MessageBase):
            FIELDS = {
                'hydratedContentText': FieldDescriptor('hydratedContentText', 6, 'string', repeated=False, packed=False),
                'hydratedFooterText': FieldDescriptor('hydratedFooterText', 7, 'string', repeated=False, packed=False),
                'hydratedButtons': FieldDescriptor('hydratedButtons', 8, "message", repeated=True, packed=False, _msg_path='HydratedTemplateButton'),
                'templateId': FieldDescriptor('templateId', 9, 'string', repeated=False, packed=False),
                'maskLinkedDevices': FieldDescriptor('maskLinkedDevices', 10, 'bool', repeated=False, packed=False),
                'documentMessage': FieldDescriptor('documentMessage', 1, "message", repeated=False, packed=False, _msg_path='Message.DocumentMessage'),
                'hydratedTitleText': FieldDescriptor('hydratedTitleText', 2, 'string', repeated=False, packed=False),
                'imageMessage': FieldDescriptor('imageMessage', 3, "message", repeated=False, packed=False, _msg_path='Message.ImageMessage'),
                'videoMessage': FieldDescriptor('videoMessage', 4, "message", repeated=False, packed=False, _msg_path='Message.VideoMessage'),
                'locationMessage': FieldDescriptor('locationMessage', 5, "message", repeated=False, packed=False, _msg_path='Message.LocationMessage'),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'contextInfo': FieldDescriptor('contextInfo', 3, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'hydratedTemplate': FieldDescriptor('hydratedTemplate', 4, "message", repeated=False, packed=False, _msg_path='Message.TemplateMessage.HydratedFourRowTemplate'),
            'templateId': FieldDescriptor('templateId', 9, 'string', repeated=False, packed=False),
            'fourRowTemplate': FieldDescriptor('fourRowTemplate', 1, "message", repeated=False, packed=False, _msg_path='Message.TemplateMessage.FourRowTemplate'),
            'hydratedFourRowTemplate': FieldDescriptor('hydratedFourRowTemplate', 2, "message", repeated=False, packed=False, _msg_path='Message.TemplateMessage.HydratedFourRowTemplate'),
            'interactiveMessageTemplate': FieldDescriptor('interactiveMessageTemplate', 5, "message", repeated=False, packed=False, _msg_path='Message.InteractiveMessage'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class URLMetadata(MessageBase):
        FIELDS = {
            'fbExperimentId': FieldDescriptor('fbExperimentId', 1, 'uint32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class VideoEndCard(MessageBase):
        FIELDS = {
            'username': FieldDescriptor('username', 1, 'string', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 2, 'string', repeated=False, packed=False),
            'thumbnailImageUrl': FieldDescriptor('thumbnailImageUrl', 3, 'string', repeated=False, packed=False),
            'profilePictureUrl': FieldDescriptor('profilePictureUrl', 4, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class VideoMessage(MessageBase):
        class Attribution(enum.IntEnum):
            NONE = 0
            GIPHY = 1
            TENOR = 2
            KLIPY = 3
        class VideoSourceType(enum.IntEnum):
            USER_VIDEO = 0
            AI_GENERATED = 1
        FIELDS = {
            'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
            'mimetype': FieldDescriptor('mimetype', 2, 'string', repeated=False, packed=False),
            'fileSha256': FieldDescriptor('fileSha256', 3, 'bytes', repeated=False, packed=False),
            'fileLength': FieldDescriptor('fileLength', 4, 'uint64', repeated=False, packed=False),
            'seconds': FieldDescriptor('seconds', 5, 'uint32', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 6, 'bytes', repeated=False, packed=False),
            'caption': FieldDescriptor('caption', 7, 'string', repeated=False, packed=False),
            'gifPlayback': FieldDescriptor('gifPlayback', 8, 'bool', repeated=False, packed=False),
            'height': FieldDescriptor('height', 9, 'uint32', repeated=False, packed=False),
            'width': FieldDescriptor('width', 10, 'uint32', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 11, 'bytes', repeated=False, packed=False),
            'interactiveAnnotations': FieldDescriptor('interactiveAnnotations', 12, "message", repeated=True, packed=False, _msg_path='InteractiveAnnotation'),
            'directPath': FieldDescriptor('directPath', 13, 'string', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 14, 'int64', repeated=False, packed=False),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 16, 'bytes', repeated=False, packed=False),
            'contextInfo': FieldDescriptor('contextInfo', 17, "message", repeated=False, packed=False, _msg_path='ContextInfo'),
            'streamingSidecar': FieldDescriptor('streamingSidecar', 18, 'bytes', repeated=False, packed=False),
            'gifAttribution': FieldDescriptor('gifAttribution', 19, "enum", repeated=False, packed=False, _enum_path='Message.VideoMessage.Attribution'),
            'viewOnce': FieldDescriptor('viewOnce', 20, 'bool', repeated=False, packed=False),
            'thumbnailDirectPath': FieldDescriptor('thumbnailDirectPath', 21, 'string', repeated=False, packed=False),
            'thumbnailSha256': FieldDescriptor('thumbnailSha256', 22, 'bytes', repeated=False, packed=False),
            'thumbnailEncSha256': FieldDescriptor('thumbnailEncSha256', 23, 'bytes', repeated=False, packed=False),
            'staticUrl': FieldDescriptor('staticUrl', 24, 'string', repeated=False, packed=False),
            'annotations': FieldDescriptor('annotations', 25, "message", repeated=True, packed=False, _msg_path='InteractiveAnnotation'),
            'accessibilityLabel': FieldDescriptor('accessibilityLabel', 26, 'string', repeated=False, packed=False),
            'processedVideos': FieldDescriptor('processedVideos', 27, "message", repeated=True, packed=False, _msg_path='ProcessedVideo'),
            'externalShareFullVideoDurationInSeconds': FieldDescriptor('externalShareFullVideoDurationInSeconds', 28, 'uint32', repeated=False, packed=False),
            'motionPhotoPresentationOffsetMs': FieldDescriptor('motionPhotoPresentationOffsetMs', 29, 'uint64', repeated=False, packed=False),
            'metadataUrl': FieldDescriptor('metadataUrl', 30, 'string', repeated=False, packed=False),
            'videoSourceType': FieldDescriptor('videoSourceType', 31, "enum", repeated=False, packed=False, _enum_path='Message.VideoMessage.VideoSourceType'),
            'mediaKeyDomain': FieldDescriptor('mediaKeyDomain', 32, "enum", repeated=False, packed=False, _enum_path='Message.MediaKeyDomain'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'conversation': FieldDescriptor('conversation', 1, 'string', repeated=False, packed=False),
        'senderKeyDistributionMessage': FieldDescriptor('senderKeyDistributionMessage', 2, "message", repeated=False, packed=False, _msg_path='Message.SenderKeyDistributionMessage'),
        'imageMessage': FieldDescriptor('imageMessage', 3, "message", repeated=False, packed=False, _msg_path='Message.ImageMessage'),
        'contactMessage': FieldDescriptor('contactMessage', 4, "message", repeated=False, packed=False, _msg_path='Message.ContactMessage'),
        'locationMessage': FieldDescriptor('locationMessage', 5, "message", repeated=False, packed=False, _msg_path='Message.LocationMessage'),
        'extendedTextMessage': FieldDescriptor('extendedTextMessage', 6, "message", repeated=False, packed=False, _msg_path='Message.ExtendedTextMessage'),
        'documentMessage': FieldDescriptor('documentMessage', 7, "message", repeated=False, packed=False, _msg_path='Message.DocumentMessage'),
        'audioMessage': FieldDescriptor('audioMessage', 8, "message", repeated=False, packed=False, _msg_path='Message.AudioMessage'),
        'videoMessage': FieldDescriptor('videoMessage', 9, "message", repeated=False, packed=False, _msg_path='Message.VideoMessage'),
        'call': FieldDescriptor('call', 10, "message", repeated=False, packed=False, _msg_path='Message.Call'),
        'chat': FieldDescriptor('chat', 11, "message", repeated=False, packed=False, _msg_path='Message.Chat'),
        'protocolMessage': FieldDescriptor('protocolMessage', 12, "message", repeated=False, packed=False, _msg_path='Message.ProtocolMessage'),
        'contactsArrayMessage': FieldDescriptor('contactsArrayMessage', 13, "message", repeated=False, packed=False, _msg_path='Message.ContactsArrayMessage'),
        'highlyStructuredMessage': FieldDescriptor('highlyStructuredMessage', 14, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage'),
        'fastRatchetKeySenderKeyDistributionMessage': FieldDescriptor('fastRatchetKeySenderKeyDistributionMessage', 15, "message", repeated=False, packed=False, _msg_path='Message.SenderKeyDistributionMessage'),
        'sendPaymentMessage': FieldDescriptor('sendPaymentMessage', 16, "message", repeated=False, packed=False, _msg_path='Message.SendPaymentMessage'),
        'liveLocationMessage': FieldDescriptor('liveLocationMessage', 18, "message", repeated=False, packed=False, _msg_path='Message.LiveLocationMessage'),
        'requestPaymentMessage': FieldDescriptor('requestPaymentMessage', 22, "message", repeated=False, packed=False, _msg_path='Message.RequestPaymentMessage'),
        'declinePaymentRequestMessage': FieldDescriptor('declinePaymentRequestMessage', 23, "message", repeated=False, packed=False, _msg_path='Message.DeclinePaymentRequestMessage'),
        'cancelPaymentRequestMessage': FieldDescriptor('cancelPaymentRequestMessage', 24, "message", repeated=False, packed=False, _msg_path='Message.CancelPaymentRequestMessage'),
        'templateMessage': FieldDescriptor('templateMessage', 25, "message", repeated=False, packed=False, _msg_path='Message.TemplateMessage'),
        'stickerMessage': FieldDescriptor('stickerMessage', 26, "message", repeated=False, packed=False, _msg_path='Message.StickerMessage'),
        'groupInviteMessage': FieldDescriptor('groupInviteMessage', 28, "message", repeated=False, packed=False, _msg_path='Message.GroupInviteMessage'),
        'templateButtonReplyMessage': FieldDescriptor('templateButtonReplyMessage', 29, "message", repeated=False, packed=False, _msg_path='Message.TemplateButtonReplyMessage'),
        'productMessage': FieldDescriptor('productMessage', 30, "message", repeated=False, packed=False, _msg_path='Message.ProductMessage'),
        'deviceSentMessage': FieldDescriptor('deviceSentMessage', 31, "message", repeated=False, packed=False, _msg_path='Message.DeviceSentMessage'),
        'messageContextInfo': FieldDescriptor('messageContextInfo', 35, "message", repeated=False, packed=False, _msg_path='MessageContextInfo'),
        'listMessage': FieldDescriptor('listMessage', 36, "message", repeated=False, packed=False, _msg_path='Message.ListMessage'),
        'viewOnceMessage': FieldDescriptor('viewOnceMessage', 37, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'orderMessage': FieldDescriptor('orderMessage', 38, "message", repeated=False, packed=False, _msg_path='Message.OrderMessage'),
        'listResponseMessage': FieldDescriptor('listResponseMessage', 39, "message", repeated=False, packed=False, _msg_path='Message.ListResponseMessage'),
        'ephemeralMessage': FieldDescriptor('ephemeralMessage', 40, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'invoiceMessage': FieldDescriptor('invoiceMessage', 41, "message", repeated=False, packed=False, _msg_path='Message.InvoiceMessage'),
        'buttonsMessage': FieldDescriptor('buttonsMessage', 42, "message", repeated=False, packed=False, _msg_path='Message.ButtonsMessage'),
        'buttonsResponseMessage': FieldDescriptor('buttonsResponseMessage', 43, "message", repeated=False, packed=False, _msg_path='Message.ButtonsResponseMessage'),
        'paymentInviteMessage': FieldDescriptor('paymentInviteMessage', 44, "message", repeated=False, packed=False, _msg_path='Message.PaymentInviteMessage'),
        'interactiveMessage': FieldDescriptor('interactiveMessage', 45, "message", repeated=False, packed=False, _msg_path='Message.InteractiveMessage'),
        'reactionMessage': FieldDescriptor('reactionMessage', 46, "message", repeated=False, packed=False, _msg_path='Message.ReactionMessage'),
        'stickerSyncRmrMessage': FieldDescriptor('stickerSyncRmrMessage', 47, "message", repeated=False, packed=False, _msg_path='Message.StickerSyncRMRMessage'),
        'interactiveResponseMessage': FieldDescriptor('interactiveResponseMessage', 48, "message", repeated=False, packed=False, _msg_path='Message.InteractiveResponseMessage'),
        'pollCreationMessage': FieldDescriptor('pollCreationMessage', 49, "message", repeated=False, packed=False, _msg_path='Message.PollCreationMessage'),
        'pollUpdateMessage': FieldDescriptor('pollUpdateMessage', 50, "message", repeated=False, packed=False, _msg_path='Message.PollUpdateMessage'),
        'keepInChatMessage': FieldDescriptor('keepInChatMessage', 51, "message", repeated=False, packed=False, _msg_path='Message.KeepInChatMessage'),
        'documentWithCaptionMessage': FieldDescriptor('documentWithCaptionMessage', 53, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'requestPhoneNumberMessage': FieldDescriptor('requestPhoneNumberMessage', 54, "message", repeated=False, packed=False, _msg_path='Message.RequestPhoneNumberMessage'),
        'viewOnceMessageV2': FieldDescriptor('viewOnceMessageV2', 55, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'encReactionMessage': FieldDescriptor('encReactionMessage', 56, "message", repeated=False, packed=False, _msg_path='Message.EncReactionMessage'),
        'editedMessage': FieldDescriptor('editedMessage', 58, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'viewOnceMessageV2Extension': FieldDescriptor('viewOnceMessageV2Extension', 59, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'pollCreationMessageV2': FieldDescriptor('pollCreationMessageV2', 60, "message", repeated=False, packed=False, _msg_path='Message.PollCreationMessage'),
        'scheduledCallCreationMessage': FieldDescriptor('scheduledCallCreationMessage', 61, "message", repeated=False, packed=False, _msg_path='Message.ScheduledCallCreationMessage'),
        'groupMentionedMessage': FieldDescriptor('groupMentionedMessage', 62, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'pinInChatMessage': FieldDescriptor('pinInChatMessage', 63, "message", repeated=False, packed=False, _msg_path='Message.PinInChatMessage'),
        'pollCreationMessageV3': FieldDescriptor('pollCreationMessageV3', 64, "message", repeated=False, packed=False, _msg_path='Message.PollCreationMessage'),
        'scheduledCallEditMessage': FieldDescriptor('scheduledCallEditMessage', 65, "message", repeated=False, packed=False, _msg_path='Message.ScheduledCallEditMessage'),
        'ptvMessage': FieldDescriptor('ptvMessage', 66, "message", repeated=False, packed=False, _msg_path='Message.VideoMessage'),
        'botInvokeMessage': FieldDescriptor('botInvokeMessage', 67, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'callLogMesssage': FieldDescriptor('callLogMesssage', 69, "message", repeated=False, packed=False, _msg_path='Message.CallLogMessage'),
        'messageHistoryBundle': FieldDescriptor('messageHistoryBundle', 70, "message", repeated=False, packed=False, _msg_path='Message.MessageHistoryBundle'),
        'encCommentMessage': FieldDescriptor('encCommentMessage', 71, "message", repeated=False, packed=False, _msg_path='Message.EncCommentMessage'),
        'bcallMessage': FieldDescriptor('bcallMessage', 72, "message", repeated=False, packed=False, _msg_path='Message.BCallMessage'),
        'lottieStickerMessage': FieldDescriptor('lottieStickerMessage', 74, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'eventMessage': FieldDescriptor('eventMessage', 75, "message", repeated=False, packed=False, _msg_path='Message.EventMessage'),
        'encEventResponseMessage': FieldDescriptor('encEventResponseMessage', 76, "message", repeated=False, packed=False, _msg_path='Message.EncEventResponseMessage'),
        'commentMessage': FieldDescriptor('commentMessage', 77, "message", repeated=False, packed=False, _msg_path='Message.CommentMessage'),
        'newsletterAdminInviteMessage': FieldDescriptor('newsletterAdminInviteMessage', 78, "message", repeated=False, packed=False, _msg_path='Message.NewsletterAdminInviteMessage'),
        'placeholderMessage': FieldDescriptor('placeholderMessage', 80, "message", repeated=False, packed=False, _msg_path='Message.PlaceholderMessage'),
        'secretEncryptedMessage': FieldDescriptor('secretEncryptedMessage', 82, "message", repeated=False, packed=False, _msg_path='Message.SecretEncryptedMessage'),
        'albumMessage': FieldDescriptor('albumMessage', 83, "message", repeated=False, packed=False, _msg_path='Message.AlbumMessage'),
        'eventCoverImage': FieldDescriptor('eventCoverImage', 85, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'stickerPackMessage': FieldDescriptor('stickerPackMessage', 86, "message", repeated=False, packed=False, _msg_path='Message.StickerPackMessage'),
        'statusMentionMessage': FieldDescriptor('statusMentionMessage', 87, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'pollResultSnapshotMessage': FieldDescriptor('pollResultSnapshotMessage', 88, "message", repeated=False, packed=False, _msg_path='Message.PollResultSnapshotMessage'),
        'pollCreationOptionImageMessage': FieldDescriptor('pollCreationOptionImageMessage', 90, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'associatedChildMessage': FieldDescriptor('associatedChildMessage', 91, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'groupStatusMentionMessage': FieldDescriptor('groupStatusMentionMessage', 92, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'pollCreationMessageV4': FieldDescriptor('pollCreationMessageV4', 93, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'statusAddYours': FieldDescriptor('statusAddYours', 95, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'groupStatusMessage': FieldDescriptor('groupStatusMessage', 96, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'richResponseMessage': FieldDescriptor('richResponseMessage', 97, "message", repeated=False, packed=False, _msg_path='AIRichResponseMessage'),
        'statusNotificationMessage': FieldDescriptor('statusNotificationMessage', 98, "message", repeated=False, packed=False, _msg_path='Message.StatusNotificationMessage'),
        'limitSharingMessage': FieldDescriptor('limitSharingMessage', 99, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'botTaskMessage': FieldDescriptor('botTaskMessage', 100, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'questionMessage': FieldDescriptor('questionMessage', 101, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'messageHistoryNotice': FieldDescriptor('messageHistoryNotice', 102, "message", repeated=False, packed=False, _msg_path='Message.MessageHistoryNotice'),
        'groupStatusMessageV2': FieldDescriptor('groupStatusMessageV2', 103, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'botForwardedMessage': FieldDescriptor('botForwardedMessage', 104, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'statusQuestionAnswerMessage': FieldDescriptor('statusQuestionAnswerMessage', 105, "message", repeated=False, packed=False, _msg_path='Message.StatusQuestionAnswerMessage'),
        'questionReplyMessage': FieldDescriptor('questionReplyMessage', 106, "message", repeated=False, packed=False, _msg_path='Message.FutureProofMessage'),
        'questionResponseMessage': FieldDescriptor('questionResponseMessage', 107, "message", repeated=False, packed=False, _msg_path='Message.QuestionResponseMessage'),
        'statusQuotedMessage': FieldDescriptor('statusQuotedMessage', 109, "message", repeated=False, packed=False, _msg_path='Message.StatusQuotedMessage'),
        'statusStickerInteractionMessage': FieldDescriptor('statusStickerInteractionMessage', 110, "message", repeated=False, packed=False, _msg_path='Message.StatusStickerInteractionMessage'),
        'pollCreationMessageV5': FieldDescriptor('pollCreationMessageV5', 111, "message", repeated=False, packed=False, _msg_path='Message.PollCreationMessage'),
        'newsletterFollowerInviteMessageV2': FieldDescriptor('newsletterFollowerInviteMessageV2', 113, "message", repeated=False, packed=False, _msg_path='Message.NewsletterFollowerInviteMessage'),
        'pollResultSnapshotMessageV3': FieldDescriptor('pollResultSnapshotMessageV3', 114, "message", repeated=False, packed=False, _msg_path='Message.PollResultSnapshotMessage'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MessageAddOn(MessageBase):
    class MessageAddOnType(enum.IntEnum):
        UNDEFINED = 0
        REACTION = 1
        EVENT_RESPONSE = 2
        POLL_UPDATE = 3
        PIN_IN_CHAT = 4
    FIELDS = {
        'messageAddOnType': FieldDescriptor('messageAddOnType', 1, "enum", repeated=False, packed=False, _enum_path='MessageAddOn.MessageAddOnType'),
        'messageAddOn': FieldDescriptor('messageAddOn', 2, "message", repeated=False, packed=False, _msg_path='Message'),
        'senderTimestampMs': FieldDescriptor('senderTimestampMs', 3, 'int64', repeated=False, packed=False),
        'serverTimestampMs': FieldDescriptor('serverTimestampMs', 4, 'int64', repeated=False, packed=False),
        'status': FieldDescriptor('status', 5, "enum", repeated=False, packed=False, _enum_path='WebMessageInfo.Status'),
        'addOnContextInfo': FieldDescriptor('addOnContextInfo', 6, "message", repeated=False, packed=False, _msg_path='MessageAddOnContextInfo'),
        'messageAddOnKey': FieldDescriptor('messageAddOnKey', 7, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'legacyMessage': FieldDescriptor('legacyMessage', 8, "message", repeated=False, packed=False, _msg_path='LegacyMessage'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MessageAddOnContextInfo(MessageBase):
    FIELDS = {
        'messageAddOnDurationInSecs': FieldDescriptor('messageAddOnDurationInSecs', 1, 'uint32', repeated=False, packed=False),
        'messageAddOnExpiryType': FieldDescriptor('messageAddOnExpiryType', 2, "enum", repeated=False, packed=False, _enum_path='MessageContextInfo.MessageAddonExpiryType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MessageAssociation(MessageBase):
    class AssociationType(enum.IntEnum):
        UNKNOWN = 0
        MEDIA_ALBUM = 1
        BOT_PLUGIN = 2
        EVENT_COVER_IMAGE = 3
        STATUS_POLL = 4
        HD_VIDEO_DUAL_UPLOAD = 5
        STATUS_EXTERNAL_RESHARE = 6
        MEDIA_POLL = 7
        STATUS_ADD_YOURS = 8
        STATUS_NOTIFICATION = 9
        HD_IMAGE_DUAL_UPLOAD = 10
        STICKER_ANNOTATION = 11
        MOTION_PHOTO = 12
        STATUS_LINK_ACTION = 13
        VIEW_ALL_REPLIES = 14
        STATUS_ADD_YOURS_AI_IMAGINE = 15
        STATUS_QUESTION = 16
        STATUS_ADD_YOURS_DIWALI = 17
        STATUS_REACTION = 18
        HEVC_VIDEO_DUAL_UPLOAD = 19
    FIELDS = {
        'associationType': FieldDescriptor('associationType', 1, "enum", repeated=False, packed=False, _enum_path='MessageAssociation.AssociationType'),
        'parentMessageKey': FieldDescriptor('parentMessageKey', 2, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'messageIndex': FieldDescriptor('messageIndex', 3, 'int32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MessageContextInfo(MessageBase):
    class MessageAddonExpiryType(enum.IntEnum):
        STATIC = 1
        DEPENDENT_ON_PARENT = 2
    FIELDS = {
        'deviceListMetadata': FieldDescriptor('deviceListMetadata', 1, "message", repeated=False, packed=False, _msg_path='DeviceListMetadata'),
        'deviceListMetadataVersion': FieldDescriptor('deviceListMetadataVersion', 2, 'int32', repeated=False, packed=False),
        'messageSecret': FieldDescriptor('messageSecret', 3, 'bytes', repeated=False, packed=False),
        'paddingBytes': FieldDescriptor('paddingBytes', 4, 'bytes', repeated=False, packed=False),
        'messageAddOnDurationInSecs': FieldDescriptor('messageAddOnDurationInSecs', 5, 'uint32', repeated=False, packed=False),
        'botMessageSecret': FieldDescriptor('botMessageSecret', 6, 'bytes', repeated=False, packed=False),
        'botMetadata': FieldDescriptor('botMetadata', 7, "message", repeated=False, packed=False, _msg_path='BotMetadata'),
        'reportingTokenVersion': FieldDescriptor('reportingTokenVersion', 8, 'int32', repeated=False, packed=False),
        'messageAddOnExpiryType': FieldDescriptor('messageAddOnExpiryType', 9, "enum", repeated=False, packed=False, _enum_path='MessageContextInfo.MessageAddonExpiryType'),
        'messageAssociation': FieldDescriptor('messageAssociation', 10, "message", repeated=False, packed=False, _msg_path='MessageAssociation'),
        'capiCreatedGroup': FieldDescriptor('capiCreatedGroup', 11, 'bool', repeated=False, packed=False),
        'supportPayload': FieldDescriptor('supportPayload', 12, 'string', repeated=False, packed=False),
        'limitSharing': FieldDescriptor('limitSharing', 13, "message", repeated=False, packed=False, _msg_path='LimitSharing'),
        'limitSharingV2': FieldDescriptor('limitSharingV2', 14, "message", repeated=False, packed=False, _msg_path='LimitSharing'),
        'threadId': FieldDescriptor('threadId', 15, "message", repeated=True, packed=False, _msg_path='ThreadID'),
        'weblinkRenderConfig': FieldDescriptor('weblinkRenderConfig', 16, "enum", repeated=False, packed=False, _enum_path='WebLinkRenderConfig'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MessageKey(MessageBase):
    FIELDS = {
        'remoteJid': FieldDescriptor('remoteJid', 1, 'string', repeated=False, packed=False),
        'fromMe': FieldDescriptor('fromMe', 2, 'bool', repeated=False, packed=False),
        'id': FieldDescriptor('id', 3, 'string', repeated=False, packed=False),
        'participant': FieldDescriptor('participant', 4, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MessageSecretMessage(MessageBase):
    FIELDS = {
        'version': FieldDescriptor('version', 1, 'sfixed32', repeated=False, packed=False),
        'encIv': FieldDescriptor('encIv', 2, 'bytes', repeated=False, packed=False),
        'encPayload': FieldDescriptor('encPayload', 3, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Money(MessageBase):
    FIELDS = {
        'value': FieldDescriptor('value', 1, 'int64', repeated=False, packed=False),
        'offset': FieldDescriptor('offset', 2, 'uint32', repeated=False, packed=False),
        'currencyCode': FieldDescriptor('currencyCode', 3, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MsgOpaqueData(MessageBase):
    class PollContentType(enum.IntEnum):
        UNKNOWN = 0
        TEXT = 1
        IMAGE = 2
    class PollType(enum.IntEnum):
        POLL = 0
        QUIZ = 1
    class EventLocation(MessageBase):
        FIELDS = {
            'degreesLatitude': FieldDescriptor('degreesLatitude', 1, 'double', repeated=False, packed=False),
            'degreesLongitude': FieldDescriptor('degreesLongitude', 2, 'double', repeated=False, packed=False),
            'name': FieldDescriptor('name', 3, 'string', repeated=False, packed=False),
            'address': FieldDescriptor('address', 4, 'string', repeated=False, packed=False),
            'url': FieldDescriptor('url', 5, 'string', repeated=False, packed=False),
            'jpegThumbnail': FieldDescriptor('jpegThumbnail', 6, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PollOption(MessageBase):
        FIELDS = {
            'name': FieldDescriptor('name', 1, 'string', repeated=False, packed=False),
            'hash': FieldDescriptor('hash', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PollVoteSnapshot(MessageBase):
        FIELDS = {
            'option': FieldDescriptor('option', 1, "message", repeated=False, packed=False, _msg_path='MsgOpaqueData.PollOption'),
            'optionVoteCount': FieldDescriptor('optionVoteCount', 2, 'int32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PollVotesSnapshot(MessageBase):
        FIELDS = {
            'pollVotes': FieldDescriptor('pollVotes', 1, "message", repeated=True, packed=False, _msg_path='MsgOpaqueData.PollVoteSnapshot'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'body': FieldDescriptor('body', 1, 'string', repeated=False, packed=False),
        'caption': FieldDescriptor('caption', 3, 'string', repeated=False, packed=False),
        'lng': FieldDescriptor('lng', 5, 'double', repeated=False, packed=False),
        'isLive': FieldDescriptor('isLive', 6, 'bool', repeated=False, packed=False),
        'lat': FieldDescriptor('lat', 7, 'double', repeated=False, packed=False),
        'paymentAmount1000': FieldDescriptor('paymentAmount1000', 8, 'int32', repeated=False, packed=False),
        'paymentNoteMsgBody': FieldDescriptor('paymentNoteMsgBody', 9, 'string', repeated=False, packed=False),
        'matchedText': FieldDescriptor('matchedText', 11, 'string', repeated=False, packed=False),
        'title': FieldDescriptor('title', 12, 'string', repeated=False, packed=False),
        'description': FieldDescriptor('description', 13, 'string', repeated=False, packed=False),
        'futureproofBuffer': FieldDescriptor('futureproofBuffer', 14, 'bytes', repeated=False, packed=False),
        'clientUrl': FieldDescriptor('clientUrl', 15, 'string', repeated=False, packed=False),
        'loc': FieldDescriptor('loc', 16, 'string', repeated=False, packed=False),
        'pollName': FieldDescriptor('pollName', 17, 'string', repeated=False, packed=False),
        'pollOptions': FieldDescriptor('pollOptions', 18, "message", repeated=True, packed=False, _msg_path='MsgOpaqueData.PollOption'),
        'pollSelectableOptionsCount': FieldDescriptor('pollSelectableOptionsCount', 20, 'uint32', repeated=False, packed=False),
        'messageSecret': FieldDescriptor('messageSecret', 21, 'bytes', repeated=False, packed=False),
        'originalSelfAuthor': FieldDescriptor('originalSelfAuthor', 51, 'string', repeated=False, packed=False),
        'senderTimestampMs': FieldDescriptor('senderTimestampMs', 22, 'int64', repeated=False, packed=False),
        'pollUpdateParentKey': FieldDescriptor('pollUpdateParentKey', 23, 'string', repeated=False, packed=False),
        'encPollVote': FieldDescriptor('encPollVote', 24, "message", repeated=False, packed=False, _msg_path='PollEncValue'),
        'isSentCagPollCreation': FieldDescriptor('isSentCagPollCreation', 28, 'bool', repeated=False, packed=False),
        'pollContentType': FieldDescriptor('pollContentType', 42, "enum", repeated=False, packed=False, _enum_path='MsgOpaqueData.PollContentType'),
        'pollType': FieldDescriptor('pollType', 46, "enum", repeated=False, packed=False, _enum_path='MsgOpaqueData.PollType'),
        'correctOptionIndex': FieldDescriptor('correctOptionIndex', 47, 'int32', repeated=False, packed=False),
        'pollVotesSnapshot': FieldDescriptor('pollVotesSnapshot', 41, "message", repeated=False, packed=False, _msg_path='MsgOpaqueData.PollVotesSnapshot'),
        'encReactionTargetMessageKey': FieldDescriptor('encReactionTargetMessageKey', 25, 'string', repeated=False, packed=False),
        'encReactionEncPayload': FieldDescriptor('encReactionEncPayload', 26, 'bytes', repeated=False, packed=False),
        'encReactionEncIv': FieldDescriptor('encReactionEncIv', 27, 'bytes', repeated=False, packed=False),
        'botMessageSecret': FieldDescriptor('botMessageSecret', 29, 'bytes', repeated=False, packed=False),
        'targetMessageKey': FieldDescriptor('targetMessageKey', 30, 'string', repeated=False, packed=False),
        'encPayload': FieldDescriptor('encPayload', 31, 'bytes', repeated=False, packed=False),
        'encIv': FieldDescriptor('encIv', 32, 'bytes', repeated=False, packed=False),
        'eventName': FieldDescriptor('eventName', 33, 'string', repeated=False, packed=False),
        'isEventCanceled': FieldDescriptor('isEventCanceled', 34, 'bool', repeated=False, packed=False),
        'eventDescription': FieldDescriptor('eventDescription', 35, 'string', repeated=False, packed=False),
        'eventJoinLink': FieldDescriptor('eventJoinLink', 36, 'string', repeated=False, packed=False),
        'eventStartTime': FieldDescriptor('eventStartTime', 37, 'int64', repeated=False, packed=False),
        'eventLocation': FieldDescriptor('eventLocation', 38, "message", repeated=False, packed=False, _msg_path='MsgOpaqueData.EventLocation'),
        'eventEndTime': FieldDescriptor('eventEndTime', 40, 'int64', repeated=False, packed=False),
        'eventIsScheduledCall': FieldDescriptor('eventIsScheduledCall', 44, 'bool', repeated=False, packed=False),
        'eventExtraGuestsAllowed': FieldDescriptor('eventExtraGuestsAllowed', 45, 'bool', repeated=False, packed=False),
        'plainProtobufBytes': FieldDescriptor('plainProtobufBytes', 43, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class MsgRowOpaqueData(MessageBase):
    FIELDS = {
        'currentMsg': FieldDescriptor('currentMsg', 1, "message", repeated=False, packed=False, _msg_path='MsgOpaqueData'),
        'quotedMsg': FieldDescriptor('quotedMsg', 2, "message", repeated=False, packed=False, _msg_path='MsgOpaqueData'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class NoiseCertificate(MessageBase):
    class Details(MessageBase):
        FIELDS = {
            'serial': FieldDescriptor('serial', 1, 'uint32', repeated=False, packed=False),
            'issuer': FieldDescriptor('issuer', 2, 'string', repeated=False, packed=False),
            'expires': FieldDescriptor('expires', 3, 'uint64', repeated=False, packed=False),
            'subject': FieldDescriptor('subject', 4, 'string', repeated=False, packed=False),
            'key': FieldDescriptor('key', 5, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'details': FieldDescriptor('details', 1, 'bytes', repeated=False, packed=False),
        'signature': FieldDescriptor('signature', 2, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class NotificationMessageInfo(MessageBase):
    FIELDS = {
        'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'message': FieldDescriptor('message', 2, "message", repeated=False, packed=False, _msg_path='Message'),
        'messageTimestamp': FieldDescriptor('messageTimestamp', 3, 'uint64', repeated=False, packed=False),
        'participant': FieldDescriptor('participant', 4, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class NotificationSettings(MessageBase):
    FIELDS = {
        'messageVibrate': FieldDescriptor('messageVibrate', 1, 'string', repeated=False, packed=False),
        'messagePopup': FieldDescriptor('messagePopup', 2, 'string', repeated=False, packed=False),
        'messageLight': FieldDescriptor('messageLight', 3, 'string', repeated=False, packed=False),
        'lowPriorityNotifications': FieldDescriptor('lowPriorityNotifications', 4, 'bool', repeated=False, packed=False),
        'reactionsMuted': FieldDescriptor('reactionsMuted', 5, 'bool', repeated=False, packed=False),
        'callVibrate': FieldDescriptor('callVibrate', 6, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PairingRequest(MessageBase):
    FIELDS = {
        'companionPublicKey': FieldDescriptor('companionPublicKey', 1, 'bytes', repeated=False, packed=False),
        'companionIdentityKey': FieldDescriptor('companionIdentityKey', 2, 'bytes', repeated=False, packed=False),
        'advSecret': FieldDescriptor('advSecret', 3, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PastParticipant(MessageBase):
    class LeaveReason(enum.IntEnum):
        LEFT = 0
        REMOVED = 1
    FIELDS = {
        'userJid': FieldDescriptor('userJid', 1, 'string', repeated=False, packed=False),
        'leaveReason': FieldDescriptor('leaveReason', 2, "enum", repeated=False, packed=False, _enum_path='PastParticipant.LeaveReason'),
        'leaveTs': FieldDescriptor('leaveTs', 3, 'uint64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PastParticipants(MessageBase):
    FIELDS = {
        'groupJid': FieldDescriptor('groupJid', 1, 'string', repeated=False, packed=False),
        'pastParticipants': FieldDescriptor('pastParticipants', 2, "message", repeated=True, packed=False, _msg_path='PastParticipant'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PatchDebugData(MessageBase):
    class Platform(enum.IntEnum):
        ANDROID = 0
        SMBA = 1
        IPHONE = 2
        SMBI = 3
        WEB = 4
        UWP = 5
        DARWIN = 6
        IPAD = 7
        WEAROS = 8
        WASG = 9
        WEARM = 10
        CAPI = 11
    FIELDS = {
        'currentLthash': FieldDescriptor('currentLthash', 1, 'bytes', repeated=False, packed=False),
        'newLthash': FieldDescriptor('newLthash', 2, 'bytes', repeated=False, packed=False),
        'patchVersion': FieldDescriptor('patchVersion', 3, 'bytes', repeated=False, packed=False),
        'collectionName': FieldDescriptor('collectionName', 4, 'bytes', repeated=False, packed=False),
        'firstFourBytesFromAHashOfSnapshotMacKey': FieldDescriptor('firstFourBytesFromAHashOfSnapshotMacKey', 5, 'bytes', repeated=False, packed=False),
        'newLthashSubtract': FieldDescriptor('newLthashSubtract', 6, 'bytes', repeated=False, packed=False),
        'numberAdd': FieldDescriptor('numberAdd', 7, 'int32', repeated=False, packed=False),
        'numberRemove': FieldDescriptor('numberRemove', 8, 'int32', repeated=False, packed=False),
        'numberOverride': FieldDescriptor('numberOverride', 9, 'int32', repeated=False, packed=False),
        'senderPlatform': FieldDescriptor('senderPlatform', 10, "enum", repeated=False, packed=False, _enum_path='PatchDebugData.Platform'),
        'isSenderPrimary': FieldDescriptor('isSenderPrimary', 11, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PaymentBackground(MessageBase):
    class Type(enum.IntEnum):
        UNKNOWN = 0
        DEFAULT = 1
    class MediaData(MessageBase):
        FIELDS = {
            'mediaKey': FieldDescriptor('mediaKey', 1, 'bytes', repeated=False, packed=False),
            'mediaKeyTimestamp': FieldDescriptor('mediaKeyTimestamp', 2, 'int64', repeated=False, packed=False),
            'fileSha256': FieldDescriptor('fileSha256', 3, 'bytes', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 4, 'bytes', repeated=False, packed=False),
            'directPath': FieldDescriptor('directPath', 5, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'id': FieldDescriptor('id', 1, 'string', repeated=False, packed=False),
        'fileLength': FieldDescriptor('fileLength', 2, 'uint64', repeated=False, packed=False),
        'width': FieldDescriptor('width', 3, 'uint32', repeated=False, packed=False),
        'height': FieldDescriptor('height', 4, 'uint32', repeated=False, packed=False),
        'mimetype': FieldDescriptor('mimetype', 5, 'string', repeated=False, packed=False),
        'placeholderArgb': FieldDescriptor('placeholderArgb', 6, 'fixed32', repeated=False, packed=False),
        'textArgb': FieldDescriptor('textArgb', 7, 'fixed32', repeated=False, packed=False),
        'subtextArgb': FieldDescriptor('subtextArgb', 8, 'fixed32', repeated=False, packed=False),
        'mediaData': FieldDescriptor('mediaData', 9, "message", repeated=False, packed=False, _msg_path='PaymentBackground.MediaData'),
        'type': FieldDescriptor('type', 10, "enum", repeated=False, packed=False, _enum_path='PaymentBackground.Type'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PaymentInfo(MessageBase):
    class Currency(enum.IntEnum):
        UNKNOWN_CURRENCY = 0
        INR = 1
    class Status(enum.IntEnum):
        UNKNOWN_STATUS = 0
        PROCESSING = 1
        SENT = 2
        NEED_TO_ACCEPT = 3
        COMPLETE = 4
        COULD_NOT_COMPLETE = 5
        REFUNDED = 6
        EXPIRED = 7
        REJECTED = 8
        CANCELLED = 9
        WAITING_FOR_PAYER = 10
        WAITING = 11
    class TxnStatus(enum.IntEnum):
        UNKNOWN = 0
        PENDING_SETUP = 1
        PENDING_RECEIVER_SETUP = 2
        INIT = 3
        SUCCESS = 4
        COMPLETED = 5
        FAILED = 6
        FAILED_RISK = 7
        FAILED_PROCESSING = 8
        FAILED_RECEIVER_PROCESSING = 9
        FAILED_DA = 10
        FAILED_DA_FINAL = 11
        REFUNDED_TXN = 12
        REFUND_FAILED = 13
        REFUND_FAILED_PROCESSING = 14
        REFUND_FAILED_DA = 15
        EXPIRED_TXN = 16
        AUTH_CANCELED = 17
        AUTH_CANCEL_FAILED_PROCESSING = 18
        AUTH_CANCEL_FAILED = 19
        COLLECT_INIT = 20
        COLLECT_SUCCESS = 21
        COLLECT_FAILED = 22
        COLLECT_FAILED_RISK = 23
        COLLECT_REJECTED = 24
        COLLECT_EXPIRED = 25
        COLLECT_CANCELED = 26
        COLLECT_CANCELLING = 27
        IN_REVIEW = 28
        REVERSAL_SUCCESS = 29
        REVERSAL_PENDING = 30
        REFUND_PENDING = 31
    FIELDS = {
        'currencyDeprecated': FieldDescriptor('currencyDeprecated', 1, "enum", repeated=False, packed=False, _enum_path='PaymentInfo.Currency'),
        'amount1000': FieldDescriptor('amount1000', 2, 'uint64', repeated=False, packed=False),
        'receiverJid': FieldDescriptor('receiverJid', 3, 'string', repeated=False, packed=False),
        'status': FieldDescriptor('status', 4, "enum", repeated=False, packed=False, _enum_path='PaymentInfo.Status'),
        'transactionTimestamp': FieldDescriptor('transactionTimestamp', 5, 'uint64', repeated=False, packed=False),
        'requestMessageKey': FieldDescriptor('requestMessageKey', 6, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'expiryTimestamp': FieldDescriptor('expiryTimestamp', 7, 'uint64', repeated=False, packed=False),
        'futureproofed': FieldDescriptor('futureproofed', 8, 'bool', repeated=False, packed=False),
        'currency': FieldDescriptor('currency', 9, 'string', repeated=False, packed=False),
        'txnStatus': FieldDescriptor('txnStatus', 10, "enum", repeated=False, packed=False, _enum_path='PaymentInfo.TxnStatus'),
        'useNoviFiatFormat': FieldDescriptor('useNoviFiatFormat', 11, 'bool', repeated=False, packed=False),
        'primaryAmount': FieldDescriptor('primaryAmount', 12, "message", repeated=False, packed=False, _msg_path='Money'),
        'exchangeAmount': FieldDescriptor('exchangeAmount', 13, "message", repeated=False, packed=False, _msg_path='Money'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PhoneNumberToLIDMapping(MessageBase):
    FIELDS = {
        'pnJid': FieldDescriptor('pnJid', 1, 'string', repeated=False, packed=False),
        'lidJid': FieldDescriptor('lidJid', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PhotoChange(MessageBase):
    FIELDS = {
        'oldPhoto': FieldDescriptor('oldPhoto', 1, 'bytes', repeated=False, packed=False),
        'newPhoto': FieldDescriptor('newPhoto', 2, 'bytes', repeated=False, packed=False),
        'newPhotoId': FieldDescriptor('newPhotoId', 3, 'uint32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PinInChat(MessageBase):
    class Type(enum.IntEnum):
        UNKNOWN_TYPE = 0
        PIN_FOR_ALL = 1
        UNPIN_FOR_ALL = 2
    FIELDS = {
        'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='PinInChat.Type'),
        'key': FieldDescriptor('key', 2, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'senderTimestampMs': FieldDescriptor('senderTimestampMs', 3, 'int64', repeated=False, packed=False),
        'serverTimestampMs': FieldDescriptor('serverTimestampMs', 4, 'int64', repeated=False, packed=False),
        'messageAddOnContextInfo': FieldDescriptor('messageAddOnContextInfo', 5, "message", repeated=False, packed=False, _msg_path='MessageAddOnContextInfo'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Point(MessageBase):
    FIELDS = {
        'xDeprecated': FieldDescriptor('xDeprecated', 1, 'int32', repeated=False, packed=False),
        'yDeprecated': FieldDescriptor('yDeprecated', 2, 'int32', repeated=False, packed=False),
        'x': FieldDescriptor('x', 3, 'double', repeated=False, packed=False),
        'y': FieldDescriptor('y', 4, 'double', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PollAdditionalMetadata(MessageBase):
    FIELDS = {
        'pollInvalidated': FieldDescriptor('pollInvalidated', 1, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PollEncValue(MessageBase):
    FIELDS = {
        'encPayload': FieldDescriptor('encPayload', 1, 'bytes', repeated=False, packed=False),
        'encIv': FieldDescriptor('encIv', 2, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PollUpdate(MessageBase):
    FIELDS = {
        'pollUpdateMessageKey': FieldDescriptor('pollUpdateMessageKey', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'vote': FieldDescriptor('vote', 2, "message", repeated=False, packed=False, _msg_path='Message.PollVoteMessage'),
        'senderTimestampMs': FieldDescriptor('senderTimestampMs', 3, 'int64', repeated=False, packed=False),
        'serverTimestampMs': FieldDescriptor('serverTimestampMs', 4, 'int64', repeated=False, packed=False),
        'unread': FieldDescriptor('unread', 5, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PreKeyRecordStructure(MessageBase):
    FIELDS = {
        'id': FieldDescriptor('id', 1, 'uint32', repeated=False, packed=False),
        'publicKey': FieldDescriptor('publicKey', 2, 'bytes', repeated=False, packed=False),
        'privateKey': FieldDescriptor('privateKey', 3, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PreKeySignalMessage(MessageBase):
    FIELDS = {
        'registrationId': FieldDescriptor('registrationId', 5, 'uint32', repeated=False, packed=False),
        'preKeyId': FieldDescriptor('preKeyId', 1, 'uint32', repeated=False, packed=False),
        'signedPreKeyId': FieldDescriptor('signedPreKeyId', 6, 'uint32', repeated=False, packed=False),
        'baseKey': FieldDescriptor('baseKey', 2, 'bytes', repeated=False, packed=False),
        'identityKey': FieldDescriptor('identityKey', 3, 'bytes', repeated=False, packed=False),
        'message': FieldDescriptor('message', 4, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PremiumMessageInfo(MessageBase):
    FIELDS = {
        'serverCampaignId': FieldDescriptor('serverCampaignId', 1, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class PrimaryEphemeralIdentity(MessageBase):
    FIELDS = {
        'publicKey': FieldDescriptor('publicKey', 1, 'bytes', repeated=False, packed=False),
        'nonce': FieldDescriptor('nonce', 2, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ProcessedVideo(MessageBase):
    class VideoQuality(enum.IntEnum):
        UNDEFINED = 0
        LOW = 1
        MID = 2
        HIGH = 3
    FIELDS = {
        'directPath': FieldDescriptor('directPath', 1, 'string', repeated=False, packed=False),
        'fileSha256': FieldDescriptor('fileSha256', 2, 'bytes', repeated=False, packed=False),
        'height': FieldDescriptor('height', 3, 'uint32', repeated=False, packed=False),
        'width': FieldDescriptor('width', 4, 'uint32', repeated=False, packed=False),
        'fileLength': FieldDescriptor('fileLength', 5, 'uint64', repeated=False, packed=False),
        'bitrate': FieldDescriptor('bitrate', 6, 'uint32', repeated=False, packed=False),
        'quality': FieldDescriptor('quality', 7, "enum", repeated=False, packed=False, _enum_path='ProcessedVideo.VideoQuality'),
        'capabilities': FieldDescriptor('capabilities', 8, 'string', repeated=True, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ProloguePayload(MessageBase):
    FIELDS = {
        'companionEphemeralIdentity': FieldDescriptor('companionEphemeralIdentity', 1, 'bytes', repeated=False, packed=False),
        'commitment': FieldDescriptor('commitment', 2, "message", repeated=False, packed=False, _msg_path='CompanionCommitment'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Pushname(MessageBase):
    FIELDS = {
        'id': FieldDescriptor('id', 1, 'string', repeated=False, packed=False),
        'pushname': FieldDescriptor('pushname', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class QuarantinedMessage(MessageBase):
    FIELDS = {
        'originalData': FieldDescriptor('originalData', 1, 'bytes', repeated=False, packed=False),
        'extractedText': FieldDescriptor('extractedText', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Reaction(MessageBase):
    FIELDS = {
        'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'text': FieldDescriptor('text', 2, 'string', repeated=False, packed=False),
        'groupingKey': FieldDescriptor('groupingKey', 3, 'string', repeated=False, packed=False),
        'senderTimestampMs': FieldDescriptor('senderTimestampMs', 4, 'int64', repeated=False, packed=False),
        'unread': FieldDescriptor('unread', 5, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class RecentEmojiWeight(MessageBase):
    FIELDS = {
        'emoji': FieldDescriptor('emoji', 1, 'string', repeated=False, packed=False),
        'weight': FieldDescriptor('weight', 2, 'float', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class RecordStructure(MessageBase):
    FIELDS = {
        'currentSession': FieldDescriptor('currentSession', 1, "message", repeated=False, packed=False, _msg_path='SessionStructure'),
        'previousSessions': FieldDescriptor('previousSessions', 2, "message", repeated=True, packed=False, _msg_path='SessionStructure'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class Reportable(MessageBase):
    FIELDS = {
        'minVersion': FieldDescriptor('minVersion', 1, 'uint32', repeated=False, packed=False),
        'maxVersion': FieldDescriptor('maxVersion', 2, 'uint32', repeated=False, packed=False),
        'notReportableMinVersion': FieldDescriptor('notReportableMinVersion', 3, 'uint32', repeated=False, packed=False),
        'never': FieldDescriptor('never', 4, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ReportingTokenInfo(MessageBase):
    FIELDS = {
        'reportingTag': FieldDescriptor('reportingTag', 1, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SenderKeyDistributionMessage(MessageBase):
    FIELDS = {
        'id': FieldDescriptor('id', 1, 'uint32', repeated=False, packed=False),
        'iteration': FieldDescriptor('iteration', 2, 'uint32', repeated=False, packed=False),
        'chainKey': FieldDescriptor('chainKey', 3, 'bytes', repeated=False, packed=False),
        'signingKey': FieldDescriptor('signingKey', 4, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SenderKeyMessage(MessageBase):
    FIELDS = {
        'id': FieldDescriptor('id', 1, 'uint32', repeated=False, packed=False),
        'iteration': FieldDescriptor('iteration', 2, 'uint32', repeated=False, packed=False),
        'ciphertext': FieldDescriptor('ciphertext', 3, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SenderKeyRecordStructure(MessageBase):
    FIELDS = {
        'senderKeyStates': FieldDescriptor('senderKeyStates', 1, "message", repeated=True, packed=False, _msg_path='SenderKeyStateStructure'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SenderKeyStateStructure(MessageBase):
    class SenderChainKey(MessageBase):
        FIELDS = {
            'iteration': FieldDescriptor('iteration', 1, 'uint32', repeated=False, packed=False),
            'seed': FieldDescriptor('seed', 2, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class SenderMessageKey(MessageBase):
        FIELDS = {
            'iteration': FieldDescriptor('iteration', 1, 'uint32', repeated=False, packed=False),
            'seed': FieldDescriptor('seed', 2, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class SenderSigningKey(MessageBase):
        FIELDS = {
            'public': FieldDescriptor('public', 1, 'bytes', repeated=False, packed=False),
            'private': FieldDescriptor('private', 2, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'senderKeyId': FieldDescriptor('senderKeyId', 1, 'uint32', repeated=False, packed=False),
        'senderChainKey': FieldDescriptor('senderChainKey', 2, "message", repeated=False, packed=False, _msg_path='SenderKeyStateStructure.SenderChainKey'),
        'senderSigningKey': FieldDescriptor('senderSigningKey', 3, "message", repeated=False, packed=False, _msg_path='SenderKeyStateStructure.SenderSigningKey'),
        'senderMessageKeys': FieldDescriptor('senderMessageKeys', 4, "message", repeated=True, packed=False, _msg_path='SenderKeyStateStructure.SenderMessageKey'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ServerErrorReceipt(MessageBase):
    FIELDS = {
        'stanzaId': FieldDescriptor('stanzaId', 1, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SessionStructure(MessageBase):
    class Chain(MessageBase):
        class ChainKey(MessageBase):
            FIELDS = {
                'index': FieldDescriptor('index', 1, 'uint32', repeated=False, packed=False),
                'key': FieldDescriptor('key', 2, 'bytes', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        class MessageKey(MessageBase):
            FIELDS = {
                'index': FieldDescriptor('index', 1, 'uint32', repeated=False, packed=False),
                'cipherKey': FieldDescriptor('cipherKey', 2, 'bytes', repeated=False, packed=False),
                'macKey': FieldDescriptor('macKey', 3, 'bytes', repeated=False, packed=False),
                'iv': FieldDescriptor('iv', 4, 'bytes', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'senderRatchetKey': FieldDescriptor('senderRatchetKey', 1, 'bytes', repeated=False, packed=False),
            'senderRatchetKeyPrivate': FieldDescriptor('senderRatchetKeyPrivate', 2, 'bytes', repeated=False, packed=False),
            'chainKey': FieldDescriptor('chainKey', 3, "message", repeated=False, packed=False, _msg_path='SessionStructure.Chain.ChainKey'),
            'messageKeys': FieldDescriptor('messageKeys', 4, "message", repeated=True, packed=False, _msg_path='SessionStructure.Chain.MessageKey'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PendingKeyExchange(MessageBase):
        FIELDS = {
            'sequence': FieldDescriptor('sequence', 1, 'uint32', repeated=False, packed=False),
            'localBaseKey': FieldDescriptor('localBaseKey', 2, 'bytes', repeated=False, packed=False),
            'localBaseKeyPrivate': FieldDescriptor('localBaseKeyPrivate', 3, 'bytes', repeated=False, packed=False),
            'localRatchetKey': FieldDescriptor('localRatchetKey', 4, 'bytes', repeated=False, packed=False),
            'localRatchetKeyPrivate': FieldDescriptor('localRatchetKeyPrivate', 5, 'bytes', repeated=False, packed=False),
            'localIdentityKey': FieldDescriptor('localIdentityKey', 7, 'bytes', repeated=False, packed=False),
            'localIdentityKeyPrivate': FieldDescriptor('localIdentityKeyPrivate', 8, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PendingPreKey(MessageBase):
        FIELDS = {
            'preKeyId': FieldDescriptor('preKeyId', 1, 'uint32', repeated=False, packed=False),
            'signedPreKeyId': FieldDescriptor('signedPreKeyId', 3, 'int32', repeated=False, packed=False),
            'baseKey': FieldDescriptor('baseKey', 2, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'sessionVersion': FieldDescriptor('sessionVersion', 1, 'uint32', repeated=False, packed=False),
        'localIdentityPublic': FieldDescriptor('localIdentityPublic', 2, 'bytes', repeated=False, packed=False),
        'remoteIdentityPublic': FieldDescriptor('remoteIdentityPublic', 3, 'bytes', repeated=False, packed=False),
        'rootKey': FieldDescriptor('rootKey', 4, 'bytes', repeated=False, packed=False),
        'previousCounter': FieldDescriptor('previousCounter', 5, 'uint32', repeated=False, packed=False),
        'senderChain': FieldDescriptor('senderChain', 6, "message", repeated=False, packed=False, _msg_path='SessionStructure.Chain'),
        'receiverChains': FieldDescriptor('receiverChains', 7, "message", repeated=True, packed=False, _msg_path='SessionStructure.Chain'),
        'pendingKeyExchange': FieldDescriptor('pendingKeyExchange', 8, "message", repeated=False, packed=False, _msg_path='SessionStructure.PendingKeyExchange'),
        'pendingPreKey': FieldDescriptor('pendingPreKey', 9, "message", repeated=False, packed=False, _msg_path='SessionStructure.PendingPreKey'),
        'remoteRegistrationId': FieldDescriptor('remoteRegistrationId', 10, 'uint32', repeated=False, packed=False),
        'localRegistrationId': FieldDescriptor('localRegistrationId', 11, 'uint32', repeated=False, packed=False),
        'needsRefresh': FieldDescriptor('needsRefresh', 12, 'bool', repeated=False, packed=False),
        'aliceBaseKey': FieldDescriptor('aliceBaseKey', 13, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SessionTransparencyMetadata(MessageBase):
    FIELDS = {
        'disclaimerText': FieldDescriptor('disclaimerText', 1, 'string', repeated=False, packed=False),
        'hcaId': FieldDescriptor('hcaId', 2, 'string', repeated=False, packed=False),
        'sessionTransparencyType': FieldDescriptor('sessionTransparencyType', 3, "enum", repeated=False, packed=False, _enum_path='SessionTransparencyType'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SignalMessage(MessageBase):
    FIELDS = {
        'ratchetKey': FieldDescriptor('ratchetKey', 1, 'bytes', repeated=False, packed=False),
        'counter': FieldDescriptor('counter', 2, 'uint32', repeated=False, packed=False),
        'previousCounter': FieldDescriptor('previousCounter', 3, 'uint32', repeated=False, packed=False),
        'ciphertext': FieldDescriptor('ciphertext', 4, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SignedPreKeyRecordStructure(MessageBase):
    FIELDS = {
        'id': FieldDescriptor('id', 1, 'uint32', repeated=False, packed=False),
        'publicKey': FieldDescriptor('publicKey', 2, 'bytes', repeated=False, packed=False),
        'privateKey': FieldDescriptor('privateKey', 3, 'bytes', repeated=False, packed=False),
        'signature': FieldDescriptor('signature', 4, 'bytes', repeated=False, packed=False),
        'timestamp': FieldDescriptor('timestamp', 5, 'fixed64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class StatusAttribution(MessageBase):
    class Type(enum.IntEnum):
        UNKNOWN = 0
        RESHARE = 1
        EXTERNAL_SHARE = 2
        MUSIC = 3
        STATUS_MENTION = 4
        GROUP_STATUS = 5
        RL_ATTRIBUTION = 6
        AI_CREATED = 7
        LAYOUTS = 8
    class AiCreatedAttribution(MessageBase):
        class Source(enum.IntEnum):
            UNKNOWN = 0
            STATUS_MIMICRY = 1
        FIELDS = {
            'source': FieldDescriptor('source', 1, "enum", repeated=False, packed=False, _enum_path='StatusAttribution.AiCreatedAttribution.Source'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ExternalShare(MessageBase):
        class Source(enum.IntEnum):
            UNKNOWN = 0
            INSTAGRAM = 1
            FACEBOOK = 2
            MESSENGER = 3
            SPOTIFY = 4
            YOUTUBE = 5
            PINTEREST = 6
            THREADS = 7
            APPLE_MUSIC = 8
            SHARECHAT = 9
            GOOGLE_PHOTOS = 10
        FIELDS = {
            'actionUrl': FieldDescriptor('actionUrl', 1, 'string', repeated=False, packed=False),
            'source': FieldDescriptor('source', 2, "enum", repeated=False, packed=False, _enum_path='StatusAttribution.ExternalShare.Source'),
            'duration': FieldDescriptor('duration', 3, 'int32', repeated=False, packed=False),
            'actionFallbackUrl': FieldDescriptor('actionFallbackUrl', 4, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class GroupStatus(MessageBase):
        FIELDS = {
            'authorJid': FieldDescriptor('authorJid', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class Music(MessageBase):
        FIELDS = {
            'authorName': FieldDescriptor('authorName', 1, 'string', repeated=False, packed=False),
            'songId': FieldDescriptor('songId', 2, 'string', repeated=False, packed=False),
            'title': FieldDescriptor('title', 3, 'string', repeated=False, packed=False),
            'author': FieldDescriptor('author', 4, 'string', repeated=False, packed=False),
            'artistAttribution': FieldDescriptor('artistAttribution', 5, 'string', repeated=False, packed=False),
            'isExplicit': FieldDescriptor('isExplicit', 6, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class RLAttribution(MessageBase):
        class Source(enum.IntEnum):
            UNKNOWN = 0
            RAY_BAN_META_GLASSES = 1
            OAKLEY_META_GLASSES = 2
            HYPERNOVA_GLASSES = 3
        FIELDS = {
            'source': FieldDescriptor('source', 1, "enum", repeated=False, packed=False, _enum_path='StatusAttribution.RLAttribution.Source'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StatusReshare(MessageBase):
        class Source(enum.IntEnum):
            UNKNOWN = 0
            INTERNAL_RESHARE = 1
            MENTION_RESHARE = 2
            CHANNEL_RESHARE = 3
            FORWARD = 4
        class Metadata(MessageBase):
            FIELDS = {
                'duration': FieldDescriptor('duration', 1, 'int32', repeated=False, packed=False),
                'channelJid': FieldDescriptor('channelJid', 2, 'string', repeated=False, packed=False),
                'channelMessageId': FieldDescriptor('channelMessageId', 3, 'int32', repeated=False, packed=False),
                'hasMultipleReshares': FieldDescriptor('hasMultipleReshares', 4, 'bool', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'source': FieldDescriptor('source', 1, "enum", repeated=False, packed=False, _enum_path='StatusAttribution.StatusReshare.Source'),
            'metadata': FieldDescriptor('metadata', 2, "message", repeated=False, packed=False, _msg_path='StatusAttribution.StatusReshare.Metadata'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='StatusAttribution.Type'),
        'actionUrl': FieldDescriptor('actionUrl', 2, 'string', repeated=False, packed=False),
        'statusReshare': FieldDescriptor('statusReshare', 3, "message", repeated=False, packed=False, _msg_path='StatusAttribution.StatusReshare'),
        'externalShare': FieldDescriptor('externalShare', 4, "message", repeated=False, packed=False, _msg_path='StatusAttribution.ExternalShare'),
        'music': FieldDescriptor('music', 5, "message", repeated=False, packed=False, _msg_path='StatusAttribution.Music'),
        'groupStatus': FieldDescriptor('groupStatus', 6, "message", repeated=False, packed=False, _msg_path='StatusAttribution.GroupStatus'),
        'rlAttribution': FieldDescriptor('rlAttribution', 7, "message", repeated=False, packed=False, _msg_path='StatusAttribution.RLAttribution'),
        'aiCreatedAttribution': FieldDescriptor('aiCreatedAttribution', 8, "message", repeated=False, packed=False, _msg_path='StatusAttribution.AiCreatedAttribution'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class StatusMentionMessage(MessageBase):
    FIELDS = {
        'quotedStatus': FieldDescriptor('quotedStatus', 1, "message", repeated=False, packed=False, _msg_path='Message'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class StatusPSA(MessageBase):
    FIELDS = {
        'campaignId': FieldDescriptor('campaignId', 44, 'uint64', repeated=False, packed=False),
        'campaignExpirationTimestamp': FieldDescriptor('campaignExpirationTimestamp', 45, 'uint64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class StickerMetadata(MessageBase):
    FIELDS = {
        'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
        'fileSha256': FieldDescriptor('fileSha256', 2, 'bytes', repeated=False, packed=False),
        'fileEncSha256': FieldDescriptor('fileEncSha256', 3, 'bytes', repeated=False, packed=False),
        'mediaKey': FieldDescriptor('mediaKey', 4, 'bytes', repeated=False, packed=False),
        'mimetype': FieldDescriptor('mimetype', 5, 'string', repeated=False, packed=False),
        'height': FieldDescriptor('height', 6, 'uint32', repeated=False, packed=False),
        'width': FieldDescriptor('width', 7, 'uint32', repeated=False, packed=False),
        'directPath': FieldDescriptor('directPath', 8, 'string', repeated=False, packed=False),
        'fileLength': FieldDescriptor('fileLength', 9, 'uint64', repeated=False, packed=False),
        'weight': FieldDescriptor('weight', 10, 'float', repeated=False, packed=False),
        'lastStickerSentTs': FieldDescriptor('lastStickerSentTs', 11, 'int64', repeated=False, packed=False),
        'isLottie': FieldDescriptor('isLottie', 12, 'bool', repeated=False, packed=False),
        'imageHash': FieldDescriptor('imageHash', 13, 'string', repeated=False, packed=False),
        'isAvatarSticker': FieldDescriptor('isAvatarSticker', 14, 'bool', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncActionData(MessageBase):
    FIELDS = {
        'index': FieldDescriptor('index', 1, 'bytes', repeated=False, packed=False),
        'value': FieldDescriptor('value', 2, "message", repeated=False, packed=False, _msg_path='SyncActionValue'),
        'padding': FieldDescriptor('padding', 3, 'bytes', repeated=False, packed=False),
        'version': FieldDescriptor('version', 4, 'int32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncActionValue(MessageBase):
    class AgentAction(MessageBase):
        FIELDS = {
            'name': FieldDescriptor('name', 1, 'string', repeated=False, packed=False),
            'deviceID': FieldDescriptor('deviceID', 2, 'int32', repeated=False, packed=False),
            'isDeleted': FieldDescriptor('isDeleted', 3, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AiThreadRenameAction(MessageBase):
        FIELDS = {
            'newTitle': FieldDescriptor('newTitle', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AndroidUnsupportedActions(MessageBase):
        FIELDS = {
            'allowed': FieldDescriptor('allowed', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ArchiveChatAction(MessageBase):
        FIELDS = {
            'archived': FieldDescriptor('archived', 1, 'bool', repeated=False, packed=False),
            'messageRange': FieldDescriptor('messageRange', 2, "message", repeated=False, packed=False, _msg_path='SyncActionValue.SyncActionMessageRange'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class AvatarUpdatedAction(MessageBase):
        class AvatarEventType(enum.IntEnum):
            UPDATED = 0
            CREATED = 1
            DELETED = 2
        FIELDS = {
            'eventType': FieldDescriptor('eventType', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.AvatarUpdatedAction.AvatarEventType'),
            'recentAvatarStickers': FieldDescriptor('recentAvatarStickers', 2, "message", repeated=True, packed=False, _msg_path='SyncActionValue.StickerAction'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class BotWelcomeRequestAction(MessageBase):
        FIELDS = {
            'isSent': FieldDescriptor('isSent', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class BroadcastListParticipant(MessageBase):
        FIELDS = {
            'lidJid': FieldDescriptor('lidJid', 1, 'string', repeated=False, packed=False),
            'pnJid': FieldDescriptor('pnJid', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class BusinessBroadcastAssociationAction(MessageBase):
        FIELDS = {
            'deleted': FieldDescriptor('deleted', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class BusinessBroadcastListAction(MessageBase):
        FIELDS = {
            'deleted': FieldDescriptor('deleted', 1, 'bool', repeated=False, packed=False),
            'participants': FieldDescriptor('participants', 2, "message", repeated=True, packed=False, _msg_path='SyncActionValue.BroadcastListParticipant'),
            'listName': FieldDescriptor('listName', 3, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class CallLogAction(MessageBase):
        FIELDS = {
            'callLogRecord': FieldDescriptor('callLogRecord', 1, "message", repeated=False, packed=False, _msg_path='CallLogRecord'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ChatAssignmentAction(MessageBase):
        FIELDS = {
            'deviceAgentID': FieldDescriptor('deviceAgentID', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ChatAssignmentOpenedStatusAction(MessageBase):
        FIELDS = {
            'chatOpened': FieldDescriptor('chatOpened', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ClearChatAction(MessageBase):
        FIELDS = {
            'messageRange': FieldDescriptor('messageRange', 1, "message", repeated=False, packed=False, _msg_path='SyncActionValue.SyncActionMessageRange'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ContactAction(MessageBase):
        FIELDS = {
            'fullName': FieldDescriptor('fullName', 1, 'string', repeated=False, packed=False),
            'firstName': FieldDescriptor('firstName', 2, 'string', repeated=False, packed=False),
            'lidJid': FieldDescriptor('lidJid', 3, 'string', repeated=False, packed=False),
            'saveOnPrimaryAddressbook': FieldDescriptor('saveOnPrimaryAddressbook', 4, 'bool', repeated=False, packed=False),
            'pnJid': FieldDescriptor('pnJid', 5, 'string', repeated=False, packed=False),
            'username': FieldDescriptor('username', 6, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class CtwaPerCustomerDataSharingAction(MessageBase):
        FIELDS = {
            'isCtwaPerCustomerDataSharingEnabled': FieldDescriptor('isCtwaPerCustomerDataSharingEnabled', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class CustomPaymentMethod(MessageBase):
        FIELDS = {
            'credentialId': FieldDescriptor('credentialId', 1, 'string', repeated=False, packed=False),
            'country': FieldDescriptor('country', 2, 'string', repeated=False, packed=False),
            'type': FieldDescriptor('type', 3, 'string', repeated=False, packed=False),
            'metadata': FieldDescriptor('metadata', 4, "message", repeated=True, packed=False, _msg_path='SyncActionValue.CustomPaymentMethodMetadata'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class CustomPaymentMethodMetadata(MessageBase):
        FIELDS = {
            'key': FieldDescriptor('key', 1, 'string', repeated=False, packed=False),
            'value': FieldDescriptor('value', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class CustomPaymentMethodsAction(MessageBase):
        FIELDS = {
            'customPaymentMethods': FieldDescriptor('customPaymentMethods', 1, "message", repeated=True, packed=False, _msg_path='SyncActionValue.CustomPaymentMethod'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class DeleteChatAction(MessageBase):
        FIELDS = {
            'messageRange': FieldDescriptor('messageRange', 1, "message", repeated=False, packed=False, _msg_path='SyncActionValue.SyncActionMessageRange'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class DeleteIndividualCallLogAction(MessageBase):
        FIELDS = {
            'peerJid': FieldDescriptor('peerJid', 1, 'string', repeated=False, packed=False),
            'isIncoming': FieldDescriptor('isIncoming', 2, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class DeleteMessageForMeAction(MessageBase):
        FIELDS = {
            'deleteMedia': FieldDescriptor('deleteMedia', 1, 'bool', repeated=False, packed=False),
            'messageTimestamp': FieldDescriptor('messageTimestamp', 2, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class DetectedOutcomesStatusAction(MessageBase):
        FIELDS = {
            'isEnabled': FieldDescriptor('isEnabled', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class ExternalWebBetaAction(MessageBase):
        FIELDS = {
            'isOptIn': FieldDescriptor('isOptIn', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class FavoritesAction(MessageBase):
        class Favorite(MessageBase):
            FIELDS = {
                'id': FieldDescriptor('id', 1, 'string', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'favorites': FieldDescriptor('favorites', 1, "message", repeated=True, packed=False, _msg_path='SyncActionValue.FavoritesAction.Favorite'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class InteractiveMessageAction(MessageBase):
        class InteractiveMessageActionMode(enum.IntEnum):
            DISABLE_CTA = 1
        FIELDS = {
            'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.InteractiveMessageAction.InteractiveMessageActionMode'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class KeyExpiration(MessageBase):
        FIELDS = {
            'expiredKeyEpoch': FieldDescriptor('expiredKeyEpoch', 1, 'int32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LabelAssociationAction(MessageBase):
        FIELDS = {
            'labeled': FieldDescriptor('labeled', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LabelEditAction(MessageBase):
        class ListType(enum.IntEnum):
            NONE = 0
            UNREAD = 1
            GROUPS = 2
            FAVORITES = 3
            PREDEFINED = 4
            CUSTOM = 5
            COMMUNITY = 6
            SERVER_ASSIGNED = 7
            DRAFTED = 8
            AI_HANDOFF = 9
        FIELDS = {
            'name': FieldDescriptor('name', 1, 'string', repeated=False, packed=False),
            'color': FieldDescriptor('color', 2, 'int32', repeated=False, packed=False),
            'predefinedId': FieldDescriptor('predefinedId', 3, 'int32', repeated=False, packed=False),
            'deleted': FieldDescriptor('deleted', 4, 'bool', repeated=False, packed=False),
            'orderIndex': FieldDescriptor('orderIndex', 5, 'int32', repeated=False, packed=False),
            'isActive': FieldDescriptor('isActive', 6, 'bool', repeated=False, packed=False),
            'type': FieldDescriptor('type', 7, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.LabelEditAction.ListType'),
            'isImmutable': FieldDescriptor('isImmutable', 8, 'bool', repeated=False, packed=False),
            'muteEndTimeMs': FieldDescriptor('muteEndTimeMs', 9, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LabelReorderingAction(MessageBase):
        FIELDS = {
            'sortedLabelIds': FieldDescriptor('sortedLabelIds', 1, 'int32', repeated=True, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LidContactAction(MessageBase):
        FIELDS = {
            'fullName': FieldDescriptor('fullName', 1, 'string', repeated=False, packed=False),
            'firstName': FieldDescriptor('firstName', 2, 'string', repeated=False, packed=False),
            'username': FieldDescriptor('username', 3, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LocaleSetting(MessageBase):
        FIELDS = {
            'locale': FieldDescriptor('locale', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class LockChatAction(MessageBase):
        FIELDS = {
            'locked': FieldDescriptor('locked', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MaibaAIFeaturesControlAction(MessageBase):
        class MaibaAIFeatureStatus(enum.IntEnum):
            ENABLED = 0
            ENABLED_HAS_LEARNING = 1
            DISABLED = 2
        FIELDS = {
            'aiFeatureStatus': FieldDescriptor('aiFeatureStatus', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.MaibaAIFeaturesControlAction.MaibaAIFeatureStatus'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MarkChatAsReadAction(MessageBase):
        FIELDS = {
            'read': FieldDescriptor('read', 1, 'bool', repeated=False, packed=False),
            'messageRange': FieldDescriptor('messageRange', 2, "message", repeated=False, packed=False, _msg_path='SyncActionValue.SyncActionMessageRange'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MarketingMessageAction(MessageBase):
        class MarketingMessagePrototypeType(enum.IntEnum):
            PERSONALIZED = 0
        FIELDS = {
            'name': FieldDescriptor('name', 1, 'string', repeated=False, packed=False),
            'message': FieldDescriptor('message', 2, 'string', repeated=False, packed=False),
            'type': FieldDescriptor('type', 3, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.MarketingMessageAction.MarketingMessagePrototypeType'),
            'createdAt': FieldDescriptor('createdAt', 4, 'int64', repeated=False, packed=False),
            'lastSentAt': FieldDescriptor('lastSentAt', 5, 'int64', repeated=False, packed=False),
            'isDeleted': FieldDescriptor('isDeleted', 6, 'bool', repeated=False, packed=False),
            'mediaId': FieldDescriptor('mediaId', 7, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MarketingMessageBroadcastAction(MessageBase):
        FIELDS = {
            'repliedCount': FieldDescriptor('repliedCount', 1, 'int32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MerchantPaymentPartnerAction(MessageBase):
        class Status(enum.IntEnum):
            ACTIVE = 0
            INACTIVE = 1
        FIELDS = {
            'status': FieldDescriptor('status', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.MerchantPaymentPartnerAction.Status'),
            'country': FieldDescriptor('country', 2, 'string', repeated=False, packed=False),
            'gatewayName': FieldDescriptor('gatewayName', 3, 'string', repeated=False, packed=False),
            'credentialId': FieldDescriptor('credentialId', 4, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MusicUserIdAction(MessageBase):
        FIELDS = {
            'musicUserId': FieldDescriptor('musicUserId', 1, 'string', repeated=False, packed=False),
            'music_user_id_map': FieldDescriptor('music_user_id_map', 2, "map", repeated=True, map_key_type='string', map_value=FieldDescriptor("value", 2, 'string')),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class MuteAction(MessageBase):
        FIELDS = {
            'muted': FieldDescriptor('muted', 1, 'bool', repeated=False, packed=False),
            'muteEndTimestamp': FieldDescriptor('muteEndTimestamp', 2, 'int64', repeated=False, packed=False),
            'autoMuted': FieldDescriptor('autoMuted', 3, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class NewsletterSavedInterestsAction(MessageBase):
        FIELDS = {
            'newsletterSavedInterests': FieldDescriptor('newsletterSavedInterests', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class NoteEditAction(MessageBase):
        class NoteType(enum.IntEnum):
            UNSTRUCTURED = 1
            STRUCTURED = 2
        FIELDS = {
            'type': FieldDescriptor('type', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.NoteEditAction.NoteType'),
            'chatJid': FieldDescriptor('chatJid', 2, 'string', repeated=False, packed=False),
            'createdAt': FieldDescriptor('createdAt', 3, 'int64', repeated=False, packed=False),
            'deleted': FieldDescriptor('deleted', 4, 'bool', repeated=False, packed=False),
            'unstructuredContent': FieldDescriptor('unstructuredContent', 5, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class NotificationActivitySettingAction(MessageBase):
        class NotificationActivitySetting(enum.IntEnum):
            DEFAULT_ALL_MESSAGES = 0
            ALL_MESSAGES = 1
            HIGHLIGHTS = 2
            DEFAULT_HIGHLIGHTS = 3
        FIELDS = {
            'notificationActivitySetting': FieldDescriptor('notificationActivitySetting', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.NotificationActivitySettingAction.NotificationActivitySetting'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class NuxAction(MessageBase):
        FIELDS = {
            'acknowledged': FieldDescriptor('acknowledged', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PaymentInfoAction(MessageBase):
        FIELDS = {
            'cpi': FieldDescriptor('cpi', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PaymentTosAction(MessageBase):
        class PaymentNotice(enum.IntEnum):
            BR_PAY_PRIVACY_POLICY = 0
        FIELDS = {
            'paymentNotice': FieldDescriptor('paymentNotice', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.PaymentTosAction.PaymentNotice'),
            'accepted': FieldDescriptor('accepted', 2, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PinAction(MessageBase):
        FIELDS = {
            'pinned': FieldDescriptor('pinned', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PnForLidChatAction(MessageBase):
        FIELDS = {
            'pnJid': FieldDescriptor('pnJid', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PrimaryFeature(MessageBase):
        FIELDS = {
            'flags': FieldDescriptor('flags', 1, 'string', repeated=True, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PrimaryVersionAction(MessageBase):
        FIELDS = {
            'version': FieldDescriptor('version', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PrivacySettingChannelsPersonalisedRecommendationAction(MessageBase):
        FIELDS = {
            'isUserOptedOut': FieldDescriptor('isUserOptedOut', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PrivacySettingDisableLinkPreviewsAction(MessageBase):
        FIELDS = {
            'isPreviewsDisabled': FieldDescriptor('isPreviewsDisabled', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PrivacySettingRelayAllCalls(MessageBase):
        FIELDS = {
            'isEnabled': FieldDescriptor('isEnabled', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PrivateProcessingSettingAction(MessageBase):
        class PrivateProcessingStatus(enum.IntEnum):
            UNDEFINED = 0
            ENABLED = 1
            DISABLED = 2
        FIELDS = {
            'privateProcessingStatus': FieldDescriptor('privateProcessingStatus', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.PrivateProcessingSettingAction.PrivateProcessingStatus'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class PushNameSetting(MessageBase):
        FIELDS = {
            'name': FieldDescriptor('name', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class QuickReplyAction(MessageBase):
        FIELDS = {
            'shortcut': FieldDescriptor('shortcut', 1, 'string', repeated=False, packed=False),
            'message': FieldDescriptor('message', 2, 'string', repeated=False, packed=False),
            'keywords': FieldDescriptor('keywords', 3, 'string', repeated=True, packed=False),
            'count': FieldDescriptor('count', 4, 'int32', repeated=False, packed=False),
            'deleted': FieldDescriptor('deleted', 5, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class RecentEmojiWeightsAction(MessageBase):
        FIELDS = {
            'weights': FieldDescriptor('weights', 1, "message", repeated=True, packed=False, _msg_path='RecentEmojiWeight'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class RemoveRecentStickerAction(MessageBase):
        FIELDS = {
            'lastStickerSentTs': FieldDescriptor('lastStickerSentTs', 1, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StarAction(MessageBase):
        FIELDS = {
            'starred': FieldDescriptor('starred', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StatusPostOptInNotificationPreferencesAction(MessageBase):
        FIELDS = {
            'enabled': FieldDescriptor('enabled', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StatusPrivacyAction(MessageBase):
        class StatusDistributionMode(enum.IntEnum):
            ALLOW_LIST = 0
            DENY_LIST = 1
            CONTACTS = 2
            CLOSE_FRIENDS = 3
        FIELDS = {
            'mode': FieldDescriptor('mode', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.StatusPrivacyAction.StatusDistributionMode'),
            'userJid': FieldDescriptor('userJid', 2, 'string', repeated=True, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class StickerAction(MessageBase):
        FIELDS = {
            'url': FieldDescriptor('url', 1, 'string', repeated=False, packed=False),
            'fileEncSha256': FieldDescriptor('fileEncSha256', 2, 'bytes', repeated=False, packed=False),
            'mediaKey': FieldDescriptor('mediaKey', 3, 'bytes', repeated=False, packed=False),
            'mimetype': FieldDescriptor('mimetype', 4, 'string', repeated=False, packed=False),
            'height': FieldDescriptor('height', 5, 'uint32', repeated=False, packed=False),
            'width': FieldDescriptor('width', 6, 'uint32', repeated=False, packed=False),
            'directPath': FieldDescriptor('directPath', 7, 'string', repeated=False, packed=False),
            'fileLength': FieldDescriptor('fileLength', 8, 'uint64', repeated=False, packed=False),
            'isFavorite': FieldDescriptor('isFavorite', 9, 'bool', repeated=False, packed=False),
            'deviceIdHint': FieldDescriptor('deviceIdHint', 10, 'uint32', repeated=False, packed=False),
            'isLottie': FieldDescriptor('isLottie', 11, 'bool', repeated=False, packed=False),
            'imageHash': FieldDescriptor('imageHash', 12, 'string', repeated=False, packed=False),
            'isAvatarSticker': FieldDescriptor('isAvatarSticker', 13, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class SubscriptionAction(MessageBase):
        FIELDS = {
            'isDeactivated': FieldDescriptor('isDeactivated', 1, 'bool', repeated=False, packed=False),
            'isAutoRenewing': FieldDescriptor('isAutoRenewing', 2, 'bool', repeated=False, packed=False),
            'expirationDate': FieldDescriptor('expirationDate', 3, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class SyncActionMessage(MessageBase):
        FIELDS = {
            'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
            'timestamp': FieldDescriptor('timestamp', 2, 'int64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class SyncActionMessageRange(MessageBase):
        FIELDS = {
            'lastMessageTimestamp': FieldDescriptor('lastMessageTimestamp', 1, 'int64', repeated=False, packed=False),
            'lastSystemMessageTimestamp': FieldDescriptor('lastSystemMessageTimestamp', 2, 'int64', repeated=False, packed=False),
            'messages': FieldDescriptor('messages', 3, "message", repeated=True, packed=False, _msg_path='SyncActionValue.SyncActionMessage'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class TimeFormatAction(MessageBase):
        FIELDS = {
            'isTwentyFourHourFormatEnabled': FieldDescriptor('isTwentyFourHourFormatEnabled', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class UGCBot(MessageBase):
        FIELDS = {
            'definition': FieldDescriptor('definition', 1, 'bytes', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class UnarchiveChatsSetting(MessageBase):
        FIELDS = {
            'unarchiveChats': FieldDescriptor('unarchiveChats', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class UserStatusMuteAction(MessageBase):
        FIELDS = {
            'muted': FieldDescriptor('muted', 1, 'bool', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class UsernameChatStartModeAction(MessageBase):
        class ChatStartMode(enum.IntEnum):
            LID = 1
            PN = 2
        FIELDS = {
            'chatStartMode': FieldDescriptor('chatStartMode', 1, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.UsernameChatStartModeAction.ChatStartMode'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class WaffleAccountLinkStateAction(MessageBase):
        class AccountLinkState(enum.IntEnum):
            ACTIVE = 0
            PAUSED = 1
            UNLINKED = 2
        FIELDS = {
            'linkState': FieldDescriptor('linkState', 2, "enum", repeated=False, packed=False, _enum_path='SyncActionValue.WaffleAccountLinkStateAction.AccountLinkState'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class WamoUserIdentifierAction(MessageBase):
        FIELDS = {
            'identifier': FieldDescriptor('identifier', 1, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'timestamp': FieldDescriptor('timestamp', 1, 'int64', repeated=False, packed=False),
        'starAction': FieldDescriptor('starAction', 2, "message", repeated=False, packed=False, _msg_path='SyncActionValue.StarAction'),
        'contactAction': FieldDescriptor('contactAction', 3, "message", repeated=False, packed=False, _msg_path='SyncActionValue.ContactAction'),
        'muteAction': FieldDescriptor('muteAction', 4, "message", repeated=False, packed=False, _msg_path='SyncActionValue.MuteAction'),
        'pinAction': FieldDescriptor('pinAction', 5, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PinAction'),
        'pushNameSetting': FieldDescriptor('pushNameSetting', 7, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PushNameSetting'),
        'quickReplyAction': FieldDescriptor('quickReplyAction', 8, "message", repeated=False, packed=False, _msg_path='SyncActionValue.QuickReplyAction'),
        'recentEmojiWeightsAction': FieldDescriptor('recentEmojiWeightsAction', 11, "message", repeated=False, packed=False, _msg_path='SyncActionValue.RecentEmojiWeightsAction'),
        'labelEditAction': FieldDescriptor('labelEditAction', 14, "message", repeated=False, packed=False, _msg_path='SyncActionValue.LabelEditAction'),
        'labelAssociationAction': FieldDescriptor('labelAssociationAction', 15, "message", repeated=False, packed=False, _msg_path='SyncActionValue.LabelAssociationAction'),
        'localeSetting': FieldDescriptor('localeSetting', 16, "message", repeated=False, packed=False, _msg_path='SyncActionValue.LocaleSetting'),
        'archiveChatAction': FieldDescriptor('archiveChatAction', 17, "message", repeated=False, packed=False, _msg_path='SyncActionValue.ArchiveChatAction'),
        'deleteMessageForMeAction': FieldDescriptor('deleteMessageForMeAction', 18, "message", repeated=False, packed=False, _msg_path='SyncActionValue.DeleteMessageForMeAction'),
        'keyExpiration': FieldDescriptor('keyExpiration', 19, "message", repeated=False, packed=False, _msg_path='SyncActionValue.KeyExpiration'),
        'markChatAsReadAction': FieldDescriptor('markChatAsReadAction', 20, "message", repeated=False, packed=False, _msg_path='SyncActionValue.MarkChatAsReadAction'),
        'clearChatAction': FieldDescriptor('clearChatAction', 21, "message", repeated=False, packed=False, _msg_path='SyncActionValue.ClearChatAction'),
        'deleteChatAction': FieldDescriptor('deleteChatAction', 22, "message", repeated=False, packed=False, _msg_path='SyncActionValue.DeleteChatAction'),
        'unarchiveChatsSetting': FieldDescriptor('unarchiveChatsSetting', 23, "message", repeated=False, packed=False, _msg_path='SyncActionValue.UnarchiveChatsSetting'),
        'primaryFeature': FieldDescriptor('primaryFeature', 24, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PrimaryFeature'),
        'androidUnsupportedActions': FieldDescriptor('androidUnsupportedActions', 26, "message", repeated=False, packed=False, _msg_path='SyncActionValue.AndroidUnsupportedActions'),
        'agentAction': FieldDescriptor('agentAction', 27, "message", repeated=False, packed=False, _msg_path='SyncActionValue.AgentAction'),
        'subscriptionAction': FieldDescriptor('subscriptionAction', 28, "message", repeated=False, packed=False, _msg_path='SyncActionValue.SubscriptionAction'),
        'userStatusMuteAction': FieldDescriptor('userStatusMuteAction', 29, "message", repeated=False, packed=False, _msg_path='SyncActionValue.UserStatusMuteAction'),
        'timeFormatAction': FieldDescriptor('timeFormatAction', 30, "message", repeated=False, packed=False, _msg_path='SyncActionValue.TimeFormatAction'),
        'nuxAction': FieldDescriptor('nuxAction', 31, "message", repeated=False, packed=False, _msg_path='SyncActionValue.NuxAction'),
        'primaryVersionAction': FieldDescriptor('primaryVersionAction', 32, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PrimaryVersionAction'),
        'stickerAction': FieldDescriptor('stickerAction', 33, "message", repeated=False, packed=False, _msg_path='SyncActionValue.StickerAction'),
        'removeRecentStickerAction': FieldDescriptor('removeRecentStickerAction', 34, "message", repeated=False, packed=False, _msg_path='SyncActionValue.RemoveRecentStickerAction'),
        'chatAssignment': FieldDescriptor('chatAssignment', 35, "message", repeated=False, packed=False, _msg_path='SyncActionValue.ChatAssignmentAction'),
        'chatAssignmentOpenedStatus': FieldDescriptor('chatAssignmentOpenedStatus', 36, "message", repeated=False, packed=False, _msg_path='SyncActionValue.ChatAssignmentOpenedStatusAction'),
        'pnForLidChatAction': FieldDescriptor('pnForLidChatAction', 37, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PnForLidChatAction'),
        'marketingMessageAction': FieldDescriptor('marketingMessageAction', 38, "message", repeated=False, packed=False, _msg_path='SyncActionValue.MarketingMessageAction'),
        'marketingMessageBroadcastAction': FieldDescriptor('marketingMessageBroadcastAction', 39, "message", repeated=False, packed=False, _msg_path='SyncActionValue.MarketingMessageBroadcastAction'),
        'externalWebBetaAction': FieldDescriptor('externalWebBetaAction', 40, "message", repeated=False, packed=False, _msg_path='SyncActionValue.ExternalWebBetaAction'),
        'privacySettingRelayAllCalls': FieldDescriptor('privacySettingRelayAllCalls', 41, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PrivacySettingRelayAllCalls'),
        'callLogAction': FieldDescriptor('callLogAction', 42, "message", repeated=False, packed=False, _msg_path='SyncActionValue.CallLogAction'),
        'ugcBot': FieldDescriptor('ugcBot', 43, "message", repeated=False, packed=False, _msg_path='SyncActionValue.UGCBot'),
        'statusPrivacy': FieldDescriptor('statusPrivacy', 44, "message", repeated=False, packed=False, _msg_path='SyncActionValue.StatusPrivacyAction'),
        'botWelcomeRequestAction': FieldDescriptor('botWelcomeRequestAction', 45, "message", repeated=False, packed=False, _msg_path='SyncActionValue.BotWelcomeRequestAction'),
        'deleteIndividualCallLog': FieldDescriptor('deleteIndividualCallLog', 46, "message", repeated=False, packed=False, _msg_path='SyncActionValue.DeleteIndividualCallLogAction'),
        'labelReorderingAction': FieldDescriptor('labelReorderingAction', 47, "message", repeated=False, packed=False, _msg_path='SyncActionValue.LabelReorderingAction'),
        'paymentInfoAction': FieldDescriptor('paymentInfoAction', 48, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PaymentInfoAction'),
        'customPaymentMethodsAction': FieldDescriptor('customPaymentMethodsAction', 49, "message", repeated=False, packed=False, _msg_path='SyncActionValue.CustomPaymentMethodsAction'),
        'lockChatAction': FieldDescriptor('lockChatAction', 50, "message", repeated=False, packed=False, _msg_path='SyncActionValue.LockChatAction'),
        'chatLockSettings': FieldDescriptor('chatLockSettings', 51, "message", repeated=False, packed=False, _msg_path='ChatLockSettings'),
        'wamoUserIdentifierAction': FieldDescriptor('wamoUserIdentifierAction', 52, "message", repeated=False, packed=False, _msg_path='SyncActionValue.WamoUserIdentifierAction'),
        'privacySettingDisableLinkPreviewsAction': FieldDescriptor('privacySettingDisableLinkPreviewsAction', 53, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PrivacySettingDisableLinkPreviewsAction'),
        'deviceCapabilities': FieldDescriptor('deviceCapabilities', 54, "message", repeated=False, packed=False, _msg_path='DeviceCapabilities'),
        'noteEditAction': FieldDescriptor('noteEditAction', 55, "message", repeated=False, packed=False, _msg_path='SyncActionValue.NoteEditAction'),
        'favoritesAction': FieldDescriptor('favoritesAction', 56, "message", repeated=False, packed=False, _msg_path='SyncActionValue.FavoritesAction'),
        'merchantPaymentPartnerAction': FieldDescriptor('merchantPaymentPartnerAction', 57, "message", repeated=False, packed=False, _msg_path='SyncActionValue.MerchantPaymentPartnerAction'),
        'waffleAccountLinkStateAction': FieldDescriptor('waffleAccountLinkStateAction', 58, "message", repeated=False, packed=False, _msg_path='SyncActionValue.WaffleAccountLinkStateAction'),
        'usernameChatStartMode': FieldDescriptor('usernameChatStartMode', 59, "message", repeated=False, packed=False, _msg_path='SyncActionValue.UsernameChatStartModeAction'),
        'notificationActivitySettingAction': FieldDescriptor('notificationActivitySettingAction', 60, "message", repeated=False, packed=False, _msg_path='SyncActionValue.NotificationActivitySettingAction'),
        'lidContactAction': FieldDescriptor('lidContactAction', 61, "message", repeated=False, packed=False, _msg_path='SyncActionValue.LidContactAction'),
        'ctwaPerCustomerDataSharingAction': FieldDescriptor('ctwaPerCustomerDataSharingAction', 62, "message", repeated=False, packed=False, _msg_path='SyncActionValue.CtwaPerCustomerDataSharingAction'),
        'paymentTosAction': FieldDescriptor('paymentTosAction', 63, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PaymentTosAction'),
        'privacySettingChannelsPersonalisedRecommendationAction': FieldDescriptor('privacySettingChannelsPersonalisedRecommendationAction', 64, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PrivacySettingChannelsPersonalisedRecommendationAction'),
        'businessBroadcastAssociationAction': FieldDescriptor('businessBroadcastAssociationAction', 65, "message", repeated=False, packed=False, _msg_path='SyncActionValue.BusinessBroadcastAssociationAction'),
        'detectedOutcomesStatusAction': FieldDescriptor('detectedOutcomesStatusAction', 66, "message", repeated=False, packed=False, _msg_path='SyncActionValue.DetectedOutcomesStatusAction'),
        'maibaAiFeaturesControlAction': FieldDescriptor('maibaAiFeaturesControlAction', 68, "message", repeated=False, packed=False, _msg_path='SyncActionValue.MaibaAIFeaturesControlAction'),
        'businessBroadcastListAction': FieldDescriptor('businessBroadcastListAction', 69, "message", repeated=False, packed=False, _msg_path='SyncActionValue.BusinessBroadcastListAction'),
        'musicUserIdAction': FieldDescriptor('musicUserIdAction', 70, "message", repeated=False, packed=False, _msg_path='SyncActionValue.MusicUserIdAction'),
        'statusPostOptInNotificationPreferencesAction': FieldDescriptor('statusPostOptInNotificationPreferencesAction', 71, "message", repeated=False, packed=False, _msg_path='SyncActionValue.StatusPostOptInNotificationPreferencesAction'),
        'avatarUpdatedAction': FieldDescriptor('avatarUpdatedAction', 72, "message", repeated=False, packed=False, _msg_path='SyncActionValue.AvatarUpdatedAction'),
        'privateProcessingSettingAction': FieldDescriptor('privateProcessingSettingAction', 74, "message", repeated=False, packed=False, _msg_path='SyncActionValue.PrivateProcessingSettingAction'),
        'newsletterSavedInterestsAction': FieldDescriptor('newsletterSavedInterestsAction', 75, "message", repeated=False, packed=False, _msg_path='SyncActionValue.NewsletterSavedInterestsAction'),
        'aiThreadRenameAction': FieldDescriptor('aiThreadRenameAction', 76, "message", repeated=False, packed=False, _msg_path='SyncActionValue.AiThreadRenameAction'),
        'interactiveMessageAction': FieldDescriptor('interactiveMessageAction', 77, "message", repeated=False, packed=False, _msg_path='SyncActionValue.InteractiveMessageAction'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncdIndex(MessageBase):
    FIELDS = {
        'blob': FieldDescriptor('blob', 1, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncdMutation(MessageBase):
    class SyncdOperation(enum.IntEnum):
        SET = 0
        REMOVE = 1
    FIELDS = {
        'operation': FieldDescriptor('operation', 1, "enum", repeated=False, packed=False, _enum_path='SyncdMutation.SyncdOperation'),
        'record': FieldDescriptor('record', 2, "message", repeated=False, packed=False, _msg_path='SyncdRecord'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncdMutations(MessageBase):
    FIELDS = {
        'mutations': FieldDescriptor('mutations', 1, "message", repeated=True, packed=False, _msg_path='SyncdMutation'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncdPatch(MessageBase):
    FIELDS = {
        'version': FieldDescriptor('version', 1, "message", repeated=False, packed=False, _msg_path='SyncdVersion'),
        'mutations': FieldDescriptor('mutations', 2, "message", repeated=True, packed=False, _msg_path='SyncdMutation'),
        'externalMutations': FieldDescriptor('externalMutations', 3, "message", repeated=False, packed=False, _msg_path='ExternalBlobReference'),
        'snapshotMac': FieldDescriptor('snapshotMac', 4, 'bytes', repeated=False, packed=False),
        'patchMac': FieldDescriptor('patchMac', 5, 'bytes', repeated=False, packed=False),
        'keyId': FieldDescriptor('keyId', 6, "message", repeated=False, packed=False, _msg_path='KeyId'),
        'exitCode': FieldDescriptor('exitCode', 7, "message", repeated=False, packed=False, _msg_path='ExitCode'),
        'deviceIndex': FieldDescriptor('deviceIndex', 8, 'uint32', repeated=False, packed=False),
        'clientDebugData': FieldDescriptor('clientDebugData', 9, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncdRecord(MessageBase):
    FIELDS = {
        'index': FieldDescriptor('index', 1, "message", repeated=False, packed=False, _msg_path='SyncdIndex'),
        'value': FieldDescriptor('value', 2, "message", repeated=False, packed=False, _msg_path='SyncdValue'),
        'keyId': FieldDescriptor('keyId', 3, "message", repeated=False, packed=False, _msg_path='KeyId'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncdSnapshot(MessageBase):
    FIELDS = {
        'version': FieldDescriptor('version', 1, "message", repeated=False, packed=False, _msg_path='SyncdVersion'),
        'records': FieldDescriptor('records', 2, "message", repeated=True, packed=False, _msg_path='SyncdRecord'),
        'mac': FieldDescriptor('mac', 3, 'bytes', repeated=False, packed=False),
        'keyId': FieldDescriptor('keyId', 4, "message", repeated=False, packed=False, _msg_path='KeyId'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncdValue(MessageBase):
    FIELDS = {
        'blob': FieldDescriptor('blob', 1, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class SyncdVersion(MessageBase):
    FIELDS = {
        'version': FieldDescriptor('version', 1, 'uint64', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class TapLinkAction(MessageBase):
    FIELDS = {
        'title': FieldDescriptor('title', 1, 'string', repeated=False, packed=False),
        'tapUrl': FieldDescriptor('tapUrl', 2, 'string', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class TemplateButton(MessageBase):
    class CallButton(MessageBase):
        FIELDS = {
            'displayText': FieldDescriptor('displayText', 1, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage'),
            'phoneNumber': FieldDescriptor('phoneNumber', 2, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class QuickReplyButton(MessageBase):
        FIELDS = {
            'displayText': FieldDescriptor('displayText', 1, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage'),
            'id': FieldDescriptor('id', 2, 'string', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    class URLButton(MessageBase):
        FIELDS = {
            'displayText': FieldDescriptor('displayText', 1, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage'),
            'url': FieldDescriptor('url', 2, "message", repeated=False, packed=False, _msg_path='Message.HighlyStructuredMessage'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'index': FieldDescriptor('index', 4, 'uint32', repeated=False, packed=False),
        'quickReplyButton': FieldDescriptor('quickReplyButton', 1, "message", repeated=False, packed=False, _msg_path='TemplateButton.QuickReplyButton'),
        'urlButton': FieldDescriptor('urlButton', 2, "message", repeated=False, packed=False, _msg_path='TemplateButton.URLButton'),
        'callButton': FieldDescriptor('callButton', 3, "message", repeated=False, packed=False, _msg_path='TemplateButton.CallButton'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class ThreadID(MessageBase):
    class ThreadType(enum.IntEnum):
        UNKNOWN = 0
        VIEW_REPLIES = 1
        AI_THREAD = 2
    FIELDS = {
        'threadType': FieldDescriptor('threadType', 1, "enum", repeated=False, packed=False, _enum_path='ThreadID.ThreadType'),
        'threadKey': FieldDescriptor('threadKey', 2, "message", repeated=False, packed=False, _msg_path='MessageKey'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class UrlTrackingMap(MessageBase):
    class UrlTrackingMapElement(MessageBase):
        FIELDS = {
            'originalUrl': FieldDescriptor('originalUrl', 1, 'string', repeated=False, packed=False),
            'unconsentedUsersUrl': FieldDescriptor('unconsentedUsersUrl', 2, 'string', repeated=False, packed=False),
            'consentedUsersUrl': FieldDescriptor('consentedUsersUrl', 3, 'string', repeated=False, packed=False),
            'cardIndex': FieldDescriptor('cardIndex', 4, 'uint32', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'urlTrackingMapElements': FieldDescriptor('urlTrackingMapElements', 1, "message", repeated=True, packed=False, _msg_path='UrlTrackingMap.UrlTrackingMapElement'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class UserPassword(MessageBase):
    class Encoding(enum.IntEnum):
        UTF8 = 0
        UTF8_BROKEN = 1
    class Transformer(enum.IntEnum):
        NONE = 0
        PBKDF2_HMAC_SHA512 = 1
        PBKDF2_HMAC_SHA384 = 2
    class TransformerArg(MessageBase):
        class Value(MessageBase):
            FIELDS = {
                'asBlob': FieldDescriptor('asBlob', 1, 'bytes', repeated=False, packed=False),
                'asUnsignedInteger': FieldDescriptor('asUnsignedInteger', 2, 'uint32', repeated=False, packed=False),
            }
            _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
        FIELDS = {
            'key': FieldDescriptor('key', 1, 'string', repeated=False, packed=False),
            'value': FieldDescriptor('value', 2, "message", repeated=False, packed=False, _msg_path='UserPassword.TransformerArg.Value'),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'encoding': FieldDescriptor('encoding', 1, "enum", repeated=False, packed=False, _enum_path='UserPassword.Encoding'),
        'transformer': FieldDescriptor('transformer', 2, "enum", repeated=False, packed=False, _enum_path='UserPassword.Transformer'),
        'transformerArg': FieldDescriptor('transformerArg', 3, "message", repeated=True, packed=False, _msg_path='UserPassword.TransformerArg'),
        'transformedData': FieldDescriptor('transformedData', 4, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class UserReceipt(MessageBase):
    FIELDS = {
        'userJid': FieldDescriptor('userJid', 1, 'string', repeated=False, packed=False),
        'receiptTimestamp': FieldDescriptor('receiptTimestamp', 2, 'int64', repeated=False, packed=False),
        'readTimestamp': FieldDescriptor('readTimestamp', 3, 'int64', repeated=False, packed=False),
        'playedTimestamp': FieldDescriptor('playedTimestamp', 4, 'int64', repeated=False, packed=False),
        'pendingDeviceJid': FieldDescriptor('pendingDeviceJid', 5, 'string', repeated=True, packed=False),
        'deliveredDeviceJid': FieldDescriptor('deliveredDeviceJid', 6, 'string', repeated=True, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class VerifiedNameCertificate(MessageBase):
    class Details(MessageBase):
        FIELDS = {
            'serial': FieldDescriptor('serial', 1, 'uint64', repeated=False, packed=False),
            'issuer': FieldDescriptor('issuer', 2, 'string', repeated=False, packed=False),
            'verifiedName': FieldDescriptor('verifiedName', 4, 'string', repeated=False, packed=False),
            'localizedNames': FieldDescriptor('localizedNames', 8, "message", repeated=True, packed=False, _msg_path='LocalizedName'),
            'issueTime': FieldDescriptor('issueTime', 10, 'uint64', repeated=False, packed=False),
        }
        _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}
    FIELDS = {
        'details': FieldDescriptor('details', 1, 'bytes', repeated=False, packed=False),
        'signature': FieldDescriptor('signature', 2, 'bytes', repeated=False, packed=False),
        'serverSignature': FieldDescriptor('serverSignature', 3, 'bytes', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class WallpaperSettings(MessageBase):
    FIELDS = {
        'filename': FieldDescriptor('filename', 1, 'string', repeated=False, packed=False),
        'opacity': FieldDescriptor('opacity', 2, 'uint32', repeated=False, packed=False),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class WebFeatures(MessageBase):
    class Flag(enum.IntEnum):
        NOT_STARTED = 0
        FORCE_UPGRADE = 1
        DEVELOPMENT = 2
        PRODUCTION = 3
    FIELDS = {
        'labelsDisplay': FieldDescriptor('labelsDisplay', 1, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'voipIndividualOutgoing': FieldDescriptor('voipIndividualOutgoing', 2, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'groupsV3': FieldDescriptor('groupsV3', 3, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'groupsV3Create': FieldDescriptor('groupsV3Create', 4, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'changeNumberV2': FieldDescriptor('changeNumberV2', 5, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'queryStatusV3Thumbnail': FieldDescriptor('queryStatusV3Thumbnail', 6, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'liveLocations': FieldDescriptor('liveLocations', 7, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'queryVname': FieldDescriptor('queryVname', 8, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'voipIndividualIncoming': FieldDescriptor('voipIndividualIncoming', 9, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'quickRepliesQuery': FieldDescriptor('quickRepliesQuery', 10, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'payments': FieldDescriptor('payments', 11, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'stickerPackQuery': FieldDescriptor('stickerPackQuery', 12, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'liveLocationsFinal': FieldDescriptor('liveLocationsFinal', 13, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'labelsEdit': FieldDescriptor('labelsEdit', 14, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'mediaUpload': FieldDescriptor('mediaUpload', 15, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'mediaUploadRichQuickReplies': FieldDescriptor('mediaUploadRichQuickReplies', 18, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'vnameV2': FieldDescriptor('vnameV2', 19, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'videoPlaybackUrl': FieldDescriptor('videoPlaybackUrl', 20, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'statusRanking': FieldDescriptor('statusRanking', 21, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'voipIndividualVideo': FieldDescriptor('voipIndividualVideo', 22, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'thirdPartyStickers': FieldDescriptor('thirdPartyStickers', 23, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'frequentlyForwardedSetting': FieldDescriptor('frequentlyForwardedSetting', 24, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'groupsV4JoinPermission': FieldDescriptor('groupsV4JoinPermission', 25, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'recentStickers': FieldDescriptor('recentStickers', 26, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'catalog': FieldDescriptor('catalog', 27, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'starredStickers': FieldDescriptor('starredStickers', 28, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'voipGroupCall': FieldDescriptor('voipGroupCall', 29, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'templateMessage': FieldDescriptor('templateMessage', 30, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'templateMessageInteractivity': FieldDescriptor('templateMessageInteractivity', 31, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'ephemeralMessages': FieldDescriptor('ephemeralMessages', 32, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'e2ENotificationSync': FieldDescriptor('e2ENotificationSync', 33, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'recentStickersV2': FieldDescriptor('recentStickersV2', 34, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'recentStickersV3': FieldDescriptor('recentStickersV3', 36, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'userNotice': FieldDescriptor('userNotice', 37, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'support': FieldDescriptor('support', 39, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'groupUiiCleanup': FieldDescriptor('groupUiiCleanup', 40, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'groupDogfoodingInternalOnly': FieldDescriptor('groupDogfoodingInternalOnly', 41, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'settingsSync': FieldDescriptor('settingsSync', 42, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'archiveV2': FieldDescriptor('archiveV2', 43, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'ephemeralAllowGroupMembers': FieldDescriptor('ephemeralAllowGroupMembers', 44, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'ephemeral24HDuration': FieldDescriptor('ephemeral24HDuration', 45, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'mdForceUpgrade': FieldDescriptor('mdForceUpgrade', 46, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'disappearingMode': FieldDescriptor('disappearingMode', 47, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'externalMdOptInAvailable': FieldDescriptor('externalMdOptInAvailable', 48, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
        'noDeleteMessageTimeLimit': FieldDescriptor('noDeleteMessageTimeLimit', 49, "enum", repeated=False, packed=False, _enum_path='WebFeatures.Flag'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class WebMessageInfo(MessageBase):
    class BizPrivacyStatus(enum.IntEnum):
        E2EE = 0
        FB = 2
        BSP = 1
        BSP_AND_FB = 3
    class Status(enum.IntEnum):
        ERROR = 0
        PENDING = 1
        SERVER_ACK = 2
        DELIVERY_ACK = 3
        READ = 4
        PLAYED = 5
    class StubType(enum.IntEnum):
        UNKNOWN = 0
        REVOKE = 1
        CIPHERTEXT = 2
        FUTUREPROOF = 3
        NON_VERIFIED_TRANSITION = 4
        UNVERIFIED_TRANSITION = 5
        VERIFIED_TRANSITION = 6
        VERIFIED_LOW_UNKNOWN = 7
        VERIFIED_HIGH = 8
        VERIFIED_INITIAL_UNKNOWN = 9
        VERIFIED_INITIAL_LOW = 10
        VERIFIED_INITIAL_HIGH = 11
        VERIFIED_TRANSITION_ANY_TO_NONE = 12
        VERIFIED_TRANSITION_ANY_TO_HIGH = 13
        VERIFIED_TRANSITION_HIGH_TO_LOW = 14
        VERIFIED_TRANSITION_HIGH_TO_UNKNOWN = 15
        VERIFIED_TRANSITION_UNKNOWN_TO_LOW = 16
        VERIFIED_TRANSITION_LOW_TO_UNKNOWN = 17
        VERIFIED_TRANSITION_NONE_TO_LOW = 18
        VERIFIED_TRANSITION_NONE_TO_UNKNOWN = 19
        GROUP_CREATE = 20
        GROUP_CHANGE_SUBJECT = 21
        GROUP_CHANGE_ICON = 22
        GROUP_CHANGE_INVITE_LINK = 23
        GROUP_CHANGE_DESCRIPTION = 24
        GROUP_CHANGE_RESTRICT = 25
        GROUP_CHANGE_ANNOUNCE = 26
        GROUP_PARTICIPANT_ADD = 27
        GROUP_PARTICIPANT_REMOVE = 28
        GROUP_PARTICIPANT_PROMOTE = 29
        GROUP_PARTICIPANT_DEMOTE = 30
        GROUP_PARTICIPANT_INVITE = 31
        GROUP_PARTICIPANT_LEAVE = 32
        GROUP_PARTICIPANT_CHANGE_NUMBER = 33
        BROADCAST_CREATE = 34
        BROADCAST_ADD = 35
        BROADCAST_REMOVE = 36
        GENERIC_NOTIFICATION = 37
        E2E_IDENTITY_CHANGED = 38
        E2E_ENCRYPTED = 39
        CALL_MISSED_VOICE = 40
        CALL_MISSED_VIDEO = 41
        INDIVIDUAL_CHANGE_NUMBER = 42
        GROUP_DELETE = 43
        GROUP_ANNOUNCE_MODE_MESSAGE_BOUNCE = 44
        CALL_MISSED_GROUP_VOICE = 45
        CALL_MISSED_GROUP_VIDEO = 46
        PAYMENT_CIPHERTEXT = 47
        PAYMENT_FUTUREPROOF = 48
        PAYMENT_TRANSACTION_STATUS_UPDATE_FAILED = 49
        PAYMENT_TRANSACTION_STATUS_UPDATE_REFUNDED = 50
        PAYMENT_TRANSACTION_STATUS_UPDATE_REFUND_FAILED = 51
        PAYMENT_TRANSACTION_STATUS_RECEIVER_PENDING_SETUP = 52
        PAYMENT_TRANSACTION_STATUS_RECEIVER_SUCCESS_AFTER_HICCUP = 53
        PAYMENT_ACTION_ACCOUNT_SETUP_REMINDER = 54
        PAYMENT_ACTION_SEND_PAYMENT_REMINDER = 55
        PAYMENT_ACTION_SEND_PAYMENT_INVITATION = 56
        PAYMENT_ACTION_REQUEST_DECLINED = 57
        PAYMENT_ACTION_REQUEST_EXPIRED = 58
        PAYMENT_ACTION_REQUEST_CANCELLED = 59
        BIZ_VERIFIED_TRANSITION_TOP_TO_BOTTOM = 60
        BIZ_VERIFIED_TRANSITION_BOTTOM_TO_TOP = 61
        BIZ_INTRO_TOP = 62
        BIZ_INTRO_BOTTOM = 63
        BIZ_NAME_CHANGE = 64
        BIZ_MOVE_TO_CONSUMER_APP = 65
        BIZ_TWO_TIER_MIGRATION_TOP = 66
        BIZ_TWO_TIER_MIGRATION_BOTTOM = 67
        OVERSIZED = 68
        GROUP_CHANGE_NO_FREQUENTLY_FORWARDED = 69
        GROUP_V4_ADD_INVITE_SENT = 70
        GROUP_PARTICIPANT_ADD_REQUEST_JOIN = 71
        CHANGE_EPHEMERAL_SETTING = 72
        E2E_DEVICE_CHANGED = 73
        VIEWED_ONCE = 74
        E2E_ENCRYPTED_NOW = 75
        BLUE_MSG_BSP_FB_TO_BSP_PREMISE = 76
        BLUE_MSG_BSP_FB_TO_SELF_FB = 77
        BLUE_MSG_BSP_FB_TO_SELF_PREMISE = 78
        BLUE_MSG_BSP_FB_UNVERIFIED = 79
        BLUE_MSG_BSP_FB_UNVERIFIED_TO_SELF_PREMISE_VERIFIED = 80
        BLUE_MSG_BSP_FB_VERIFIED = 81
        BLUE_MSG_BSP_FB_VERIFIED_TO_SELF_PREMISE_UNVERIFIED = 82
        BLUE_MSG_BSP_PREMISE_TO_SELF_PREMISE = 83
        BLUE_MSG_BSP_PREMISE_UNVERIFIED = 84
        BLUE_MSG_BSP_PREMISE_UNVERIFIED_TO_SELF_PREMISE_VERIFIED = 85
        BLUE_MSG_BSP_PREMISE_VERIFIED = 86
        BLUE_MSG_BSP_PREMISE_VERIFIED_TO_SELF_PREMISE_UNVERIFIED = 87
        BLUE_MSG_CONSUMER_TO_BSP_FB_UNVERIFIED = 88
        BLUE_MSG_CONSUMER_TO_BSP_PREMISE_UNVERIFIED = 89
        BLUE_MSG_CONSUMER_TO_SELF_FB_UNVERIFIED = 90
        BLUE_MSG_CONSUMER_TO_SELF_PREMISE_UNVERIFIED = 91
        BLUE_MSG_SELF_FB_TO_BSP_PREMISE = 92
        BLUE_MSG_SELF_FB_TO_SELF_PREMISE = 93
        BLUE_MSG_SELF_FB_UNVERIFIED = 94
        BLUE_MSG_SELF_FB_UNVERIFIED_TO_SELF_PREMISE_VERIFIED = 95
        BLUE_MSG_SELF_FB_VERIFIED = 96
        BLUE_MSG_SELF_FB_VERIFIED_TO_SELF_PREMISE_UNVERIFIED = 97
        BLUE_MSG_SELF_PREMISE_TO_BSP_PREMISE = 98
        BLUE_MSG_SELF_PREMISE_UNVERIFIED = 99
        BLUE_MSG_SELF_PREMISE_VERIFIED = 100
        BLUE_MSG_TO_BSP_FB = 101
        BLUE_MSG_TO_CONSUMER = 102
        BLUE_MSG_TO_SELF_FB = 103
        BLUE_MSG_UNVERIFIED_TO_BSP_FB_VERIFIED = 104
        BLUE_MSG_UNVERIFIED_TO_BSP_PREMISE_VERIFIED = 105
        BLUE_MSG_UNVERIFIED_TO_SELF_FB_VERIFIED = 106
        BLUE_MSG_UNVERIFIED_TO_VERIFIED = 107
        BLUE_MSG_VERIFIED_TO_BSP_FB_UNVERIFIED = 108
        BLUE_MSG_VERIFIED_TO_BSP_PREMISE_UNVERIFIED = 109
        BLUE_MSG_VERIFIED_TO_SELF_FB_UNVERIFIED = 110
        BLUE_MSG_VERIFIED_TO_UNVERIFIED = 111
        BLUE_MSG_BSP_FB_UNVERIFIED_TO_BSP_PREMISE_VERIFIED = 112
        BLUE_MSG_BSP_FB_UNVERIFIED_TO_SELF_FB_VERIFIED = 113
        BLUE_MSG_BSP_FB_VERIFIED_TO_BSP_PREMISE_UNVERIFIED = 114
        BLUE_MSG_BSP_FB_VERIFIED_TO_SELF_FB_UNVERIFIED = 115
        BLUE_MSG_SELF_FB_UNVERIFIED_TO_BSP_PREMISE_VERIFIED = 116
        BLUE_MSG_SELF_FB_VERIFIED_TO_BSP_PREMISE_UNVERIFIED = 117
        E2E_IDENTITY_UNAVAILABLE = 118
        GROUP_CREATING = 119
        GROUP_CREATE_FAILED = 120
        GROUP_BOUNCED = 121
        BLOCK_CONTACT = 122
        EPHEMERAL_SETTING_NOT_APPLIED = 123
        SYNC_FAILED = 124
        SYNCING = 125
        BIZ_PRIVACY_MODE_INIT_FB = 126
        BIZ_PRIVACY_MODE_INIT_BSP = 127
        BIZ_PRIVACY_MODE_TO_FB = 128
        BIZ_PRIVACY_MODE_TO_BSP = 129
        DISAPPEARING_MODE = 130
        E2E_DEVICE_FETCH_FAILED = 131
        ADMIN_REVOKE = 132
        GROUP_INVITE_LINK_GROWTH_LOCKED = 133
        COMMUNITY_LINK_PARENT_GROUP = 134
        COMMUNITY_LINK_SIBLING_GROUP = 135
        COMMUNITY_LINK_SUB_GROUP = 136
        COMMUNITY_UNLINK_PARENT_GROUP = 137
        COMMUNITY_UNLINK_SIBLING_GROUP = 138
        COMMUNITY_UNLINK_SUB_GROUP = 139
        GROUP_PARTICIPANT_ACCEPT = 140
        GROUP_PARTICIPANT_LINKED_GROUP_JOIN = 141
        COMMUNITY_CREATE = 142
        EPHEMERAL_KEEP_IN_CHAT = 143
        GROUP_MEMBERSHIP_JOIN_APPROVAL_REQUEST = 144
        GROUP_MEMBERSHIP_JOIN_APPROVAL_MODE = 145
        INTEGRITY_UNLINK_PARENT_GROUP = 146
        COMMUNITY_PARTICIPANT_PROMOTE = 147
        COMMUNITY_PARTICIPANT_DEMOTE = 148
        COMMUNITY_PARENT_GROUP_DELETED = 149
        COMMUNITY_LINK_PARENT_GROUP_MEMBERSHIP_APPROVAL = 150
        GROUP_PARTICIPANT_JOINED_GROUP_AND_PARENT_GROUP = 151
        MASKED_THREAD_CREATED = 152
        MASKED_THREAD_UNMASKED = 153
        BIZ_CHAT_ASSIGNMENT = 154
        CHAT_PSA = 155
        CHAT_POLL_CREATION_MESSAGE = 156
        CAG_MASKED_THREAD_CREATED = 157
        COMMUNITY_PARENT_GROUP_SUBJECT_CHANGED = 158
        CAG_INVITE_AUTO_ADD = 159
        BIZ_CHAT_ASSIGNMENT_UNASSIGN = 160
        CAG_INVITE_AUTO_JOINED = 161
        SCHEDULED_CALL_START_MESSAGE = 162
        COMMUNITY_INVITE_RICH = 163
        COMMUNITY_INVITE_AUTO_ADD_RICH = 164
        SUB_GROUP_INVITE_RICH = 165
        SUB_GROUP_PARTICIPANT_ADD_RICH = 166
        COMMUNITY_LINK_PARENT_GROUP_RICH = 167
        COMMUNITY_PARTICIPANT_ADD_RICH = 168
        SILENCED_UNKNOWN_CALLER_AUDIO = 169
        SILENCED_UNKNOWN_CALLER_VIDEO = 170
        GROUP_MEMBER_ADD_MODE = 171
        GROUP_MEMBERSHIP_JOIN_APPROVAL_REQUEST_NON_ADMIN_ADD = 172
        COMMUNITY_CHANGE_DESCRIPTION = 173
        SENDER_INVITE = 174
        RECEIVER_INVITE = 175
        COMMUNITY_ALLOW_MEMBER_ADDED_GROUPS = 176
        PINNED_MESSAGE_IN_CHAT = 177
        PAYMENT_INVITE_SETUP_INVITER = 178
        PAYMENT_INVITE_SETUP_INVITEE_RECEIVE_ONLY = 179
        PAYMENT_INVITE_SETUP_INVITEE_SEND_AND_RECEIVE = 180
        LINKED_GROUP_CALL_START = 181
        REPORT_TO_ADMIN_ENABLED_STATUS = 182
        EMPTY_SUBGROUP_CREATE = 183
        SCHEDULED_CALL_CANCEL = 184
        SUBGROUP_ADMIN_TRIGGERED_AUTO_ADD_RICH = 185
        GROUP_CHANGE_RECENT_HISTORY_SHARING = 186
        PAID_MESSAGE_SERVER_CAMPAIGN_ID = 187
        GENERAL_CHAT_CREATE = 188
        GENERAL_CHAT_ADD = 189
        GENERAL_CHAT_AUTO_ADD_DISABLED = 190
        SUGGESTED_SUBGROUP_ANNOUNCE = 191
        BIZ_BOT_1P_MESSAGING_ENABLED = 192
        CHANGE_USERNAME = 193
        BIZ_COEX_PRIVACY_INIT_SELF = 194
        BIZ_COEX_PRIVACY_TRANSITION_SELF = 195
        SUPPORT_AI_EDUCATION = 196
        BIZ_BOT_3P_MESSAGING_ENABLED = 197
        REMINDER_SETUP_MESSAGE = 198
        REMINDER_SENT_MESSAGE = 199
        REMINDER_CANCEL_MESSAGE = 200
        BIZ_COEX_PRIVACY_INIT = 201
        BIZ_COEX_PRIVACY_TRANSITION = 202
        GROUP_DEACTIVATED = 203
        COMMUNITY_DEACTIVATE_SIBLING_GROUP = 204
        EVENT_UPDATED = 205
        EVENT_CANCELED = 206
        COMMUNITY_OWNER_UPDATED = 207
        COMMUNITY_SUB_GROUP_VISIBILITY_HIDDEN = 208
        CAPI_GROUP_NE2EE_SYSTEM_MESSAGE = 209
        STATUS_MENTION = 210
        USER_CONTROLS_SYSTEM_MESSAGE = 211
        SUPPORT_SYSTEM_MESSAGE = 212
        CHANGE_LID = 213
        BIZ_CUSTOMER_3PD_DATA_SHARING_OPT_IN_MESSAGE = 214
        BIZ_CUSTOMER_3PD_DATA_SHARING_OPT_OUT_MESSAGE = 215
        CHANGE_LIMIT_SHARING = 216
        GROUP_MEMBER_LINK_MODE = 217
        BIZ_AUTOMATICALLY_LABELED_CHAT_SYSTEM_MESSAGE = 218
        PHONE_NUMBER_HIDING_CHAT_DEPRECATED_MESSAGE = 219
        QUARANTINED_MESSAGE = 220
        GROUP_MEMBER_SHARE_GROUP_HISTORY_MODE = 221
    FIELDS = {
        'key': FieldDescriptor('key', 1, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'message': FieldDescriptor('message', 2, "message", repeated=False, packed=False, _msg_path='Message'),
        'messageTimestamp': FieldDescriptor('messageTimestamp', 3, 'uint64', repeated=False, packed=False),
        'status': FieldDescriptor('status', 4, "enum", repeated=False, packed=False, _enum_path='WebMessageInfo.Status'),
        'participant': FieldDescriptor('participant', 5, 'string', repeated=False, packed=False),
        'messageC2STimestamp': FieldDescriptor('messageC2STimestamp', 6, 'uint64', repeated=False, packed=False),
        'ignore': FieldDescriptor('ignore', 16, 'bool', repeated=False, packed=False),
        'starred': FieldDescriptor('starred', 17, 'bool', repeated=False, packed=False),
        'broadcast': FieldDescriptor('broadcast', 18, 'bool', repeated=False, packed=False),
        'pushName': FieldDescriptor('pushName', 19, 'string', repeated=False, packed=False),
        'mediaCiphertextSha256': FieldDescriptor('mediaCiphertextSha256', 20, 'bytes', repeated=False, packed=False),
        'multicast': FieldDescriptor('multicast', 21, 'bool', repeated=False, packed=False),
        'urlText': FieldDescriptor('urlText', 22, 'bool', repeated=False, packed=False),
        'urlNumber': FieldDescriptor('urlNumber', 23, 'bool', repeated=False, packed=False),
        'messageStubType': FieldDescriptor('messageStubType', 24, "enum", repeated=False, packed=False, _enum_path='WebMessageInfo.StubType'),
        'clearMedia': FieldDescriptor('clearMedia', 25, 'bool', repeated=False, packed=False),
        'messageStubParameters': FieldDescriptor('messageStubParameters', 26, 'string', repeated=True, packed=False),
        'duration': FieldDescriptor('duration', 27, 'uint32', repeated=False, packed=False),
        'labels': FieldDescriptor('labels', 28, 'string', repeated=True, packed=False),
        'paymentInfo': FieldDescriptor('paymentInfo', 29, "message", repeated=False, packed=False, _msg_path='PaymentInfo'),
        'finalLiveLocation': FieldDescriptor('finalLiveLocation', 30, "message", repeated=False, packed=False, _msg_path='Message.LiveLocationMessage'),
        'quotedPaymentInfo': FieldDescriptor('quotedPaymentInfo', 31, "message", repeated=False, packed=False, _msg_path='PaymentInfo'),
        'ephemeralStartTimestamp': FieldDescriptor('ephemeralStartTimestamp', 32, 'uint64', repeated=False, packed=False),
        'ephemeralDuration': FieldDescriptor('ephemeralDuration', 33, 'uint32', repeated=False, packed=False),
        'ephemeralOffToOn': FieldDescriptor('ephemeralOffToOn', 34, 'bool', repeated=False, packed=False),
        'ephemeralOutOfSync': FieldDescriptor('ephemeralOutOfSync', 35, 'bool', repeated=False, packed=False),
        'bizPrivacyStatus': FieldDescriptor('bizPrivacyStatus', 36, "enum", repeated=False, packed=False, _enum_path='WebMessageInfo.BizPrivacyStatus'),
        'verifiedBizName': FieldDescriptor('verifiedBizName', 37, 'string', repeated=False, packed=False),
        'mediaData': FieldDescriptor('mediaData', 38, "message", repeated=False, packed=False, _msg_path='MediaData'),
        'photoChange': FieldDescriptor('photoChange', 39, "message", repeated=False, packed=False, _msg_path='PhotoChange'),
        'userReceipt': FieldDescriptor('userReceipt', 40, "message", repeated=True, packed=False, _msg_path='UserReceipt'),
        'reactions': FieldDescriptor('reactions', 41, "message", repeated=True, packed=False, _msg_path='Reaction'),
        'quotedStickerData': FieldDescriptor('quotedStickerData', 42, "message", repeated=False, packed=False, _msg_path='MediaData'),
        'futureproofData': FieldDescriptor('futureproofData', 43, 'bytes', repeated=False, packed=False),
        'statusPsa': FieldDescriptor('statusPsa', 44, "message", repeated=False, packed=False, _msg_path='StatusPSA'),
        'pollUpdates': FieldDescriptor('pollUpdates', 45, "message", repeated=True, packed=False, _msg_path='PollUpdate'),
        'pollAdditionalMetadata': FieldDescriptor('pollAdditionalMetadata', 46, "message", repeated=False, packed=False, _msg_path='PollAdditionalMetadata'),
        'agentId': FieldDescriptor('agentId', 47, 'string', repeated=False, packed=False),
        'statusAlreadyViewed': FieldDescriptor('statusAlreadyViewed', 48, 'bool', repeated=False, packed=False),
        'messageSecret': FieldDescriptor('messageSecret', 49, 'bytes', repeated=False, packed=False),
        'keepInChat': FieldDescriptor('keepInChat', 50, "message", repeated=False, packed=False, _msg_path='KeepInChat'),
        'originalSelfAuthorUserJidString': FieldDescriptor('originalSelfAuthorUserJidString', 51, 'string', repeated=False, packed=False),
        'revokeMessageTimestamp': FieldDescriptor('revokeMessageTimestamp', 52, 'uint64', repeated=False, packed=False),
        'pinInChat': FieldDescriptor('pinInChat', 54, "message", repeated=False, packed=False, _msg_path='PinInChat'),
        'premiumMessageInfo': FieldDescriptor('premiumMessageInfo', 55, "message", repeated=False, packed=False, _msg_path='PremiumMessageInfo'),
        'is1PBizBotMessage': FieldDescriptor('is1PBizBotMessage', 56, 'bool', repeated=False, packed=False),
        'isGroupHistoryMessage': FieldDescriptor('isGroupHistoryMessage', 57, 'bool', repeated=False, packed=False),
        'botMessageInvokerJid': FieldDescriptor('botMessageInvokerJid', 58, 'string', repeated=False, packed=False),
        'commentMetadata': FieldDescriptor('commentMetadata', 59, "message", repeated=False, packed=False, _msg_path='CommentMetadata'),
        'eventResponses': FieldDescriptor('eventResponses', 61, "message", repeated=True, packed=False, _msg_path='EventResponse'),
        'reportingTokenInfo': FieldDescriptor('reportingTokenInfo', 62, "message", repeated=False, packed=False, _msg_path='ReportingTokenInfo'),
        'newsletterServerId': FieldDescriptor('newsletterServerId', 63, 'uint64', repeated=False, packed=False),
        'eventAdditionalMetadata': FieldDescriptor('eventAdditionalMetadata', 64, "message", repeated=False, packed=False, _msg_path='EventAdditionalMetadata'),
        'isMentionedInStatus': FieldDescriptor('isMentionedInStatus', 65, 'bool', repeated=False, packed=False),
        'statusMentions': FieldDescriptor('statusMentions', 66, 'string', repeated=True, packed=False),
        'targetMessageId': FieldDescriptor('targetMessageId', 67, "message", repeated=False, packed=False, _msg_path='MessageKey'),
        'messageAddOns': FieldDescriptor('messageAddOns', 68, "message", repeated=True, packed=False, _msg_path='MessageAddOn'),
        'statusMentionMessageInfo': FieldDescriptor('statusMentionMessageInfo', 69, "message", repeated=False, packed=False, _msg_path='StatusMentionMessage'),
        'isSupportAiMessage': FieldDescriptor('isSupportAiMessage', 70, 'bool', repeated=False, packed=False),
        'statusMentionSources': FieldDescriptor('statusMentionSources', 71, 'string', repeated=True, packed=False),
        'supportAiCitations': FieldDescriptor('supportAiCitations', 72, "message", repeated=True, packed=False, _msg_path='Citation'),
        'botTargetId': FieldDescriptor('botTargetId', 73, 'string', repeated=False, packed=False),
        'groupHistoryIndividualMessageInfo': FieldDescriptor('groupHistoryIndividualMessageInfo', 74, "message", repeated=False, packed=False, _msg_path='GroupHistoryIndividualMessageInfo'),
        'groupHistoryBundleInfo': FieldDescriptor('groupHistoryBundleInfo', 75, "message", repeated=False, packed=False, _msg_path='GroupHistoryBundleInfo'),
        'interactiveMessageAdditionalMetadata': FieldDescriptor('interactiveMessageAdditionalMetadata', 76, "message", repeated=False, packed=False, _msg_path='InteractiveMessageAdditionalMetadata'),
        'quarantinedMessage': FieldDescriptor('quarantinedMessage', 77, "message", repeated=False, packed=False, _msg_path='QuarantinedMessage'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}

class WebNotificationsInfo(MessageBase):
    FIELDS = {
        'timestamp': FieldDescriptor('timestamp', 2, 'uint64', repeated=False, packed=False),
        'unreadChats': FieldDescriptor('unreadChats', 3, 'uint32', repeated=False, packed=False),
        'notifyMessageCount': FieldDescriptor('notifyMessageCount', 4, 'uint32', repeated=False, packed=False),
        'notifyMessages': FieldDescriptor('notifyMessages', 5, "message", repeated=True, packed=False, _msg_path='WebMessageInfo'),
    }
    _BY_NUMBER = {fd.number: name for name, fd in FIELDS.items()}



# --- post-linking: resolve message_cls / enum_cls references ---

def _walk_classes(cls):
    yield cls
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, type) and issubclass(attr, MessageBase) and attr is not MessageBase:
            yield from _walk_classes(attr)


def _find_in_namespace(root, path_parts):
    node = root
    for part in path_parts:
        if isinstance(node, dict):
            node = node.get(part)
        else:
            node = getattr(node, part, None)
        if node is None:
            return None
    return node


def _link():
    # module globals serve as the top-level namespace
    root = {name: obj for name, obj in globals().items()
            if isinstance(obj, type) and (issubclass(obj, MessageBase) or issubclass(obj, enum.IntEnum))}
    seen = set()
    for name, obj in root.items():
        if not (isinstance(obj, type) and issubclass(obj, MessageBase)):
            continue
        for cls in _walk_classes(obj):
            if id(cls) in seen:
                continue
            seen.add(id(cls))
            for fd in cls.FIELDS.values():
                if fd.field_type == "message" and fd._msg_path is not None:
                    fd.message_cls = _find_in_namespace(root, fd._msg_path.split("."))
                elif fd.field_type == "enum" and fd._enum_path is not None:
                    fd.enum_cls = _find_in_namespace(root, fd._enum_path.split("."))
                elif fd.field_type == "map":
                    mv = fd.map_value
                    if mv.field_type == "message" and mv._msg_path is not None:
                        mv.message_cls = _find_in_namespace(root, mv._msg_path.split("."))
                    elif mv.field_type == "enum" and mv._enum_path is not None:
                        mv.enum_cls = _find_in_namespace(root, mv._enum_path.split("."))


_link()
