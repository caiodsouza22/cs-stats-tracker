"""T-side execute proxies from early utility density."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.models.utility_event import UtilityKind
from roundwire.stats.aggregates import mean


def early_t_utility(match: Match, before_ms: int = 25000) -> list[int]:
    pmap = match.player_map()
    out: list[int] = []
    for rnd in match.rounds:
        count = 0
        for event in rnd.utility:
            thrower = pmap.get(event.thrower_id)
            if thrower is None or thrower.team is not TeamSide.T:
                continue
            if int(event.tick_ms) <= before_ms:
                count += 1
        out.append(count)
    return out


def execute_score(match: Match) -> float:
    dens = early_t_utility(match)
    smoke_weight = 0.0
    pmap = match.player_map()
    for rnd in match.rounds:
        for event in rnd.utility:
            thrower = pmap.get(event.thrower_id)
            if (
                thrower
                and thrower.team is TeamSide.T
                and event.kind is UtilityKind.SMOKE
                and int(event.tick_ms) <= 25000
            ):
                smoke_weight += 1.0
    return mean([float(x) for x in dens]) + 0.25 * smoke_weight / max(1, len(match.rounds))
