"""Loss bonus ladder computation."""

from __future__ import annotations

from roundwire.models.edition import GameEdition
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.rules.edition_rules import rules_for


def consecutive_losses_before(match: Match, round_index: int, side: TeamSide) -> int:
    """Count consecutive losses for ``side`` ending just before ``round_index``."""
    losses = 0
    for rnd in reversed(match.rounds[:round_index]):
        if rnd.winner is side:
            break
        losses += 1
    return losses


def loss_bonus_for_round(match: Match, round_index: int, side: TeamSide) -> int:
    rules = rules_for(match.edition)
    streak = consecutive_losses_before(match, round_index, side)
    return rules.loss_bonus(streak)


def loss_bonus_table(edition: GameEdition) -> list[int]:
    return list(rules_for(edition).economy.loss_bonus_steps)
