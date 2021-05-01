"""Per-weapon kill reward overrides."""

from __future__ import annotations

from roundwire.rules.weapon_aliases import canonical_weapon_name

KILL_REWARDS: dict[str, int] = {
    "ak47": 300,
    "m4a1": 300,
    "m4a1_silencer": 300,
    "awp": 100,
    "ssg08": 300,
    "deagle": 300,
    "knife": 1500,
    "taser": 100,
    "hegrenade": 300,
    "molotov": 300,
    "incgrenade": 300,
    "nova": 900,
    "xm1014": 900,
    "mag7": 900,
    "sawedoff": 900,
}


def kill_reward_for(weapon_name: str, default: int = 300) -> int:
    try:
        canon = canonical_weapon_name(weapon_name)
    except KeyError:
        return default
    return KILL_REWARDS.get(canon, default)
