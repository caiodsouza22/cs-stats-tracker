"""Tests for season roster, report packs, and dump enrichment."""

from pathlib import Path

from roundwire.catalog.samples import sample_match
from roundwire.io.enrich import enrich_round_damage, enrich_round_survivors, summarize_sparsity
from roundwire.players.season import season_from_catalog, top_map_specialists
from roundwire.reports.pack import season_report_pack, text_report_pack, write_report_pack


def test_season_from_catalog():
    roster = season_from_catalog()
    snap = roster.snapshot()
    assert snap["matches"] >= 3
    assert snap["leaderboard"]
    assert top_map_specialists(roster)


def test_report_packs(cs2_match, tmp_path: Path):
    text = text_report_pack(cs2_match)
    assert "Scoreboard" in text or "Players" in text
    paths = write_report_pack(cs2_match, tmp_path / "out")
    assert Path(paths["text"]).exists()
    assert Path(paths["json"]).exists()
    season = season_report_pack()
    assert "snapshot" in season


def test_enrichment_helpers(cs2_match):
    sparse = summarize_sparsity(cs2_match)
    assert sparse["rounds"] > 0
    filled = enrich_round_survivors(cs2_match)
    assert len(filled.rounds) == len(cs2_match.rounds)
    dmg = enrich_round_damage(sample_match("cs2_02"))
    assert len(dmg.rounds) > 0
