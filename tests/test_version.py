from roundwire import __version__
from roundwire.catalog import default_sample_id, sample_match


def test_version():
    assert __version__ == "0.5.0"


def test_default_sample_is_cs2():
    assert default_sample_id() == "cs2_01"
    match = sample_match()
    assert match.edition.value == "CS2"
