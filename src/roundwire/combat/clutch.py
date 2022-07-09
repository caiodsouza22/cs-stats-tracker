"""Lightweight clutch heuristics from survivors + win."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.types import PlayerId


def _alive_on_side(match: Match, round_survivors: list[PlayerId], side: TeamSide) -> list[PlayerId]:
    pmap = match.player_map()
    return [pid for pid in round_survivors if pid in pmap and pmap[pid].team is side]


def clutch_wins(match: Match, player_id: PlayerId) -> int:
    """Count rounds where player was sole survivor on winning side."""
    wins = 0
    pmap = match.player_map()
    player = pmap.get(player_id)
    if player is None:
        return 0
    for rnd in match.rounds:
        if rnd.winner is not player.team:
            continue
        alive = _alive_on_side(match, rnd.survivors, player.team)
        if alive == [player_id]:
            wins += 1
    return wins
