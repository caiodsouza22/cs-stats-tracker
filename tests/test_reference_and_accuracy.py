"""Batch of lightweight regression tests to lock public player APIs."""

from roundwire.combat.accuracy import accuracy_table
from roundwire.maps.callout_books import book_for
from roundwire.maps.nade_lines import lines_for_side
from roundwire.players.context_stats import buy_context_stats
from roundwire.players.weapon_economy import rifle_vs_eco_weapon_mix
from roundwire.rules.damage_tables import catalog_ttk, estimate_damage, ttk_table


def test_damage_tables():
    est = estimate_damage(36, "head", armored=True, helmet=True)
    assert est.after_armor > 0
    assert ttk_table("ak47")["head"] >= 1
    assert "awp" in catalog_ttk()


def test_accuracy_and_context(cs2_match):
    assert accuracy_table(cs2_match)
    pid = cs2_match.players[0].player_id
    assert buy_context_stats(cs2_match, pid)
    mix = rifle_vs_eco_weapon_mix(cs2_match, pid)
    assert "rifle_on_full" in mix


def test_map_reference_data():
    assert book_for("anubis") is not None
    assert lines_for_side("mirage", "T")
