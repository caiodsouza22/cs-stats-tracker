from __future__ import annotations

import pytest

from roundwire.catalog import list_samples, sample_match
from roundwire.combat.opening import opening_duels
from roundwire.economy.classify import classify_round_buy
from roundwire.migrate.upgrade import migrate_match_to_cs2
from roundwire.models.edition import GameEdition
from roundwire.rating.impact import impact_table
from roundwire.reports.scoreboard import scoreboard_table

@pytest.mark.parametrize('sample_id', list_samples())
def test_sample_deep(sample_id: str) -> None:
    match = sample_match(sample_id)
    assert len(match.players) == 10
    assert len(match.rounds) >= 20
    ct, t = match.score()
    assert ct + t == len(match.rounds)
    assert opening_duels(match)
    assert impact_table(match)
    assert 'ADR' in scoreboard_table(match)
    for rnd in match.rounds:
        buys = classify_round_buy(rnd, match)
        assert buys['CT'].value
        assert buys['T'].value
        assert rnd.kills
        assert rnd.damage
        assert rnd.utility
        assert rnd.inventories
    if match.edition is GameEdition.CSGO:
        upgraded = migrate_match_to_cs2(match)
        assert upgraded.edition is GameEdition.CS2

def test_sample_player_alive_invariant_0() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_1() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_2() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_3() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_4() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_5() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_6() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_7() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_8() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_9() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_10() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_11() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_12() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_13() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_14() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_15() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_16() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_17() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_18() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_19() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_20() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_21() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_22() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_23() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_24() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_25() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_26() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_27() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_28() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_29() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_30() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_31() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_32() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_33() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_34() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_35() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_36() -> None:
    match = sample_match(list_samples()[0])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_37() -> None:
    match = sample_match(list_samples()[1])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_38() -> None:
    match = sample_match(list_samples()[2])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()

def test_sample_player_alive_invariant_39() -> None:
    match = sample_match(list_samples()[3])
    for rnd in match.rounds:
        for sid in rnd.survivors:
            assert sid in match.player_map()
