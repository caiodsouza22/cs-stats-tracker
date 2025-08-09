"""Hitgroup and armor damage helpers (approximate CS values)."""

from __future__ import annotations

from dataclasses import dataclass

# Approximate multipliers vs unarmored / armored (public wiki-style figures).
HITGROUP_MULTIPLIER = {
    "head": 4.0,
    "chest": 1.0,
    "stomach": 1.25,
    "left_arm": 1.0,
    "right_arm": 1.0,
    "left_leg": 0.75,
    "right_leg": 0.75,
    "neck": 1.0,
    "generic": 1.0,
}

ARMOR_ABSORPTION = {
    "head": 0.5,  # helmet matters separately
    "chest": 0.5,
    "stomach": 0.5,
    "left_arm": 0.5,
    "right_arm": 0.5,
    "left_leg": 0.0,
    "right_leg": 0.0,
    "neck": 0.5,
    "generic": 0.5,
}


@dataclass(frozen=True, slots=True)
class DamageEstimate:
    raw: float
    after_armor: float
    hitgroup: str
    armored: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "raw": round(self.raw, 1),
            "after_armor": round(self.after_armor, 1),
            "hitgroup": self.hitgroup,
            "armored": self.armored,
        }


def estimate_damage(
    base_damage: float,
    hitgroup: str,
    *,
    armored: bool = False,
    helmet: bool = False,
    armor_pen: float = 1.0,
) -> DamageEstimate:
    group = hitgroup if hitgroup in HITGROUP_MULTIPLIER else "generic"
    raw = base_damage * HITGROUP_MULTIPLIER[group]
    if group == "head" and not helmet:
        after = raw
    elif armored:
        absorb = ARMOR_ABSORPTION[group] * (1.0 - max(0.0, min(1.0, armor_pen - 1.0)))
        # armor_pen ~1.0 means full pen scale; keep simple
        after = raw * (1.0 - 0.5 * (1.0 if armored else 0.0) * (0.0 if group.endswith("leg") else 1.0))
        after = raw * (1.0 - absorb * 0.5)
    else:
        after = raw
    return DamageEstimate(raw=raw, after_armor=after, hitgroup=group, armored=armored)


def shots_to_kill(
    base_damage: float,
    hitgroup: str,
    *,
    armored: bool = False,
    helmet: bool = False,
    hp: int = 100,
) -> int:
    dmg = estimate_damage(base_damage, hitgroup, armored=armored, helmet=helmet).after_armor
    if dmg <= 0:
        return 99
    n = 0
    health = float(hp)
    while health > 0 and n < 100:
        health -= dmg
        n += 1
    return n


# Representative base damages for common weapons (body shot baselines).
WEAPON_BASE_DAMAGE = {
    "ak47": 36.0,
    "m4a1": 33.0,
    "m4a1_silencer": 38.0,
    "awp": 115.0,
    "ssg08": 88.0,
    "deagle": 53.0,
    "usp_silencer": 35.0,
    "glock": 30.0,
    "mac10": 29.0,
    "mp9": 26.0,
    "nova": 26.0,
    "p250": 38.0,
    "famas": 30.0,
    "galilar": 30.0,
}


def ttk_table(weapon: str, *, armored: bool = True) -> dict[str, int]:
    base = WEAPON_BASE_DAMAGE.get(weapon)
    if base is None:
        return {}
    return {
        group: shots_to_kill(base, group, armored=armored, helmet=(group == "head" and armored))
        for group in ("head", "chest", "stomach")
    }


def catalog_ttk(armored: bool = True) -> dict[str, dict[str, int]]:
    return {weapon: ttk_table(weapon, armored=armored) for weapon in sorted(WEAPON_BASE_DAMAGE)}
