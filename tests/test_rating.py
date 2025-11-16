from roundwire.models.edition import GameEdition
from roundwire.rating.impact import impact_score, impact_table, impact_weights


def test_impact(cs2_match):
    table = impact_table(cs2_match)
    assert len(table) == 10
    assert table[0].impact >= table[-1].impact
    pid = cs2_match.players[0].player_id
    assert impact_score(cs2_match, pid) >= 0.0


def test_cs2_weights_prefer_adr():
    cs2 = impact_weights(GameEdition.CS2)
    csgo = impact_weights(GameEdition.CSGO)
    assert cs2.adr > csgo.adr
    assert abs((cs2.kpr + cs2.adr + cs2.survival + cs2.opening) - 0.98) < 1e-9
