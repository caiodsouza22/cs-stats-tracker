from roundwire.analysis.match_overview import match_overview
def test_overview(cs2_match):
    ov = match_overview(cs2_match)
    assert ov["map"] == cs2_match.map_name
    assert ov["top_fragger"]
