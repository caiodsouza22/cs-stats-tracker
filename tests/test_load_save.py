from pathlib import Path
from roundwire.io.loaders import load_match, save_match
from roundwire.catalog import sample_match

def test_roundtrip(tmp_path: Path, cs2_match):
    path = tmp_path / "m.json"
    save_match(cs2_match, path)
    loaded = load_match(path)
    assert loaded.match_id == cs2_match.match_id
    assert loaded.score() == cs2_match.score()
    assert len(loaded.rounds) == len(cs2_match.rounds)

def test_sample_files_exist():
    root = Path(__file__).resolve().parents[1]
    for name in ("match_csgo_01.json", "match_cs2_01.json"):
        assert (root / "examples" / name).is_file()
