"""Damage output stratified by buy type."""

from __future__ import annotations

from roundwire.economy.classify import classify_team_buy
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.stats.aggregates import safe_div


def damage_for_buy(match: Match, buy: BuyType) -> float:
    total = 0
    support = 0
    for rnd in match.rounds:
        for side in (TeamSide.CT, TeamSide.T):
            if classify_team_buy(rnd, match, side) is not buy:
                continue
            support += 1
            pids = {p.player_id for p in match.players_on(side)}
            total += sum(d.damage for d in rnd.damage if d.attacker_id in pids)
    return safe_div(float(total), float(support))


def eco_damage_avg(match: Match) -> float:
    return damage_for_buy(match, BuyType.ECO)


def force_damage_avg(match: Match) -> float:
    return damage_for_buy(match, BuyType.FORCE)


def full_damage_avg(match: Match) -> float:
    return damage_for_buy(match, BuyType.FULL)
