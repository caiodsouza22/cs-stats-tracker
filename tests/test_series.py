from roundwire.models.series import Series
from roundwire.catalog import sample_match

def test_series():
    s = Series("s1", "Aurora", "Nimbus", best_of=3, maps=[sample_match("cs2_01")])
    a, b = s.map_wins()
    assert a + b <= 1
