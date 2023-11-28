"""Tunable weights for the impact formula."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ImpactWeights:
    kpr: float = 0.40
    adr: float = 0.25
    survival: float = 0.20
    opening: float = 0.15
    multi: float = 0.05

    def normalized(self) -> ImpactWeights:
        base = self.kpr + self.adr + self.survival + self.opening
        if base <= 0:
            return self
        return ImpactWeights(
            kpr=self.kpr / base * 0.95,
            adr=self.adr / base * 0.95,
            survival=self.survival / base * 0.95,
            opening=self.opening / base * 0.95,
            multi=self.multi,
        )


DEFAULT_WEIGHTS = ImpactWeights()
