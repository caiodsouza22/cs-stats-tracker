"""Per-player utility throw counts."""

from __future__ import annotations

from collections import Counter

from roundwire.models.match import Match
from roundwire.models.utility_event import UtilityKind
from roundwire.types import PlayerId


def utility_counts(match: Match, player_id: PlayerId | None = None) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for rnd in match.rounds:
        for event in rnd.utility:
            if player_id is not None and event.thrower_id != player_id:
                continue
            counter[event.kind.value] += 1
    return dict(counter)


def utility_by_kind(match: Match, kind: UtilityKind) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.kind is kind:
                total += 1
    return total
