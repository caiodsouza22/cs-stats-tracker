"""Player identity within a match."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.models.team import TeamSide
from roundwire.types import PlayerId, SteamId


@dataclass(slots=True)
class Player:
    player_id: PlayerId
    name: str
    team: TeamSide
    steam_id: SteamId | None = None
    country: str | None = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "player_id": str(self.player_id),
            "name": self.name,
            "team": self.team.value,
        }
        if self.steam_id is not None:
            payload["steam_id"] = str(self.steam_id)
        if self.country is not None:
            payload["country"] = self.country
        if self.tags:
            payload["tags"] = list(self.tags)
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Player:
        steam_raw = data.get("steam_id")
        tags_raw = data.get("tags", [])
        tags: list[str] = [str(t) for t in tags_raw] if isinstance(tags_raw, list) else []
        return cls(
            player_id=PlayerId(str(data["player_id"])),
            name=str(data["name"]),
            team=TeamSide.parse(str(data["team"])),
            steam_id=SteamId(str(steam_raw)) if steam_raw else None,
            country=str(data["country"]) if data.get("country") else None,
            tags=tags,
        )
