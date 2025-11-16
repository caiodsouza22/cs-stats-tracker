from roundwire.reports.economy_report import economy_summary_table
from roundwire.reports.full_report import compact_report, full_text_report
from roundwire.reports.impact_report import impact_report_table
from roundwire.reports.round_log import round_log_table
from roundwire.reports.scoreboard import scoreboard_table
from roundwire.reports.tables import format_table
from roundwire.reports.utility_report import utility_summary_table

def test_all_reports(csgo_match):
    assert "K/D" in scoreboard_table(csgo_match)
    assert "Force" in economy_summary_table(csgo_match)
    assert "Flash" in utility_summary_table(csgo_match)
    assert "Winner" in round_log_table(csgo_match)
    assert "Impact" in impact_report_table(csgo_match)
    assert "Scoreboard" in full_text_report(csgo_match, include_rounds=True)
    assert csgo_match.map_name in compact_report(csgo_match)
    table = format_table(["A", "B"], [["1", "2"], ["3", "4"]])
    assert "A" in table and "3" in table
