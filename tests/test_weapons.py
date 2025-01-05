from roundwire.rules.weapon_aliases import canonical_weapon_name, weapon_cost
from roundwire.migrate.weapons import rewrite_weapon_name

def test_aliases():
    assert canonical_weapon_name("weapon_ak47") == "ak47"
    assert canonical_weapon_name("usp-s") == "usp_silencer"
    assert canonical_weapon_name("ck75") == "fiveseven"
    assert weapon_cost("awp") == 4750

def test_rewrite():
    assert rewrite_weapon_name("weapon_glock") == "glock"
