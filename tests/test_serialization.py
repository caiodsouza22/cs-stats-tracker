from roundwire.models.serialization import match_from_json, match_to_json, compact_match_view
def test_serde(cs2_match):
    text = match_to_json(cs2_match)
    again = match_from_json(text)
    assert again.match_id == cs2_match.match_id
    view = compact_match_view(cs2_match)
    assert view["score"]["CT"] + view["score"]["T"] == len(cs2_match.rounds)
