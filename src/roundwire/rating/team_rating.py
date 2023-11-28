"""Aggregate team impact."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.rating.impact import impact_score


def team_average_impact(match: Match, side: TeamSide) -> float:
    players = match.players_on(side)
    if not players:
        return 0.0
    return sum(impact_score(match, p.player_id) for p in players) / len(players)


def team_impact_gap(match: Match) -> float:
    return team_average_impact(match, TeamSide.CT) - team_average_impact(match, TeamSide.T)
