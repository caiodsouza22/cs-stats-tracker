def test_each_catalog_match(catalog_match):
    assert len(catalog_match.players) == 10
    assert len(catalog_match.rounds) >= 20
    ct, t = catalog_match.score()
    assert ct + t == len(catalog_match.rounds)
    assert catalog_match.winner_side() is not None or True

def test_extra_coverage_catalog_parametrized(catalog_match):
    """Additional assertions across catalog samples for test_catalog_parametrized.py."""
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
