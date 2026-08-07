"""Additional integration-style tests for weapon economy, pace, context, api."""

from roundwire import api
from roundwire.analysis.pace import pace_report, stall_rounds
from roundwire.players.context_stats import context_report, team_buy_win_table
from roundwire.players.weapon_economy import kill_reward_estimate, weapon_value_table
from roundwire.reports.extended_scoreboard import extended_scoreboard_table, team_blocks


def test_api_exports_smoke():
    assert "build_player_profile" in api.__all__
    assert callable(api.sample_match)


def test_weapon_economy_and_context(cs2_match):
    pid = cs2_match.players[0].player_id
    table = weapon_value_table(cs2_match, pid)
    assert isinstance(table, list)
    assert kill_reward_estimate(cs2_match, pid) >= 0
    report = context_report(cs2_match, pid)
    assert report["buys"] and report["halves"]
    assert team_buy_win_table(cs2_match)


def test_pace_and_extended_scoreboard(cs2_match):
    report = pace_report(cs2_match)
    assert "bands" in report
    assert isinstance(stall_rounds(cs2_match), list)
    text = extended_scoreboard_table(cs2_match)
    assert "R3.0" in text
    blocks = team_blocks(cs2_match)
    assert "Final:" in blocks
