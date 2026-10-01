from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Basis(str, Enum):
    MEASURED = "measured"
    MODELLED = "modelled"
    UNAVAILABLE = "unavailable"


class Denominator(str, Enum):
    ALL_CALLS = "all_calls"
    BOOKING_INTENT = "booking_intent"


class CallOutcome(str, Enum):
    NO_ANSWER = "no_answer"
    BOOKED = "booked"
    NOT_BOOKING_INTENT = "not_booking_intent"


@dataclass(frozen=True, slots=True)
class Figure:
    value: float | None
    basis: Basis
    label: str
    display: str = "number"

    def __post_init__(self) -> None:
        if self.display not in {"number", "rate"}:
            raise ValueError("unsupported_figure_display")

    def _formatted_value(self) -> str:
        if self.value is None:
            return "not available"
        if self.display == "rate":
            return f"{self.value:.1%}"
        return f"{self.value:,.0f}"

    def __str__(self) -> str:
        if self.value is None or self.basis is Basis.UNAVAILABLE:
            return f"{self.label}: not available ({self.basis.value})"
        value = self._formatted_value()
        if self.basis is Basis.MODELLED:
            return f"{self.label}: {value} (modelled estimate, not measured)"
        return f"{self.label}: {value} (measured)"

    @property
    def safe_to_quote(self) -> bool:
        return self.basis is Basis.MEASURED and self.value is not None


@dataclass(frozen=True, slots=True)
class Call:
    outcome: CallOutcome
    intent_flagged: bool
    treatment_value: float | None = None
