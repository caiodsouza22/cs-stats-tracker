"""Describe catalog samples as short paragraphs."""

from __future__ import annotations

from roundwire.catalog.index import catalog_index
from roundwire.catalog.samples import sample_match
from roundwire.text.labels import edition_label


def describe_sample(sample_id: str) -> str:
    match = sample_match(sample_id)
    ct, t = match.score()
    return (
        f"{sample_id}: {edition_label(match.edition)} on {match.map_name} "
        f"— {match.team_ct_name} {ct}:{t} {match.team_t_name} "
        f"({len(match.rounds)} rounds)."
    )


def describe_catalog() -> str:
    lines = [describe_sample(info.sample_id) for info in catalog_index()]
    return "\n".join(lines)
