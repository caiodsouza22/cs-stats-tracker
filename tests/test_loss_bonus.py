from roundwire.rules.loss_bonus import loss_bonus_table
from roundwire.models.edition import GameEdition
from roundwire.economy.loss_bonus import team_loss_bonus_streak
from roundwire.models.team import TeamSide

def test_loss_bonus(cs2_match):
    table = loss_bonus_table(GameEdition.CS2)
    assert table[0] == 1400
    assert table[-1] == 3400
    streak = team_loss_bonus_streak(cs2_match, TeamSide.CT)
    assert len(streak) == len(cs2_match.rounds)
