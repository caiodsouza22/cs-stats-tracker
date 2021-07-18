"""Detailed weapon profile notes used by analytics."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.rules.weapon_aliases import WEAPON_CATALOG, canonical_weapon_name


@dataclass(frozen=True, slots=True)
class WeaponProfile:
    name: str
    slot: str
    cost: int
    typical_range: str
    armor_pen: str
    notes: str


_PROFILES: dict[str, WeaponProfile] = {
    "ak47": WeaponProfile("ak47", "rifle", 2700, "mid-long", "high", "T rifle staple"),
    "m4a1": WeaponProfile("m4a1", "rifle", 3100, "mid-long", "medium", "CT unsilenced rifle"),
    "m4a1_silencer": WeaponProfile("m4a1_silencer", "rifle", 2900, "mid", "medium", "CT silenced rifle"),
    "awp": WeaponProfile("awp", "sniper", 4750, "long", "extreme", "Magnum sniper"),
    "ssg08": WeaponProfile("ssg08", "sniper", 1700, "mid-long", "high", "Scout"),
    "deagle": WeaponProfile("deagle", "pistol", 700, "mid", "high", "Force opener"),
    "usp_silencer": WeaponProfile("usp_silencer", "pistol", 200, "close", "low", "CT default"),
    "glock": WeaponProfile("glock", "pistol", 200, "close", "low", "T default"),
    "mac10": WeaponProfile("mac10", "smg", 1050, "close", "low", "T SMG"),
    "mp9": WeaponProfile("mp9", "smg", 1250, "close", "low", "CT SMG"),
    "flashbang": WeaponProfile("flashbang", "grenade", 200, "n/a", "n/a", "Flash"),
    "smokegrenade": WeaponProfile("smokegrenade", "grenade", 300, "n/a", "n/a", "Smoke"),
    "hegrenade": WeaponProfile("hegrenade", "grenade", 300, "n/a", "n/a", "HE"),
    "molotov": WeaponProfile("molotov", "grenade", 400, "n/a", "n/a", "T molly"),
    "incgrenade": WeaponProfile("incgrenade", "grenade", 600, "n/a", "n/a", "CT incendiary"),
}


def profile_for(name: str) -> WeaponProfile:
    canon = canonical_weapon_name(name)
    if canon in _PROFILES:
        return _PROFILES[canon]
    meta = WEAPON_CATALOG[canon]
    return WeaponProfile(
        name=canon,
        slot=str(meta["slot"]),
        cost=int(meta["cost"]),
        typical_range="unknown",
        armor_pen="unknown",
        notes="",
    )


def profiles_for_slot(slot: str) -> list[WeaponProfile]:
    return [profile_for(name) for name, meta in WEAPON_CATALOG.items() if meta["slot"] == slot]


def expensive_weapons(min_cost: int = 3000) -> list[WeaponProfile]:
    return [profile_for(n) for n, m in WEAPON_CATALOG.items() if int(m["cost"]) >= min_cost]
