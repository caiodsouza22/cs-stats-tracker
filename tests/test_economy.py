from roundwire.economy.classify import classify_round_buy, buy_histogram
from roundwire.economy.pistol import is_pistol_round
from roundwire.models.team import TeamSide

def test_classify(cs2_match):
    buys = classify_round_buy(cs2_match.rounds[0], cs2_match)
    assert set(buys) == {"CT", "T"}
    assert is_pistol_round(cs2_match.rounds[0], cs2_match.edition)
    hist = buy_histogram(cs2_match, TeamSide.CT)
    assert sum(hist.values()) == len(cs2_match.rounds)

def test_extra_coverage_economy(catalog_match):
    """Additional assertions across catalog samples for test_economy.py."""
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
