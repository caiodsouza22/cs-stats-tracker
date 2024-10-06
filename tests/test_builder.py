from roundwire.models.builder import MatchBuilder
from roundwire.models.edition import GameEdition
from roundwire.models.team import TeamSide

def test_builder():
    m = (
        MatchBuilder("b1", "de_mirage", GameEdition.CS2)
        .teams("A", "B")
        .add_player("p1", "Alice", TeamSide.CT)
        .add_player("p2", "Bob", TeamSide.T)
        .empty_round(1, TeamSide.CT)
        .build()
    )
    assert m.score() == (1, 0)
