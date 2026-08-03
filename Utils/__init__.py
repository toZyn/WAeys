"""Utils — ported Baileys utility modules.

Mirrors src/Utils/index.ts: re-exports the ported helper modules.
Modules that are still pending port (link-preview, use-multi-file-auth-state)
will be added here as they land.
"""

from __future__ import annotations

from . import (
    auth_utils,
    browser_utils,
    companion_reg_client_utils,
    crypto,
    decode_wa_message,
    event_buffer,
    generics,
    history,
    identity_change_handler,
    logger,
    lru_cache,
    lt_hash,
    make_mutex,
    message_retry_manager,
    messages,
    messages_media,
    noise_handler,
    offline_node_processor,
    pre_key_manager,
    process_message,
    reporting_utils,
    signal,
    stanza_ack,
    sync_action_utils,
    tc_token_utils,
    validate_connection,
)
from .auth_utils import add_transaction_capability, init_auth_creds, make_cacheable_signal_key_store, make_memory_key_store
from .browser_utils import Browsers
from .companion_reg_client_utils import CompanionWebClientType, build_pairing_qr_data, get_companion_platform_id
from .crypto import Curve, aes_encrypt_ctr, curve25519_donna_sign, derive_pairing_code_key, signed_key_pair
from .event_buffer import make_event_buffer
from .generics import (
    Boom,
    bind_wait_for_connection_update,
    bind_wait_for_event,
    bytes_to_crockford,
    delay_cancellable,
    generate_md_tag_prefix,
    generate_message_id,
    get_code_from_ws_error,
    promise_timeout,
    trim_undefined,
)
from .decode_wa_message import (
    decode_message_node,
    decrypt_message_node,
    extract_addressing_context,
    get_decryption_jid,
    store_mapping_from_envelope,
)
from .history import download_and_process_history_sync_notification, download_history, process_history_message
from .identity_change_handler import handle_identity_change
from .messages import get_content_type, normalize_message_content, update_message_with_receipt
from .message_retry_manager import MessageRetryManager, RetryReason
from .messages_media import (
    download_content_from_message,
    download_encrypted_content,
    encrypted_stream,
    extension_for_media_message,
    generate_profile_picture,
    get_media_keys,
    get_url_from_direct_path,
    get_wa_upload_to_server,
    media_message_sha256_b64,
)
from .noise_handler import make_noise_handler
from .offline_node_processor import make_offline_node_processor
from .pre_key_manager import PreKeyManager
from .process_message import clean_message, get_chat_id, is_real_message, should_increment_chat_unread
from .reporting_utils import get_message_reporting_token, should_include_reporting_token
from .signal import (
    create_signal_identity,
    extract_device_jids,
    get_next_pre_keys,
    get_next_pre_keys_node,
    xmpp_pre_key,
    xmpp_signed_pre_key,
)
from .stanza_ack import build_ack_stanza
from .sync_action_utils import emit_sync_action_results, process_contact_action
from .tc_token_utils import build_merged_tc_token_index_write, build_tc_token_from_jid, is_tc_token_expired, should_send_new_tc_token
from .validate_connection import configure_successful_pairing, generate_login_node, generate_registration_node

__all__ = [
    'auth_utils',
    'browser_utils',
    'companion_reg_client_utils',
    'crypto',
    'decode_wa_message',
    'event_buffer',
    'generics',
    'history',
    'identity_change_handler',
    'logger',
    'lru_cache',
    'lt_hash',
    'make_mutex',
    'message_retry_manager',
    'messages',
    'messages_media',
    'noise_handler',
    'offline_node_processor',
    'pre_key_manager',
    'process_message',
    'reporting_utils',
    'signal',
    'stanza_ack',
    'sync_action_utils',
    'tc_token_utils',
    'validate_connection',
    'add_transaction_capability',
    'init_auth_creds',
    'make_cacheable_signal_key_store',
    'make_memory_key_store',
    'Browsers',
    'CompanionWebClientType',
    'build_pairing_qr_data',
    'get_companion_platform_id',
    'Curve',
    'aes_encrypt_ctr',
    'curve25519_donna_sign',
    'derive_pairing_code_key',
    'signed_key_pair',
    'make_event_buffer',
    'Boom',
    'bind_wait_for_connection_update',
    'bind_wait_for_event',
    'bytes_to_crockford',
    'delay_cancellable',
    'generate_md_tag_prefix',
    'generate_message_id',
    'get_code_from_ws_error',
    'promise_timeout',
    'trim_undefined',
    'decode_message_node',
    'decrypt_message_node',
    'extract_addressing_context',
    'get_decryption_jid',
    'store_mapping_from_envelope',
    'download_and_process_history_sync_notification',
    'download_history',
    'process_history_message',
    'handle_identity_change',
    'get_content_type',
    'normalize_message_content',
    'update_message_with_receipt',
    'MessageRetryManager',
    'RetryReason',
    'download_content_from_message',
    'download_encrypted_content',
    'encrypted_stream',
    'extension_for_media_message',
    'generate_profile_picture',
    'get_media_keys',
    'get_url_from_direct_path',
    'get_wa_upload_to_server',
    'media_message_sha256_b64',
    'make_noise_handler',
    'make_offline_node_processor',
    'PreKeyManager',
    'clean_message',
    'get_chat_id',
    'is_real_message',
    'should_increment_chat_unread',
    'get_message_reporting_token',
    'should_include_reporting_token',
    'create_signal_identity',
    'extract_device_jids',
    'get_next_pre_keys',
    'get_next_pre_keys_node',
    'xmpp_pre_key',
    'xmpp_signed_pre_key',
    'build_ack_stanza',
    'emit_sync_action_results',
    'process_contact_action',
    'build_merged_tc_token_index_write',
    'build_tc_token_from_jid',
    'is_tc_token_expired',
    'should_send_new_tc_token',
    'configure_successful_pairing',
    'generate_login_node',
    'generate_registration_node',
]
