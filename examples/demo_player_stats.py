"""Examples demonstrating player analytics APIs."""

from __future__ import annotations

from roundwire.catalog.samples import sample_match
from roundwire.players.export import match_player_export
from roundwire.players.leaderboard import leaderboard
from roundwire.players.profile import build_all_profiles
from roundwire.players.roles import role_table
from roundwire.reports.player_report import player_report_table
from roundwire.text.player_blurbs import mvp_blurb, team_blurb


def main() -> None:
    match = sample_match("cs2_01")
    print(team_blurb(match))
    print(mvp_blurb(match))
    print()
    print(player_report_table(match))
    print()
    print("Roles:")
    for row in role_table(match):
        print(f"  {row['name']}: {row['primary']}" + (f"/{row['secondary']}" if row["secondary"] else ""))
    print()
    print("Top rating:")
    for row in leaderboard(match, "rating", limit=5):
        print(f"  {row.rank}. {row.name} {row.value:.3f}")
    export = match_player_export(match)
    print()
    print(f"export players={len(export['players'])} mvp={export['mvp']}")
    profiles = build_all_profiles(match)
    print(f"profiles built={len(profiles)} top={profiles[0].name if profiles else '-'}")


if __name__ == "__main__":
    main()
