from roundwire.catalog import list_samples, sample_match
from roundwire.models.edition import GameEdition


def test_catalog_lists_cs2_first():
    samples = list_samples()
    assert samples[0].startswith("cs2_")
    assert set(samples) >= {"cs2_01", "cs2_02", "cs2_03", "csgo_01", "csgo_02"}
    assert sample_match("csgo_01").edition is GameEdition.CSGO
    assert sample_match("cs2_03").edition is GameEdition.CS2
    assert sample_match("cs2_03").map_name == "de_ancient"


def test_catalog_match_has_rounds(catalog_match):
    match = catalog_match
    assert match.event_name
    assert match.team_ct_name and match.team_t_name
    assert len(match.rounds) >= 1
    winners = {r.winner.value for r in match.rounds}
    assert winners <= {"CT", "T"}
