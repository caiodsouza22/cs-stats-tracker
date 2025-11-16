from roundwire.catalog import sample_match
from roundwire.models.edition import GameEdition
from roundwire.rating.rating30 import (
    DEFAULT_RATING30_WEIGHTS,
    rating_3_0,
    rating_3_0_table,
)
from roundwire.rating.round_swing import round_swing_total, win_prob_ct


def test_rating_3_0_table_sorted():
    match = sample_match("cs2_01")
    table = rating_3_0_table(match)
    assert len(table) == 10
    assert table[0].rating >= table[-1].rating
    assert all(row.rating >= 0 for row in table)


def test_rating_3_0_weights_sum():
    w = DEFAULT_RATING30_WEIGHTS
    total = w.kills + w.round_swing + w.damage + w.survival + w.kast + w.multi_kills
    assert abs(total - 1.0) < 1e-9
    assert w.kills == 0.25
    assert w.round_swing == 0.33


def test_round_swing_runs_on_cs2():
    match = sample_match("cs2_03")
    pid = match.players[0].player_id
    total = round_swing_total(match, pid)
    assert isinstance(total, float)
    assert rating_3_0(match, pid) > 0


def test_win_prob_ct_monotonic_in_man_count():
    low = win_prob_ct(alive_ct=2, alive_t=4, bomb_planted=False, eq_ct=4000, eq_t=4000)
    high = win_prob_ct(alive_ct=4, alive_t=2, bomb_planted=False, eq_ct=4000, eq_t=4000)
    assert high > low


def test_cs2_edition_default_sample_has_rating():
    match = sample_match()
    assert match.edition is GameEdition.CS2
    assert rating_3_0_table(match)[0].name
