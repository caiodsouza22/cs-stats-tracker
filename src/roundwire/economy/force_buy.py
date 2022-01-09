"""Force-buy specific helpers."""

from __future__ import annotations

from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.economy.classify import classify_team_buy


def force_rounds(match: Match, side: TeamSide) -> list[int]:
    out: list[int] = []
    for rnd in match.rounds:
        if classify_team_buy(rnd, match, side) is BuyType.FORCE:
            out.append(int(rnd.number))
    return out


def force_success_rate(match: Match, side: TeamSide) -> float:
    forces = 0
    wins = 0
    for rnd in match.rounds:
        if classify_team_buy(rnd, match, side) is BuyType.FORCE:
            forces += 1
            if rnd.winner is side:
                wins += 1
    if forces == 0:
        return 0.0
    return wins / forces
