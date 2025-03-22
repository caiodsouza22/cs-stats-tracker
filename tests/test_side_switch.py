from roundwire.rules.side_switch import should_switch_sides, switched_players
from roundwire.models.edition import GameEdition
def test_switch(cs2_match):
    assert should_switch_sides(13, GameEdition.CS2)
    switched = switched_players(cs2_match.players)
    assert switched[0].team is cs2_match.players[0].team.opposite()
