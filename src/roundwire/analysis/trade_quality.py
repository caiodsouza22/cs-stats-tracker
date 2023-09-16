"""Opening trade success metrics."""

from __future__ import annotations

from roundwire.combat.opening import opening_duels
from roundwire.combat.trades import all_trades
from roundwire.models.match import Match
from roundwire.models.team import TeamSide


def opening_trade_rate(match: Match) -> float:
    duels = opening_duels(match)
    if not duels:
        return 0.0
    return sum(1 for d in duels if d.traded) / len(duels)


def trade_rate_by_side(match: Match) -> dict[str, float]:
    pmap = match.player_map()
    sides = {TeamSide.CT: [0, 0], TeamSide.T: [0, 0]}
    for duel in opening_duels(match):
        victim = pmap.get(duel.kill.victim_id)
        if victim is None:
            continue
        sides[victim.team][1] += 1
        if duel.traded:
            sides[victim.team][0] += 1
    return {
        side.value: (vals[0] / vals[1] if vals[1] else 0.0)
        for side, vals in sides.items()
    }


def total_trades(match: Match) -> int:
    return len(all_trades(match))
