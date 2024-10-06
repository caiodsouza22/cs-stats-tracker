def test_half(cs2_match):
    first, second = cs2_match.half_scores()
    assert sum(first) + sum(second) == len(cs2_match.rounds)
