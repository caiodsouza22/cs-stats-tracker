"""Team bank / cash trajectory across rounds."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.economy.equipment import cash_remaining, team_equipment_value
from roundwire.models.match import Match
from roundwire.models.team import TeamSide


@dataclass(frozen=True, slots=True)
class BankSnapshot:
    round_number: int
    side: str
    cash: int
    equipment: int

    @property
    def total_value(self) -> int:
        return self.cash + self.equipment


def bank_trajectory(match: Match, side: TeamSide) -> list[BankSnapshot]:
    out: list[BankSnapshot] = []
    for rnd in match.rounds:
        out.append(
            BankSnapshot(
                round_number=int(rnd.number),
                side=side.value,
                cash=cash_remaining(rnd, match, side),
                equipment=team_equipment_value(rnd, match, side),
            )
        )
    return out


def average_bank(match: Match, side: TeamSide) -> float:
    snaps = bank_trajectory(match, side)
    if not snaps:
        return 0.0
    return sum(s.total_value for s in snaps) / len(snaps)


def poorest_round(match: Match, side: TeamSide) -> BankSnapshot | None:
    snaps = bank_trajectory(match, side)
    if not snaps:
        return None
    return min(snaps, key=lambda s: s.total_value)


def richest_round(match: Match, side: TeamSide) -> BankSnapshot | None:
    snaps = bank_trajectory(match, side)
    if not snaps:
        return None
    return max(snaps, key=lambda s: s.total_value)


def bank_swing(match: Match, side: TeamSide) -> int:
    """Max equipment+cash minus min across the match."""
    snaps = bank_trajectory(match, side)
    if not snaps:
        return 0
    values = [s.total_value for s in snaps]
    return max(values) - min(values)


def compare_banks(match: Match) -> list[tuple[int, int, int]]:
    """Per-round (round_number, CT total, T total)."""
    rows: list[tuple[int, int, int]] = []
    ct = bank_trajectory(match, TeamSide.CT)
    t = {s.round_number: s for s in bank_trajectory(match, TeamSide.T)}
    for snap in ct:
        other = t.get(snap.round_number)
        rows.append((snap.round_number, snap.total_value, other.total_value if other else 0))
    return rows
