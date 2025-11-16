from roundwire.analysis.momentum import detect_swings, lead_changes
def test_momentum(cs2_match):
    swings = detect_swings(cs2_match, min_length=2)
    assert isinstance(swings, list)
    assert lead_changes(cs2_match) >= 0
