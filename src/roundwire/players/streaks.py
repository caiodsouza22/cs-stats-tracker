"""Kill, death, and round-win streaks for a player."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.players.round_card import player_round_log
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class Streak:
    kind: str
    start_round: int
    end_round: int
    length: int

    def to_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "start_round": self.start_round,
            "end_round": self.end_round,
            "length": self.length,
        }


def _streaks_from_flags(flags: list[tuple[int, bool]], kind: str, min_length: int = 2) -> list[Streak]:
    out: list[Streak] = []
    if not flags:
        return out
    start_round, active = flags[0][0], flags[0][1]
    length = 1 if active else 0
    current_start = start_round if active else None
    for round_number, flag in flags[1:]:
        if flag:
            if current_start is None:
                current_start = round_number
                length = 1
            else:
                length += 1
        else:
            if current_start is not None and length >= min_length:
                out.append(
                    Streak(
                        kind=kind,
                        start_round=current_start,
                        end_round=round_number - 1 if round_number > current_start else current_start,
                        length=length,
                    )
                )
            current_start = None
            length = 0
    if current_start is not None and length >= min_length:
        end = flags[-1][0]
        out.append(Streak(kind=kind, start_round=current_start, end_round=end, length=length))
    return out


def kill_participation_streaks(match: Match, player_id: PlayerId, min_length: int = 3) -> list[Streak]:
    flags = [(c.round_number, c.kills > 0) for c in player_round_log(match, player_id)]
    return _streaks_from_flags(flags, "kill_round", min_length=min_length)


def deathless_streaks(match: Match, player_id: PlayerId, min_length: int = 3) -> list[Streak]:
    flags = [(c.round_number, c.deaths == 0) for c in player_round_log(match, player_id)]
    return _streaks_from_flags(flags, "deathless", min_length=min_length)


def win_streaks(match: Match, player_id: PlayerId, min_length: int = 3) -> list[Streak]:
    flags = [(c.round_number, c.won) for c in player_round_log(match, player_id)]
    return _streaks_from_flags(flags, "win", min_length=min_length)


def loss_streaks(match: Match, player_id: PlayerId, min_length: int = 3) -> list[Streak]:
    flags = [(c.round_number, not c.won) for c in player_round_log(match, player_id)]
    return _streaks_from_flags(flags, "loss", min_length=min_length)


def multi_kill_streaks(match: Match, player_id: PlayerId, min_length: int = 2) -> list[Streak]:
    flags = [(c.round_number, c.multi_kill) for c in player_round_log(match, player_id)]
    return _streaks_from_flags(flags, "multi_kill", min_length=min_length)


def longest_streak(streaks: list[Streak]) -> Streak | None:
    if not streaks:
        return None
    return max(streaks, key=lambda s: (s.length, -s.start_round))


def streak_report(match: Match, player_id: PlayerId) -> dict[str, object]:
    packs = {
        "kill_round": kill_participation_streaks(match, player_id),
        "deathless": deathless_streaks(match, player_id),
        "win": win_streaks(match, player_id),
        "loss": loss_streaks(match, player_id),
        "multi_kill": multi_kill_streaks(match, player_id),
    }
    return {
        key: {
            "count": len(items),
            "longest": longest_streak(items).to_dict() if longest_streak(items) else None,
            "items": [s.to_dict() for s in items],
        }
        for key, items in packs.items()
    }


def consecutive_opening_kills(match: Match, player_id: PlayerId) -> int:
    """Longest run of consecutive rounds with an opening kill."""
    streaks = _streaks_from_flags(
        [(c.round_number, c.opening_kill) for c in player_round_log(match, player_id)],
        "opening",
        min_length=1,
    )
    best = longest_streak(streaks)
    return best.length if best else 0
