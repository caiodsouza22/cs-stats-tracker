"""Assist networks and flash-into-kill chains."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.models.utility_event import UtilityKind
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class AssistEdge:
    from_id: str
    from_name: str
    to_id: str
    to_name: str
    assists: int

    def to_dict(self) -> dict[str, object]:
        return {
            "from_id": self.from_id,
            "from_name": self.from_name,
            "to_id": self.to_id,
            "to_name": self.to_name,
            "assists": self.assists,
        }


def assist_edges(match: Match) -> list[AssistEdge]:
    counts: dict[tuple[str, str], int] = defaultdict(int)
    pmap = match.player_map()
    for rnd in match.rounds:
        for kill in rnd.kills:
            if kill.assisted_by is None:
                continue
            key = (str(kill.assisted_by), str(kill.killer_id))
            counts[key] += 1
    edges = []
    for (src, dst), n in counts.items():
        a = pmap.get(PlayerId(src))
        b = pmap.get(PlayerId(dst))
        edges.append(
            AssistEdge(
                from_id=src,
                from_name=a.name if a else src,
                to_id=dst,
                to_name=b.name if b else dst,
                assists=n,
            )
        )
    return sorted(edges, key=lambda e: (-e.assists, e.from_name, e.to_name))


def flash_assist_proxy_edges(match: Match, window_ms: int = 4000) -> list[AssistEdge]:
    """Count flash thrower -> killer pairs when flash precedes kill."""
    counts: dict[tuple[str, str], int] = defaultdict(int)
    pmap = match.player_map()
    for rnd in match.rounds:
        flashes = [u for u in rnd.utility if u.kind is UtilityKind.FLASH and u.enemies_flashed > 0]
        for kill in rnd.kills:
            for flash in flashes:
                dt = int(kill.tick_ms) - int(flash.tick_ms)
                if 0 <= dt <= window_ms:
                    counts[(str(flash.thrower_id), str(kill.killer_id))] += 1
    edges = []
    for (src, dst), n in counts.items():
        if src == dst:
            continue
        a = pmap.get(PlayerId(src))
        b = pmap.get(PlayerId(dst))
        edges.append(
            AssistEdge(
                from_id=src,
                from_name=a.name if a else src,
                to_id=dst,
                to_name=b.name if b else dst,
                assists=n,
            )
        )
    return sorted(edges, key=lambda e: (-e.assists, e.from_name, e.to_name))


def assist_leaderboard(match: Match) -> list[dict[str, object]]:
    counter: Counter[str] = Counter()
    for edge in assist_edges(match):
        counter[edge.from_name] += edge.assists
    return [{"name": name, "assists": n} for name, n in counter.most_common()]


def support_to_star_pairs(match: Match, limit: int = 5) -> list[dict[str, object]]:
    edges = flash_assist_proxy_edges(match) + assist_edges(match)
    merged: dict[tuple[str, str], int] = defaultdict(int)
    names: dict[tuple[str, str], tuple[str, str]] = {}
    for edge in edges:
        key = (edge.from_id, edge.to_id)
        merged[key] += edge.assists
        names[key] = (edge.from_name, edge.to_name)
    rows = []
    for (src, dst), n in merged.items():
        fn, tn = names[(src, dst)]
        rows.append({"support": fn, "finisher": tn, "links": n})
    return sorted(rows, key=lambda r: (-r["links"], r["support"]))[: max(0, limit)]


def self_flash_rate(match: Match, player_id: PlayerId) -> float:
    enemies = team = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.thrower_id != player_id or event.kind is not UtilityKind.FLASH:
                continue
            enemies += event.enemies_flashed
            team += event.teammates_flashed
    return safe_div(float(team), float(enemies + team))
