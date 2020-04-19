"""Reusable error message helpers."""

from __future__ import annotations


def missing_field(field: str) -> str:
    return f"missing required field: {field}"


def bad_type(field: str, expected: str, got: str) -> str:
    return f"field {field!r} expected {expected}, got {got}"


def unknown_weapon(name: str) -> str:
    return f"unknown weapon name: {name!r}"


def unknown_edition(value: str) -> str:
    return f"unknown game edition: {value!r}"


def round_out_of_range(number: int, maximum: int) -> str:
    return f"round {number} exceeds regulation maximum {maximum}"
