from roundwire.analysis.coaching import all_advice, round_advice

def test_coaching(cs2_match):
    advice = all_advice(cs2_match)
    assert "execute" in advice
    assert round_advice(cs2_match, 1)
