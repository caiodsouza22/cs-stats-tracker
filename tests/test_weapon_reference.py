from roundwire.rules.weapon_reference import get_ref, all_notes, budget_weapons

def test_refs():
    assert get_ref("ak47") is not None
    assert len(all_notes()) >= 40
    assert budget_weapons(1000, "pistol")
