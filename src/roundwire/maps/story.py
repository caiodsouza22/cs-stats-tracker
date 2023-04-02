"""Map control story combining plants, utility tags, and side winrates."""

from __future__ import annotations

from roundwire.maps.analytics import format_map_card, map_card
from roundwire.maps.control import ct_hold_without_plant, plant_rate, post_plant_wins, site_mention_share
from roundwire.maps.guides import narrative, sites
from roundwire.maps.side_pref import side_preference_label, side_winrate
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.players.callouts import team_tag_heatmap
from roundwire.utility.timing import early_flash_count, util_density


def map_story(match: Match) -> dict[str, object]:
    card = map_card(match)
    site = sites(match.map_name)
    return {
        "card": {
            "map_name": card.map_name,
            "active_pool": card.active_pool,
            "ct_winrate": card.ct_winrate,
            "t_winrate": card.t_winrate,
            "preference": card.preference,
            "plant_rate": card.plant_rate,
            "post_plant_t_winrate": card.post_plant_t_winrate,
            "ct_hold_no_plant": card.ct_hold_no_plant,
            "site_share": card.site_share,
        },
        "formatted": format_map_card(card),
        "narrative": narrative(match.map_name),
        "sites": list(site) if site else [],
        "heatmap": team_tag_heatmap(match),
        "early_flashes": early_flash_count(match),
        "util_density": util_density(match),
        "side_preference": side_preference_label(match),
        "ct_wr": side_winrate(match, TeamSide.CT),
        "t_wr": side_winrate(match, TeamSide.T),
        "plant_rate": plant_rate(match),
        "post_plant_t": post_plant_wins(match),
        "ct_holds": ct_hold_without_plant(match),
        "site_mentions": site_mention_share(match),
    }


def map_pressure_rounds(match: Match) -> list[dict[str, object]]:
    """Rounds with plants or heavy early utility."""
    rows = []
    for rnd in match.rounds:
        early_util = sum(1 for u in rnd.utility if int(u.tick_ms) <= 20000)
        if rnd.bomb_planted or early_util >= 4:
            rows.append(
                {
                    "round": int(rnd.number),
                    "planted": rnd.bomb_planted,
                    "early_util": early_util,
                    "winner": rnd.winner.value,
                    "kills": len(rnd.kills),
                }
            )
    return rows


def execute_density_by_half(match: Match) -> dict[str, float]:
    from roundwire.rules.mr_rules import half_length

    half = half_length(match.edition)
    first = match.rounds[:half]
    second = match.rounds[half:]

    def dens(rounds):
        if not rounds:
            return 0.0
        return sum(len(r.utility) for r in rounds) / len(rounds)

    return {"first_half": dens(first), "second_half": dens(second)}
