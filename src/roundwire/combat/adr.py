"""Average damage per round."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.types import PlayerId


def damage_total(match: Match, player_id: PlayerId) -> int:
    return sum(rnd.damage_dealt_by(player_id) for rnd in match.rounds)


def adr_for_player(match: Match, player_id: PlayerId) -> float:
    if not match.rounds:
        return 0.0
    return damage_total(match, player_id) / len(match.rounds)


def adr_by_player(match: Match) -> dict[str, float]:
    return {str(p.player_id): adr_for_player(match, p.player_id) for p in match.players}
