"""Molotov / incendiary tracking."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.utility_event import UtilityKind
from roundwire.types import PlayerId


_FIRE = {UtilityKind.MOLOTOV, UtilityKind.INCENDIARY}


def fire_throws(match: Match, player_id: PlayerId | None = None) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.kind in _FIRE:
                if player_id is None or event.thrower_id == player_id:
                    total += 1
    return total


def fire_damage(match: Match, player_id: PlayerId | None = None) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.kind in _FIRE:
                if player_id is None or event.thrower_id == player_id:
                    total += event.damage_dealt
    return total
