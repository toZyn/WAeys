"""Browser identification helpers mirroring src/Utils/browser-utils.ts."""
import platform as _platform

PLATFORM_MAP = {
    "aix": "AIX",
    "darwin": "Mac OS",
    "win32": "Windows",
    "android": "Android",
    "freebsd": "FreeBSD",
    "openbsd": "OpenBSD",
    "sunos": "Solaris",
    "linux": None,
    "haiku": None,
    "cygwin": None,
    "netbsd": None,
}


def _release():
    try:
        return _platform.release()
    except Exception:
        return ""


class Browsers:
    @staticmethod
    def ubuntu(browser):
        return ["Ubuntu", browser, "22.04.4"]

    @staticmethod
    def macOS(browser):
        return ["Mac OS", browser, "14.4.1"]

    @staticmethod
    def baileys(browser):
        return ["Baileys", browser, "6.5.0"]

    @staticmethod
    def windows(browser):
        return ["Windows", browser, "10.0.22631"]

    @staticmethod
    def android(browser):
        return [browser, "Android", ""]

    @staticmethod
    def appropriate(browser):
        sys_name = _platform.system().lower()
        platform_type = PLATFORM_MAP.get(sys_name) or "Ubuntu"
        return [platform_type, browser, _release()]


def get_platform_id(browser: str) -> str:
    """Map a browser name to proto.DeviceProps.PlatformType id, defaulting to 1 (chrome)."""
    # proto import deferred to avoid circular import at module load time
    from ..WAProto.WAProto import DeviceProps

    name = browser.upper()
    try:
        platform_type = DeviceProps.PlatformType[name]
    except (KeyError, AttributeError):
        return "1"
    return str(platform_type)
