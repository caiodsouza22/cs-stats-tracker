"""Additional coverage for splits, callouts, money, fights, rating cards."""

from pathlib import Path

from roundwire.catalog.analytics import catalog_healthcheck, catalog_mvp_table
from roundwire.catalog.samples import list_samples
from roundwire.combat.fights import fight_segments, man_advantage_rounds
from roundwire.io.batch import summarize_folder
from roundwire.players.callouts import affinity_table, callout_affinity
from roundwire.players.money_story import money_story, poorest_round
from roundwire.players.splits import half_splits, split_report
from roundwire.rating.cards import rating_cards, rating_component_matrix
from roundwire.text.player_blurbs import mvp_blurb, profile_blurb, team_blurb


def test_splits_and_callouts(cs2_match):
    pid = cs2_match.players[0].player_id
    halves = half_splits(cs2_match, pid)
    assert len(halves) == 2
    report = split_report(cs2_match, pid)
    assert report["halves"]
    aff = callout_affinity(cs2_match, pid)
    assert aff.name
    assert affinity_table(cs2_match)


def test_money_and_fights(cs2_match):
    pid = cs2_match.players[0].player_id
    story = money_story(cs2_match, pid)
    assert "beats" in story and "notes" in story
    assert poorest_round(cs2_match, pid) is not None
    segs = fight_segments(cs2_match)
    assert isinstance(segs, list)
    assert isinstance(man_advantage_rounds(cs2_match), list)


def test_rating_cards_and_blurbs(cs2_match):
    cards = rating_cards(cs2_match)
    assert len(cards) == len(cs2_match.players)
    assert cards[0].rank_rating == 1
    assert rating_component_matrix(cs2_match)
    pid = cs2_match.players[0].player_id
    assert cs2_match.players[0].name in profile_blurb(cs2_match, pid)
    blurb = mvp_blurb(cs2_match)
    assert "MVP" in blurb or "mvp" in blurb.lower()
    assert cs2_match.map_name in team_blurb(cs2_match)


def test_catalog_analytics_and_batch(tmp_path: Path):
    from roundwire.catalog.samples import sample_match
    from roundwire.io.loaders import save_match

    match = sample_match("cs2_01")
    target = tmp_path / "m.json"
    save_match(match, target)
    summary = summarize_folder(tmp_path)
    assert summary["matches"] == 1
    health = catalog_healthcheck()
    assert health["ok"] >= 1
    assert catalog_mvp_table()
    assert list_samples()
