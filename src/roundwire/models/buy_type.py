"""Buy type enumeration shared by economy classifiers."""

from __future__ import annotations

from enum import Enum


class BuyType(str, Enum):
    ECO = "eco"
    FORCE = "force"
    SEMI = "semi"
    FULL = "full"
    PISTOL = "pistol"
    UNKNOWN = "unknown"
