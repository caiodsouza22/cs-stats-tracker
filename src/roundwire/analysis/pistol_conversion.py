"""Pistol round second-round conversion."""

from __future__ import annotations

from roundwire.economy.pistol import pistol_round_numbers
from roundwire.models.match import Match


def pistol_conversion_rate(match: Match) -> float:
    p1, p2 = pistol_round_numbers(match.edition)
    converted = 0
    support = 0
    for pistol_n in (p1, p2):
        pistol = match.round_by_number(pistol_n)
        nxt = match.round_by_number(pistol_n + 1)
        if pistol is None or nxt is None:
            continue
        support += 1
        if pistol.winner is nxt.winner:
            converted += 1
    if support == 0:
        return 0.0
    return converted / support


def pistol_winners(match: Match) -> list[str]:
    p1, p2 = pistol_round_numbers(match.edition)
    out: list[str] = []
    for n in (p1, p2):
        rnd = match.round_by_number(n)
        if rnd is not None:
            out.append(rnd.winner.value)
    return out
