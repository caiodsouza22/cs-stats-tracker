"""CT / T side preference on a map from a single match."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.team import TeamSide


def side_winrate(match: Match, side: TeamSide) -> float:
    if not match.rounds:
        return 0.0
    wins = sum(1 for rnd in match.rounds if rnd.winner is side)
    return wins / len(match.rounds)


def side_preference_label(match: Match) -> str:
    ct = side_winrate(match, TeamSide.CT)
    t = side_winrate(match, TeamSide.T)
    if abs(ct - t) < 0.05:
        return "balanced"
    return "CT" if ct > t else "T"
