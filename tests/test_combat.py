from roundwire.combat.summary import combat_summary
from roundwire.combat.opening import opening_duels
from roundwire.combat.adr import adr_by_player

def test_combat(cs2_match):
    lines = combat_summary(cs2_match)
    assert len(lines) == 10
    assert lines[0].kills >= lines[-1].kills
    duels = opening_duels(cs2_match)
    assert len(duels) == len(cs2_match.rounds)
    adr = adr_by_player(cs2_match)
    assert len(adr) == 10

def test_extra_coverage_combat(catalog_match):
    """Additional assertions across catalog samples for test_combat.py."""
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
