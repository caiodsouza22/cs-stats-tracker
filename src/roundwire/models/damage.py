"""Damage event model."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.weapon import Weapon
from roundwire.types import Milliseconds, PlayerId


@dataclass(frozen=True, slots=True)
class DamageEvent:
    attacker_id: PlayerId
    victim_id: PlayerId
    weapon: Weapon
    damage: int
    tick_ms: Milliseconds
    hitgroup: str = "generic"
    armor_damage: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "attacker_id": str(self.attacker_id),
            "victim_id": str(self.victim_id),
            "weapon": self.weapon.to_dict(),
            "damage": self.damage,
            "tick_ms": int(self.tick_ms),
            "hitgroup": self.hitgroup,
            "armor_damage": self.armor_damage,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> DamageEvent:
        weapon_raw = data.get("weapon", {})
        if not isinstance(weapon_raw, dict):
            raise ValueError("damage.weapon must be an object")
        return cls(
            attacker_id=PlayerId(str(data["attacker_id"])),
            victim_id=PlayerId(str(data["victim_id"])),
            weapon=Weapon.from_dict(weapon_raw),
            damage=int(data["damage"]),
            tick_ms=Milliseconds(int(data["tick_ms"])),
            hitgroup=str(data.get("hitgroup", "generic")),
            armor_damage=int(data.get("armor_damage", 0)),
        )
