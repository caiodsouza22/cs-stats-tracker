from roundwire.rating.extended import extended_table

def test_ext(cs2_match):
    rows = extended_table(cs2_match)
    assert rows[0].composite >= rows[-1].composite
