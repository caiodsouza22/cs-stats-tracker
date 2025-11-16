"""Kill timing bands within rounds."""

from __future__ import annotations

from roundwire.models.match import Match


def kills_before(match: Match, ms: int) -> int:
    return sum(1 for rnd in match.rounds for k in rnd.kills if int(k.tick_ms) <= ms)


def kills_after(match: Match, ms: int) -> int:
    return sum(1 for rnd in match.rounds for k in rnd.kills if int(k.tick_ms) >= ms)


def early_kill_share(match: Match, ms: int = 20000) -> float:
    total = sum(len(r.kills) for r in match.rounds)
    if total == 0:
        return 0.0
    return kills_before(match, ms) / total


def late_kill_share(match: Match, ms: int = 70000) -> float:
    total = sum(len(r.kills) for r in match.rounds)
    if total == 0:
        return 0.0
    return kills_after(match, ms) / total


def average_first_kill_ms(match: Match) -> float:
    samples: list[int] = []
    for rnd in match.rounds:
        if not rnd.kills:
            continue
        samples.append(min(int(k.tick_ms) for k in rnd.kills))
    if not samples:
        return 0.0
    return sum(samples) / len(samples)
