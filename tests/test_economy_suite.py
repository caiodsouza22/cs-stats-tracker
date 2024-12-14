from roundwire.economy.bank import average_bank, compare_banks, poorest_round, richest_round
from roundwire.economy.classify import buy_advantage, mirror_buys
from roundwire.economy.eco_rounds import eco_upsets
from roundwire.economy.equipment import average_equipment_value, cash_remaining
from roundwire.economy.force_buy import force_rounds
from roundwire.economy.full_buy import full_buy_rounds
from roundwire.economy.investment import equipment_spent_losing, equipment_spent_winning, overinvested_losses
from roundwire.economy.loss_bonus import streak_lengths
from roundwire.economy.pistol import pistol_round_numbers
from roundwire.economy.round_patterns import patterns_for_buy, suggest_pattern
from roundwire.economy.simulator import player_cash_history
from roundwire.economy.summary import economy_match_summary, format_economy_summary
from roundwire.models.buy_type import BuyType
from roundwire.models.edition import GameEdition
from roundwire.models.team import TeamSide

def test_economy_bundle(cs2_match):
    assert average_bank(cs2_match, TeamSide.CT) >= 0
    assert compare_banks(cs2_match)
    assert poorest_round(cs2_match, TeamSide.T) is not None
    assert richest_round(cs2_match, TeamSide.CT) is not None
    assert isinstance(buy_advantage(cs2_match), list)
    assert isinstance(mirror_buys(cs2_match), list)
    assert isinstance(eco_upsets(cs2_match, TeamSide.CT), list)
    rnd = cs2_match.rounds[3]
    assert average_equipment_value(rnd, cs2_match, TeamSide.CT) >= 0
    assert cash_remaining(rnd, cs2_match, TeamSide.T) >= 0
    assert isinstance(force_rounds(cs2_match, TeamSide.T), list)
    assert isinstance(full_buy_rounds(cs2_match, TeamSide.CT), list)
    assert equipment_spent_winning(cs2_match, TeamSide.CT) >= 0
    assert equipment_spent_losing(cs2_match, TeamSide.T) >= 0
    assert isinstance(overinvested_losses(cs2_match, TeamSide.CT), list)
    assert len(streak_lengths(cs2_match, TeamSide.CT)) == len(cs2_match.rounds)
    assert pistol_round_numbers(GameEdition.CS2) == (1, 13)
    assert patterns_for_buy(BuyType.FULL)
    assert suggest_pattern(1000, GameEdition.CS2).buy_type in {BuyType.ECO, BuyType.SEMI, BuyType.FORCE}
    hist = player_cash_history(cs2_match, str(cs2_match.players[0].player_id))
    assert len(hist) == len(cs2_match.rounds)
    assert len(economy_match_summary(cs2_match)) == 2
    assert format_economy_summary(cs2_match)
