from roundwire.economy.round_patterns import suggest_pattern, explain_all
from roundwire.models.edition import GameEdition

def test_patterns():
    assert suggest_pattern(5000, GameEdition.CS2).key == "full_rifles"
    assert suggest_pattern(500, GameEdition.CS2, pistol=True).key == "pistol_default"
    assert "full_rifles" in explain_all(GameEdition.CS2)
