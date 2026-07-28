"""Extended player API tests: matchups, opening quality, util timing."""

from roundwire.players.matchups import matchup_summary, team_matchup_matrix
from roundwire.players.opening_quality import opening_quality, opening_tempo
from roundwire.utility.timing_patterns import util_timing_card, util_timing_table


def test_opening_quality(cs2_match):
    pid = cs2_match.players[0].player_id
    card = opening_quality(cs2_match, pid)
    assert card.name
    data = card.to_dict()
    assert "conversion_rate" in data
    tempo = opening_tempo(cs2_match)
    assert "avg_ms" in tempo


def test_matchups(cs2_match):
    pid = cs2_match.players[0].player_id
    summary = matchup_summary(cs2_match, pid)
    assert summary["player"]
    assert isinstance(summary["rows"], list)
    matrix = team_matchup_matrix(cs2_match)
    assert isinstance(matrix, list)


def test_util_timing_patterns(cs2_match):
    pid = cs2_match.players[0].player_id
    card = util_timing_card(cs2_match, pid)
    assert card.name
    assert util_timing_table(cs2_match)
