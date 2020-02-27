"""Shared type aliases for roundwire public and internal APIs."""

from __future__ import annotations

from typing import NewType, TypeAlias

MatchId = NewType("MatchId", str)
PlayerId = NewType("PlayerId", str)
SteamId = NewType("SteamId", str)
RoundNumber = NewType("RoundNumber", int)
Tick = NewType("Tick", int)
Milliseconds = NewType("Milliseconds", int)

JsonDict: TypeAlias = dict[str, object]
JsonList: TypeAlias = list[object]
StringMap: TypeAlias = dict[str, str]
IntMap: TypeAlias = dict[str, int]
FloatMap: TypeAlias = dict[str, float]
