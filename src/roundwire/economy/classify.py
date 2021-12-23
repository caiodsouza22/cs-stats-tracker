"""Classify eco / force / full buys from inventory snapshots."""

from __future__ import annotations

from collections import Counter

from roundwire.models.buy_type import BuyType
from roundwire.models.edition import GameEdition
from roundwire.models.inventory import InventorySnapshot
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.team import TeamSide
from roundwire.rules.buy_rules import classify_equipment_value


def _team_inv(round_: Round, match: Match, side: TeamSide) -> list[InventorySnapshot]:
    ids = {p.player_id for p in match.players_on(side)}
    return [inv for inv in round_.inventories if inv.player_id in ids]


def classify_team_buy(
    round_: Round,
    match: Match,
    side: TeamSide,
    *,
    pistol_round: bool = False,
) -> BuyType:
    invs = _team_inv(round_, match, side)
    if not invs:
        return BuyType.UNKNOWN
    avg = sum(i.equipment_value for i in invs) / len(invs)
    return classify_equipment_value(int(avg), match.edition, pistol_round=pistol_round)


def classify_round_buy(round_: Round, match: Match) -> dict[str, BuyType]:
    pistol = int(round_.number) in {1, match.edition.regulation_rounds // 2 + 1}
    return {
        "CT": classify_team_buy(round_, match, TeamSide.CT, pistol_round=pistol),
        "T": classify_team_buy(round_, match, TeamSide.T, pistol_round=pistol),
    }


def buy_histogram(match: Match, side: TeamSide) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for rnd in match.rounds:
        pistol = int(rnd.number) in {1, match.edition.regulation_rounds // 2 + 1}
        buy = classify_team_buy(rnd, match, side, pistol_round=pistol)
        counter[buy.value] += 1
    return dict(counter)

def buy_advantage(match: Match) -> list[tuple[int, str]]:
    """Rounds where one side full-bought and the other eco'd."""
    from roundwire.models.buy_type import BuyType

    rows: list[tuple[int, str]] = []
    for rnd in match.rounds:
        buys = classify_round_buy(rnd, match)
        ct, t = buys["CT"], buys["T"]
        if ct is BuyType.FULL and t is BuyType.ECO:
            rows.append((int(rnd.number), "CT_advantage"))
        elif t is BuyType.FULL and ct is BuyType.ECO:
            rows.append((int(rnd.number), "T_advantage"))
    return rows


def mirror_buys(match: Match) -> list[int]:
    return [
        int(rnd.number)
        for rnd in match.rounds
        if (b := classify_round_buy(rnd, match)) and b["CT"] == b["T"]
    ]
