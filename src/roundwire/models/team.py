"""Team side enumeration and helpers."""

from __future__ import annotations

from enum import Enum


class TeamSide(str, Enum):
    CT = "CT"
    T = "T"

    def opposite(self) -> TeamSide:
        return TeamSide.T if self is TeamSide.CT else TeamSide.CT

    @classmethod
    def parse(cls, value: str) -> TeamSide:
        key = value.strip().upper()
        if key in {"CT", "COUNTER", "COUNTERTERRORIST", "COUNTER-TERRORIST"}:
            return cls.CT
        if key in {"T", "TERRORIST", "TERRORISTS"}:
            return cls.T
        raise ValueError(f"unknown team side: {value!r}")
