"""Defaults & connection config mirroring src/Defaults/index.ts."""
import re

from ..Utils.browser_utils import Browsers
from ..Utils.logger import logger as _logger

version = [2, 3000, 1043857760]

UNAUTHORIZED_CODES = [401, 403, 419]

DEFAULT_ORIGIN = "https://web.whatsapp.com"
CALL_VIDEO_PREFIX = "https://call.whatsapp.com/video/"
CALL_AUDIO_PREFIX = "https://call.whatsapp.com/voice/"
DEF_CALLBACK_PREFIX = "CB:"
DEF_TAG_PREFIX = "TAG:"
PHONE_CONNECTION_CB = "CB:Pong"

WA_ADV_ACCOUNT_SIG_PREFIX = bytes([6, 0])
WA_ADV_DEVICE_SIG_PREFIX = bytes([6, 1])
WA_ADV_HOSTED_ACCOUNT_SIG_PREFIX = bytes([6, 5])
WA_ADV_HOSTED_DEVICE_SIG_PREFIX = bytes([6, 6])

WA_DEFAULT_EPHEMERAL = 7 * 24 * 60 * 60

STATUS_EXPIRY_SECONDS = 24 * 60 * 60

PLACEHOLDER_MAX_AGE_SECONDS = 14 * 24 * 60 * 60

NOISE_MODE = "Noise_XX_25519_AESGCM_SHA256\0\0\0\0"
DICT_VERSION = 3
KEY_BUNDLE_TYPE = bytes([5])
NOISE_WA_HEADER = bytes([87, 65, 6, DICT_VERSION])

URL_REGEX = re.compile(
    r"https://(?![^:@/\s]+:[^:@/\s]+@)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(:\d+)?(/[^\s]*)?"
)

WA_CERT_DETAILS = {
    "SERIAL": 0,
    "ISSUER": "WhatsAppLongTerm1",
    "PUBLIC_KEY": bytes.fromhex(
        "142375574d0a587166aae71ebe516437c4a28b73e3695c6ce1f7f9545da8ee6b"
    ),
}

PROCESSABLE_HISTORY_TYPES = None  # set lazily after WAProto is ported

DEFAULT_CACHE_TTLS = {
    "SIGNAL_STORE": 5 * 60,
    "MSG_RETRY": 60 * 60,
    "CALL_OFFER": 5 * 60,
    "USER_DEVICES": 5 * 60,
}


def _default_patch_message(msg):
    return msg


def _default_should_sync_history_message(sync_type):
    from ..WAProto.WAProto import HistorySync

    return sync_type != HistorySync.HistorySyncType.FULL


def default_connection_config():
    """Build the DEFAULT_CONNECTION_CONFIG dict (lazy, post WAProto/Signal port)."""
    from ..Signal.libsignal import make_libsignal_repository

    return {
        "version": version,
        "browser": Browsers.macOS("Chrome"),
        "waWebSocketUrl": "wss://web.whatsapp.com/ws/chat",
        "connectTimeoutMs": 20_000,
        "keepAliveIntervalMs": 30_000,
        "logger": _logger.child({"class": "baileys"}),
        "emitOwnEvents": True,
        "defaultQueryTimeoutMs": 60_000,
        "customUploadHosts": [],
        "retryRequestDelayMs": 250,
        "maxMsgRetryCount": 5,
        "fireInitQueries": True,
        "auth": None,
        "markOnlineOnConnect": True,
        "syncFullHistory": True,
        "patchMessageBeforeSending": _default_patch_message,
        "shouldSyncHistoryMessage": _default_should_sync_history_message,
        "shouldIgnoreJid": lambda jid: False,
        "linkPreviewImageThumbnailWidth": 192,
        "transactionOpts": {"maxCommitRetries": 10, "delayBetweenTriesMs": 3000},
        "generateHighQualityLinkPreview": False,
        "enableAutoSessionRecreation": True,
        "enableRecentMessageCache": True,
        "options": {},
        "appStateMacVerification": {"patch": False, "snapshot": False},
        "countryCode": "US",
        "getMessage": lambda: None,
        "cachedGroupMetadata": lambda: None,
        "makeSignalRepository": make_libsignal_repository,
    }


MEDIA_PATH_MAP = {
    "image": "/mms/image",
    "video": "/mms/video",
    "document": "/mms/document",
    "audio": "/mms/audio",
    "sticker": "/mms/image",
    "thumbnail-link": "/mms/image",
    "product-catalog-image": "/product/image",
    "md-app-state": "",
    "md-msg-hist": "/mms/md-app-state",
    "biz-cover-photo": "/pps/biz-cover-photo",
}

MEDIA_HKDF_KEY_MAPPING = {
    "audio": "Audio",
    "document": "Document",
    "gif": "Video",
    "image": "Image",
    "ppic": "",
    "product": "Image",
    "ptt": "Audio",
    "sticker": "Image",
    "video": "Video",
    "thumbnail-document": "Document Thumbnail",
    "thumbnail-image": "Image Thumbnail",
    "thumbnail-video": "Video Thumbnail",
    "thumbnail-link": "Link Thumbnail",
    "md-msg-hist": "History",
    "md-app-state": "App State",
    "product-catalog-image": "",
    "payment-bg-image": "Payment Background",
    "ptv": "Video",
    "biz-cover-photo": "Image",
}

MEDIA_KEYS = list(MEDIA_PATH_MAP.keys())

HISTORY_SYNC_PAUSED_TIMEOUT_MS = 120_000

MIN_PREKEY_COUNT = 5

INITIAL_PREKEY_COUNT = 812

UPLOAD_TIMEOUT = 30000

TimeMs = {
    "Minute": 60 * 1000,
    "Hour": 60 * 60 * 1000,
    "Day": 24 * 60 * 60 * 1000,
    "Week": 7 * 24 * 60 * 60 * 1000,
}


def _init_processable_history_types():
    """Populate PROCESSABLE_HISTORY_TYPES once WAProto is importable."""
    global PROCESSABLE_HISTORY_TYPES
    if PROCESSABLE_HISTORY_TYPES is not None:
        return
    from ..WAProto.WAProto import HistorySync

    PROCESSABLE_HISTORY_TYPES = [
        HistorySync.HistorySyncType.INITIAL_BOOTSTRAP,
        HistorySync.HistorySyncType.PUSH_NAME,
        HistorySync.HistorySyncType.RECENT,
        HistorySync.HistorySyncType.FULL,
        HistorySync.HistorySyncType.ON_DEMAND,
        HistorySync.HistorySyncType.NON_BLOCKING_DATA,
        HistorySync.HistorySyncType.INITIAL_STATUS_V3,
    ]
