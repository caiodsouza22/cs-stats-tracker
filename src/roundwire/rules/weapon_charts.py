"""Compact weapon chart table for analytics tooltips."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WeaponChart:
    name: str
    slot: str
    side: str
    base_damage: int
    rpm: int
    armor_pen_unarmored: int
    armor_pen_armored: int
    kill_reward: float
    range_band: str

    def to_dict(self) -> dict[str, object]:
        return {
            'name': self.name,
            'slot': self.slot,
            'side': self.side,
            'base_damage': self.base_damage,
            'rpm': self.rpm,
            'armor_pen_unarmored': self.armor_pen_unarmored,
            'armor_pen_armored': self.armor_pen_armored,
            'kill_reward': self.kill_reward,
            'range_band': self.range_band,
        }


CHARTS: dict[str, WeaponChart] = {
    'ak47': WeaponChart('ak47', 'rifle', 'T', 360, 600, 77, 90, 2.5, 'mid-long'),
    'm4a1': WeaponChart('m4a1', 'rifle', 'CT', 330, 666, 64, 70, 3.1, 'mid-long'),
    'm4a1_silencer': WeaponChart('m4a1_silencer', 'rifle', 'CT', 380, 600, 65, 70, 3.4, 'mid'),
    'awp': WeaponChart('awp', 'sniper', 'BOTH', 1150, 41, 97, 100, 1.5, 'long'),
    'ssg08': WeaponChart('ssg08', 'sniper', 'BOTH', 880, 67, 85, 85, 1.9, 'long'),
    'aug': WeaponChart('aug', 'rifle', 'CT', 330, 666, 63, 70, 3.3, 'long'),
    'sg556': WeaponChart('sg556', 'rifle', 'T', 330, 666, 66, 100, 3.0, 'long'),
    'famas': WeaponChart('famas', 'rifle', 'CT', 300, 666, 57, 70, 3.3, 'mid'),
    'galilar': WeaponChart('galilar', 'rifle', 'T', 300, 666, 60, 77, 3.0, 'mid'),
    'mac10': WeaponChart('mac10', 'smg', 'T', 290, 800, 45, 57, 2.5, 'close'),
    'mp9': WeaponChart('mp9', 'smg', 'CT', 260, 857, 47, 60, 2.4, 'close'),
    'mp7': WeaponChart('mp7', 'smg', 'BOTH', 290, 750, 49, 62, 2.7, 'close'),
    'ump45': WeaponChart('ump45', 'smg', 'BOTH', 350, 666, 52, 64, 2.9, 'close'),
    'p90': WeaponChart('p90', 'smg', 'BOTH', 260, 857, 51, 69, 2.6, 'close'),
    'bizon': WeaponChart('bizon', 'smg', 'BOTH', 270, 750, 40, 50, 2.5, 'close'),
    'nova': WeaponChart('nova', 'shotgun', 'BOTH', 234, 68, 50, 50, 1.2, 'close'),
    'xm1014': WeaponChart('xm1014', 'shotgun', 'BOTH', 200, 171, 50, 50, 1.1, 'close'),
    'mag7': WeaponChart('mag7', 'shotgun', 'CT', 240, 71, 50, 50, 1.2, 'close'),
    'sawedoff': WeaponChart('sawedoff', 'shotgun', 'T', 256, 71, 50, 50, 1.1, 'close'),
    'deagle': WeaponChart('deagle', 'pistol', 'BOTH', 530, 267, 93, 93, 2.2, 'mid'),
    'usp_silencer': WeaponChart('usp_silencer', 'pistol', 'CT', 350, 353, 63, 63, 2.2, 'close'),
    'glock': WeaponChart('glock', 'pistol', 'T', 300, 400, 47, 47, 2.0, 'close'),
    'p250': WeaponChart('p250', 'pistol', 'BOTH', 380, 400, 64, 64, 2.1, 'close'),
    'tec9': WeaponChart('tec9', 'pistol', 'T', 330, 500, 55, 55, 2.0, 'close'),
    'fiveseven': WeaponChart('fiveseven', 'pistol', 'CT', 320, 400, 65, 65, 2.1, 'close'),
    'cz75a': WeaponChart('cz75a', 'pistol', 'BOTH', 310, 600, 60, 60, 2.0, 'close'),
    'elite': WeaponChart('elite', 'pistol', 'BOTH', 380, 500, 52, 52, 2.0, 'close'),
    'revolver': WeaponChart('revolver', 'pistol', 'BOTH', 860, 120, 93, 93, 2.3, 'mid'),
    'hegrenade': WeaponChart('hegrenade', 'grenade', 'BOTH', 98, 0, 0, 0, 0, 'n/a'),
    'flashbang': WeaponChart('flashbang', 'grenade', 'BOTH', 0, 0, 0, 0, 0, 'n/a'),
    'smokegrenade': WeaponChart('smokegrenade', 'grenade', 'BOTH', 0, 0, 0, 0, 0, 'n/a'),
    'molotov': WeaponChart('molotov', 'grenade', 'T', 40, 0, 0, 0, 0, 'n/a'),
    'incgrenade': WeaponChart('incgrenade', 'grenade', 'CT', 40, 0, 0, 0, 0, 'n/a'),
}


def chart(name: str) -> WeaponChart | None:
    return CHARTS.get(name)


def charts_for_slot(slot: str) -> list[WeaponChart]:
    return [c for c in CHARTS.values() if c.slot == slot]


def chart_table() -> list[dict[str, object]]:
    return [c.to_dict() for c in sorted(CHARTS.values(), key=lambda x: (x.slot, x.name))]
