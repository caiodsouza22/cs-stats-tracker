from __future__ import annotations

from roundwire.analysis.annotations import annotate_match, explain_labels, label_histogram
from roundwire.analysis.scenarios import describe_all, high_tension, scenarios_for_map
from roundwire.catalog import sample_match


def test_annotations_cs2() -> None:
    match = sample_match("cs2_01")
    anns = annotate_match(match)
    assert len(anns) == len(match.rounds)
    hist = label_histogram(match)
    assert isinstance(hist, dict)
    if anns[0].labels:
        assert explain_labels(anns[0].labels)


def test_scenarios_library() -> None:
    all_desc = describe_all()
    assert len(all_desc) >= 8
    assert scenarios_for_map("de_mirage")
    assert high_tension(5)
    key, text = next(iter(all_desc.items()))
    assert key
    assert "wins via" in text or "tension=" in text
