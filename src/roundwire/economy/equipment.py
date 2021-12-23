"""Equipment value aggregates."""

from __future__ import annotations

from roundwire.models.inventory import InventorySnapshot
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.team import TeamSide


def team_equipment_value(round_: Round, match: Match, side: TeamSide) -> int:
    ids = {p.player_id for p in match.players_on(side)}
    return sum(inv.equipment_value for inv in round_.inventories if inv.player_id in ids)


def average_equipment_value(round_: Round, match: Match, side: TeamSide) -> float:
    ids = {p.player_id for p in match.players_on(side)}
    invs = [inv for inv in round_.inventories if inv.player_id in ids]
    if not invs:
        return 0.0
    return sum(i.equipment_value for i in invs) / len(invs)


def cash_remaining(round_: Round, match: Match, side: TeamSide) -> int:
    ids = {p.player_id for p in match.players_on(side)}
    return sum(inv.cash for inv in round_.inventories if inv.player_id in ids)


def inventory_for_player(round_: Round, player_id: str) -> InventorySnapshot | None:
    for inv in round_.inventories:
        if str(inv.player_id) == player_id:
            return inv
    return None
