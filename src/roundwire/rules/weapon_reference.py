"""Extended weapon reference tables for analytics and docs."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WeaponRef:
    name: str
    side: str
    slot: str
    cost: int
    magazine: int
    kill_award_hint: int
    armor_pen: str
    blurb: str
    range_band: str
    common: bool


WEAPON_REFS: dict[str, WeaponRef] = {
    'ak47': WeaponRef('ak47', 'T', 'rifle', 2700, 30, 90, 'high', 'iconic T rifle', 'mid-long', True),
    'm4a1': WeaponRef('m4a1', 'CT', 'rifle', 3100, 30, 90, 'medium', 'unsilenced CT rifle', 'mid-long', True),
    'm4a1_silencer': WeaponRef('m4a1_silencer', 'CT', 'rifle', 2900, 25, 90, 'medium', 'silenced CT rifle', 'mid', True),
    'aug': WeaponRef('aug', 'CT', 'rifle', 3300, 30, 90, 'medium', 'scoped CT rifle', 'long', True),
    'sg556': WeaponRef('sg556', 'T', 'rifle', 3000, 30, 90, 'high', 'scoped T rifle', 'long', True),
    'famas': WeaponRef('famas', 'CT', 'rifle', 2050, 25, 90, 'medium', 'CT budget rifle', 'mid', False),
    'galilar': WeaponRef('galilar', 'T', 'rifle', 1800, 35, 90, 'high', 'T budget rifle', 'mid', False),
    'awp': WeaponRef('awp', 'BOTH', 'sniper', 4750, 10, 100, 'extreme', 'magnum sniper', 'long', True),
    'ssg08': WeaponRef('ssg08', 'BOTH', 'sniper', 1700, 10, 100, 'high', 'scout', 'long', False),
    'scar20': WeaponRef('scar20', 'CT', 'sniper', 5000, 20, 100, 'extreme', 'CT autosniper', 'long', False),
    'g3sg1': WeaponRef('g3sg1', 'T', 'sniper', 5000, 20, 100, 'extreme', 'T autosniper', 'long', False),
    'mp9': WeaponRef('mp9', 'CT', 'smg', 1250, 30, 90, 'low', 'CT SMG', 'close', False),
    'mac10': WeaponRef('mac10', 'T', 'smg', 1050, 30, 90, 'low', 'T SMG', 'close', False),
    'mp7': WeaponRef('mp7', 'BOTH', 'smg', 1500, 30, 90, 'low', 'accurate SMG', 'close-mid', False),
    'mp5sd': WeaponRef('mp5sd', 'BOTH', 'smg', 1500, 30, 90, 'low', 'silenced SMG', 'close', False),
    'ump45': WeaponRef('ump45', 'BOTH', 'smg', 1200, 25, 90, 'medium', 'UMP', 'close-mid', False),
    'p90': WeaponRef('p90', 'BOTH', 'smg', 2350, 50, 90, 'medium', 'P90', 'close', False),
    'bizon': WeaponRef('bizon', 'BOTH', 'smg', 1400, 64, 90, 'low', 'high capacity SMG', 'close', False),
    'nova': WeaponRef('nova', 'BOTH', 'shotgun', 1050, 8, 90, 'low', 'pump shotgun', 'close', False),
    'xm1014': WeaponRef('xm1014', 'BOTH', 'shotgun', 2000, 7, 90, 'low', 'auto shotgun', 'close', False),
    'mag7': WeaponRef('mag7', 'CT', 'shotgun', 1300, 5, 90, 'low', 'CT tube shotgun', 'close', False),
    'sawedoff': WeaponRef('sawedoff', 'T', 'shotgun', 1100, 7, 90, 'low', 'T shotgun', 'close', False),
    'm249': WeaponRef('m249', 'BOTH', 'lmg', 5200, 100, 90, 'high', 'LMG', 'mid', False),
    'negev': WeaponRef('negev', 'BOTH', 'lmg', 1700, 150, 90, 'high', 'Negev', 'mid', False),
    'deagle': WeaponRef('deagle', 'BOTH', 'pistol', 700, 7, 90, 'high', 'Desert Eagle', 'mid', True),
    'revolver': WeaponRef('revolver', 'BOTH', 'pistol', 600, 8, 90, 'high', 'R8 Revolver', 'mid', False),
    'usp_silencer': WeaponRef('usp_silencer', 'CT', 'pistol', 200, 12, 90, 'low', 'USP-S', 'close', True),
    'hkp2000': WeaponRef('hkp2000', 'CT', 'pistol', 200, 13, 90, 'low', 'P2000', 'close', True),
    'glock': WeaponRef('glock', 'T', 'pistol', 200, 20, 90, 'low', 'Glock-18', 'close', True),
    'p250': WeaponRef('p250', 'BOTH', 'pistol', 300, 13, 90, 'medium', 'P250', 'close-mid', False),
    'fiveseven': WeaponRef('fiveseven', 'CT', 'pistol', 500, 20, 90, 'medium', 'Five-SeveN', 'close-mid', False),
    'tec9': WeaponRef('tec9', 'T', 'pistol', 500, 18, 90, 'medium', 'Tec-9', 'close', False),
    'cz75a': WeaponRef('cz75a', 'BOTH', 'pistol', 500, 12, 90, 'medium', 'CZ75-Auto', 'close', False),
    'elite': WeaponRef('elite', 'BOTH', 'pistol', 400, 30, 90, 'low', 'Dual Berettas', 'close', False),
    'flashbang': WeaponRef('flashbang', 'BOTH', 'grenade', 200, 1, 0, 'n/a', 'Flashbang', 'n/a', True),
    'smokegrenade': WeaponRef('smokegrenade', 'BOTH', 'grenade', 300, 1, 0, 'n/a', 'Smoke', 'n/a', True),
    'hegrenade': WeaponRef('hegrenade', 'BOTH', 'grenade', 300, 1, 0, 'n/a', 'HE', 'n/a', True),
    'molotov': WeaponRef('molotov', 'T', 'grenade', 400, 1, 0, 'n/a', 'Molotov', 'n/a', True),
    'incgrenade': WeaponRef('incgrenade', 'CT', 'grenade', 600, 1, 0, 'n/a', 'Incendiary', 'n/a', True),
    'decoy': WeaponRef('decoy', 'BOTH', 'grenade', 50, 1, 0, 'n/a', 'Decoy', 'n/a', False),
    'knife': WeaponRef('knife', 'BOTH', 'melee', 0, 1, 0, 'n/a', 'Knife', 'close', True),
    'taser': WeaponRef('taser', 'BOTH', 'other', 200, 1, 0, 'n/a', 'Zeus x27', 'close', False),
    'c4': WeaponRef('c4', 'T', 'other', 0, 1, 0, 'n/a', 'Bomb', 'n/a', True),
}


def get_ref(name: str) -> WeaponRef | None:
    return WEAPON_REFS.get(name)


def refs_for_side(side: str) -> list[WeaponRef]:
    key = side.upper()
    return [r for r in WEAPON_REFS.values() if r.side in {key, 'BOTH'}]


def refs_for_slot(slot: str) -> list[WeaponRef]:
    return [r for r in WEAPON_REFS.values() if r.slot == slot]


def common_refs() -> list[WeaponRef]:
    return [r for r in WEAPON_REFS.values() if r.common]


def budget_weapons(max_cost: int, slot: str | None = None) -> list[WeaponRef]:
    out = [r for r in WEAPON_REFS.values() if r.cost <= max_cost and r.cost > 0]
    if slot is not None:
        out = [r for r in out if r.slot == slot]
    return sorted(out, key=lambda r: (r.cost, r.name))


def full_buy_primaries(side: str) -> list[WeaponRef]:
    rifles = refs_for_slot('rifle')
    snipers = refs_for_slot('sniper')
    pool = rifles + snipers
    key = side.upper()
    return [r for r in pool if r.side in {key, 'BOTH'} and r.cost >= 2700]


def force_buy_options(side: str) -> list[WeaponRef]:
    key = side.upper()
    return [
        r for r in WEAPON_REFS.values()
        if r.side in {key, 'BOTH'} and r.slot in {'smg', 'shotgun', 'pistol'} and 300 <= r.cost <= 2000
    ]


def describe_weapon(name: str) -> str:
    ref = get_ref(name)
    if ref is None:
        return f'unknown weapon {name!r}'
    return (
        f'{ref.name} ({ref.slot}, {ref.side}) cost={ref.cost} '
        f'mag={ref.magazine} pen={ref.armor_pen} range={ref.range_band}: {ref.blurb}'
    )

def reference_index() -> list[str]:
    return sorted(WEAPON_REFS)


def note(name: str) -> str:
    ref = WEAPON_REFS[name]
    return (
        f'Reference note for {ref.name}: side={ref.side}, slot={ref.slot}, '
        f'cost={ref.cost}, common={ref.common}. {ref.blurb} '
        f'(range={ref.range_band}, pen={ref.armor_pen}).'
    )


def all_notes() -> dict[str, str]:
    return {name: note(name) for name in WEAPON_REFS}

