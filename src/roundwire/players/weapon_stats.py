"""Per-player weapon usage and accuracy-ish breakdowns."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from roundwire.models.match import Match
from roundwire.rules.weapon_aliases import canonical_weapon_name, weapon_slot
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId


@dataclass(slots=True)
class WeaponLine:
    weapon: str
    slot: str
    kills: int
    damage: int
    headshots: int
    shots_proxy: int
    hs_pct: float
    damage_per_kill: float

    def to_dict(self) -> dict[str, object]:
        return {
            "weapon": self.weapon,
            "slot": self.slot,
            "kills": self.kills,
            "damage": self.damage,
            "headshots": self.headshots,
            "shots_proxy": self.shots_proxy,
            "hs_pct": round(self.hs_pct, 3),
            "damage_per_kill": round(self.damage_per_kill, 1),
        }


@dataclass(slots=True)
class WeaponBreakdown:
    player_id: str
    lines: list[WeaponLine] = field(default_factory=list)
    by_slot: dict[str, int] = field(default_factory=dict)
    unique_weapons: int = 0
    primary_slot: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "lines": [line.to_dict() for line in self.lines],
            "by_slot": dict(self.by_slot),
            "unique_weapons": self.unique_weapons,
            "primary_slot": self.primary_slot,
        }


def _canon(name: str) -> str:
    try:
        return canonical_weapon_name(name)
    except KeyError:
        return name.lower()


def _slot(name: str) -> str:
    try:
        return weapon_slot(name)
    except KeyError:
        return "unknown"


def weapon_breakdown(match: Match, player_id: PlayerId) -> WeaponBreakdown:
    kills: Counter[str] = Counter()
    hs: Counter[str] = Counter()
    damage: Counter[str] = Counter()
    shots: Counter[str] = Counter()

    for rnd in match.rounds:
        for kill in rnd.kills_for(player_id):
            weapon = _canon(kill.weapon.name)
            kills[weapon] += 1
            if kill.headshot:
                hs[weapon] += 1
        for event in rnd.damage:
            if event.attacker_id != player_id:
                continue
            weapon = _canon(event.weapon.name)
            damage[weapon] += event.damage
            shots[weapon] += 1

    lines: list[WeaponLine] = []
    by_slot: dict[str, int] = defaultdict(int)
    for weapon in sorted(set(kills) | set(damage), key=lambda w: (-kills[w], -damage[w], w)):
        slot = _slot(weapon)
        k = kills[weapon]
        d = damage[weapon]
        h = hs[weapon]
        s = shots[weapon]
        lines.append(
            WeaponLine(
                weapon=weapon,
                slot=slot,
                kills=k,
                damage=d,
                headshots=h,
                shots_proxy=s,
                hs_pct=safe_div(float(h), float(k)),
                damage_per_kill=safe_div(float(d), float(k)),
            )
        )
        by_slot[slot] += k

    primary = None
    if by_slot:
        primary = max(by_slot.items(), key=lambda kv: kv[1])[0]

    return WeaponBreakdown(
        player_id=str(player_id),
        lines=lines,
        by_slot=dict(by_slot),
        unique_weapons=len(lines),
        primary_slot=primary,
    )


def top_weapons(match: Match, player_id: PlayerId, n: int = 5) -> list[WeaponLine]:
    return weapon_breakdown(match, player_id).lines[: max(0, n)]


def slot_kill_share(match: Match, player_id: PlayerId) -> dict[str, float]:
    breakdown = weapon_breakdown(match, player_id)
    total = sum(breakdown.by_slot.values())
    return {slot: safe_div(float(kills), float(total)) for slot, kills in breakdown.by_slot.items()}


def awp_dependency(match: Match, player_id: PlayerId) -> float:
    """Share of kills coming from AWP."""
    breakdown = weapon_breakdown(match, player_id)
    total = sum(line.kills for line in breakdown.lines)
    awp = next((line.kills for line in breakdown.lines if line.weapon == "awp"), 0)
    return safe_div(float(awp), float(total))


def rifle_hs_rate(match: Match, player_id: PlayerId) -> float:
    breakdown = weapon_breakdown(match, player_id)
    rifle_kills = 0
    rifle_hs = 0
    for line in breakdown.lines:
        if line.slot == "rifle":
            rifle_kills += line.kills
            rifle_hs += line.headshots
    return safe_div(float(rifle_hs), float(rifle_kills))


def pistol_round_weapon_kills(match: Match, player_id: PlayerId) -> dict[str, int]:
    from roundwire.economy.pistol import is_pistol_round

    counter: Counter[str] = Counter()
    for rnd in match.rounds:
        if not is_pistol_round(rnd, match.edition):
            continue
        for kill in rnd.kills_for(player_id):
            counter[_canon(kill.weapon.name)] += 1
    return dict(counter)
