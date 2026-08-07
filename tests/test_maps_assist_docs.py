"""Tests for callout books, nade lines, assist graph."""

from roundwire.analysis.assist_graph import assist_edges, assist_leaderboard, support_to_star_pairs
from roundwire.maps.callout_books import all_callouts, book_for, indexed_callouts
from roundwire.maps.nade_lines import catalog_size, describe_line, lines_for_map
from roundwire.text.analytics_docs import render_docs


def test_callout_books():
    book = book_for("mirage")
    assert book is not None
    assert "window" in all_callouts("mirage")
    assert indexed_callouts()


def test_nade_lines():
    assert catalog_size() >= 20
    lines = lines_for_map("de_mirage")
    assert lines
    assert "smoke" in describe_line(lines[0].key)


def test_assist_graph(cs2_match):
    edges = assist_edges(cs2_match)
    assert isinstance(edges, list)
    assert isinstance(assist_leaderboard(cs2_match), list)
    assert isinstance(support_to_star_pairs(cs2_match), list)


def test_analytics_docs_render():
    text = render_docs()
    assert "Player analytics" in text
