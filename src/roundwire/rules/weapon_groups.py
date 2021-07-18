"""Grouped weapon lists for filters and reports."""

from __future__ import annotations

from roundwire.rules.weapon_aliases import WEAPON_CATALOG, weapons_in_slot

RIFLES = tuple(weapons_in_slot("rifle"))
SNIPERS = tuple(weapons_in_slot("sniper"))
SMGS = tuple(weapons_in_slot("smg"))
SHOTGUNS = tuple(weapons_in_slot("shotgun"))
LMGS = tuple(weapons_in_slot("lmg"))
PISTOLS = tuple(weapons_in_slot("pistol"))
GRENADES = tuple(weapons_in_slot("grenade"))

CT_STARTING = ("usp_silencer", "hkp2000")
T_STARTING = ("glock",)
CT_RIFLES = ("m4a1", "m4a1_silencer", "famas", "aug")
T_RIFLES = ("ak47", "galilar", "sg556")


def group_for(canonical: str) -> str:
    meta = WEAPON_CATALOG.get(canonical)
    if meta is None:
        return "unknown"
    return str(meta["slot"])


def starting_pistols(side: str) -> tuple[str, ...]:
    return CT_STARTING if side.upper() == "CT" else T_STARTING


def side_rifles(side: str) -> tuple[str, ...]:
    return CT_RIFLES if side.upper() == "CT" else T_RIFLES


def all_groups() -> dict[str, tuple[str, ...]]:
    return {
        "rifle": RIFLES,
        "sniper": SNIPERS,
        "smg": SMGS,
        "shotgun": SHOTGUNS,
        "lmg": LMGS,
        "pistol": PISTOLS,
        "grenade": GRENADES,
    }
