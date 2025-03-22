from roundwire.rules.armor_rules import armor_cost, can_afford_armor
from roundwire.rules.buy_rules import classify_equipment_value
from roundwire.rules.edition_rules import rules_for
from roundwire.rules.economy_constants import constants_for
from roundwire.rules.grenade_limits import is_legal_loadout
from roundwire.rules.kill_rewards import kill_reward_for
from roundwire.rules.map_economy_notes import notes_for_map
from roundwire.rules.money_awards import estimated_round_income, plant_bonus
from roundwire.rules.mr_rules import expected_regulation_cap, is_overtime_eligible
from roundwire.rules.overtime import OVERTIME_MR, overtime_win_target
from roundwire.rules.side_switch import should_switch_sides
from roundwire.rules.weapon_aliases import all_canonical_weapons, alias_count, is_rifle
from roundwire.rules.weapon_groups import CT_RIFLES, all_groups
from roundwire.rules.weapon_profiles import expensive_weapons, profile_for
from roundwire.rules.weapon_reference import force_buy_options, full_buy_primaries
from roundwire.models.buy_type import BuyType
from roundwire.models.edition import GameEdition
from roundwire.models.team import TeamSide

def test_rules_bundle():
    assert constants_for(GameEdition.CS2).full_buy_threshold >= 4000
    assert rules_for(GameEdition.CSGO).mr_label == "MR15"
    assert classify_equipment_value(4500, GameEdition.CS2) is BuyType.FULL
    assert armor_cost(GameEdition.CS2, helmet=False) == 650
    assert can_afford_armor(650, GameEdition.CS2, helmet=False)
    assert is_legal_loadout(["smoke", "he"])
    assert kill_reward_for("nova") == 900
    assert "ct_bias" in notes_for_map("de_inferno")
    assert estimated_round_income(GameEdition.CS2, won=False, consecutive_losses=2, kill_weapons=[]) >= 1400
    assert plant_bonus() == 300
    assert expected_regulation_cap(GameEdition.CS2) == 24
    assert is_overtime_eligible(12, 12, GameEdition.CS2)
    assert OVERTIME_MR == 3
    assert overtime_win_target(GameEdition.CSGO, 1) == 18
    assert should_switch_sides(16, GameEdition.CSGO)
    assert "ak47" in all_canonical_weapons()
    assert alias_count() > len(all_canonical_weapons())
    assert is_rifle("weapon_ak47")
    assert "m4a1" in CT_RIFLES
    assert "smg" in all_groups()
    assert profile_for("awp").cost == 4750
    assert expensive_weapons(4000)
    assert full_buy_primaries("T")
    assert force_buy_options("CT")
