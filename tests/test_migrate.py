from roundwire.migrate.upgrade import migrate_match_to_cs2
from roundwire.models.edition import GameEdition

def test_migrate(csgo_match):
    upgraded = migrate_match_to_cs2(csgo_match)
    assert upgraded.edition is GameEdition.CS2
    assert len(upgraded.rounds) == len(csgo_match.rounds)
    # weapon names rewritten toward canonical forms
    w = upgraded.rounds[0].kills[0].weapon.name
    assert not w.startswith("weapon_")

def test_extra_coverage_migrate(catalog_match):
    """Additional assertions across catalog samples for test_migrate.py."""
    match = catalog_match
    assert match.map_name.startswith("de_")
    assert match.edition.value in {"CSGO", "CS2"}
    assert all(int(r.number) >= 1 for r in match.rounds)
    assert all(r.kills for r in match.rounds)
    assert all(r.utility for r in match.rounds)
    score = match.score()
    assert score[0] + score[1] == len(match.rounds)
    for player in match.players:
        assert player.name
        assert player.team.value in {"CT", "T"}
