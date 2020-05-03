"""Game edition / ruleset selector."""

from __future__ import annotations

from enum import Enum

from roundwire.errors.domain import InvalidEditionError


class GameEdition(str, Enum):
    """Supported Counter-Strike editions."""

    CSGO = "CSGO"
    CS2 = "CS2"

    @property
    def regulation_rounds(self) -> int:
        """Maximum rounds per half * 2 before overtime (MR15 → 30, MR12 → 24)."""
        return 30 if self is GameEdition.CSGO else 24

    @property
    def win_threshold(self) -> int:
        """Rounds needed to win regulation (16 for CS:GO, 13 for CS2)."""
        return 16 if self is GameEdition.CSGO else 13

    @property
    def mr_label(self) -> str:
        return "MR15" if self is GameEdition.CSGO else "MR12"

    @classmethod
    def parse(cls, value: str) -> GameEdition:
        key = value.strip().upper().replace(":", "").replace("-", "")
        if key in {"CSGO", "CSGOLEGACY"}:
            return cls.CSGO
        if key in {"CS2", "CSII", "COUNTERSTRIKE2"}:
            return cls.CS2
        raise InvalidEditionError(f"unknown game edition: {value!r}")
