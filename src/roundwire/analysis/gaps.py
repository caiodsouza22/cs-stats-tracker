"""Cash and equipment gaps between sides."""

from __future__ import annotations

from roundwire.economy.equipment import cash_remaining, team_equipment_value
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.stats.aggregates import mean


def cash_gaps(match: Match) -> list[int]:
    return [
        abs(cash_remaining(r, match, TeamSide.CT) - cash_remaining(r, match, TeamSide.T))
        for r in match.rounds
    ]


def equipment_gaps(match: Match) -> list[int]:
    return [
        abs(
            team_equipment_value(r, match, TeamSide.CT)
            - team_equipment_value(r, match, TeamSide.T)
        )
        for r in match.rounds
    ]


def average_cash_gap(match: Match) -> float:
    return mean([float(x) for x in cash_gaps(match)])


def average_equipment_gap(match: Match) -> float:
    return mean([float(x) for x in equipment_gaps(match)])


def largest_equipment_gap_round(match: Match) -> int | None:
    gaps = equipment_gaps(match)
    if not gaps:
        return None
    idx = max(range(len(gaps)), key=lambda i: gaps[i])
    return int(match.rounds[idx].number)
