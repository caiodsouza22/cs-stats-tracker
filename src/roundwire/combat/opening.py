"""Opening duel and trade kill detection."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.kill import Kill
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.timing import DEFAULT_TRADE_WINDOW_MS, trade_window_after
from roundwire.types import Milliseconds, PlayerId


@dataclass(frozen=True, slots=True)
class OpeningDuel:
    round_number: int
    kill: Kill
    traded: bool


def first_kill(round_: Round) -> Kill | None:
    if not round_.kills:
        return None
    return min(round_.kills, key=lambda k: int(k.tick_ms))


def was_traded(
    round_: Round,
    opening: Kill,
    window_ms: Milliseconds = DEFAULT_TRADE_WINDOW_MS,
) -> bool:
    window = trade_window_after(opening.tick_ms, window_ms)
    for kill in round_.kills:
        if kill is opening:
            continue
        if kill.victim_id == opening.killer_id and window.contains(kill.tick_ms):
            return True
    return False


def opening_duels(match: Match) -> list[OpeningDuel]:
    out: list[OpeningDuel] = []
    for rnd in match.rounds:
        fk = first_kill(rnd)
        if fk is None:
            continue
        out.append(
            OpeningDuel(
                round_number=int(rnd.number),
                kill=fk,
                traded=was_traded(rnd, fk),
            )
        )
    return out


def opening_kills_for(match: Match, player_id: PlayerId) -> int:
    return sum(1 for d in opening_duels(match) if d.kill.killer_id == player_id)


def opening_deaths_for(match: Match, player_id: PlayerId) -> int:
    return sum(1 for d in opening_duels(match) if d.kill.victim_id == player_id)
