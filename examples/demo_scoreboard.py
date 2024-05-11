"""Tiny demo script printing a sample scoreboard."""

from __future__ import annotations

from roundwire.catalog import sample_match
from roundwire.reports.scoreboard import scoreboard_table


def main() -> None:
    match = sample_match("cs2_01")
    print(scoreboard_table(match))


if __name__ == "__main__":
    main()
