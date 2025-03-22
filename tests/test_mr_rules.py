from roundwire.rules.mr_rules import half_length, is_halftime
from roundwire.models.edition import GameEdition

def test_mr():
    assert half_length(GameEdition.CSGO) == 15
    assert half_length(GameEdition.CS2) == 12
    assert is_halftime(12, GameEdition.CS2)
