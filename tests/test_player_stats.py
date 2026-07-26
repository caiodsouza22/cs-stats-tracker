"""Tests for per-player analytics package."""

from roundwire.analysis.entry_fragging import best_entry, entry_table
from roundwire.analysis.round_impact import impact_leaderboard, round_impacts
from roundwire.analysis.support_score import best_support, support_table
from roundwire.catalog import sample_match
from roundwire.players.clutch_book import clutch_book
from roundwire.players.compare import compare_players, roster_comparison
from roundwire.players.export import match_player_export, player_pack
from roundwire.players.form import current_form, form_summary
from roundwire.players.leaderboard import available_metrics, leaderboard, mvp
from roundwire.players.profile import build_all_profiles, build_player_profile, profile_table
from roundwire.players.roles import infer_role, role_table
from roundwire.players.round_card import player_round_log
from roundwire.players.streaks import streak_report
from roundwire.players.timeline import player_timeline
from roundwire.players.weapon_stats import weapon_breakdown
from roundwire.reports.player_report import player_detail_report, player_report_table
from roundwire.series_analytics import SeriesBook
from roundwire.stats.matrix import pearson
from roundwire.stats.normalize import minmax, zscores
from roundwire.stats.rolling import rolling_mean


def test_profiles_cover_roster(cs2_match):
    profiles = build_all_profiles(cs2_match)
    assert len(profiles) == len(cs2_match.players)
    assert profiles[0].rating_3_0 >= profiles[-1].rating_3_0
    row = profile_table(cs2_match)[0]
    assert "rating" in row and "name" in row


def test_single_profile_fields(cs2_match):
    pid = cs2_match.players[0].player_id
    profile = build_player_profile(cs2_match, pid)
    data = profile.to_dict()
    assert data["kills"] >= 0
    assert "economy" in data and "utility" in data and "weapons" in data
    assert isinstance(data["tags"], list)


def test_roles_and_leaderboard(cs2_match):
    roles = role_table(cs2_match)
    assert len(roles) == len(cs2_match.players)
    assert roles[0]["primary"]
    board = leaderboard(cs2_match, "kills", limit=3)
    assert board[0].rank == 1
    assert mvp(cs2_match) is not None
    assert "rating" in available_metrics()


def test_round_cards_form_streaks(cs2_match):
    pid = cs2_match.players[0].player_id
    cards = player_round_log(cs2_match, pid)
    assert len(cards) == len(cs2_match.rounds)
    summary = form_summary(cs2_match, pid)
    assert "latest" in summary
    assert current_form(cs2_match, pid) is None or current_form(cs2_match, pid).label
    streaks = streak_report(cs2_match, pid)
    assert "win" in streaks and "deathless" in streaks


def test_weapons_timeline_clutch_export(cs2_match):
    pid = cs2_match.players[0].player_id
    weapons = weapon_breakdown(cs2_match, pid)
    assert weapons.unique_weapons >= 0
    assert player_timeline(cs2_match, pid) is not None
    book = clutch_book(cs2_match, pid)
    assert "solo_wr" in book
    pack = player_pack(cs2_match, pid)
    assert pack["profile"]["player_id"] == str(pid)
    export = match_player_export(cs2_match)
    assert export["mvp"] is not None
    assert len(export["players"]) == len(cs2_match.players)


def test_compare_and_reports(cs2_match):
    a, b = cs2_match.players[0], cs2_match.players[1]
    cmp = compare_players(cs2_match, a.player_id, b.player_id)
    assert cmp.left_name and cmp.right_name
    assert roster_comparison(cs2_match)
    text = player_report_table(cs2_match)
    assert "R3.0" in text or "Player" in text
    detail = player_detail_report(cs2_match, a.name)
    assert a.name in detail


def test_entry_support_round_impact(cs2_match):
    assert entry_table(cs2_match)
    assert best_entry(cs2_match) is not None
    assert support_table(cs2_match)
    assert best_support(cs2_match) is not None
    pid = cs2_match.players[0].player_id
    impacts = round_impacts(cs2_match, pid)
    assert len(impacts) == len(cs2_match.rounds)
    assert impact_leaderboard(cs2_match)


def test_series_book_and_stats_helpers(cs2_match):
    book = SeriesBook()
    book.ingest_match(cs2_match)
    book.ingest_match(sample_match("cs2_02"))
    assert book.as_rows()
    assert rolling_mean([1.0, 2.0, 3.0, 4.0], 2)[-1] == 3.5
    assert minmax([0.0, 5.0, 10.0]) == [0.0, 0.5, 1.0]
    zs = zscores([1.0, 1.0, 1.0])
    assert zs == [0.0, 0.0, 0.0]
    assert pearson([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]) > 0.99


def test_role_inference_smoke(cs2_match):
    for player in cs2_match.players:
        role = infer_role(cs2_match, player.player_id)
        assert role.primary.value
        assert role.scores
