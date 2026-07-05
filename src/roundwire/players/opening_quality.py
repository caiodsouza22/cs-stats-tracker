"""Opening duel quality and trade-after-entry metrics."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.opening import opening_duels
from roundwire.models.match import Match
from roundwire.stats.aggregates import mean, safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class OpeningQuality:
    player_id: str
    name: str
    openings: int
    opening_deaths: int
    traded_openings: int
    converted_openings: int
    avg_open_tick_ms: float
    weapon_mix: dict[str, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "openings": self.openings,
            "opening_deaths": self.opening_deaths,
            "traded_openings": self.traded_openings,
            "converted_openings": self.converted_openings,
            "avg_open_tick_ms": round(self.avg_open_tick_ms, 1),
            "weapon_mix": dict(self.weapon_mix),
            "conversion_rate": round(
                safe_div(float(self.converted_openings), float(self.openings)), 3
            ),
            "death_trade_rate": round(
                safe_div(float(self.traded_openings), float(self.opening_deaths)), 3
            ),
        }


def opening_quality(match: Match, player_id: PlayerId) -> OpeningQuality:
    player = match.player_map()[player_id]
    openings = opening_deaths = traded = converted = 0
    ticks: list[float] = []
    weapons: dict[str, int] = {}
    pmap = match.player_map()
    for duel in opening_duels(match):
        rnd = match.round_by_number(duel.round_number)
        if duel.kill.killer_id == player_id:
            openings += 1
            ticks.append(float(duel.kill.tick_ms))
            w = duel.kill.weapon.name.lower()
            weapons[w] = weapons.get(w, 0) + 1
            if rnd is not None and rnd.winner is player.team:
                converted += 1
        elif duel.kill.victim_id == player_id:
            opening_deaths += 1
            if duel.traded:
                traded += 1
    return OpeningQuality(
        player_id=str(player_id),
        name=player.name,
        openings=openings,
        opening_deaths=opening_deaths,
        traded_openings=traded,
        converted_openings=converted,
        avg_open_tick_ms=mean(ticks),
        weapon_mix=weapons,
    )


def opening_quality_table(match: Match) -> list[dict[str, object]]:
    rows = [opening_quality(match, p.player_id).to_dict() for p in match.players]
    return sorted(rows, key=lambda r: (-r["openings"], -r["conversion_rate"], r["name"]))


def earliest_openers(match: Match, limit: int = 5) -> list[dict[str, object]]:
    rows = []
    for duel in opening_duels(match):
        killer = match.player_map().get(duel.kill.killer_id)
        rows.append(
            {
                "round": duel.round_number,
                "tick_ms": int(duel.kill.tick_ms),
                "killer": killer.name if killer else str(duel.kill.killer_id),
                "weapon": duel.kill.weapon.name,
                "traded": duel.traded,
            }
        )
    rows.sort(key=lambda r: (r["tick_ms"], r["round"]))
    return rows[: max(0, limit)]


def opening_tempo(match: Match) -> dict[str, float]:
    ticks = [float(d.kill.tick_ms) for d in opening_duels(match)]
    if not ticks:
        return {"avg_ms": 0.0, "p50_ms": 0.0, "fast_share": 0.0}
    ordered = sorted(ticks)
    mid = ordered[len(ordered) // 2]
    fast = sum(1 for t in ticks if t <= 15000)
    return {
        "avg_ms": mean(ticks),
        "p50_ms": float(mid),
        "fast_share": fast / len(ticks),
    }
