"""Simple overtime scoring hints (MR3 style)."""

from __future__ import annotations

from roundwire.models.edition import GameEdition


OVERTIME_MR = 3


def overtime_win_target(edition: GameEdition, ot_period: int = 1) -> int:
    """Return cumulative round target including regulation + OT periods."""
    base = edition.win_threshold - 1  # e.g. 15 or 12 tied
    return base + OVERTIME_MR * ot_period


def is_in_overtime(total_rounds_played: int, edition: GameEdition) -> bool:
    return total_rounds_played > edition.regulation_rounds
