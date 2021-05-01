"""Armor purchase helpers."""

from __future__ import annotations

from roundwire.models.edition import GameEdition
from roundwire.rules.economy_constants import constants_for


def armor_cost(edition: GameEdition, *, helmet: bool) -> int:
    consts = constants_for(edition)
    return consts.armor_helmet if helmet else consts.armor_kevlar


def can_afford_armor(cash: int, edition: GameEdition, *, helmet: bool) -> bool:
    return cash >= armor_cost(edition, helmet=helmet)
