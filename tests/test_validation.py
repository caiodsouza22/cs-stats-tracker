import pytest
from roundwire.errors.validation import ValidationError
from roundwire.models.validation import validate_match
from roundwire.catalog.synthetic import default_cs2_match

def test_validate_ok(syn_cs2):
    validate_match(syn_cs2)

def test_validate_empty_players():
    m = default_cs2_match()
    m.players = []
    with pytest.raises(ValidationError):
        validate_match(m)
