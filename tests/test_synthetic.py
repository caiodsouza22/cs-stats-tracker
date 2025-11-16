from roundwire.catalog.synthetic import build_synthetic_match, SyntheticConfig
from roundwire.models.edition import GameEdition

def test_syn():
    m = build_synthetic_match(SyntheticConfig(
        match_id="x", map_name="de_mirage", edition=GameEdition.CS2,
        target_ct_rounds=13, total_rounds=20,
    ))
    assert m.score()[0] == 13
    assert len(m.players) == 10
