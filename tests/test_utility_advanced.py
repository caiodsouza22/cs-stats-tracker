from roundwire.utility.advanced import utility_cards, team_utility_spend

def test_util_adv(cs2_match):
    cards = utility_cards(cs2_match)
    assert cards[0].value_score >= cards[-1].value_score
    spend = team_utility_spend(cs2_match)
    assert spend["CT"] > 0 and spend["T"] > 0
