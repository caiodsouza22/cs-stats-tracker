"""Utility throw / detonation events."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from roundwire.types import Milliseconds, PlayerId


class UtilityKind(str, Enum):
    FLASH = "flash"
    SMOKE = "smoke"
    HE = "he"
    MOLOTOV = "molotov"
    INCENDIARY = "incendiary"
    DECOY = "decoy"


@dataclass(frozen=True, slots=True)
class UtilityEvent:
    thrower_id: PlayerId
    kind: UtilityKind
    tick_ms: Milliseconds
    enemies_flashed: int = 0
    teammates_flashed: int = 0
    damage_dealt: int = 0
    tags: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "thrower_id": str(self.thrower_id),
            "kind": self.kind.value,
            "tick_ms": int(self.tick_ms),
            "enemies_flashed": self.enemies_flashed,
            "teammates_flashed": self.teammates_flashed,
            "damage_dealt": self.damage_dealt,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> UtilityEvent:
        tags_raw = data.get("tags", [])
        tags = tuple(str(t) for t in tags_raw) if isinstance(tags_raw, list) else ()
        return cls(
            thrower_id=PlayerId(str(data["thrower_id"])),
            kind=UtilityKind(str(data["kind"])),
            tick_ms=Milliseconds(int(data["tick_ms"])),
            enemies_flashed=int(data.get("enemies_flashed", 0)),
            teammates_flashed=int(data.get("teammates_flashed", 0)),
            damage_dealt=int(data.get("damage_dealt", 0)),
            tags=tags,
        )
