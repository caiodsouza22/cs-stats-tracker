from roundwire.analysis.match_story import build_match_story

def test_story(cs2_match):
    story = build_match_story(cs2_match)
    text = story.render()
    assert cs2_match.map_name in text or "Mirage" in text or "de_mirage" in text
    assert "Economy" in text or "economy" in text.lower() or story.economy_notes
