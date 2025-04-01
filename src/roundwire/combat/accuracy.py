"""Accuracy / spray proxies from damage event spacing."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.stats.aggregates import mean, safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class AccuracyCard:
    player_id: str
    name: str
    hits: int
    head_hits: int
    head_share: float
    avg_gap_ms: float
    sprays: int

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "hits": self.hits,
            "head_hits": self.head_hits,
            "head_share": round(self.head_share, 3),
            "avg_gap_ms": round(self.avg_gap_ms, 1),
            "sprays": self.sprays,
        }


def accuracy_card(match: Match, player_id: PlayerId, spray_gap_ms: int = 120) -> AccuracyCard:
    player = match.player_map()[player_id]
    hits = head = sprays = 0
    gaps: list[float] = []
    for rnd in match.rounds:
        events = sorted(
            [d for d in rnd.damage if d.attacker_id == player_id],
            key=lambda d: int(d.tick_ms),
        )
        hits += len(events)
        head += sum(1 for d in events if d.hitgroup == "head")
        for prev, cur in zip(events, events[1:]):
            gap = int(cur.tick_ms) - int(prev.tick_ms)
            gaps.append(float(gap))
            if 0 < gap <= spray_gap_ms:
                sprays += 1
    return AccuracyCard(
        player_id=str(player_id),
        name=player.name,
        hits=hits,
        head_hits=head,
        head_share=safe_div(float(head), float(hits)),
        avg_gap_ms=mean(gaps),
        sprays=sprays,
    )


def accuracy_table(match: Match) -> list[dict[str, object]]:
    rows = [accuracy_card(match, p.player_id).to_dict() for p in match.players]
    return sorted(rows, key=lambda r: (-r["head_share"], -r["hits"], r["name"]))
