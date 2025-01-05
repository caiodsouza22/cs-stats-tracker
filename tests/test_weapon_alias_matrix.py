from __future__ import annotations

import pytest

from roundwire.rules.weapon_aliases import canonical_weapon_name, weapon_cost, weapon_slot
from roundwire.migrate.weapons import rewrite_weapon_name
from roundwire.rules.weapon_reference import describe_weapon, get_ref

@pytest.mark.parametrize('raw,canon', [
    ('weapon_ak47', 'ak47'),
    ('AK-47', 'ak47'),
    ('weapon_m4a1_silencer', 'm4a1_silencer'),
    ('m4a1-s', 'm4a1_silencer'),
    ('usp-s', 'usp_silencer'),
    ('weapon_usp_silencer', 'usp_silencer'),
    ('ck75', 'fiveseven'),
    ('weapon_deagle', 'deagle'),
    ('scout', 'ssg08'),
    ('weapon_awp', 'awp'),
    ('glock18', 'glock'),
    ('weapon_mac10', 'mac10'),
    ('ump', 'ump45'),
    ('weapon_hegrenade', 'hegrenade'),
    ('flash', 'flashbang'),
    ('weapon_smokegrenade', 'smokegrenade'),
    ('molotov', 'molotov'),
    ('incendiary', 'incgrenade'),
    ('zeus', 'taser'),
    ('r8', 'revolver'),
])
def test_alias_matrix(raw: str, canon: str) -> None:
    assert canonical_weapon_name(raw) == canon
    assert rewrite_weapon_name(raw) == canon
    assert get_ref(canon) is not None
    assert weapon_cost(canon) >= 0
    assert weapon_slot(canon)
    assert canon in describe_weapon(canon)

def test_weapon_slot_consistency_0() -> None:
    canon = 'ak47'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_1() -> None:
    canon = 'ak47'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_2() -> None:
    canon = 'm4a1_silencer'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_3() -> None:
    canon = 'm4a1_silencer'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_4() -> None:
    canon = 'usp_silencer'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_5() -> None:
    canon = 'usp_silencer'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_6() -> None:
    canon = 'fiveseven'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_7() -> None:
    canon = 'deagle'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_8() -> None:
    canon = 'ssg08'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_9() -> None:
    canon = 'awp'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_10() -> None:
    canon = 'glock'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_11() -> None:
    canon = 'mac10'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_12() -> None:
    canon = 'ump45'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_13() -> None:
    canon = 'hegrenade'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_14() -> None:
    canon = 'flashbang'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_15() -> None:
    canon = 'smokegrenade'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_16() -> None:
    canon = 'molotov'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_17() -> None:
    canon = 'incgrenade'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_18() -> None:
    canon = 'taser'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_19() -> None:
    canon = 'revolver'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_20() -> None:
    canon = 'ak47'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_21() -> None:
    canon = 'ak47'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_22() -> None:
    canon = 'm4a1_silencer'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_23() -> None:
    canon = 'm4a1_silencer'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_24() -> None:
    canon = 'usp_silencer'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_25() -> None:
    canon = 'usp_silencer'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_26() -> None:
    canon = 'fiveseven'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_27() -> None:
    canon = 'deagle'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_28() -> None:
    canon = 'ssg08'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost

def test_weapon_slot_consistency_29() -> None:
    canon = 'awp'
    ref = get_ref(canon)
    assert ref is not None
    assert weapon_slot(canon) == ref.slot
    assert weapon_cost(canon) == ref.cost
