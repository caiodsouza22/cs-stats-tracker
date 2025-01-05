from roundwire.combat.duels import duel_matrix, head_to_head
def test_duels(cs2_match):
    matrix = duel_matrix(cs2_match)
    assert matrix
    a = cs2_match.players[0].player_id
    b = cs2_match.players[5].player_id
    h2h = head_to_head(cs2_match, a, b)
    assert h2h.total >= 0
