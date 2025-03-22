from roundwire.io.schema_doc import markdown_schema, all_field_docs
from roundwire.io.validate_dump import validate_dump
import pytest
from roundwire.errors.validation import ValidationError

def test_schema_docs():
    assert "match_id" in markdown_schema()
    assert len(all_field_docs()) > 10

def test_validate_dump(cs2_match):
    validate_dump(cs2_match.to_dict())
    with pytest.raises(Exception):
        validate_dump({"match_id": "x"})
