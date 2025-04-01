"""Generate short narrative blurbs from combat stats."""

from __future__ import annotations

from roundwire.combat.summary import combat_summary
from roundwire.models.match import Match
from roundwire.rating.impact import impact_table


def match_blurb(match: Match) -> str:
    ct, t = match.score()
    top = combat_summary(match)[0] if match.players else None
    impact = impact_table(match)[0] if match.players else None
    parts = [
        f"{match.team_ct_name} and {match.team_t_name} played {match.map_name}",
        f"to a {ct}-{t} scoreline under {match.edition.mr_label}.",
    ]
    if top is not None:
        parts.append(
            f" {top.name} led frags with {top.kills} kills at {top.adr:.0f} ADR."
        )
    if impact is not None and (top is None or impact.name != top.name):
        parts.append(f" Impact edged to {impact.name} ({impact.impact:.2f}).")
    return "".join(parts)


def player_blurb(match: Match, player_name: str) -> str:
    player = match.player_by_name(player_name)
    if player is None:
        return f"No player named {player_name!r}."
    line = next(l for l in combat_summary(match) if l.player_id == str(player.player_id))
    return (
        f"{line.name} ({line.team}) finished {line.kills}/{line.deaths}/{line.assists} "
        f"with {line.adr:.1f} ADR, {line.hs_pct*100:.0f}% HS, "
        f"{line.opening_kills} opening kills."
    )
