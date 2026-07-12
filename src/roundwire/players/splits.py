"""Half-split and side-split player performance."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.players.profile import build_player_profile
from roundwire.rules.mr_rules import half_length
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class SplitLine:
    label: str
    rounds: int
    kills: int
    deaths: int
    adr: float
    kd: float
    wins: int
    win_rate: float

    def to_dict(self) -> dict[str, object]:
        return {
            "label": self.label,
            "rounds": self.rounds,
            "kills": self.kills,
            "deaths": self.deaths,
            "adr": round(self.adr, 1),
            "kd": round(self.kd, 3),
            "wins": self.wins,
            "win_rate": round(self.win_rate, 3),
        }


def _split(match: Match, player_id: PlayerId, rounds_slice: slice, label: str) -> SplitLine:
    player = match.player_map()[player_id]
    rounds = match.rounds[rounds_slice]
    kills = deaths = damage = wins = 0
    for rnd in rounds:
        kills += len(rnd.kills_for(player_id))
        deaths += len(rnd.deaths_for(player_id))
        damage += rnd.damage_dealt_by(player_id)
        if rnd.winner is player.team:
            wins += 1
    n = len(rounds)
    return SplitLine(
        label=label,
        rounds=n,
        kills=kills,
        deaths=deaths,
        adr=safe_div(float(damage), float(n)),
        kd=safe_div(float(kills), float(deaths), default=float(kills)),
        wins=wins,
        win_rate=safe_div(float(wins), float(n)),
    )


def half_splits(match: Match, player_id: PlayerId) -> list[SplitLine]:
    half = half_length(match.edition)
    return [
        _split(match, player_id, slice(0, half), "first_half"),
        _split(match, player_id, slice(half, None), "second_half"),
    ]


def side_splits(match: Match, player_id: PlayerId) -> list[SplitLine]:
    """Approximate CT/T splits using starting side for first half, flipped later.

    Dumps often omit mid-match side swaps on player objects; we treat first half
    as the roster's declared team and second half as the opposite for scoring.
    """
    player = match.player_map()[player_id]
    half = half_length(match.edition)
    first = match.rounds[:half]
    second = match.rounds[half:]

    def _side_slice(rounds, side: TeamSide, label: str) -> SplitLine:
        kills = deaths = damage = wins = 0
        for rnd in rounds:
            kills += len(rnd.kills_for(player_id))
            deaths += len(rnd.deaths_for(player_id))
            damage += rnd.damage_dealt_by(player_id)
            # win credit if the round winner matches the side we're attributing
            if rnd.winner is side:
                wins += 1
        n = len(rounds)
        return SplitLine(
            label=label,
            rounds=n,
            kills=kills,
            deaths=deaths,
            adr=safe_div(float(damage), float(n)),
            kd=safe_div(float(kills), float(deaths), default=float(kills)),
            wins=wins,
            win_rate=safe_div(float(wins), float(n)),
        )

    start = player.team
    return [
        _side_slice(first, start, f"start_as_{start.value}"),
        _side_slice(second, start.opposite(), f"then_{start.opposite().value}"),
    ]


def split_report(match: Match, player_id: PlayerId) -> dict[str, object]:
    profile = build_player_profile(match, player_id)
    return {
        "player": profile.name,
        "team": profile.team,
        "halves": [s.to_dict() for s in half_splits(match, player_id)],
        "sides": [s.to_dict() for s in side_splits(match, player_id)],
    }


def clutch_half_bias(match: Match, player_id: PlayerId) -> dict[str, int]:
    from roundwire.players.clutch_book import clutch_cases

    half = half_length(match.edition)
    first = second = 0
    for case in clutch_cases(match, player_id, max_allies=2):
        if case.round_number <= half:
            first += 1
        else:
            second += 1
    return {"first_half": first, "second_half": second}
