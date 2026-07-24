"""Public facade re-exports for notebooks and downstream apps."""

from __future__ import annotations

# Combat
from roundwire.combat.summary import combat_summary
from roundwire.combat.fights import fight_segments
from roundwire.combat.damage_timing import damage_timing_summary

# Economy
from roundwire.economy.classify import classify_round_buy
from roundwire.economy.swing_report import economy_swing_report

# Players
from roundwire.players.profile import build_all_profiles, build_player_profile, profile_table
from roundwire.players.roles import infer_role, role_table
from roundwire.players.leaderboard import leaderboard, mvp
from roundwire.players.export import match_player_export, player_pack
from roundwire.players.season import SeasonRoster, season_from_catalog
from roundwire.players.compare import compare_players
from roundwire.players.form import form_summary
from roundwire.players.streaks import streak_report
from roundwire.players.matchups import matchup_summary
from roundwire.players.opening_quality import opening_quality
from roundwire.players.money_story import money_story
from roundwire.players.splits import split_report
from roundwire.players.context_stats import context_report

# Rating
from roundwire.rating.impact import impact_score, impact_table
from roundwire.rating.rating30 import rating_3_0, rating_3_0_table
from roundwire.rating.cards import rating_cards
from roundwire.rating.history import build_histories

# Analysis
from roundwire.analysis.dashboard import coaching_dashboard, slim_dashboard
from roundwire.analysis.entry_fragging import entry_table
from roundwire.analysis.support_score import support_table
from roundwire.analysis.round_impact import impact_leaderboard
from roundwire.analysis.match_story import build_match_story

# Maps / IO
from roundwire.maps.story import map_story
from roundwire.io.batch import load_matches, summarize_folder
from roundwire.io.loaders import load_match, save_match

# Reports
from roundwire.reports.player_report import player_report_table, player_detail_report
from roundwire.reports.pack import text_report_pack, json_report_pack
from roundwire.reports.scoreboard import scoreboard_table

# Catalog
from roundwire.catalog.samples import sample_match, list_samples
from roundwire.catalog.analytics import catalog_healthcheck

# Series
from roundwire.series_analytics import SeriesBook, series_summary

__all__ = [
    "SeasonRoster",
    "SeriesBook",
    "build_all_profiles",
    "build_histories",
    "build_match_story",
    "build_player_profile",
    "catalog_healthcheck",
    "classify_round_buy",
    "coaching_dashboard",
    "combat_summary",
    "compare_players",
    "context_report",
    "damage_timing_summary",
    "economy_swing_report",
    "entry_table",
    "fight_segments",
    "form_summary",
    "impact_leaderboard",
    "impact_score",
    "impact_table",
    "infer_role",
    "json_report_pack",
    "leaderboard",
    "list_samples",
    "load_match",
    "load_matches",
    "map_story",
    "match_player_export",
    "matchup_summary",
    "money_story",
    "mvp",
    "opening_quality",
    "player_detail_report",
    "player_pack",
    "player_report_table",
    "profile_table",
    "rating_3_0",
    "rating_3_0_table",
    "rating_cards",
    "role_table",
    "sample_match",
    "save_match",
    "scoreboard_table",
    "season_from_catalog",
    "series_summary",
    "slim_dashboard",
    "split_report",
    "streak_report",
    "summarize_folder",
    "support_table",
    "text_report_pack",
]
