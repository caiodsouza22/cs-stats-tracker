from roundwire.utility.summary import utility_summary
from roundwire.utility.flashes import enemies_flashed_total

def test_utility(cs2_match):
    rows = utility_summary(cs2_match)
    assert len(rows) == 10
    assert enemies_flashed_total(cs2_match) > 0
