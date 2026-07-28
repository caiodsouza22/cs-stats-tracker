from roundwire.players.scouting import scouting_report, scouting_report_by_name
from roundwire.stats.correlations import rating_correlations
from roundwire.utility.league import utility_league


def test_scouting_and_correlations(cs2_match):
    pid = cs2_match.players[0].player_id
    text = scouting_report(cs2_match, pid)
    assert cs2_match.players[0].name in text
    assert scouting_report_by_name(cs2_match, cs2_match.players[0].name)
    assert rating_correlations(cs2_match)
    assert utility_league(cs2_match)
