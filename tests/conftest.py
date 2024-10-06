"""Shared fixtures."""

from __future__ import annotations

import pytest

from roundwire.catalog import sample_match
from roundwire.catalog.synthetic import default_cs2_match, default_csgo_match
from roundwire.models.match import Match


@pytest.fixture(params=["cs2_01", "cs2_02", "cs2_03", "csgo_01", "csgo_02"])
def catalog_match(request: pytest.FixtureRequest) -> Match:
    return sample_match(request.param)


@pytest.fixture
def cs2_match() -> Match:
    return sample_match("cs2_01")


@pytest.fixture
def csgo_match() -> Match:
    return sample_match("csgo_01")


@pytest.fixture
def syn_cs2() -> Match:
    return default_cs2_match()


@pytest.fixture
def syn_csgo() -> Match:
    return default_csgo_match()
