"""Round money award computation helpers."""

from __future__ import annotations

from roundwire.models.edition import GameEdition
from roundwire.models.team import TeamSide
from roundwire.rules.economy_constants import constants_for
from roundwire.rules.kill_rewards import kill_reward_for


def win_bonus(reason: str, side: TeamSide) -> int:
    reason_key = reason.lower()
    if reason_key in {"bomb_exploded", "explosion"} and side is TeamSide.T:
        return 3500
    if reason_key in {"bomb_defused", "defuse"} and side is TeamSide.CT:
        return 3500
    if reason_key in {"time", "timeout"} and side is TeamSide.CT:
        return 3250
    return 3250


def estimated_round_income(
    edition: GameEdition,
    *,
    won: bool,
    consecutive_losses: int,
    kill_weapons: list[str],
    win_reason: str = "elimination",
    side: TeamSide = TeamSide.CT,
) -> int:
    consts = constants_for(edition)
    income = 0
    if won:
        income += win_bonus(win_reason, side)
    else:
        steps = consts.loss_bonus_steps
        idx = max(0, min(consecutive_losses, len(steps) - 1))
        income += steps[idx]
    for weapon in kill_weapons:
        income += kill_reward_for(weapon, default=consts.kill_reward_default)
    return min(income, consts.max_money)


def plant_bonus() -> int:
    return 300


def defuse_alive_bonus() -> int:
    """Legacy note: surviving CTs get no separate bonus beyond win award."""
    return 0
