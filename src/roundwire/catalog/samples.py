"""Load bundled sample matches."""

from __future__ import annotations

from pathlib import Path

from roundwire.io.loaders import load_match
from roundwire.models.match import Match

# CS2 samples first; CS:GO kept for legacy migrate demos.
_SAMPLE_IDS = ("cs2_01", "cs2_02", "cs2_03", "csgo_01", "csgo_02")
_DEFAULT_SAMPLE = "cs2_01"


def list_samples() -> list[str]:
    return list(_SAMPLE_IDS)


def default_sample_id() -> str:
    return _DEFAULT_SAMPLE


def sample_match(sample_id: str | None = None) -> Match:
    sid = _DEFAULT_SAMPLE if sample_id is None else sample_id
    if sid not in _SAMPLE_IDS:
        raise KeyError(f"unknown sample id: {sid!r}")
    base = Path(__file__).resolve().parent / "data" / f"match_{sid}.json"
    return load_match(base)


def sample_editions() -> dict[str, str]:
    return {sample_id: sample_match(sample_id).edition.value for sample_id in list_samples()}


def sample_maps() -> dict[str, str]:
    return {sample_id: sample_match(sample_id).map_name for sample_id in list_samples()}
