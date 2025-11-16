from roundwire import load_match, migrate_match_to_cs2, scoreboard_table, impact_score, classify_round_buy
from roundwire.catalog import sample_match
from roundwire.io.loaders import save_match
from roundwire.reports.economy_report import economy_summary_table
from roundwire.reports.utility_report import utility_summary_table
from roundwire.analysis.match_story import build_match_story
from roundwire.models.edition import GameEdition

def test_end_to_end(tmp_path):
    match = sample_match("csgo_01")
    path = tmp_path / "m.json"
    save_match(match, path)
    loaded = load_match(path)
    assert loaded.edition is GameEdition.CSGO
    upgraded = migrate_match_to_cs2(loaded)
    assert upgraded.edition is GameEdition.CS2
    text = scoreboard_table(upgraded)
    assert "Impact" in text
    assert economy_summary_table(upgraded)
    assert utility_summary_table(upgraded)
    story = build_match_story(upgraded)
    assert story.headline
    buys = classify_round_buy(upgraded.rounds[0], upgraded)
    assert "CT" in buys
    for p in upgraded.players:
        assert impact_score(upgraded, p.player_id) >= 0
