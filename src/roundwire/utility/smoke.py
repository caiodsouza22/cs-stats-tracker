"""Smoke usage counters."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.utility_event import UtilityKind
from roundwire.types import PlayerId


def smoke_count(match: Match, player_id: PlayerId | None = None) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.kind is UtilityKind.SMOKE:
                if player_id is None or event.thrower_id == player_id:
                    total += 1
    return total
