"""Human labels for enums."""

from __future__ import annotations

from roundwire.models.buy_type import BuyType
from roundwire.models.edition import GameEdition


def edition_label(edition: GameEdition) -> str:
    return "CS:GO" if edition is GameEdition.CSGO else "Counter-Strike 2"


def buy_label(buy: BuyType) -> str:
    mapping = {
        BuyType.ECO: "Eco",
        BuyType.FORCE: "Force buy",
        BuyType.SEMI: "Semi buy",
        BuyType.FULL: "Full buy",
        BuyType.PISTOL: "Pistol round",
        BuyType.UNKNOWN: "Unknown",
    }
    return mapping[buy]
