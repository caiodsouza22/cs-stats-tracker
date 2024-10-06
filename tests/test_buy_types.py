from roundwire.rules.buy_rules import classify_equipment_value
from roundwire.models.buy_type import BuyType
from roundwire.models.edition import GameEdition

def test_buy_rules():
    assert classify_equipment_value(5000, GameEdition.CS2) is BuyType.FULL
    assert classify_equipment_value(500, GameEdition.CS2) is BuyType.ECO
    assert classify_equipment_value(100, GameEdition.CS2, pistol_round=True) is BuyType.PISTOL
