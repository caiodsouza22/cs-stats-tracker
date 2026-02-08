"""Batch I/O helpers for folders of match dumps."""

from __future__ import annotations

from pathlib import Path

from roundwire.errors.io_errors import LoadError
from roundwire.io.loaders import load_match
from roundwire.models.match import Match
from roundwire.players.export import match_player_export
from roundwire.series_analytics import SeriesBook, build_player_book


def discover_match_files(root: Path, pattern: str = "*.json") -> list[Path]:
    root = Path(root)
    if not root.exists():
        raise LoadError(f"path does not exist: {root}", path=root)
    if root.is_file():
        return [root]
    return sorted(p for p in root.rglob(pattern) if p.is_file())


def load_matches(root: Path, pattern: str = "*.json") -> list[Match]:
    matches: list[Match] = []
    errors: list[str] = []
    for path in discover_match_files(root, pattern=pattern):
        try:
            matches.append(load_match(path))
        except Exception as exc:  # noqa: BLE001 - collect and continue for batch
            errors.append(f"{path}: {exc}")
    if not matches and errors:
        raise LoadError("; ".join(errors[:5]), path=Path(root))
    return matches


def batch_scorelines(root: Path) -> list[dict[str, object]]:
    rows = []
    for match in load_matches(root):
        ct, t = match.score()
        rows.append(
            {
                "match_id": str(match.match_id),
                "map": match.map_name,
                "edition": match.edition.value,
                "score": f"{ct}:{t}",
                "rounds": len(match.rounds),
            }
        )
    return rows


def batch_player_book(root: Path):
    matches = load_matches(root)
    return build_player_book(matches)


def batch_series_book(root: Path) -> SeriesBook:
    book = SeriesBook()
    for match in load_matches(root):
        book.ingest_match(match)
    return book


def batch_exports(root: Path) -> list[dict[str, object]]:
    return [match_player_export(match) for match in load_matches(root)]


def summarize_folder(root: Path) -> dict[str, object]:
    matches = load_matches(root)
    maps: dict[str, int] = {}
    editions: dict[str, int] = {}
    for match in matches:
        maps[match.map_name] = maps.get(match.map_name, 0) + 1
        editions[match.edition.value] = editions.get(match.edition.value, 0) + 1
    return {
        "matches": len(matches),
        "maps": maps,
        "editions": editions,
        "total_rounds": sum(len(m.rounds) for m in matches),
        "total_players_seen": len({p.name for m in matches for p in m.players}),
    }
