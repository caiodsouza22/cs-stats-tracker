"""Higher-level event wrappers combining kill/damage/utility chronologically."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from roundwire.models.round import Round


class EventKind(str, Enum):
    KILL = "kill"
    DAMAGE = "damage"
    UTILITY = "utility"


@dataclass(frozen=True, slots=True)
class ChronoEvent:
    tick_ms: int
    kind: EventKind
    summary: str


def chronological_events(round_: Round) -> list[ChronoEvent]:
    events: list[ChronoEvent] = []
    for kill in round_.kills:
        events.append(
            ChronoEvent(
                tick_ms=int(kill.tick_ms),
                kind=EventKind.KILL,
                summary=f"{kill.killer_id} killed {kill.victim_id} with {kill.weapon.name}",
            )
        )
    for dmg in round_.damage:
        events.append(
            ChronoEvent(
                tick_ms=int(dmg.tick_ms),
                kind=EventKind.DAMAGE,
                summary=f"{dmg.attacker_id} dealt {dmg.damage} to {dmg.victim_id}",
            )
        )
    for util in round_.utility:
        events.append(
            ChronoEvent(
                tick_ms=int(util.tick_ms),
                kind=EventKind.UTILITY,
                summary=f"{util.thrower_id} threw {util.kind.value}",
            )
        )
    events.sort(key=lambda e: (e.tick_ms, e.kind.value, e.summary))
    return events


def event_counts(round_: Round) -> dict[str, int]:
    return {
        "kills": len(round_.kills),
        "damage": len(round_.damage),
        "utility": len(round_.utility),
    }
