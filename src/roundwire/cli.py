"""Command-line interface for roundwire."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from roundwire import __version__
from roundwire.io.loaders import load_match
from roundwire.migrate.upgrade import migrate_match_to_cs2
from roundwire.models.match import Match
from roundwire.reports.economy_report import economy_summary_table
from roundwire.reports.scoreboard import scoreboard_table
from roundwire.reports.utility_report import utility_summary_table
from roundwire.reports.round_log import round_log_table


def _load(path: str) -> Match:
    return load_match(Path(path))


def cmd_scoreboard(args: argparse.Namespace) -> int:
    match = _load(args.path)
    print(scoreboard_table(match))
    return 0


def cmd_economy(args: argparse.Namespace) -> int:
    match = _load(args.path)
    print(economy_summary_table(match))
    return 0


def cmd_utility(args: argparse.Namespace) -> int:
    match = _load(args.path)
    print(utility_summary_table(match))
    return 0


def cmd_rounds(args: argparse.Namespace) -> int:
    match = _load(args.path)
    print(round_log_table(match))
    return 0


def cmd_migrate(args: argparse.Namespace) -> int:
    match = _load(args.path)
    upgraded = migrate_match_to_cs2(match)
    if args.summary:
        print(
            f"migrated edition={upgraded.edition.value} "
            f"map={upgraded.map_name} rounds={len(upgraded.rounds)}"
        )
    else:
        print(json.dumps(upgraded.to_dict(), indent=2, sort_keys=True))
    return 0


def cmd_impact(args: argparse.Namespace) -> int:
    from roundwire.reports.impact_report import impact_report_table

    match = _load(args.path)
    print(impact_report_table(match))
    return 0


def cmd_rating(args: argparse.Namespace) -> int:
    from roundwire.reports.rating30_report import rating30_report_table

    match = _load(args.path)
    print(rating30_report_table(match))
    return 0


def cmd_players(args: argparse.Namespace) -> int:
    from roundwire.reports.player_report import player_detail_report, player_report_table

    match = _load(args.path)
    if args.name:
        print(player_detail_report(match, args.name))
    else:
        print(player_report_table(match))
    return 0


def cmd_leaderboard(args: argparse.Namespace) -> int:
    from roundwire.reports.player_report import leaderboard_report

    match = _load(args.path)
    print(leaderboard_report(match, metric=args.metric))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="roundwire",
        description="Counter-Strike match/round analytics CLI",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"roundwire {__version__}",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_sb = sub.add_parser("scoreboard", help="Print match scoreboard")
    p_sb.add_argument("path", help="Path to match JSON dump")
    p_sb.set_defaults(func=cmd_scoreboard)

    p_eco = sub.add_parser("economy", help="Print economy summary")
    p_eco.add_argument("path", help="Path to match JSON dump")
    p_eco.set_defaults(func=cmd_economy)

    p_util = sub.add_parser("utility", help="Print utility usage")
    p_util.add_argument("path", help="Path to match JSON dump")
    p_util.set_defaults(func=cmd_utility)

    p_rounds = sub.add_parser("rounds", help="Print round log")
    p_rounds.add_argument("path", help="Path to match JSON dump")
    p_rounds.set_defaults(func=cmd_rounds)

    p_imp = sub.add_parser("impact", help="Print simple impact rating table")
    p_imp.add_argument("path", help="Path to match JSON dump")
    p_imp.set_defaults(func=cmd_impact)

    p_r30 = sub.add_parser("rating", help="Print HLTV-inspired Rating 3.0 table")
    p_r30.add_argument("path", help="Path to match JSON dump")
    p_r30.set_defaults(func=cmd_rating)

    p_pl = sub.add_parser("players", help="Print per-player stats table or detail")
    p_pl.add_argument("path", help="Path to match JSON dump")
    p_pl.add_argument("--name", help="Optional player display name for detail view")
    p_pl.set_defaults(func=cmd_players)

    p_lb = sub.add_parser("leaderboard", help="Print a metric leaderboard")
    p_lb.add_argument("path", help="Path to match JSON dump")
    p_lb.add_argument(
        "--metric",
        default="rating",
        help="Metric key (rating, kills, adr, impact, opening_kills, ...)",
    )
    p_lb.set_defaults(func=cmd_leaderboard)

    p_mig = sub.add_parser("migrate", help="Upgrade CS:GO dump toward CS2")
    p_mig.add_argument("path", help="Path to match JSON dump")
    p_mig.add_argument(
        "--summary",
        action="store_true",
        help="Print a short summary instead of full JSON",
    )
    p_mig.set_defaults(func=cmd_migrate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
