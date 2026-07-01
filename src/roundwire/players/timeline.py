"""Event timeline filtered to a single player."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class PlayerEvent:
    round_number: int
    tick_ms: int
    kind: str
    detail: str

    def to_dict(self) -> dict[str, object]:
        return {
            "round": self.round_number,
            "tick_ms": self.tick_ms,
            "kind": self.kind,
            "detail": self.detail,
        }


def player_timeline(match: Match, player_id: PlayerId) -> list[PlayerEvent]:
    events: list[PlayerEvent] = []
    for rnd in match.rounds:
        n = int(rnd.number)
        for kill in rnd.kills:
            if kill.killer_id == player_id:
                events.append(
                    PlayerEvent(
                        n,
                        int(kill.tick_ms),
                        "kill",
                        f"{kill.weapon.name}"
                        + (" HS" if kill.headshot else "")
                        + (f" assisted_by={kill.assisted_by}" if kill.assisted_by else ""),
                    )
                )
            elif kill.victim_id == player_id:
                events.append(
                    PlayerEvent(
                        n,
                        int(kill.tick_ms),
                        "death",
                        f"by {kill.weapon.name} from {kill.killer_id}",
                    )
                )
            elif kill.assisted_by == player_id:
                events.append(
                    PlayerEvent(
                        n,
                        int(kill.tick_ms),
                        "assist",
                        f"on {kill.victim_id}",
                    )
                )
        for dmg in rnd.damage:
            if dmg.attacker_id == player_id and dmg.damage >= 40:
                events.append(
                    PlayerEvent(
                        n,
                        int(dmg.tick_ms),
                        "damage",
                        f"{dmg.damage} to {dmg.victim_id} ({dmg.hitgroup})",
                    )
                )
        for util in rnd.utility:
            if util.thrower_id == player_id:
                detail = util.kind.value
                if util.enemies_flashed:
                    detail += f" enemies={util.enemies_flashed}"
                if util.damage_dealt:
                    detail += f" dmg={util.damage_dealt}"
                events.append(PlayerEvent(n, int(util.tick_ms), "utility", detail))
    events.sort(key=lambda e: (e.round_number, e.tick_ms, e.kind))
    return events


def timeline_by_round(match: Match, player_id: PlayerId) -> dict[int, list[PlayerEvent]]:
    grouped: dict[int, list[PlayerEvent]] = {}
    for event in player_timeline(match, player_id):
        grouped.setdefault(event.round_number, []).append(event)
    return grouped


def first_action_round(match: Match, player_id: PlayerId) -> PlayerEvent | None:
    events = player_timeline(match, player_id)
    return events[0] if events else None


def kill_feed(match: Match, player_id: PlayerId) -> list[str]:
    return [
        f"R{e.round_number} @{e.tick_ms}ms {e.detail}"
        for e in player_timeline(match, player_id)
        if e.kind == "kill"
    ]


def death_feed(match: Match, player_id: PlayerId) -> list[str]:
    return [
        f"R{e.round_number} @{e.tick_ms}ms {e.detail}"
        for e in player_timeline(match, player_id)
        if e.kind == "death"
    ]


def busy_rounds(match: Match, player_id: PlayerId, minimum_events: int = 4) -> list[int]:
    grouped = timeline_by_round(match, player_id)
    return sorted(r for r, ev in grouped.items() if len(ev) >= minimum_events)
