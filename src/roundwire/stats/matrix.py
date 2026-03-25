"""Small matrix helpers for duel and correlation-style tables."""

from __future__ import annotations

from roundwire.stats.aggregates import mean, safe_div


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    if not matrix:
        return []
    cols = len(matrix[0])
    return [[row[c] for row in matrix] for c in range(cols)]


def row_sums(matrix: list[list[float]]) -> list[float]:
    return [sum(row) for row in matrix]


def col_sums(matrix: list[list[float]]) -> list[float]:
    if not matrix:
        return []
    return [sum(row[c] for row in matrix) for c in range(len(matrix[0]))]


def normalize_rows(matrix: list[list[float]]) -> list[list[float]]:
    out: list[list[float]] = []
    for row in matrix:
        total = sum(row)
        out.append([safe_div(v, total) for v in row])
    return out


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0
    mx = mean(xs)
    my = mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = sum((x - mx) ** 2 for x in xs) ** 0.5
    deny = sum((y - my) ** 2 for y in ys) ** 0.5
    return safe_div(num, denx * deny)


def covariance(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or not xs:
        return 0.0
    mx = mean(xs)
    my = mean(ys)
    return mean([(x - mx) * (y - my) for x, y in zip(xs, ys)])


def identity(n: int) -> list[list[float]]:
    return [[1.0 if r == c else 0.0 for c in range(n)] for r in range(n)]


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    if not a or not b:
        return []
    bt = transpose(b)
    out: list[list[float]] = []
    for row in a:
        out.append([sum(x * y for x, y in zip(row, col)) for col in bt])
    return out
