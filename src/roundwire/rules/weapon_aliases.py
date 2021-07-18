"""Weapon catalog with CS:GO / CS2 name aliases and costs."""

from __future__ import annotations

from roundwire.errors.messages import unknown_weapon

# canonical CS2-ish name -> metadata
WEAPON_CATALOG: dict[str, dict[str, object]] = {
    "ak47": {"cost": 2700, "slot": "rifle", "aliases": ["weapon_ak47", "ak-47", "ak"]},
    "m4a1": {"cost": 3100, "slot": "rifle", "aliases": ["weapon_m4a1", "m4a4"]},
    "m4a1_silencer": {"cost": 2900, "slot": "rifle", "aliases": ["weapon_m4a1_silencer", "m4a1-s", "m4s"]},
    "awp": {"cost": 4750, "slot": "sniper", "aliases": ["weapon_awp"]},
    "ssg08": {"cost": 1700, "slot": "sniper", "aliases": ["weapon_ssg08", "scout"]},
    "aug": {"cost": 3300, "slot": "rifle", "aliases": ["weapon_aug"]},
    "sg556": {"cost": 3000, "slot": "rifle", "aliases": ["weapon_sg556", "sg553", "krieg"]},
    "famas": {"cost": 2050, "slot": "rifle", "aliases": ["weapon_famas"]},
    "galilar": {"cost": 1800, "slot": "rifle", "aliases": ["weapon_galilar", "galil"]},
    "mp9": {"cost": 1250, "slot": "smg", "aliases": ["weapon_mp9"]},
    "mac10": {"cost": 1050, "slot": "smg", "aliases": ["weapon_mac10"]},
    "mp7": {"cost": 1500, "slot": "smg", "aliases": ["weapon_mp7"]},
    "ump45": {"cost": 1200, "slot": "smg", "aliases": ["weapon_ump45", "ump"]},
    "p90": {"cost": 2350, "slot": "smg", "aliases": ["weapon_p90"]},
    "bizon": {"cost": 1400, "slot": "smg", "aliases": ["weapon_bizon", "ppbizon"]},
    "nova": {"cost": 1050, "slot": "shotgun", "aliases": ["weapon_nova"]},
    "xm1014": {"cost": 2000, "slot": "shotgun", "aliases": ["weapon_xm1014"]},
    "mag7": {"cost": 1300, "slot": "shotgun", "aliases": ["weapon_mag7"]},
    "sawedoff": {"cost": 1100, "slot": "shotgun", "aliases": ["weapon_sawedoff"]},
    "m249": {"cost": 5200, "slot": "lmg", "aliases": ["weapon_m249"]},
    "negev": {"cost": 1700, "slot": "lmg", "aliases": ["weapon_negev"]},
    "deagle": {"cost": 700, "slot": "pistol", "aliases": ["weapon_deagle", "desert_eagle"]},
    "usp_silencer": {"cost": 200, "slot": "pistol", "aliases": ["weapon_usp_silencer", "usp", "usp-s"]},
    "glock": {"cost": 200, "slot": "pistol", "aliases": ["weapon_glock", "glock18"]},
    "p250": {"cost": 300, "slot": "pistol", "aliases": ["weapon_p250"]},
    "fiveseven": {"cost": 500, "slot": "pistol", "aliases": ["weapon_fiveseven", "five_seven", "ck75"]},
    "tec9": {"cost": 500, "slot": "pistol", "aliases": ["weapon_tec9"]},
    "cz75a": {"cost": 500, "slot": "pistol", "aliases": ["weapon_cz75a", "cz75", "cz"]},
    "elite": {"cost": 400, "slot": "pistol", "aliases": ["weapon_elite", "dualies", "dual_berettas"]},
    "revolver": {"cost": 600, "slot": "pistol", "aliases": ["weapon_revolver", "r8"]},
    "hkp2000": {"cost": 200, "slot": "pistol", "aliases": ["weapon_hkp2000", "p2000"]},
    "knife": {"cost": 0, "slot": "melee", "aliases": ["weapon_knife", "weapon_knife_t"]},
    "hegrenade": {"cost": 300, "slot": "grenade", "aliases": ["weapon_hegrenade", "he"]},
    "flashbang": {"cost": 200, "slot": "grenade", "aliases": ["weapon_flashbang", "flash"]},
    "smokegrenade": {"cost": 300, "slot": "grenade", "aliases": ["weapon_smokegrenade", "smoke"]},
    "molotov": {"cost": 400, "slot": "grenade", "aliases": ["weapon_molotov"]},
    "incgrenade": {"cost": 600, "slot": "grenade", "aliases": ["weapon_incgrenade", "incendiary"]},
    "decoy": {"cost": 50, "slot": "grenade", "aliases": ["weapon_decoy"]},
    "c4": {"cost": 0, "slot": "other", "aliases": ["weapon_c4", "bomb"]},
    "taser": {"cost": 200, "slot": "other", "aliases": ["weapon_taser", "zeus"]},
}

