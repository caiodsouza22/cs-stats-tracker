"""Advanced utility effectiveness metrics."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.types import PlayerId
from roundwire.utility.cost import utility_spend
from roundwire.utility.flashes import enemies_flashed_total, flash_efficiency
from roundwire.utility.he import he_damage, he_throws
from roundwire.utility.molotov import fire_damage, fire_throws
from roundwire.utility.smoke import smoke_count
from roundwire.utility.usage import utility_counts


@dataclass(frozen=True, slots=True)
class UtilityCard:
    player_id: str
    name: str
    counts: dict[str, int]
    enemies_flashed: int
    flash_eff: float
    he_damage: int
    fire_damage: int
    spend: int
    value_score: float


def utility_value_score(match: Match, player_id: PlayerId) -> float:
    """Rough value: enemies flashed + HE/fire damage per 1000 spend."""
    spend = max(1, utility_spend(match, player_id))
    value = (
        enemies_flashed_total(match, player_id) * 20
        + he_damage(match, player_id)
        + fire_damage(match, player_id)
    )
    return value / spend * 1000.0


def utility_card(match: Match, player_id: PlayerId) -> UtilityCard:
    player = match.player_map()[player_id]
    return UtilityCard(
        player_id=str(player_id),
        name=player.name,
        counts=utility_counts(match, player_id),
        enemies_flashed=enemies_flashed_total(match, player_id),
        flash_eff=flash_efficiency(match, player_id),
        he_damage=he_damage(match, player_id),
        fire_damage=fire_damage(match, player_id),
        spend=utility_spend(match, player_id),
        value_score=utility_value_score(match, player_id),
    )


def utility_cards(match: Match) -> list[UtilityCard]:
    cards = [utility_card(match, p.player_id) for p in match.players]
    return sorted(cards, key=lambda c: (-c.value_score, c.name))


def team_utility_spend(match: Match) -> dict[str, int]:
    out = {"CT": 0, "T": 0}
    for player in match.players:
        out[player.team.value] += utility_spend(match, player.player_id)
    return out


def utility_volume(match: Match) -> dict[str, int]:
    totals = {"flash": 0, "smoke": 0, "he": 0, "fire": 0}
    for player in match.players:
        totals["flash"] += utility_counts(match, player.player_id).get("flash", 0)
        totals["smoke"] += smoke_count(match, player.player_id)
        totals["he"] += he_throws(match, player.player_id)
        totals["fire"] += fire_throws(match, player.player_id)
    return totals
