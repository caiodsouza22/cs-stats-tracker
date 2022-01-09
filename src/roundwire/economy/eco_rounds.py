"""Eco round success tracking."""

from __future__ import annotations

from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.economy.classify import classify_team_buy


def eco_rounds(match: Match, side: TeamSide) -> list[int]:
    return [
        int(rnd.number)
        for rnd in match.rounds
        if classify_team_buy(rnd, match, side) is BuyType.ECO
    ]


def eco_upsets(match: Match, side: TeamSide) -> list[int]:
    """Eco rounds won by ``side``."""
    return [
        int(rnd.number)
        for rnd in match.rounds
        if classify_team_buy(rnd, match, side) is BuyType.ECO and rnd.winner is side
    ]
