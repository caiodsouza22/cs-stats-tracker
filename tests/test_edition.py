import pytest
from roundwire.models.edition import GameEdition
from roundwire.errors.domain import InvalidEditionError

def test_mr_labels():
    assert GameEdition.CSGO.mr_label == "MR15"
    assert GameEdition.CS2.mr_label == "MR12"
    assert GameEdition.CSGO.win_threshold == 16
    assert GameEdition.CS2.win_threshold == 13

def test_parse():
    assert GameEdition.parse("csgo") is GameEdition.CSGO
    assert GameEdition.parse("CS2") is GameEdition.CS2
    with pytest.raises(InvalidEditionError):
        GameEdition.parse("cs3")
