"""Full-buy round tracking."""

from __future__ import annotations

from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.economy.classify import classify_team_buy


def full_buy_rounds(match: Match, side: TeamSide) -> list[int]:
    return [
        int(rnd.number)
        for rnd in match.rounds
        if classify_team_buy(rnd, match, side) is BuyType.FULL
    ]


def full_buy_winrate(match: Match, side: TeamSide) -> float:
    fulls = 0
    wins = 0
    for rnd in match.rounds:
        if classify_team_buy(rnd, match, side) is BuyType.FULL:
            fulls += 1
            if rnd.winner is side:
                wins += 1
    return 0.0 if fulls == 0 else wins / fulls
