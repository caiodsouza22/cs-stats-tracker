"""Duel matrix and first-blood vs rematch framing."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class DuelRecord:
    a: str
    b: str
    a_wins: int
    b_wins: int

    @property
    def total(self) -> int:
        return self.a_wins + self.b_wins

    @property
    def a_rate(self) -> float:
        return 0.0 if self.total == 0 else self.a_wins / self.total


def duel_matrix(match: Match) -> list[DuelRecord]:
    """Pairwise kill counts between players (unordered pair keyed by sorted ids)."""
    wins: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for rnd in match.rounds:
        for kill in rnd.kills:
            a = str(kill.killer_id)
            b = str(kill.victim_id)
            key = tuple(sorted((a, b)))
            wins[key][a] += 1
    out: list[DuelRecord] = []
    for (a, b), table in wins.items():
        out.append(DuelRecord(a=a, b=b, a_wins=table.get(a, 0), b_wins=table.get(b, 0)))
    out.sort(key=lambda r: (-r.total, r.a, r.b))
    return out


def head_to_head(match: Match, a: PlayerId, b: PlayerId) -> DuelRecord:
    a_s, b_s = str(a), str(b)
    a_wins = 0
    b_wins = 0
    for rnd in match.rounds:
        for kill in rnd.kills:
            if kill.killer_id == a and kill.victim_id == b:
                a_wins += 1
            elif kill.killer_id == b and kill.victim_id == a:
                b_wins += 1
    return DuelRecord(a=a_s, b=b_s, a_wins=a_wins, b_wins=b_wins)


def top_rivalries(match: Match, limit: int = 5) -> list[DuelRecord]:
    return duel_matrix(match)[: max(0, limit)]


def one_sided_duels(match: Match, min_kills: int = 3) -> list[DuelRecord]:
    """Duels where one player has all the kills (min threshold)."""
    return [
        d
        for d in duel_matrix(match)
        if d.total >= min_kills and (d.a_wins == 0 or d.b_wins == 0)
    ]
