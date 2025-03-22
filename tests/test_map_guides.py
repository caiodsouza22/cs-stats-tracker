from roundwire.maps.guides import all_guide_summaries, guide_for, narrative, sites


def test_guides():
    assert guide_for("mirage") is not None
    assert len(all_guide_summaries()) >= 8
    assert "mirage" in narrative("mirage").lower()
    assert sites("nuke")[0] == "A"
