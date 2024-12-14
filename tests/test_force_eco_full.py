from roundwire.economy.force_buy import force_success_rate
from roundwire.economy.eco_rounds import eco_rounds
from roundwire.economy.full_buy import full_buy_winrate
from roundwire.models.team import TeamSide
def test_buy_modules(cs2_match):
    assert 0.0 <= force_success_rate(cs2_match, TeamSide.CT) <= 1.0
    assert isinstance(eco_rounds(cs2_match, TeamSide.T), list)
    assert 0.0 <= full_buy_winrate(cs2_match, TeamSide.CT) <= 1.0
