"""High-level edition ruleset object."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.edition import GameEdition
from roundwire.rules.economy_constants import EconomyConstants, constants_for


@dataclass(frozen=True, slots=True)
class EditionRules:
    edition: GameEdition
    economy: EconomyConstants

    @property
    def mr_label(self) -> str:
        return self.edition.mr_label

    @property
    def win_threshold(self) -> int:
        return self.edition.win_threshold

    @property
    def regulation_rounds(self) -> int:
        return self.edition.regulation_rounds

    def loss_bonus(self, consecutive_losses: int) -> int:
        steps = self.economy.loss_bonus_steps
        idx = max(0, min(consecutive_losses, len(steps) - 1))
        return steps[idx]


def rules_for(edition: GameEdition) -> EditionRules:
    return EditionRules(edition=edition, economy=constants_for(edition))
