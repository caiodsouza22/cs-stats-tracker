"""Tests for dashboard, map story, and rating history."""

from roundwire.analysis.dashboard import coaching_dashboard, slim_dashboard
from roundwire.catalog.samples import sample_match
from roundwire.maps.story import execute_density_by_half, map_story
from roundwire.rating.history import build_histories, history_leaderboard


def test_coaching_dashboard(cs2_match):
    dash = coaching_dashboard(cs2_match)
    assert "headline" in dash and "roles" in dash and "export" in dash
    slim = slim_dashboard(cs2_match)
    assert "leaderboards" in slim


def test_map_story(cs2_match):
    story = map_story(cs2_match)
    assert story["card"]["map_name"]
    assert "heatmap" in story
    dens = execute_density_by_half(cs2_match)
    assert "first_half" in dens


def test_rating_history_across_samples():
    matches = [sample_match("cs2_01"), sample_match("cs2_02"), sample_match("cs2_03")]
    histories = build_histories(matches)
    assert histories
    board = history_leaderboard(matches, n=5)
    assert board
    assert "rating" in board[0]
