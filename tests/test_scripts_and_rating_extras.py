from roundwire.catalog import sample_match
from roundwire.maps.execute_scripts import describe_all_scripts, scripts_for_map
from roundwire.migrate.diff import migration_summary
from roundwire.models.team import TeamSide
from roundwire.rating.team_rating import team_average_impact, team_impact_gap
from roundwire.reports.commentary import lines_for, render
from roundwire.reports.rating30_report import rating30_report_table
from roundwire.utility.timing import avg_first_util_ms, early_flash_count


def test_commentary_lines_for_mirage():
    lines = lines_for("de_mirage", side="CT")
    assert lines
    assert render(lines[0].key).startswith("[")


def test_execute_scripts_mirage():
    scripts = scripts_for_map("de_mirage")
    assert scripts
    assert "mirage" in describe_all_scripts()["mirage_a_default"].lower()


def test_migration_summary_csgo():
    summary = migration_summary(sample_match("csgo_01"))
    assert summary["to_edition"] == "CS2"
    assert summary["rounds"] > 0


def test_team_rating_gap():
    match = sample_match("cs2_01")
    assert team_average_impact(match, TeamSide.CT) >= 0
    assert isinstance(team_impact_gap(match), float)


def test_rating30_report_has_header():
    text = rating30_report_table(sample_match("cs2_02"))
    assert "R3.0" in text
    assert "Swing" in text


def test_utility_timing_helpers():
    match = sample_match("cs2_01")
    assert early_flash_count(match) >= 0
    assert avg_first_util_ms(match) >= 0
