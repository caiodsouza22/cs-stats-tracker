"""Utility timing relative to first kill / plant windows."""

from __future__ import annotations

from roundwire.combat.opening import first_kill
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.utility_event import UtilityEvent, UtilityKind


def utility_before_opening(round_: Round) -> list[UtilityEvent]:
    fk = first_kill(round_)
    if fk is None:
        return list(round_.utility)
    return [u for u in round_.utility if int(u.tick_ms) <= int(fk.tick_ms)]


def utility_after_opening(round_: Round) -> list[UtilityEvent]:
    fk = first_kill(round_)
    if fk is None:
        return []
    return [u for u in round_.utility if int(u.tick_ms) > int(fk.tick_ms)]


def early_flash_count(match: Match, before_ms: int = 6000) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.kind is UtilityKind.FLASH and int(event.tick_ms) <= before_ms:
                total += 1
    return total


def avg_first_util_ms(match: Match) -> float:
    samples: list[int] = []
    for rnd in match.rounds:
        if not rnd.utility:
            continue
        samples.append(min(int(u.tick_ms) for u in rnd.utility))
    if not samples:
        return 0.0
    return sum(samples) / len(samples)


def util_density(match: Match) -> float:
    """Average utility events per round."""
    if not match.rounds:
        return 0.0
    return sum(len(r.utility) for r in match.rounds) / len(match.rounds)
