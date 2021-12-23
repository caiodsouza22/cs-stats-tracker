"""Team loss-bonus streak tracking across a match."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.rules.loss_bonus import consecutive_losses_before, loss_bonus_for_round


def team_loss_bonus_streak(match: Match, side: TeamSide) -> list[int]:
    """Return loss-bonus dollar amount entering each round for ``side``."""
    return [loss_bonus_for_round(match, idx, side) for idx in range(len(match.rounds))]


def streak_lengths(match: Match, side: TeamSide) -> list[int]:
    return [consecutive_losses_before(match, idx, side) for idx in range(len(match.rounds))]
