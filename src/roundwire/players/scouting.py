"""Human-readable scouting reports for a player or full roster."""

from __future__ import annotations

from roundwire.analysis.entry_fragging import entry_card
from roundwire.analysis.pace import pace_report
from roundwire.analysis.support_score import support_card
from roundwire.combat.accuracy import accuracy_card
from roundwire.models.match import Match
from roundwire.players.clutch_book import clutch_book
from roundwire.players.form import form_summary
from roundwire.players.matchups import matchup_summary
from roundwire.players.money_story import money_story
from roundwire.players.opening_quality import opening_quality
from roundwire.players.profile import build_player_profile, profile_by_name
from roundwire.players.roles import infer_role
from roundwire.players.splits import split_report
from roundwire.players.streaks import streak_report
from roundwire.players.weapon_economy import weapon_value_table
from roundwire.text.player_blurbs import profile_blurb, role_blurb
from roundwire.types import PlayerId


def scouting_report(match: Match, player_id: PlayerId) -> str:
    profile = build_player_profile(match, player_id)
    role = infer_role(match, player_id)
    lines = [
        profile_blurb(match, player_id),
        role_blurb(match, player_id),
        "",
        f"Rating {profile.rating_3_0:.3f} | Impact {profile.impact:.3f} | "
        f"ADR {profile.adr:.1f} | KAST {profile.kast * 100:.0f}%",
        f"Openings {profile.opening_kills}/{profile.opening_deaths} | "
        f"Clutches {profile.clutch_wins} | Multi-kills {profile.multi_kills}",
        f"Favorite weapon: {profile.favorite_weapon or '-'} | "
        f"Util spend {profile.utility_spend}",
        "",
        "== Opening ==",
    ]
    oq = opening_quality(match, player_id).to_dict()
    lines.append(
        f"attempts={oq['openings']}+{oq['opening_deaths']} "
        f"convert={oq['conversion_rate']:.0%} trade={oq['death_trade_rate']:.0%}"
    )
    entry = entry_card(match, player_id).to_dict()
    lines.append(f"entry success={entry['success_rate']:.0%} converted={entry['converted']}")
    lines.append("")
    lines.append("== Support ==")
    support = support_card(match, player_id).to_dict()
    lines.append(
        f"index={support['support_index']:.2f} flash_value={support['flash_value']:.1f} "
        f"efficiency={support['efficiency']:.2f}"
    )
    lines.append("")
    lines.append("== Form ==")
    form = form_summary(match, player_id)
    latest = form.get("latest") or {}
    lines.append(f"hot={form['hot']} cold={form['cold']} latest={latest.get('label', '-')}")
    lines.append("")
    lines.append("== Splits ==")
    for half in split_report(match, player_id)["halves"]:
        lines.append(
            f"{half['label']}: ADR {half['adr']} K/D {half['kd']} WR {half['win_rate']:.0%}"
        )
    lines.append("")
    lines.append("== Matchups ==")
    mu = matchup_summary(match, player_id)
    lines.append(f"soft target={mu['soft_target']} problem={mu['problem_opponent']} +/-={mu['plus_minus']}")
    for row in mu["rows"][:5]:
        lines.append(f"  vs {row['opponent_name']}: {row['kills']}-{row['deaths']}")
    lines.append("")
    lines.append("== Money ==")
    money = money_story(match, player_id)
    lines.append(f"avg EQ {money['avg_equipment']} slope={money['equipment_slope']} notes={money['notes']}")
    lines.append("")
    lines.append("== Weapons ==")
    for w in weapon_value_table(match, player_id)[:5]:
        lines.append(f"  {w.weapon}: {w.kills} kills @~{w.value_per_kill:.0f}/kill")
    lines.append("")
    lines.append("== Accuracy ==")
    acc = accuracy_card(match, player_id).to_dict()
    lines.append(f"hits={acc['hits']} HS%={acc['head_share']:.0%} sprays={acc['sprays']}")
    lines.append("")
    lines.append("== Clutch ==")
    clutch = clutch_book(match, player_id)
    lines.append(f"solo {clutch['solo_wins']}/{clutch['solo_cases']} WR={clutch['solo_wr']:.0%}")
    lines.append("")
    lines.append("== Streaks ==")
    streaks = streak_report(match, player_id)
    for kind, payload in streaks.items():
        longest = payload.get("longest")
        if longest:
            lines.append(f"{kind}: longest {longest['length']} (R{longest['start_round']}-R{longest['end_round']})")
    _ = role  # role used in blurbs
    return "\n".join(lines)


def scouting_report_by_name(match: Match, name: str) -> str:
    profile = profile_by_name(match, name)
    if profile is None:
        return f"player not found: {name!r}"
    return scouting_report(match, PlayerId(profile.player_id))


def roster_scouting_book(match: Match) -> str:
    chunks = [f"Scouting book — {match.map_name} ({match.edition.value})", ""]
    pace = pace_report(match)
    chunks.append(f"Pace avg={pace['avg_duration_ms']}ms time_wins={pace['time_wins']}")
    chunks.append("")
    for player in match.players:
        chunks.append("-" * 48)
        chunks.append(scouting_report(match, player.player_id))
        chunks.append("")
    return "\n".join(chunks)
