from roundwire.combat.advanced import advanced_cards, match_combat_dashboard

def test_advanced(cs2_match):
    cards = advanced_cards(cs2_match)
    assert len(cards) == 10
    dash = match_combat_dashboard(cs2_match)
    assert "adr" in dash and "players" in dash
