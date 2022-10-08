"""Flashbang effectiveness."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.utility_event import UtilityKind
from roundwire.types import PlayerId


def enemies_flashed_total(match: Match, player_id: PlayerId | None = None) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.kind is not UtilityKind.FLASH:
                continue
            if player_id is not None and event.thrower_id != player_id:
                continue
            total += event.enemies_flashed
    return total


def teammates_flashed_total(match: Match, player_id: PlayerId | None = None) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.kind is not UtilityKind.FLASH:
                continue
            if player_id is not None and event.thrower_id != player_id:
                continue
            total += event.teammates_flashed
    return total


def flash_efficiency(match: Match, player_id: PlayerId) -> float:
    enemies = enemies_flashed_total(match, player_id)
    team = teammates_flashed_total(match, player_id)
    denom = enemies + team
    if denom == 0:
        return 0.0
    return enemies / denom
