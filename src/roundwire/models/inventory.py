"""Per-player round start inventory snapshot."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.models.weapon import Weapon
from roundwire.types import PlayerId


@dataclass(slots=True)
class InventorySnapshot:
    player_id: PlayerId
    cash: int
    equipment_value: int
    primary: Weapon | None = None
    secondary: Weapon | None = None
    armor: bool = False
    helmet: bool = False
    defuse_kit: bool = False
    grenades: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "player_id": str(self.player_id),
            "cash": self.cash,
            "equipment_value": self.equipment_value,
            "armor": self.armor,
            "helmet": self.helmet,
            "defuse_kit": self.defuse_kit,
            "grenades": list(self.grenades),
        }
        if self.primary is not None:
            payload["primary"] = self.primary.to_dict()
        if self.secondary is not None:
            payload["secondary"] = self.secondary.to_dict()
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> InventorySnapshot:
        primary_raw = data.get("primary")
        secondary_raw = data.get("secondary")
        grenades_raw = data.get("grenades", [])
        grenades = [str(g) for g in grenades_raw] if isinstance(grenades_raw, list) else []
        return cls(
            player_id=PlayerId(str(data["player_id"])),
            cash=int(data["cash"]),
            equipment_value=int(data["equipment_value"]),
            primary=Weapon.from_dict(primary_raw) if isinstance(primary_raw, dict) else None,
            secondary=Weapon.from_dict(secondary_raw) if isinstance(secondary_raw, dict) else None,
            armor=bool(data.get("armor", False)),
            helmet=bool(data.get("helmet", False)),
            defuse_kit=bool(data.get("defuse_kit", False)),
            grenades=grenades,
        )
