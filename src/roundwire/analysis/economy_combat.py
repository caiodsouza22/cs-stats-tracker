"""Join economy buy type with combat outcomes."""

from __future__ import annotations

from roundwire.economy.classify import classify_team_buy
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide


def winrate_by_buy(match: Match, side: TeamSide) -> dict[str, float]:
    totals: dict[str, list[int]] = {}
    for rnd in match.rounds:
        buy = classify_team_buy(rnd, match, side)
        totals.setdefault(buy.value, []).append(1 if rnd.winner is side else 0)
    return {k: (sum(v) / len(v) if v else 0.0) for k, v in totals.items()}


def upset_candidates(match: Match) -> list[tuple[int, str]]:
    """Eco/force wins against full buys."""
    out: list[tuple[int, str]] = []
    for rnd in match.rounds:
        ct = classify_team_buy(rnd, match, TeamSide.CT)
        t = classify_team_buy(rnd, match, TeamSide.T)
        if rnd.winner is TeamSide.CT and ct in {BuyType.ECO, BuyType.FORCE} and t is BuyType.FULL:
            out.append((int(rnd.number), "CT"))
        if rnd.winner is TeamSide.T and t in {BuyType.ECO, BuyType.FORCE} and ct is BuyType.FULL:
            out.append((int(rnd.number), "T"))
    return out
