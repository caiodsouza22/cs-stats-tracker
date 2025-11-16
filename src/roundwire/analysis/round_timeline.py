"""Flatten round events into a timeline of labeled moments."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.round import Round


@dataclass(frozen=True, slots=True)
class TimelineEvent:
    tick_ms: int
    kind: str
    detail: str


def round_timeline(round_: Round) -> list[TimelineEvent]:
    events: list[TimelineEvent] = []
    for kill in round_.kills:
        events.append(
            TimelineEvent(
                tick_ms=int(kill.tick_ms),
                kind="kill",
                detail=f"{kill.killer_id}->{kill.victim_id} ({kill.weapon.name})",
            )
        )
    for util in round_.utility:
        events.append(
            TimelineEvent(
                tick_ms=int(util.tick_ms),
                kind="utility",
                detail=f"{util.thrower_id} {util.kind.value}",
            )
        )
    events.sort(key=lambda e: e.tick_ms)
    return events
