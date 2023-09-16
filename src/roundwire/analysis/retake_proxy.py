"""Heuristic retake pressure after bomb plants."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.models.utility_event import UtilityKind


def post_plant_ct_utility(match: Match, after_ms: int = 45000) -> float:
    planted = [r for r in match.rounds if r.bomb_planted]
    if not planted:
        return 0.0
    total = 0
    for rnd in planted:
        total += sum(
            1
            for event in rnd.utility
            if int(event.tick_ms) >= after_ms
            and match.player_map().get(event.thrower_id)
            and match.player_map()[event.thrower_id].team is TeamSide.CT
        )
    return total / len(planted)


def post_plant_winrate(match: Match) -> dict[str, float]:
    planted = [r for r in match.rounds if r.bomb_planted]
    if not planted:
        return {"CT": 0.0, "T": 0.0}
    ct = sum(1 for r in planted if r.winner is TeamSide.CT) / len(planted)
    return {"CT": ct, "T": 1.0 - ct}


def retake_flash_density(match: Match) -> float:
    planted = [r for r in match.rounds if r.bomb_planted]
    if not planted:
        return 0.0
    flashes = 0
    for rnd in planted:
        flashes += sum(
            1
            for e in rnd.utility
            if e.kind is UtilityKind.FLASH and int(e.tick_ms) >= 45000
        )
    return flashes / len(planted)
