"""Investment efficiency: rounds won per equipment dollar."""

from __future__ import annotations

from roundwire.economy.equipment import team_equipment_value
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.economy.classify import classify_team_buy
from roundwire.stats.aggregates import safe_div


def equipment_spent_winning(match: Match, side: TeamSide) -> int:
    total = 0
    for rnd in match.rounds:
        if rnd.winner is side:
            total += team_equipment_value(rnd, match, side)
    return total


def equipment_spent_losing(match: Match, side: TeamSide) -> int:
    total = 0
    for rnd in match.rounds:
        if rnd.winner is not side:
            total += team_equipment_value(rnd, match, side)
    return total


def win_per_million(match: Match, side: TeamSide) -> float:
    """Rounds won per 1,000,000 equipment value invested."""
    spent = sum(team_equipment_value(rnd, match, side) for rnd in match.rounds)
    wins = sum(1 for rnd in match.rounds if rnd.winner is side)
    return safe_div(wins * 1_000_000, float(spent))


def investment_by_buy_type(match: Match, side: TeamSide) -> dict[str, float]:
    totals: dict[str, list[int]] = {}
    for rnd in match.rounds:
        buy = classify_team_buy(rnd, match, side)
        totals.setdefault(buy.value, []).append(team_equipment_value(rnd, match, side))
    return {k: (sum(v) / len(v) if v else 0.0) for k, v in totals.items()}


def overinvested_losses(match: Match, side: TeamSide, threshold: int = 20000) -> list[int]:
    """Full-ish investments that still lost."""
    out: list[int] = []
    for rnd in match.rounds:
        value = team_equipment_value(rnd, match, side)
        buy = classify_team_buy(rnd, match, side)
        if value >= threshold and buy is BuyType.FULL and rnd.winner is not side:
            out.append(int(rnd.number))
    return out
