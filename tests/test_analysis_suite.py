from roundwire.analysis.anti_eco import anti_eco_cases, anti_eco_success_rate
from roundwire.analysis.awp_rounds import awp_kills, rounds_with_awp_kill
from roundwire.analysis.buy_damage import force_damage_avg, full_damage_avg
from roundwire.analysis.coaching import all_advice, round_advice
from roundwire.analysis.execute_proxy import early_t_utility, execute_score
from roundwire.analysis.gaps import cash_gaps, equipment_gaps
from roundwire.analysis.match_overview import match_overview
from roundwire.analysis.opening_economy import eco_openers, full_buy_opening_conversion
from roundwire.analysis.pistol_conversion import pistol_winners
from roundwire.analysis.retake_proxy import post_plant_ct_utility, retake_flash_density
from roundwire.analysis.round_timing_bands import late_kill_share
from roundwire.analysis.trade_quality import trade_rate_by_side

def test_analysis_bundle(cs2_match):
    assert 0 <= anti_eco_success_rate(cs2_match) <= 1
    assert isinstance(anti_eco_cases(cs2_match), list)
    assert awp_kills(cs2_match) >= 0
    assert isinstance(rounds_with_awp_kill(cs2_match), list)
    assert full_damage_avg(cs2_match) >= 0
    assert force_damage_avg(cs2_match) >= 0
    assert "default" in all_advice(cs2_match)
    assert round_advice(cs2_match, 2)
    assert early_t_utility(cs2_match)
    assert execute_score(cs2_match) >= 0
    assert len(cash_gaps(cs2_match)) == len(cs2_match.rounds)
    assert len(equipment_gaps(cs2_match)) == len(cs2_match.rounds)
    ov = match_overview(cs2_match)
    assert ov["edition"] == "CS2"
    assert 0 <= full_buy_opening_conversion(cs2_match) <= 1
    assert isinstance(eco_openers(cs2_match), list)
    assert pistol_winners(cs2_match)
    assert post_plant_ct_utility(cs2_match) >= 0
    assert retake_flash_density(cs2_match) >= 0
    assert 0 <= late_kill_share(cs2_match) <= 1
    assert set(trade_rate_by_side(cs2_match)) == {"CT", "T"}