_ALIAS_TO_CANONICAL: dict[str, str] = {}
for canon, meta in WEAPON_CATALOG.items():
    _ALIAS_TO_CANONICAL[canon] = canon
    aliases = meta.get("aliases", [])
    if isinstance(aliases, list):
        for alias in aliases:
            raw = str(alias).lower()
            _ALIAS_TO_CANONICAL[raw] = canon
            _ALIAS_TO_CANONICAL[raw.replace("-", "_").replace(" ", "_")] = canon
            _ALIAS_TO_CANONICAL[raw.replace("-", "").replace("_", "").replace(" ", "")] = canon


def _norm(name: str) -> str:
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def canonical_weapon_name(name: str) -> str:
    key = _norm(name)
    compact = key.replace("_", "")
    for candidate in (key, compact, name.strip().lower()):
        if candidate in _ALIAS_TO_CANONICAL:
            return _ALIAS_TO_CANONICAL[candidate]
    if key.startswith("weapon_"):
        stripped = key[len("weapon_") :]
        for candidate in (stripped, stripped.replace("_", "")):
            if candidate in _ALIAS_TO_CANONICAL:
                return _ALIAS_TO_CANONICAL[candidate]
    raise KeyError(unknown_weapon(name))


def weapon_cost(canonical: str) -> int:
    meta = WEAPON_CATALOG.get(canonical)
    if meta is None:
        raise KeyError(unknown_weapon(canonical))
    return int(meta["cost"])


def weapon_slot(canonical: str) -> str:
    meta = WEAPON_CATALOG.get(canonical)
    if meta is None:
        raise KeyError(unknown_weapon(canonical))
    return str(meta["slot"])


def all_canonical_weapons() -> list[str]:
    return sorted(WEAPON_CATALOG)


def resolve_alias(name: str) -> str | None:
    try:
        return canonical_weapon_name(name)
    except KeyError:
        return None


def csgo_to_cs2_name(name: str) -> str:
    """Map a CS:GO-era weapon string to a canonical CS2 catalog name."""
    return canonical_weapon_name(name)

def weapons_in_slot(slot: str) -> list[str]:
    return sorted(
        name for name, meta in WEAPON_CATALOG.items() if str(meta.get("slot")) == slot
    )


def is_rifle(name: str) -> bool:
    try:
        return weapon_slot(canonical_weapon_name(name)) == "rifle"
    except KeyError:
        return False


def is_pistol(name: str) -> bool:
    try:
        return weapon_slot(canonical_weapon_name(name)) == "pistol"
    except KeyError:
        return False


def is_grenade(name: str) -> bool:
    try:
        return weapon_slot(canonical_weapon_name(name)) == "grenade"
    except KeyError:
        return False


def catalog_size() -> int:
    return len(WEAPON_CATALOG)


def alias_count() -> int:
    return len(_ALIAS_TO_CANONICAL)


CSGO_LEGACY_PREFIXES = ("weapon_",)

SPECIAL_CASES = {
    "ck75": "fiveseven",
    "five-seven": "fiveseven",
    "usp-s": "usp_silencer",
    "m4a1-s": "m4a1_silencer",
}


def normalize_raw_weapon(name: str) -> str:
    key = name.strip().lower().replace(" ", "_")
    if key in SPECIAL_CASES:
        return SPECIAL_CASES[key]
    return key


def try_canonical(name: str) -> str:
    try:
        return canonical_weapon_name(normalize_raw_weapon(name))
    except KeyError:
        return normalize_raw_weapon(name)
