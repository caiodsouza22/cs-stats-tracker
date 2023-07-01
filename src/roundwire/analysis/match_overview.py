"""Aggregate overview dict for a match."""

from __future__ import annotations

from roundwire.combat.summary import combat_summary
from roundwire.economy.summary import economy_match_summary
from roundwire.models.match import Match
from roundwire.rating.impact import impact_table
from roundwire.utility.summary import utility_summary


def match_overview(match: Match) -> dict[str, object]:
    ct, t = match.score()
    return {
        "match_id": str(match.match_id),
        "map": match.map_name,
        "edition": match.edition.value,
        "score": {"CT": ct, "T": t},
        "top_fragger": combat_summary(match)[0].name if match.players else None,
        "top_impact": impact_table(match)[0].name if match.players else None,
        "economy": [
            {"side": s.side, "buys": s.buys, "eco_upsets": s.eco_upsets}
            for s in economy_match_summary(match)
        ],
        "utility_leaders": [
            {"name": u.name, "enemies_flashed": u.enemies_flashed}
            for u in utility_summary(match)[:3]
        ],
    }
