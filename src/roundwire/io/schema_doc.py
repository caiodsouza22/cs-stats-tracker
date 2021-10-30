"""Documented JSON schema fields for match dumps (stdlib descriptive only)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FieldDoc:
    path: str
    type_name: str
    required: bool
    description: str


ROOT_FIELDS: tuple[FieldDoc, ...] = (
    FieldDoc("match_id", "string", True, "Stable match identifier"),
    FieldDoc("map_name", "string", True, "Map name, preferably de_* form"),
    FieldDoc("edition", "string", True, "CSGO or CS2"),
    FieldDoc("team_ct_name", "string", False, "Display name for CT side"),
    FieldDoc("team_t_name", "string", False, "Display name for T side"),
    FieldDoc("players", "array", True, "Player objects"),
    FieldDoc("rounds", "array", True, "Round objects in order"),
    FieldDoc("series_score", "array[int,int]", False, "Optional series map score"),
    FieldDoc("event_name", "string", False, "Tournament or event label"),
    FieldDoc("played_at", "string", False, "ISO-8601 timestamp"),
)

PLAYER_FIELDS: tuple[FieldDoc, ...] = (
    FieldDoc("players[].player_id", "string", True, "Unique within match"),
    FieldDoc("players[].name", "string", True, "Display name"),
    FieldDoc("players[].team", "string", True, "CT or T"),
    FieldDoc("players[].steam_id", "string", False, "Optional Steam id"),
    FieldDoc("players[].country", "string", False, "ISO country code"),
    FieldDoc("players[].tags", "array[string]", False, "Freeform tags"),
)

ROUND_FIELDS: tuple[FieldDoc, ...] = (
    FieldDoc("rounds[].number", "int", True, "1-based round number"),
    FieldDoc("rounds[].winner", "string", True, "CT or T"),
    FieldDoc("rounds[].win_reason", "string", True, "elimination/bomb_*/time"),
    FieldDoc("rounds[].bomb_planted", "bool", False, "Whether bomb was planted"),
    FieldDoc("rounds[].inventories", "array", False, "Round-start inventories"),
    FieldDoc("rounds[].kills", "array", False, "Kill events"),
    FieldDoc("rounds[].damage", "array", False, "Damage events"),
    FieldDoc("rounds[].utility", "array", False, "Utility events"),
    FieldDoc("rounds[].survivors", "array[string]", False, "Surviving player ids"),
    FieldDoc("rounds[].duration_ms", "int", False, "Round length"),
)


def all_field_docs() -> list[FieldDoc]:
    return list(ROOT_FIELDS) + list(PLAYER_FIELDS) + list(ROUND_FIELDS)


def markdown_schema() -> str:
    lines = ["# Match dump schema", ""]
    for section, docs in (
        ("Root", ROOT_FIELDS),
        ("Players", PLAYER_FIELDS),
        ("Rounds", ROUND_FIELDS),
    ):
        lines.append(f"## {section}")
        lines.append("")
        lines.append("| Path | Type | Required | Description |")
        lines.append("|------|------|----------|-------------|")
        for doc in docs:
            req = "yes" if doc.required else "no"
            lines.append(
                f"| `{doc.path}` | {doc.type_name} | {req} | {doc.description} |"
            )
        lines.append("")
    return "\n".join(lines)
