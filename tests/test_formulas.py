from roundwire.combat.formulas import player_formula_pack
def test_formulas(cs2_match):
    pack = player_formula_pack(cs2_match, cs2_match.players[0].player_id)
    assert "blended" in pack
