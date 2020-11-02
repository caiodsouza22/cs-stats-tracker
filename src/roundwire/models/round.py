"""Single round within a match."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.models.damage import DamageEvent
from roundwire.models.inventory import InventorySnapshot
from roundwire.models.kill import Kill
from roundwire.models.team import TeamSide
from roundwire.models.utility_event import UtilityEvent
from roundwire.types import PlayerId, RoundNumber


@dataclass(slots=True)
class Round:
    number: RoundNumber
    winner: TeamSide
    win_reason: str
    bomb_planted: bool = False
    inventories: list[InventorySnapshot] = field(default_factory=list)
    kills: list[Kill] = field(default_factory=list)
    damage: list[DamageEvent] = field(default_factory=list)
    utility: list[UtilityEvent] = field(default_factory=list)
    survivors: list[PlayerId] = field(default_factory=list)
    duration_ms: int = 0

    def kills_for(self, player_id: PlayerId) -> list[Kill]:
        return [k for k in self.kills if k.killer_id == player_id]

    def deaths_for(self, player_id: PlayerId) -> list[Kill]:
        return [k for k in self.kills if k.victim_id == player_id]

    def damage_dealt_by(self, player_id: PlayerId) -> int:
        return sum(d.damage for d in self.damage if d.attacker_id == player_id)

    def to_dict(self) -> dict[str, object]:
        return {
            "number": int(self.number),
            "winner": self.winner.value,
            "win_reason": self.win_reason,
            "bomb_planted": self.bomb_planted,
            "inventories": [inv.to_dict() for inv in self.inventories],
            "kills": [k.to_dict() for k in self.kills],
            "damage": [d.to_dict() for d in self.damage],
            "utility": [u.to_dict() for u in self.utility],
            "survivors": [str(s) for s in self.survivors],
            "duration_ms": self.duration_ms,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Round:
        inv_raw = data.get("inventories", [])
        kills_raw = data.get("kills", [])
        dmg_raw = data.get("damage", [])
        util_raw = data.get("utility", [])
        surv_raw = data.get("survivors", [])
        if not all(isinstance(x, list) for x in (inv_raw, kills_raw, dmg_raw, util_raw, surv_raw)):
            raise ValueError("round event lists must be arrays")
        assert isinstance(inv_raw, list)
        assert isinstance(kills_raw, list)
        assert isinstance(dmg_raw, list)
        assert isinstance(util_raw, list)
        assert isinstance(surv_raw, list)
        return cls(
            number=RoundNumber(int(data["number"])),
            winner=TeamSide.parse(str(data["winner"])),
            win_reason=str(data.get("win_reason", "elimination")),
            bomb_planted=bool(data.get("bomb_planted", False)),
            inventories=[
                InventorySnapshot.from_dict(x) for x in inv_raw if isinstance(x, dict)
            ],
            kills=[Kill.from_dict(x) for x in kills_raw if isinstance(x, dict)],
            damage=[DamageEvent.from_dict(x) for x in dmg_raw if isinstance(x, dict)],
            utility=[UtilityEvent.from_dict(x) for x in util_raw if isinstance(x, dict)],
            survivors=[PlayerId(str(s)) for s in surv_raw],
            duration_ms=int(data.get("duration_ms", 0)),
        )
