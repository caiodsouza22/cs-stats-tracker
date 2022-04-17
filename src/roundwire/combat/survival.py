"""Round survival rates."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.types import PlayerId


def rounds_survived(match: Match, player_id: PlayerId) -> int:
    return sum(1 for rnd in match.rounds if player_id in rnd.survivors)


def survival_rate(match: Match, player_id: PlayerId) -> float:
    if not match.rounds:
        return 0.0
    return rounds_survived(match, player_id) / len(match.rounds)
