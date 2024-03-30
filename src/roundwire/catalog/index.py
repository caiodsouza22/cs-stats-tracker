"""Catalog index metadata."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.catalog.samples import list_samples, sample_match


@dataclass(frozen=True, slots=True)
class SampleInfo:
    sample_id: str
    map_name: str
    edition: str
    rounds: int


def catalog_index() -> list[SampleInfo]:
    out: list[SampleInfo] = []
    for sample_id in list_samples():
        match = sample_match(sample_id)
        out.append(
            SampleInfo(
                sample_id=sample_id,
                map_name=match.map_name,
                edition=match.edition.value,
                rounds=len(match.rounds),
            )
        )
    return out
