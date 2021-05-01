"""Grenade slot limits shared across editions."""

from __future__ import annotations

MAX_TOTAL_GRENADES = 4
MAX_FLASH = 2
MAX_SMOKE = 1
MAX_HE = 1
MAX_FIRE = 1
MAX_DECOY = 1


def is_legal_loadout(grenades: list[str]) -> bool:
    if len(grenades) > MAX_TOTAL_GRENADES:
        return False
    counts = {
        "flash": 0,
        "smoke": 0,
        "he": 0,
        "fire": 0,
        "decoy": 0,
    }
    for g in grenades:
        key = g.lower()
        if "flash" in key:
            counts["flash"] += 1
        elif "smoke" in key:
            counts["smoke"] += 1
        elif key in {"he", "hegrenade", "weapon_hegrenade"}:
            counts["he"] += 1
        elif key in {"molotov", "incendiary", "incgrenade", "weapon_molotov", "weapon_incgrenade"}:
            counts["fire"] += 1
        elif "decoy" in key:
            counts["decoy"] += 1
    return (
        counts["flash"] <= MAX_FLASH
        and counts["smoke"] <= MAX_SMOKE
        and counts["he"] <= MAX_HE
        and counts["fire"] <= MAX_FIRE
        and counts["decoy"] <= MAX_DECOY
    )
