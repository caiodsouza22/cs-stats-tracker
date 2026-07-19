"""Docs index for analytics surfaces beyond the core scoreboard."""

PLAYER = """
Player analytics surface
========================

Core entrypoints
----------------
- roundwire.players.profile.build_player_profile
- roundwire.players.roles.infer_role
- roundwire.players.leaderboard.leaderboard / mvp
- roundwire.players.export.match_player_export
- roundwire.analysis.dashboard.coaching_dashboard
- roundwire.players.season.SeasonRoster

CLI
---
- roundwire players <dump.json>
- roundwire players <dump.json> --name lux
- roundwire leaderboard <dump.json> --metric rating|adr|kills|impact

Concepts
--------
Profiles merge combat, economy, utility, weapons, Rating 3.0, impact and tags.
Roles are heuristic (entry/awper/support/lurker/anchor/star/flex).
Form windows label hot/cold stretches over rolling rounds.
Streaks cover kill participation, deathless, win/loss, multi-kill.
Matchups expose head-to-head sheets versus the opposite roster.
SeasonRoster aggregates rating history across many dumps.

Exports
-------
player_pack(match, player_id) -> deep JSON for one player
match_player_export(match) -> roster + leaderboards + roles
text_report_pack / write_report_pack for offline artifacts
"""

PACE = """
Pace and fights
===============
analysis.pace.pace_report — duration bands and time wins
combat.fights.fight_segments — clustered kill bursts
analysis.assist_graph — assist and flash-link networks
"""

ECONOMY = """
Economy story
=============
players.money_story — per-round EQ beats and slopes
economy.swing_report — team bank gaps and full-vs-eco
players.weapon_economy — catalog cost efficiency proxies
players.context_stats — buy/half/pistol context splits
"""


def render_docs() -> str:
    return "\n\n".join([PLAYER.strip(), PACE.strip(), ECONOMY.strip()])
