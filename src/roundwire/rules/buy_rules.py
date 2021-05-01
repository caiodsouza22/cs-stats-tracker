"""Threshold helpers for classifying buys."""

from __future__ import annotations

from roundwire.models.buy_type import BuyType
from roundwire.models.edition import GameEdition
from roundwire.rules.economy_constants import constants_for


def classify_equipment_value(value: int, edition: GameEdition, *, pistol_round: bool = False) -> BuyType:
    if pistol_round:
        return BuyType.PISTOL
    consts = constants_for(edition)
    if value >= consts.full_buy_threshold:
        return BuyType.FULL
    if value >= consts.force_buy_threshold:
        return BuyType.FORCE
    if value >= int(consts.eco_threshold * 0.6):
        return BuyType.SEMI
    return BuyType.ECO
