"""Per-player utility deep stats."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.models.utility_event import UtilityKind
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId
from roundwire.utility.cost import utility_spend
from roundwire.utility.flashes import enemies_flashed_total, flash_efficiency, teammates_flashed_total
from roundwire.utility.he import he_damage, he_throws
from roundwire.utility.molotov import fire_damage, fire_throws
from roundwire.utility.smoke import smoke_count
from roundwire.utility.usage import utility_counts


@dataclass(slots=True)
class PlayerUtilityProfile:
    player_id: str
    flashes: int
    smokes: int
    hes: int
    fires: int
    decoys: int
    enemies_flashed: int
    teammates_flashed: int
    flash_efficiency: float
    he_damage: int
    fire_damage: int
    spend: int
    util_per_round: float
    flash_assist_proxy: float
    early_util: int
    late_util: int

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "flashes": self.flashes,
            "smokes": self.smokes,
            "hes": self.hes,
            "fires": self.fires,
            "decoys": self.decoys,
            "enemies_flashed": self.enemies_flashed,
            "teammates_flashed": self.teammates_flashed,
            "flash_efficiency": round(self.flash_efficiency, 3),
            "he_damage": self.he_damage,
            "fire_damage": self.fire_damage,
            "spend": self.spend,
            "util_per_round": round(self.util_per_round, 3),
            "flash_assist_proxy": round(self.flash_assist_proxy, 3),
            "early_util": self.early_util,
            "late_util": self.late_util,
        }


def _count_kind(match: Match, player_id: PlayerId, kind: UtilityKind) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.thrower_id == player_id and event.kind is kind:
                total += 1
    return total


def _timing_split(match: Match, player_id: PlayerId, early_ms: int = 20000, late_ms: int = 70000) -> tuple[int, int]:
    early = late = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.thrower_id != player_id:
                continue
            tick = int(event.tick_ms)
            if tick <= early_ms:
                early += 1
            if tick >= late_ms:
                late += 1
    return early, late


def build_utility_profile(match: Match, player_id: PlayerId) -> PlayerUtilityProfile:
    counts = utility_counts(match, player_id)
    rounds = max(1, len(match.rounds))
    early, late = _timing_split(match, player_id)
    enemies = enemies_flashed_total(match, player_id)
    flashes = counts.get("flash", 0)
    return PlayerUtilityProfile(
        player_id=str(player_id),
        flashes=flashes,
        smokes=smoke_count(match, player_id),
        hes=he_throws(match, player_id),
        fires=fire_throws(match, player_id),
        decoys=_count_kind(match, player_id, UtilityKind.DECOY),
        enemies_flashed=enemies,
        teammates_flashed=teammates_flashed_total(match, player_id),
        flash_efficiency=flash_efficiency(match, player_id),
        he_damage=he_damage(match, player_id),
        fire_damage=fire_damage(match, player_id),
        spend=utility_spend(match, player_id),
        util_per_round=sum(counts.values()) / rounds,
        flash_assist_proxy=safe_div(float(enemies), float(max(1, flashes))),
        early_util=early,
        late_util=late,
    )


def utility_round_series(match: Match, player_id: PlayerId) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for rnd in match.rounds:
        flashes = smokes = hes = fires = 0
        enemies = 0
        for event in rnd.utility:
            if event.thrower_id != player_id:
                continue
            if event.kind is UtilityKind.FLASH:
                flashes += 1
                enemies += event.enemies_flashed
            elif event.kind is UtilityKind.SMOKE:
                smokes += 1
            elif event.kind is UtilityKind.HE:
                hes += 1
            elif event.kind in {UtilityKind.MOLOTOV, UtilityKind.INCENDIARY}:
                fires += 1
        rows.append(
            {
                "round": int(rnd.number),
                "flash": flashes,
                "smoke": smokes,
                "he": hes,
                "fire": fires,
                "enemies_flashed": enemies,
            }
        )
    return rows


def support_index(match: Match, player_id: PlayerId) -> float:
    """Blend of flash value, smoke volume, and spend relative to frags."""
    from roundwire.combat.kd import kill_count

    profile = build_utility_profile(match, player_id)
    kills = max(1, kill_count(match, player_id))
    return (
        profile.enemies_flashed * 1.5
        + profile.smokes * 1.2
        + profile.fires * 0.8
        + profile.he_damage / 50.0
    ) / kills


def util_heavy_rounds(match: Match, player_id: PlayerId, minimum: int = 3) -> list[int]:
    out: list[int] = []
    for row in utility_round_series(match, player_id):
        total = row["flash"] + row["smoke"] + row["he"] + row["fire"]
        if total >= minimum:
            out.append(row["round"])
    return out
