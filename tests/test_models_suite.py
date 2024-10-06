from roundwire.models.damage import DamageEvent
from roundwire.models.hitgroup import normalize_hitgroup
from roundwire.models.kill import Kill
from roundwire.models.match import Match
from roundwire.models.player import Player
from roundwire.models.round import Round
from roundwire.models.scoreline import Scoreline
from roundwire.models.team import TeamSide
from roundwire.models.timing import trade_window_after
from roundwire.models.utility_event import UtilityEvent, UtilityKind
from roundwire.models.weapon import Weapon
from roundwire.models.win_reason import WinReason
from roundwire.models.edition import GameEdition
from roundwire.types import MatchId, Milliseconds, PlayerId, RoundNumber

def test_models_roundtrip_pieces():
    w = Weapon("ak47")
    assert w.canonical() == "ak47"
    assert w.cost == 2700
    kill = Kill(PlayerId("a"), PlayerId("b"), w, Milliseconds(10), headshot=True)
    assert Kill.from_dict(kill.to_dict()).headshot
    dmg = DamageEvent(PlayerId("a"), PlayerId("b"), w, 50, Milliseconds(9), hitgroup="head")
    assert DamageEvent.from_dict(dmg.to_dict()).damage == 50
    util = UtilityEvent(PlayerId("a"), UtilityKind.FLASH, Milliseconds(5), enemies_flashed=2)
    assert UtilityEvent.from_dict(util.to_dict()).enemies_flashed == 2
    assert normalize_hitgroup("body") == "chest"
    assert WinReason.parse("explosion") is WinReason.BOMB_EXPLODED
    window = trade_window_after(Milliseconds(1000))
    assert window.contains(Milliseconds(1500))
    sl = Scoreline(13, 9, GameEdition.CS2)
    assert sl.leader is TeamSide.CT
    assert sl.is_regulation_complete()

def test_match_helpers(cs2_match: Match):
    assert cs2_match.round_by_number(1) is not None
    assert cs2_match.player_by_name("lux") is not None
    assert cs2_match.rounds_won_by(TeamSide.CT) == cs2_match.score()[0]
    first, second = cs2_match.half_scores()
    assert sum(first) + sum(second) == len(cs2_match.rounds)
