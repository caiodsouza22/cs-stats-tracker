"""Multi-kill detection within a round."""

from __future__ import annotations

from collections import Counter

from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.types import PlayerId


def multi_kills_in_round(round_: Round, minimum: int = 2) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for kill in round_.kills:
        counter[str(kill.killer_id)] += 1
    return {pid: n for pid, n in counter.items() if n >= minimum}


def multi_kill_count(match: Match, player_id: PlayerId, minimum: int = 2) -> int:
    total = 0
    for rnd in match.rounds:
        n = len(rnd.kills_for(player_id))
        if n >= minimum:
            total += 1
    return total


def ace_rounds(match: Match, player_id: PlayerId) -> list[int]:
    return [int(rnd.number) for rnd in match.rounds if len(rnd.kills_for(player_id)) >= 5]
