"""Anti-eco (full vs eco) outcome tracking."""

from __future__ import annotations

from roundwire.economy.classify import classify_team_buy
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide


def anti_eco_cases(match: Match) -> list[tuple[int, str, bool]]:
    cases: list[tuple[int, str, bool]] = []
    for rnd in match.rounds:
        ct = classify_team_buy(rnd, match, TeamSide.CT)
        t = classify_team_buy(rnd, match, TeamSide.T)
        if ct is BuyType.FULL and t is BuyType.ECO:
            cases.append((int(rnd.number), "CT", rnd.winner is TeamSide.CT))
        if t is BuyType.FULL and ct is BuyType.ECO:
            cases.append((int(rnd.number), "T", rnd.winner is TeamSide.T))
    return cases


def anti_eco_success_rate(match: Match) -> float:
    cases = anti_eco_cases(match)
    if not cases:
        return 0.0
    return sum(1 for _n, _side, ok in cases if ok) / len(cases)
