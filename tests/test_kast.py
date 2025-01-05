from roundwire.combat.kast import kast_pct
def test_kast(cs2_match):
    for p in cs2_match.players:
        assert 0.0 <= kast_pct(cs2_match, p.player_id) <= 1.0
