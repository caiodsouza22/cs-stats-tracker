"""Utility spend efficiency league tables."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.players.utility_profile import build_utility_profile, support_index
from roundwire.stats.aggregates import safe_div


def utility_league(match: Match) -> list[dict[str, object]]:
    rows = []
    for player in match.players:
        util = build_utility_profile(match, player.player_id)
        rows.append(
            {
                "name": player.name,
                "team": player.team.value,
                "spend": util.spend,
                "enemies_flashed": util.enemies_flashed,
                "he_damage": util.he_damage,
                "fire_damage": util.fire_damage,
                "support_index": round(support_index(match, player.player_id), 3),
                "flash_per_1000": round(
                    safe_div(float(util.enemies_flashed) * 1000.0, float(max(1, util.spend))),
                    2,
                ),
            }
        )
    return sorted(rows, key=lambda r: (-r["support_index"], -r["enemies_flashed"], r["name"]))


def util_specialists(match: Match) -> dict[str, str | None]:
    league = utility_league(match)
    if not league:
        return {"flash": None, "he": None, "fire": None, "support": None}
    return {
        "flash": max(league, key=lambda r: r["enemies_flashed"])["name"],
        "he": max(league, key=lambda r: r["he_damage"])["name"],
        "fire": max(league, key=lambda r: r["fire_damage"])["name"],
        "support": league[0]["name"],
    }
