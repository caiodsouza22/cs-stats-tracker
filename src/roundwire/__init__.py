"""roundwire — Counter-Strike 2 match and round analytics."""

from __future__ import annotations

from roundwire.combat.summary import combat_summary
from roundwire.economy.classify import classify_round_buy
from roundwire.io.loaders import load_match, save_match
from roundwire.migrate.upgrade import migrate_match_to_cs2
from roundwire.models.edition import GameEdition
from roundwire.models.match import Match
from roundwire.models.player import Player
from roundwire.models.round import Round
from roundwire.rating.impact import impact_score
from roundwire.rating.rating30 import rating_3_0, rating_3_0_table
from roundwire.reports.scoreboard import scoreboard_table
from roundwire.types import MatchId, PlayerId, RoundNumber, SteamId

__version__ = "0.5.0"

__all__ = [
    "GameEdition",
    "Match",
    "MatchId",
    "Player",
    "PlayerId",
    "Round",
    "RoundNumber",
    "SteamId",
    "__version__",
    "classify_round_buy",
    "combat_summary",
    "impact_score",
    "load_match",
    "migrate_match_to_cs2",
    "rating_3_0",
    "rating_3_0_table",
    "save_match",
    "scoreboard_table",
]
