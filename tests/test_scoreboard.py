from roundwire.reports.scoreboard import scoreboard_table
from roundwire.reports.economy_report import economy_summary_table
from roundwire.reports.utility_report import utility_summary_table
from roundwire.reports.round_log import round_log_table

def test_tables(cs2_match):
    sb = scoreboard_table(cs2_match)
    assert "ADR" in sb
    assert cs2_match.team_ct_name in sb
    assert "Economy" in economy_summary_table(cs2_match)
    assert "Utility" in utility_summary_table(cs2_match)
    assert "Rounds" in round_log_table(cs2_match)
