"""Momentum and swing detection from round winners."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.models.team import TeamSide


@dataclass(frozen=True, slots=True)
class Swing:
    start_round: int
    end_round: int
    side: str
    length: int


def detect_swings(match: Match, min_length: int = 3) -> list[Swing]:
    swings: list[Swing] = []
    if not match.rounds:
        return swings
    current = match.rounds[0].winner
    start = int(match.rounds[0].number)
    length = 1
    for rnd in match.rounds[1:]:
        if rnd.winner is current:
            length += 1
        else:
            if length >= min_length:
                swings.append(
                    Swing(
                        start_round=start,
                        end_round=start + length - 1,
                        side=current.value,
                        length=length,
                    )
                )
            current = rnd.winner
            start = int(rnd.number)
            length = 1
    if length >= min_length:
        swings.append(
            Swing(
                start_round=start,
                end_round=start + length - 1,
                side=current.value,
                length=length,
            )
        )
    return swings


def lead_changes(match: Match) -> int:
    changes = 0
    ct = 0
    t = 0
    leader: TeamSide | None = None
    for rnd in match.rounds:
        if rnd.winner is TeamSide.CT:
            ct += 1
        else:
            t += 1
        now: TeamSide | None
        if ct > t:
            now = TeamSide.CT
        elif t > ct:
            now = TeamSide.T
        else:
            now = None
        if leader is not None and now is not None and now is not leader:
            changes += 1
        if now is not None:
            leader = now
    return changes


def comeback_rounds(match: Match, deficit: int = 3) -> list[int]:
    """Rounds after which the eventual winner erased a deficit of ``deficit``."""
    winner = match.winner_side()
    if winner is None:
        return []
    ct = 0
    t = 0
    markers: list[int] = []
    saw_deficit = False
    for rnd in match.rounds:
        if rnd.winner is TeamSide.CT:
            ct += 1
        else:
            t += 1
        if winner is TeamSide.CT and t - ct >= deficit:
            saw_deficit = True
        if winner is TeamSide.T and ct - t >= deficit:
            saw_deficit = True
        if saw_deficit:
            if winner is TeamSide.CT and ct >= t:
                markers.append(int(rnd.number))
                saw_deficit = False
            if winner is TeamSide.T and t >= ct:
                markers.append(int(rnd.number))
                saw_deficit = False
    return markers
