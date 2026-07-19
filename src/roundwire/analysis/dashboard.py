"""Full coaching dashboard aggregating player and match signals."""

from __future__ import annotations

from roundwire.analysis.entry_fragging import entry_table
from roundwire.analysis.match_overview import match_overview
from roundwire.analysis.round_impact import impact_leaderboard, match_round_mvp
from roundwire.analysis.support_score import support_table
from roundwire.combat.fights import conversion_after_first_blood, man_advantage_rounds
from roundwire.economy.swing_report import economy_swing_report, player_economy_briefs
from roundwire.models.match import Match
from roundwire.players.export import match_player_export
from roundwire.players.form import form_summary
from roundwire.players.leaderboard import dual_mvp, multi_leaderboard
from roundwire.players.profile import build_all_profiles, team_profile_averages
from roundwire.players.roles import role_counts, role_table
from roundwire.models.team import TeamSide
from roundwire.rating.cards import normalized_rating_vector, rating_cards, rating_component_matrix
from roundwire.text.player_blurbs import mvp_blurb, team_blurb


def coaching_dashboard(match: Match) -> dict[str, object]:
    """One-shot dict suitable for UI / notebook export."""
    profiles = build_all_profiles(match)
    return {
        "headline": team_blurb(match),
        "mvp_line": mvp_blurb(match),
        "overview": match_overview(match),
        "dual_mvp": {
            key: (row.to_dict() if row else None)
            for key, row in dual_mvp(match).items()
        },
        "roles": role_table(match),
        "role_counts": role_counts(match),
        "leaderboards": multi_leaderboard(match),
        "rating_cards": [c.to_dict() for c in rating_cards(match)],
        "rating_components": rating_component_matrix(match),
        "rating_norms": normalized_rating_vector(match),
        "entry": entry_table(match),
        "support": support_table(match),
        "impact_leaders": impact_leaderboard(match),
        "round_mvps": match_round_mvp(match)[:12],
        "economy": economy_swing_report(match),
        "economy_briefs": player_economy_briefs(match),
        "man_advantage": man_advantage_rounds(match),
        "opening_conversion": conversion_after_first_blood(match),
        "team_averages": {
            "CT": team_profile_averages(match, TeamSide.CT),
            "T": team_profile_averages(match, TeamSide.T),
        },
        "player_form": {
            p.name: form_summary(match, p.player_id) for p in match.players
        },
        "export": match_player_export(match),
        "top_profile": profiles[0].to_dict() if profiles else None,
    }


def dashboard_keys(match: Match) -> list[str]:
    return sorted(coaching_dashboard(match))


def slim_dashboard(match: Match) -> dict[str, object]:
    full = coaching_dashboard(match)
    return {
        "headline": full["headline"],
        "mvp_line": full["mvp_line"],
        "roles": full["roles"],
        "leaderboards": {
            "rating": full["leaderboards"].get("rating", [])[:5],
            "adr": full["leaderboards"].get("adr", [])[:5],
        },
        "team_averages": full["team_averages"],
        "opening_conversion": full["opening_conversion"],
    }


def player_coach_card(match: Match, name: str) -> dict[str, object] | None:
    from roundwire.players.export import player_pack_by_name
    from roundwire.players.matchups import matchup_summary
    from roundwire.players.opening_quality import opening_quality
    from roundwire.players.splits import split_report
    from roundwire.types import PlayerId

    pack = player_pack_by_name(match, name)
    if pack is None:
        return None
    player = match.player_by_name(name)
    if player is None:
        return None
    pid = player.player_id
    return {
        "pack": pack,
        "matchups": matchup_summary(match, pid),
        "opening": opening_quality(match, pid).to_dict(),
        "splits": split_report(match, pid),
    }
