"""Port of src/Utils/companion-reg-client-utils.ts."""

from __future__ import annotations

import enum


class CompanionWebClientType(enum.IntEnum):
    UNKNOWN = 0
    CHROME = 1
    EDGE = 2
    FIREFOX = 3
    IE = 4
    OPERA = 5
    SAFARI = 6
    ELECTRON = 7
    UWP = 8
    OTHER_WEB_CLIENT = 9


_BROWSER_TO_COMPANION_WEB_CLIENT = {
    'Chrome': CompanionWebClientType.CHROME,
    'Edge': CompanionWebClientType.EDGE,
    'Firefox': CompanionWebClientType.FIREFOX,
    'IE': CompanionWebClientType.IE,
    'Opera': CompanionWebClientType.OPERA,
    'Safari': CompanionWebClientType.SAFARI,
}


def get_companion_web_client_type(browser) -> CompanionWebClientType:
    """browser: WABrowserDescription = [os, browserName, ...]."""
    os_name, browser_name = browser[0], browser[1]
    if browser_name == 'Desktop':
        return CompanionWebClientType.UWP if os_name == 'Windows' else CompanionWebClientType.ELECTRON
    return _BROWSER_TO_COMPANION_WEB_CLIENT.get(browser_name, CompanionWebClientType.OTHER_WEB_CLIENT)


def get_companion_platform_id(browser) -> str:
    return str(int(get_companion_web_client_type(browser)))


_DEFAULT_PAIRING_CODE_BROWSER_PLATFORM = {'id': '1', 'displayName': 'Chrome'}

_PAIRING_CODE_BROWSER_PLATFORM = {
    'Chrome': _DEFAULT_PAIRING_CODE_BROWSER_PLATFORM,
    'Firefox': {'id': '2', 'displayName': 'Firefox'},
    'IE': {'id': '3', 'displayName': 'IE'},
    'Opera': {'id': '4', 'displayName': 'Opera'},
    'Safari': {'id': '5', 'displayName': 'Safari'},
    'Edge': {'id': '6', 'displayName': 'Edge'},
}

_PAIRING_CODE_OS_DISPLAY = {'Mac OS', 'Windows', 'Ubuntu'}


def get_pairing_code_platform(browser) -> dict:
    """browser: WABrowserDescription = [os, browserName, ...]."""
    os_name, browser_name = browser[0], browser[1]
    platform = _PAIRING_CODE_BROWSER_PLATFORM.get(browser_name, _DEFAULT_PAIRING_CODE_BROWSER_PLATFORM)
    os_display = os_name if os_name in _PAIRING_CODE_OS_DISPLAY else 'Mac OS'
    return {'id': platform['id'], 'display': f'{platform["displayName"]} ({os_display})'}


def build_pairing_qr_data(ref: str, noise_key_b64: str, identity_key_b64: str, adv_b64: str, browser) -> str:
    return (
        'https://wa.me/settings/linked_devices#'
        + ','.join([ref, noise_key_b64, identity_key_b64, adv_b64, get_companion_platform_id(browser)])
    )
