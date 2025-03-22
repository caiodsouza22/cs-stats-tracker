from roundwire.cli import main
from roundwire.io.loaders import save_match

def test_cli_economy(cs2_match, tmp_path, capsys):
    path = tmp_path / "m.json"
    save_match(cs2_match, path)
    assert main(["economy", str(path)]) == 0
    assert "Full" in capsys.readouterr().out

def test_cli_utility(cs2_match, tmp_path, capsys):
    path = tmp_path / "m.json"
    save_match(cs2_match, path)
    assert main(["utility", str(path)]) == 0
    assert "Flash" in capsys.readouterr().out
