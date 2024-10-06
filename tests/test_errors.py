from roundwire.errors.messages import missing_field, unknown_weapon


def test_errors():
    assert "foo" in missing_field("foo")
    assert "ak" in unknown_weapon("ak")
