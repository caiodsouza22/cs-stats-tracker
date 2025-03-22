from roundwire.cli import main

def test_cli_scoreboard(cs2_match, tmp_path, capsys):
    from roundwire.io.loaders import save_match
    path = tmp_path / "m.json"
    save_match(cs2_match, path)
    assert main(["scoreboard", str(path)]) == 0
    out = capsys.readouterr().out
    assert "ADR" in out

def test_cli_migrate(csgo_match, tmp_path, capsys):
    from roundwire.io.loaders import save_match
    path = tmp_path / "m.json"
    save_match(csgo_match, path)
    assert main(["migrate", str(path), "--summary"]) == 0
    assert "CS2" in capsys.readouterr().out
