from roundwire.reports.full_report import full_text_report, compact_report

def test_report(cs2_match):
    text = full_text_report(cs2_match, include_rounds=False)
    assert "Scoreboard" in text
    assert compact_report(cs2_match)
