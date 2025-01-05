from roundwire.combat.first_blood import opening_conversion, first_blood_players
def test_fb(cs2_match):
    assert 0.0 <= opening_conversion(cs2_match) <= 1.0
    assert first_blood_players(cs2_match)
