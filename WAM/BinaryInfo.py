"""Port of src/WAM/BinaryInfo.ts."""

from __future__ import annotations


class BinaryInfo:
    def __init__(self, **options):
        self.protocolVersion = 5
        self.sequence = 0
        self.events = []
        self.buffer = []
        for k, v in options.items():
            if hasattr(self, k):
                setattr(self, k, v)
