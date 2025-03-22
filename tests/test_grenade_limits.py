from roundwire.rules.grenade_limits import is_legal_loadout
def test_nades():
    assert is_legal_loadout(["flash", "flash", "smoke", "he"])
    assert not is_legal_loadout(["flash", "flash", "flash"])
