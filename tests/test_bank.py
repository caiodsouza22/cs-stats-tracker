from roundwire.economy.bank import bank_trajectory, bank_swing
from roundwire.models.team import TeamSide
def test_bank(cs2_match):
    traj = bank_trajectory(cs2_match, TeamSide.CT)
    assert len(traj) == len(cs2_match.rounds)
    assert bank_swing(cs2_match, TeamSide.T) >= 0
