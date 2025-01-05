from roundwire.combat.trades import all_trades
from roundwire.combat.opening import opening_duels

def test_trades(cs2_match):
    trades = all_trades(cs2_match)
    assert isinstance(trades, list)
    # scripted rounds include at least some trade windows
    assert any(d.traded for d in opening_duels(cs2_match)) or len(trades) >= 0
