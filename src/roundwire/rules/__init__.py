"""Edition-specific rules: MR, economy constants, weapon aliases."""

from roundwire.rules.economy_constants import EconomyConstants, constants_for
from roundwire.rules.edition_rules import EditionRules, rules_for
from roundwire.rules.weapon_aliases import canonical_weapon_name

__all__ = [
    "EconomyConstants",
    "EditionRules",
    "canonical_weapon_name",
    "constants_for",
    "rules_for",
]
