"""JID helpers (ported from src/WABinary/jid-utils.ts)."""

from __future__ import annotations

import re
from typing import Optional

S_WHATSAPP_NET = '@s.whatsapp.net'
OFFICIAL_BIZ_JID = '16505361212@c.us'
SERVER_JID = 'server@c.us'
PSA_WID = '0@c.us'
STORIES_JID = 'status@broadcast'
META_AI_JID = '13135550002@c.us'


class WAJIDDomains:
    WHATSAPP = 0
    LID = 1
    HOSTED = 128
    HOSTED_LID = 129


class FullJid:
    __slots__ = ('user', 'server', 'device', 'domainType', 'agent')

    def __init__(self, user: str = '', server: str = 's.whatsapp.net', device: Optional[int] = None,
                 domainType: int = WAJIDDomains.WHATSAPP, agent: Optional[int] = None):
        self.user = user
        self.server = server
        self.device = device
        self.domainType = domainType
        self.agent = agent

    def __repr__(self):
        return f'FullJid(user={self.user!r}, server={self.server!r}, device={self.device!r}, domainType={self.domainType!r})'


def get_server_from_domain_type(initial_server: str, domain_type: Optional[int]) -> str:
    if domain_type == WAJIDDomains.LID:
        return 'lid'
    if domain_type == WAJIDDomains.HOSTED:
        return 'hosted'
    if domain_type == WAJIDDomains.HOSTED_LID:
        return 'hosted.lid'
    return initial_server


def jid_encode(user: str | int | None, server: str, device: Optional[int] = None, agent: Optional[int] = None) -> str:
    u = str(user) if user is not None else ''
    return f'{u}{f"_{agent}" if agent else ""}{f":{device}" if device else ""}@{server}'


def jid_decode(jid: Optional[str]) -> Optional[FullJid]:
    if not isinstance(jid, str):
        return None
    sep_idx = jid.find('@')
    if sep_idx < 0:
        return None

    server = jid[sep_idx + 1:]
    user_combined = jid[:sep_idx]

    parts = user_combined.split(':')
    user_agent = parts[0]
    device_str = parts[1] if len(parts) > 1 else None

    sub = user_agent.split('_')
    user = sub[0]
    agent = sub[1] if len(sub) > 1 else None

    domain_type = WAJIDDomains.WHATSAPP
    if server == 'lid':
        domain_type = WAJIDDomains.LID
    elif server == 'hosted':
        domain_type = WAJIDDomains.HOSTED
    elif server == 'hosted.lid':
        domain_type = WAJIDDomains.HOSTED_LID
    elif agent:
        try:
            domain_type = int(agent)
        except ValueError:
            pass

    return FullJid(user=user, server=server, domainType=domain_type,
                   device=int(device_str) if device_str else None, agent=int(agent) if agent else None)


def are_jids_same_user(jid1: Optional[str], jid2: Optional[str]) -> bool:
    user1 = jid_decode(jid1).user if jid_decode(jid1) else None
    user2 = jid_decode(jid2).user if jid_decode(jid2) else None
    return user1 == user2


def is_jid_meta_ai(jid: Optional[str]) -> bool:
    return bool(jid and jid.endswith('@bot'))


def is_pn_user(jid: Optional[str]) -> bool:
    return bool(jid and jid.endswith('@s.whatsapp.net'))


def is_lid_user(jid: Optional[str]) -> bool:
    return bool(jid and jid.endswith('@lid'))


def is_jid_broadcast(jid: Optional[str]) -> bool:
    return bool(jid and jid.endswith('@broadcast'))


def is_jid_group(jid: Optional[str]) -> bool:
    return bool(jid and jid.endswith('@g.us'))


def is_jid_status_broadcast(jid: str) -> bool:
    return jid == 'status@broadcast'


def is_jid_newsletter(jid: Optional[str]) -> bool:
    return bool(jid and jid.endswith('@newsletter'))


def is_hosted_pn_user(jid: Optional[str]) -> bool:
    return bool(jid and jid.endswith('@hosted'))


def is_hosted_lid_user(jid: Optional[str]) -> bool:
    return bool(jid and jid.endswith('@hosted.lid'))


_bot_regexp = re.compile(r'^1313555\d{4}$|^131655500\d{2}$')


def is_jid_bot(jid: Optional[str]) -> bool:
    return bool(jid and _bot_regexp.match(jid.split('@')[0]) and jid.endswith('@c.us'))


def jid_normalized_user(jid: Optional[str]) -> str:
    result = jid_decode(jid)
    if not result:
        return ''
    return jid_encode(result.user, 's.whatsapp.net' if result.server == 'c.us' else result.server)


def transfer_device(from_jid: str, to_jid: str) -> str:
    from_decoded = jid_decode(from_jid)
    device_id = from_decoded.device or 0 if from_decoded else 0
    to_decoded = jid_decode(to_jid)
    return jid_encode(to_decoded.user if to_decoded else '', to_decoded.server if to_decoded else '', device_id)
