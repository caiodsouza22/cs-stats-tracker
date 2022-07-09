"""KAST-like participation metric (kill/assist/survive/trade)."""

from __future__ import annotations

from roundwire.combat.trades import trades_in_round
from roundwire.models.match import Match
from roundwire.types import PlayerId


def kast_rounds(match: Match, player_id: PlayerId) -> int:
    count = 0
    for rnd in match.rounds:
        contributed = False
        if rnd.kills_for(player_id):
            contributed = True
        elif any(k.assisted_by == player_id for k in rnd.kills):
            contributed = True
        elif player_id in rnd.survivors:
            contributed = True
        else:
            for trade in trades_in_round(rnd):
                if trade.trade.killer_id == player_id:
                    contributed = True
                    break
        if contributed:
            count += 1
    return count


def kast_pct(match: Match, player_id: PlayerId) -> float:
    if not match.rounds:
        return 0.0
    return kast_rounds(match, player_id) / len(match.rounds)
