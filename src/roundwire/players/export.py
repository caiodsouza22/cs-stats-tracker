"""Serialize player analytics packs for exports and APIs."""

from __future__ import annotations

import json

from roundwire.models.match import Match
from roundwire.players.clutch_book import clutch_book
from roundwire.players.compare import relative_share_card
from roundwire.players.form import form_summary
from roundwire.players.leaderboard import multi_leaderboard, mvp
from roundwire.players.profile import build_all_profiles, build_player_profile, profile_by_name
from roundwire.players.roles import infer_role, role_table
from roundwire.players.round_card import player_round_log
from roundwire.players.streaks import streak_report
from roundwire.players.timeline import player_timeline
from roundwire.types import PlayerId


def player_pack(match: Match, player_id: PlayerId) -> dict[str, object]:
    profile = build_player_profile(match, player_id)
    return {
        "profile": profile.to_dict(),
        "role": infer_role(match, player_id).to_dict(),
        "form": form_summary(match, player_id),
        "streaks": streak_report(match, player_id),
        "clutch": clutch_book(match, player_id),
        "shares": relative_share_card(match, player_id),
        "rounds": [c.to_dict() for c in player_round_log(match, player_id)],
        "timeline": [e.to_dict() for e in player_timeline(match, player_id)],
    }


def player_pack_by_name(match: Match, name: str) -> dict[str, object] | None:
    profile = profile_by_name(match, name)
    if profile is None:
        return None
    return player_pack(match, PlayerId(profile.player_id))


def match_player_export(match: Match) -> dict[str, object]:
    mvp_row = mvp(match)
    return {
        "match_id": str(match.match_id),
        "map": match.map_name,
        "edition": match.edition.value,
        "score": {"CT": match.score()[0], "T": match.score()[1]},
        "mvp": mvp_row.to_dict() if mvp_row else None,
        "roles": role_table(match),
        "leaderboards": multi_leaderboard(match),
        "players": [p.to_dict() for p in build_all_profiles(match)],
    }


def match_player_export_json(match: Match, *, indent: int | None = 2) -> str:
    return json.dumps(match_player_export(match), indent=indent, sort_keys=True)


def player_pack_json(match: Match, player_id: PlayerId, *, indent: int | None = 2) -> str:
    return json.dumps(player_pack(match, player_id), indent=indent, sort_keys=True)
