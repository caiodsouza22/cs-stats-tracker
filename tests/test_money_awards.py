from roundwire.rules.money_awards import estimated_round_income, win_bonus
from roundwire.models.edition import GameEdition
from roundwire.models.team import TeamSide
def test_income():
    assert win_bonus("elimination", TeamSide.CT) == 3250
    income = estimated_round_income(GameEdition.CS2, won=True, consecutive_losses=0, kill_weapons=["ak47"])
    assert income >= 3250
