from roundwire.analysis.gaps import average_cash_gap, largest_equipment_gap_round
def test_gaps(cs2_match):
    assert average_cash_gap(cs2_match) >= 0
    assert largest_equipment_gap_round(cs2_match) is not None
