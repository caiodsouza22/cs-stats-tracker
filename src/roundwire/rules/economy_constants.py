"""Economy constants that differ slightly between editions."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.edition import GameEdition


@dataclass(frozen=True, slots=True)
class EconomyConstants:
    starting_money: int
    max_money: int
    kill_reward_default: int
    loss_bonus_steps: tuple[int, ...]
    full_buy_threshold: int
    force_buy_threshold: int
    eco_threshold: int
    armor_kevlar: int
    armor_helmet: int
    defuse_kit: int

CSGO_ECONOMY = EconomyConstants(
    starting_money=800,
    max_money=16000,
    kill_reward_default=300,
    loss_bonus_steps=(1400, 1900, 2400, 2900, 3400),
    full_buy_threshold=4000,
    force_buy_threshold=2000,
    eco_threshold=2000,
    armor_kevlar=650,
    armor_helmet=1000,
    defuse_kit=400,
)

CS2_ECONOMY = EconomyConstants(
    starting_money=800,
    max_money=16000,
    kill_reward_default=300,
    loss_bonus_steps=(1400, 1900, 2400, 2900, 3400),
    full_buy_threshold=4200,
    force_buy_threshold=2100,
    eco_threshold=2000,
    armor_kevlar=650,
    armor_helmet=1000,
    defuse_kit=400,
)


def constants_for(edition: GameEdition) -> EconomyConstants:
    return CSGO_ECONOMY if edition is GameEdition.CSGO else CS2_ECONOMY
