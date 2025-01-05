from roundwire.combat.adr import damage_total
from roundwire.combat.advanced import team_advanced_summary
from roundwire.combat.clutch import clutch_wins
from roundwire.combat.damage_breakdown import armor_damage_total, damage_delta, per_round_damage
from roundwire.combat.duels import one_sided_duels, top_rivalries
from roundwire.combat.first_blood import died_first_count, opening_weapon_freq
from roundwire.combat.formulas import soft_score, team_formula_pack
from roundwire.combat.headshot import headshot_kills
from roundwire.combat.kast import kast_rounds
from roundwire.combat.kd import assist_count, death_count, kill_count
from roundwire.combat.multikill import ace_rounds, multi_kills_in_round
from roundwire.combat.opening import opening_deaths_for, opening_kills_for
from roundwire.combat.summary import format_combat_line, leaders, team_combat_totals
from roundwire.combat.survival import rounds_survived
from roundwire.combat.trades import trades_in_round
from roundwire.models.team import TeamSide

def test_combat_bundle(cs2_match):
    pid = cs2_match.players[0].player_id
    assert damage_total(cs2_match, pid) >= 0
    assert team_advanced_summary(cs2_match, TeamSide.CT)["kills"] >= 0
    assert clutch_wins(cs2_match, pid) >= 0
    assert armor_damage_total(cs2_match, pid) >= 0
    assert isinstance(damage_delta(cs2_match, pid), int)
    assert len(per_round_damage(cs2_match, pid)) == len(cs2_match.rounds)
    assert isinstance(top_rivalries(cs2_match, 3), list)
    assert isinstance(one_sided_duels(cs2_match), list)
    assert died_first_count(cs2_match, pid) >= 0
    assert isinstance(opening_weapon_freq(cs2_match), dict)
    assert soft_score(1.2) > 0
    assert team_formula_pack(cs2_match)
    assert headshot_kills(cs2_match, pid) >= 0
    assert kast_rounds(cs2_match, pid) >= 0
    assert kill_count(cs2_match, pid) >= 0
    assert death_count(cs2_match, pid) >= 0
    assert assist_count(cs2_match, pid) >= 0
    assert isinstance(ace_rounds(cs2_match, pid), list)
    assert isinstance(multi_kills_in_round(cs2_match.rounds[0]), dict)
    assert opening_kills_for(cs2_match, pid) >= 0
    assert opening_deaths_for(cs2_match, pid) >= 0
    lines = leaders(cs2_match, "adr", 2)
    assert len(lines) == 2
    assert format_combat_line(lines[0])
    assert "CT" in team_combat_totals(cs2_match)
    assert rounds_survived(cs2_match, pid) >= 0
    assert isinstance(trades_in_round(cs2_match.rounds[0]), list)
