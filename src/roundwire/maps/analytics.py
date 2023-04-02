"""Map analytics combining side preference and control proxies."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.maps.control import ct_hold_without_plant, plant_rate, post_plant_wins, site_mention_share
from roundwire.maps.pool import is_active_pool, normalize_map_name
from roundwire.maps.side_pref import side_preference_label, side_winrate
from roundwire.models.match import Match
from roundwire.models.team import TeamSide


@dataclass(frozen=True, slots=True)
class MapCard:
    map_name: str
    active_pool: bool
    ct_winrate: float
    t_winrate: float
    preference: str
    plant_rate: float
    post_plant_t_winrate: float
    ct_hold_no_plant: float
    site_share: dict[str, float]


def map_card(match: Match) -> MapCard:
    name = normalize_map_name(match.map_name)
    return MapCard(
        map_name=name,
        active_pool=is_active_pool(name),
        ct_winrate=side_winrate(match, TeamSide.CT),
        t_winrate=side_winrate(match, TeamSide.T),
        preference=side_preference_label(match),
        plant_rate=plant_rate(match),
        post_plant_t_winrate=post_plant_wins(match),
        ct_hold_no_plant=ct_hold_without_plant(match),
        site_share=site_mention_share(match),
    )


def format_map_card(card: MapCard) -> str:
    return (
        f"{card.map_name} [{'active' if card.active_pool else 'legacy'}] "
        f"CT {card.ct_winrate*100:.0f}% / T {card.t_winrate*100:.0f}% "
        f"pref={card.preference} plants={card.plant_rate*100:.0f}% "
        f"post-plant T WR={card.post_plant_t_winrate*100:.0f}%"
    )
