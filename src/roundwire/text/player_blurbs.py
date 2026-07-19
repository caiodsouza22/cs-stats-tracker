"""Text blurbs for player profiles and leaderboards."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.players.form import current_form
from roundwire.players.leaderboard import mvp
from roundwire.players.profile import build_player_profile, profile_by_name
from roundwire.players.roles import infer_role
from roundwire.types import PlayerId


def profile_blurb(match: Match, player_id: PlayerId) -> str:
    profile = build_player_profile(match, player_id)
    role = infer_role(match, player_id)
    form = current_form(match, player_id)
    form_bit = f" Form looks {form.label}." if form else ""
    tags = f" Tags: {', '.join(profile.tags)}." if profile.tags else ""
    return (
        f"{profile.name} ({profile.team}) posted {profile.kills}/{profile.deaths}/{profile.assists} "
        f"with {profile.adr:.0f} ADR and Rating {profile.rating_3_0:.2f} "
        f"as primary {role.primary.value}.{form_bit}{tags}"
    )


def profile_blurb_by_name(match: Match, name: str) -> str:
    profile = profile_by_name(match, name)
    if profile is None:
        return f"No player named {name!r} in this match."
    return profile_blurb(match, PlayerId(profile.player_id))


def mvp_blurb(match: Match) -> str:
    row = mvp(match)
    if row is None:
        return "No MVP could be determined."
    return (
        f"MVP: {row.name} ({row.team}) leads {row.metric} at {row.value:.3f} "
        f"on {match.map_name}."
    )


def leaderboard_blurb(match: Match, metric: str = "rating", n: int = 3) -> str:
    from roundwire.players.leaderboard import leaderboard

    rows = leaderboard(match, metric=metric, limit=n)
    if not rows:
        return "Leaderboard empty."
    bits = [f"{r.rank}. {r.name} ({r.value:.2f})" for r in rows]
    return f"Top {metric}: " + "; ".join(bits)


def team_blurb(match: Match) -> str:
    from roundwire.players.profile import team_profile_averages
    from roundwire.models.team import TeamSide

    ct = team_profile_averages(match, TeamSide.CT)
    t = team_profile_averages(match, TeamSide.T)
    ct_s, t_s = match.score()
    return (
        f"{match.team_ct_name} {ct_s}-{t_s} {match.team_t_name} on {match.map_name}. "
        f"CT avg rating {ct['rating']:.2f} / ADR {ct['adr']:.0f}; "
        f"T avg rating {t['rating']:.2f} / ADR {t['adr']:.0f}."
    )


def role_blurb(match: Match, player_id: PlayerId) -> str:
    role = infer_role(match, player_id)
    reasons = []
    if role.scores:
        reasons = list(role.scores[0].reasons[:2])
    reason_txt = f" ({'; '.join(reasons)})" if reasons else ""
    secondary = f", secondary {role.secondary.value}" if role.secondary else ""
    return f"{role.name} reads as {role.primary.value}{secondary}{reason_txt}."
