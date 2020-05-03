"""Normalized round win reasons."""

from __future__ import annotations

from enum import Enum


class WinReason(str, Enum):
    ELIMINATION = "elimination"
    BOMB_EXPLODED = "bomb_exploded"
    BOMB_DEFUSED = "bomb_defused"
    TIME = "time"
    UNKNOWN = "unknown"

    @classmethod
    def parse(cls, value: str) -> WinReason:
        key = value.strip().lower().replace(" ", "_").replace("-", "_")
        aliases = {
            "elim": cls.ELIMINATION,
            "kill": cls.ELIMINATION,
            "explode": cls.BOMB_EXPLODED,
            "explosion": cls.BOMB_EXPLODED,
            "defuse": cls.BOMB_DEFUSED,
            "defused": cls.BOMB_DEFUSED,
            "timeout": cls.TIME,
        }
        if key in aliases:
            return aliases[key]
        try:
            return cls(key)
        except ValueError:
            return cls.UNKNOWN
