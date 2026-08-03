"""Pino-compatible structured logger for WAeys.

Mirrors src/Utils/logger.ts which creates a pino instance with ISO timestamp.
The ILogger interface accepts (obj, msg) like pino; this logger serializes
the bound object fields plus the message string.
"""
import json
import sys
import threading
from datetime import datetime, timezone


class ILogger:
    level = "info"
    _bound = None

    def child(self, obj):
        new = ILogger()
        new.level = self.level
        merged = dict(self._bound or {})
        merged.update(obj)
        new._bound = merged
        return new

    def _emit(self, level, obj, msg=None):
        record = dict(self._bound or {})
        if isinstance(obj, dict):
            record.update(obj)
        else:
            record["obj"] = obj
        record["level"] = level
        if msg:
            record["msg"] = msg
        record["time"] = datetime.now(timezone.utc).isoformat()
        line = json.dumps(record, default=str)
        stream = sys.stderr if level == "error" else sys.stdout
        with threading.Lock():
            print(line, file=stream, flush=True)

    def trace(self, obj=None, msg=None):
        self._emit("trace", obj, msg)

    def debug(self, obj=None, msg=None):
        self._emit("debug", obj, msg)

    def info(self, obj=None, msg=None):
        self._emit("info", obj, msg)

    def warn(self, obj=None, msg=None):
        self._emit("warn", obj, msg)

    def error(self, obj=None, msg=None):
        self._emit("error", obj, msg)


logger = ILogger()
