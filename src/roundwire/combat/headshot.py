"""Headshot percentage helpers."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.types import PlayerId


def headshot_kills(match: Match, player_id: PlayerId) -> int:
    total = 0
    for rnd in match.rounds:
        for kill in rnd.kills_for(player_id):
            if kill.headshot:
                total += 1
    return total


def headshot_pct(match: Match, player_id: PlayerId) -> float:
    kills = 0
    hs = 0
    for rnd in match.rounds:
        for kill in rnd.kills_for(player_id):
            kills += 1
            if kill.headshot:
                hs += 1
    if kills == 0:
        return 0.0
    return hs / kills
