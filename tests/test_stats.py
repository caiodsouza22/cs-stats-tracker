from roundwire.stats.aggregates import mean, safe_div, clamp
from roundwire.stats.distribution import summarize
def test_stats():
    assert mean([1.0, 3.0]) == 2.0
    assert safe_div(1, 0) == 0.0
    assert clamp(5, 0, 2) == 2
    assert summarize([1.0, 2.0, 3.0])["p50"] == 2.0
