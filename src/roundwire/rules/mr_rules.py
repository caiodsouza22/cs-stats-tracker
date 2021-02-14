"""Max-rounds helpers for regulation and overtime hints."""

from __future__ import annotations

from roundwire.models.edition import GameEdition


def half_length(edition: GameEdition) -> int:
    return 15 if edition is GameEdition.CSGO else 12


def is_halftime(round_number: int, edition: GameEdition) -> bool:
    return round_number == half_length(edition)


def is_overtime_eligible(ct_score: int, t_score: int, edition: GameEdition) -> bool:
    threshold = edition.win_threshold
    return ct_score == threshold - 1 and t_score == threshold - 1


def expected_regulation_cap(edition: GameEdition) -> int:
    return edition.regulation_rounds
