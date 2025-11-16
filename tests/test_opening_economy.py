from roundwire.analysis.opening_economy import opening_economy_rows
def test_open_eco(cs2_match):
    rows = opening_economy_rows(cs2_match)
    assert len(rows) == len(cs2_match.rounds)
