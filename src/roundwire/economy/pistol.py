"""Pistol round detection."""

from __future__ import annotations

from roundwire.models.edition import GameEdition
from roundwire.models.round import Round
from roundwire.rules.mr_rules import half_length


def is_pistol_round(round_: Round, edition: GameEdition) -> bool:
    n = int(round_.number)
    return n == 1 or n == half_length(edition) + 1


def pistol_round_numbers(edition: GameEdition) -> tuple[int, int]:
    return 1, half_length(edition) + 1
