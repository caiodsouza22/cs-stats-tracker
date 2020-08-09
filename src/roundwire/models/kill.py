"""Kill event model."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.weapon import Weapon
from roundwire.types import Milliseconds, PlayerId


@dataclass(frozen=True, slots=True)
class Kill:
    killer_id: PlayerId
    victim_id: PlayerId
    weapon: Weapon
    tick_ms: Milliseconds
    headshot: bool = False
    wallbang: bool = False
    noscope: bool = False
    through_smoke: bool = False
    assisted_by: PlayerId | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "killer_id": str(self.killer_id),
            "victim_id": str(self.victim_id),
            "weapon": self.weapon.to_dict(),
            "tick_ms": int(self.tick_ms),
            "headshot": self.headshot,
            "wallbang": self.wallbang,
            "noscope": self.noscope,
            "through_smoke": self.through_smoke,
        }
        if self.assisted_by is not None:
            payload["assisted_by"] = str(self.assisted_by)
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Kill:
        weapon_raw = data.get("weapon", {})
        if not isinstance(weapon_raw, dict):
            raise ValueError("kill.weapon must be an object")
        assisted = data.get("assisted_by")
        return cls(
            killer_id=PlayerId(str(data["killer_id"])),
            victim_id=PlayerId(str(data["victim_id"])),
            weapon=Weapon.from_dict(weapon_raw),
            tick_ms=Milliseconds(int(data["tick_ms"])),
            headshot=bool(data.get("headshot", False)),
            wallbang=bool(data.get("wallbang", False)),
            noscope=bool(data.get("noscope", False)),
            through_smoke=bool(data.get("through_smoke", False)),
            assisted_by=PlayerId(str(assisted)) if assisted else None,
        )
