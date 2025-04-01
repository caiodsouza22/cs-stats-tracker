"""Damage timing and burst detection per player."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.stats.aggregates import mean, safe_div
from roundwire.stats.rolling import rolling_mean
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class DamageBurst:
    round_number: int
    start_ms: int
    end_ms: int
    damage: int
    hits: int

    def to_dict(self) -> dict[str, object]:
        return {
            "round": self.round_number,
            "start_ms": self.start_ms,
            "end_ms": self.end_ms,
            "damage": self.damage,
            "hits": self.hits,
        }


def damage_bursts(match: Match, player_id: PlayerId, gap_ms: int = 2500, min_damage: int = 40) -> list[DamageBurst]:
    out: list[DamageBurst] = []
    for rnd in match.rounds:
        events = sorted(
            [d for d in rnd.damage if d.attacker_id == player_id],
            key=lambda d: int(d.tick_ms),
        )
        if not events:
            continue
        cluster = [events[0]]
        for event in events[1:]:
            if int(event.tick_ms) - int(cluster[-1].tick_ms) <= gap_ms:
                cluster.append(event)
            else:
                dmg = sum(e.damage for e in cluster)
                if dmg >= min_damage:
                    out.append(
                        DamageBurst(
                            int(rnd.number),
                            int(cluster[0].tick_ms),
                            int(cluster[-1].tick_ms),
                            dmg,
                            len(cluster),
                        )
                    )
                cluster = [event]
        dmg = sum(e.damage for e in cluster)
        if dmg >= min_damage:
            out.append(
                DamageBurst(
                    int(rnd.number),
                    int(cluster[0].tick_ms),
                    int(cluster[-1].tick_ms),
                    dmg,
                    len(cluster),
                )
            )
    return out


def damage_timing_summary(match: Match, player_id: PlayerId) -> dict[str, object]:
    bursts = damage_bursts(match, player_id)
    per_round = []
    for rnd in match.rounds:
        per_round.append(float(rnd.damage_dealt_by(player_id)))
    return {
        "bursts": len(bursts),
        "avg_burst_damage": round(mean([float(b.damage) for b in bursts]), 1),
        "max_burst": max((b.damage for b in bursts), default=0),
        "damage_series": per_round,
        "rolling_adr_proxy": [
            None if v is None else round(v, 1) for v in rolling_mean(per_round, 3)
        ],
        "early_damage_share": _band_share(match, player_id, 0, 25000),
        "late_damage_share": _band_share(match, player_id, 70000, 10**9),
    }


def _band_share(match: Match, player_id: PlayerId, start: int, end: int) -> float:
    band = total = 0
    for rnd in match.rounds:
        for event in rnd.damage:
            if event.attacker_id != player_id:
                continue
            total += event.damage
            if start <= int(event.tick_ms) < end:
                band += event.damage
    return safe_div(float(band), float(total))


def highest_damage_round(match: Match, player_id: PlayerId) -> tuple[int, int] | None:
    best: tuple[int, int] | None = None
    for rnd in match.rounds:
        dmg = rnd.damage_dealt_by(player_id)
        if best is None or dmg > best[1]:
            best = (int(rnd.number), dmg)
    return best
