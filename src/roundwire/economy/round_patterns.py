"""Named round buy patterns used in coaching-style summaries."""
from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.buy_type import BuyType
from roundwire.models.edition import GameEdition
from roundwire.rules.economy_constants import constants_for


@dataclass(frozen=True, slots=True)
class BuyPattern:
    key: str
    title: str
    buy_type: BuyType
    typical_eq_min: int
    typical_eq_max: int
    notes: str
    example_loadout: tuple[str, ...]


PATTERNS: dict[str, BuyPattern] = {
    "pistol_default": BuyPattern(
        "pistol_default", "Pistol round default buys", BuyType.PISTOL, 0, 1200,
        "Keep pistols; optional kit on CT; light utility only.",
        ("usp_silencer",),
    ),
    "eco_save": BuyPattern(
        "eco_save", "Full save eco", BuyType.ECO, 0, 2000,
        "Minimize spend to stabilize next gun round.",
        ("p250",),
    ),
    "force_armor_smg": BuyPattern(
        "force_armor_smg", "Armor + SMG force", BuyType.FORCE, 2000, 3500,
        "Spend enough to contest without full rifles.",
        ("mac10", "p250", "armor"),
    ),
    "force_deagle": BuyPattern(
        "force_deagle", "Deagle force without rifle", BuyType.FORCE, 2000, 3500,
        "Deagle + armor when rifle money is short.",
        ("deagle", "armor"),
    ),
    "semi_scout": BuyPattern(
        "semi_scout", "Scout semi-buy", BuyType.SEMI, 2500, 4000,
        "Partial investment, often scout or single rifle.",
        ("ssg08", "armor"),
    ),
    "full_rifles": BuyPattern(
        "full_rifles", "Standard rifle full buy", BuyType.FULL, 4000, 7000,
        "Rifles plus utility; standard gun round.",
        ("ak47", "flashbang", "smokegrenade", "armor"),
    ),
    "full_awp_mix": BuyPattern(
        "full_awp_mix", "AWP + rifles", BuyType.FULL, 4500, 7500,
        "One AWP dropped into an otherwise full rifle buy.",
        ("awp", "ak47", "flashbang", "armor"),
    ),
    "anti_eco_smg": BuyPattern(
        "anti_eco_smg", "Anti-eco SMG buy", BuyType.FULL, 3000, 5000,
        "SMGs vs known eco to farm money and close angles.",
        ("mp9", "mac10", "armor"),
    ),
    "utility_heavy": BuyPattern(
        "utility_heavy", "Utility-heavy execute buy", BuyType.FULL, 4000, 7000,
        "Extra smokes/flashes for a planned site hit.",
        ("ak47", "flashbang", "smokegrenade", "molotov", "armor"),
    ),
    "stack_a": BuyPattern(
        "stack_a", "A stack eco pistols", BuyType.ECO, 0, 2000,
        "Stack A on eco; gamble info with pistols.",
        ("p250",),
    ),
}


def pattern(key: str) -> BuyPattern:
    return PATTERNS[key]


def patterns_for_buy(buy: BuyType) -> list[BuyPattern]:
    return [p for p in PATTERNS.values() if p.buy_type is buy]


def suggest_pattern(eq_value: int, edition: GameEdition, *, pistol: bool = False) -> BuyPattern:
    if pistol:
        return PATTERNS["pistol_default"]
    consts = constants_for(edition)
    if eq_value >= consts.full_buy_threshold:
        return PATTERNS["full_rifles"]
    if eq_value >= consts.force_buy_threshold:
        return PATTERNS["force_armor_smg"]
    if eq_value >= int(consts.eco_threshold * 0.6):
        return PATTERNS["semi_scout"]
    return PATTERNS["eco_save"]


def explain(key: str, edition: GameEdition) -> str:
    pat = PATTERNS[key]
    consts = constants_for(edition)
    loadout = ", ".join(pat.example_loadout)
    return (
        f"{pat.title} [{pat.buy_type.value}] typical EQ "
        f"{pat.typical_eq_min}-{pat.typical_eq_max} "
        f"(edition full threshold {consts.full_buy_threshold}). {pat.notes} "
        f"Example: {loadout}."
    )


def explain_all(edition: GameEdition) -> dict[str, str]:
    return {key: explain(key, edition) for key in PATTERNS}
