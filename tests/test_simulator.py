from roundwire.economy.simulator import simulate_team_cash, final_team_cash

def test_sim(cs2_match):
    result = simulate_team_cash(cs2_match)
    assert len(result.team_cash_by_round) == len(cs2_match.rounds)
    final = final_team_cash(cs2_match)
    assert set(final) == {"CT", "T"}
