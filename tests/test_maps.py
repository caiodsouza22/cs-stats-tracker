from roundwire.maps.pool import normalize_map_name, is_active_pool
from roundwire.maps.side_pref import side_preference_label
from roundwire.maps.guides import guide_for, format_guide

def test_maps(cs2_match):
    assert normalize_map_name("mirage") == "de_mirage"
    assert is_active_pool("de_mirage")
    assert side_preference_label(cs2_match) in {"CT", "T", "balanced"}
    assert guide_for("de_nuke") is not None
    assert "de_nuke" in format_guide("nuke")
