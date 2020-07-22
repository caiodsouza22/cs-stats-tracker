"""Weapon identity and catalog lookups."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.rules.weapon_aliases import canonical_weapon_name, weapon_cost, weapon_slot


@dataclass(frozen=True, slots=True)
class Weapon:
    """A weapon reference used on kills, buys, and inventories."""

    name: str

    def canonical(self) -> str:
        return canonical_weapon_name(self.name)

    @property
    def cost(self) -> int:
        return weapon_cost(self.canonical())

    @property
    def slot(self) -> str:
        return weapon_slot(self.canonical())

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Weapon:
        name = str(data.get("name", ""))
        if not name:
            raise ValueError("weapon missing name")
        return cls(name=name)
