"""Kill / death aggregates."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.types import PlayerId


def kill_count(match: Match, player_id: PlayerId) -> int:
    return sum(len(rnd.kills_for(player_id)) for rnd in match.rounds)


def death_count(match: Match, player_id: PlayerId) -> int:
    return sum(len(rnd.deaths_for(player_id)) for rnd in match.rounds)


def assist_count(match: Match, player_id: PlayerId) -> int:
    total = 0
    for rnd in match.rounds:
        for kill in rnd.kills:
            if kill.assisted_by == player_id:
                total += 1
    return total


def kd_ratio(match: Match, player_id: PlayerId) -> float:
    kills = kill_count(match, player_id)
    deaths = death_count(match, player_id)
    if deaths == 0:
        return float(kills)
    return kills / deaths


def kpr(match: Match, player_id: PlayerId) -> float:
    if not match.rounds:
        return 0.0
    return kill_count(match, player_id) / len(match.rounds)
