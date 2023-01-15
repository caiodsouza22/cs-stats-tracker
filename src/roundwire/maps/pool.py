"""Active and legacy map pool names."""

from __future__ import annotations

ACTIVE_POOL = (
    "de_mirage",
    "de_inferno",
    "de_nuke",
    "de_overpass",
    "de_vertigo",
    "de_ancient",
    "de_anubis",
)

LEGACY_POOL = (
    "de_dust2",
    "de_train",
    "de_cache",
    "de_cobblestone",
    "de_tuscan",
)

ALIASES = {
    "mirage": "de_mirage",
    "inferno": "de_inferno",
    "nuke": "de_nuke",
    "overpass": "de_overpass",
    "vertigo": "de_vertigo",
    "ancient": "de_ancient",
    "anubis": "de_anubis",
    "dust2": "de_dust2",
    "dust_2": "de_dust2",
    "d2": "de_dust2",
    "train": "de_train",
    "cache": "de_cache",
    "cbble": "de_cobblestone",
    "cobblestone": "de_cobblestone",
}


def normalize_map_name(name: str) -> str:
    key = name.strip().lower().replace(" ", "_").replace("-", "_")
    if key in ALIASES:
        return ALIASES[key]
    if not key.startswith("de_"):
        candidate = f"de_{key}"
        if candidate in ACTIVE_POOL or candidate in LEGACY_POOL:
            return candidate
    return key


def is_active_pool(name: str) -> bool:
    return normalize_map_name(name) in ACTIVE_POOL
