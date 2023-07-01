"""Correlate opening duels with buy classifications."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.opening import opening_duels
from roundwire.economy.classify import classify_team_buy
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide


@dataclass(frozen=True, slots=True)
class OpeningEconomyRow:
    round_number: int
    opener_side: str
    opener_buy: str
    victim_buy: str
    traded: bool
    converted: bool


def opening_economy_rows(match: Match) -> list[OpeningEconomyRow]:
    pmap = match.player_map()
    rows: list[OpeningEconomyRow] = []
    for duel in opening_duels(match):
        rnd = match.round_by_number(duel.round_number)
        if rnd is None:
            continue
        killer = pmap.get(duel.kill.killer_id)
        victim = pmap.get(duel.kill.victim_id)
        if killer is None or victim is None:
            continue
        opener_buy = classify_team_buy(rnd, match, killer.team)
        victim_buy = classify_team_buy(rnd, match, victim.team)
        rows.append(
            OpeningEconomyRow(
                round_number=duel.round_number,
                opener_side=killer.team.value,
                opener_buy=opener_buy.value,
                victim_buy=victim_buy.value,
                traded=duel.traded,
                converted=rnd.winner is killer.team,
            )
        )
    return rows


def full_buy_opening_conversion(match: Match) -> float:
    rows = [r for r in opening_economy_rows(match) if r.opener_buy == BuyType.FULL.value]
    if not rows:
        return 0.0
    return sum(1 for r in rows if r.converted) / len(rows)


def eco_openers(match: Match) -> list[int]:
    return [r.round_number for r in opening_economy_rows(match) if r.opener_buy == BuyType.ECO.value]
