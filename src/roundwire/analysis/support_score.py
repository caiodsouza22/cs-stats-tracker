"""Support / flash impact scoring beyond raw utility counts."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.players.utility_profile import build_utility_profile, support_index
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class SupportCard:
    player_id: str
    name: str
    team: str
    support_index: float
    flash_value: float
    smoke_value: float
    damage_util: float
    spend: int
    efficiency: float

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "team": self.team,
            "support_index": round(self.support_index, 3),
            "flash_value": round(self.flash_value, 3),
            "smoke_value": round(self.smoke_value, 3),
            "damage_util": round(self.damage_util, 1),
            "spend": self.spend,
            "efficiency": round(self.efficiency, 3),
        }


def support_card(match: Match, player_id: PlayerId) -> SupportCard:
    player = match.player_map()[player_id]
    util = build_utility_profile(match, player_id)
    flash_value = util.enemies_flashed * 1.0 - util.teammates_flashed * 0.5
    smoke_value = util.smokes * 1.25 + util.early_util * 0.15
    damage_util = float(util.he_damage + util.fire_damage)
    efficiency = safe_div(flash_value * 20 + damage_util, float(max(1, util.spend)))
    return SupportCard(
        player_id=str(player_id),
        name=player.name,
        team=player.team.value,
        support_index=support_index(match, player_id),
        flash_value=flash_value,
        smoke_value=smoke_value,
        damage_util=damage_util,
        spend=util.spend,
        efficiency=efficiency,
    )


def support_table(match: Match) -> list[dict[str, object]]:
    rows = [support_card(match, p.player_id).to_dict() for p in match.players]
    return sorted(rows, key=lambda r: (-r["support_index"], r["name"]))


def best_support(match: Match) -> SupportCard | None:
    cards = [support_card(match, p.player_id) for p in match.players]
    if not cards:
        return None
    return max(cards, key=lambda c: (c.support_index, c.efficiency, c.name))
