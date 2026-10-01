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
    population: str | None = None
    numerator: int | None = None
    denominator: int | None = None
    quotable: bool | None = None
    quote_reason: str | None = None

    def __post_init__(self) -> None:
        if self.display not in {"number", "rate"}:
            raise ValueError("unsupported_figure_display")
        if self.basis is Basis.UNAVAILABLE and self.value is not None:
            raise ValueError("unavailable_figure_cannot_have_value")
        if self.denominator is not None and self.denominator <= 0:
            raise ValueError("denominator_must_be_positive")
        if self.denominator is not None and self.numerator is None:
            raise ValueError("denominator_requires_numerator")
        if self.numerator is not None and self.numerator < 0:
            raise ValueError("numerator_must_be_non_negative")
        if self.quotable is True and (self.basis is not Basis.MEASURED or self.value is None):
            raise ValueError("unsafe_quote_configuration")

    def formatted_value(self) -> str:
        if self.value is None:
            return "not available"
        if self.display == "rate":
            return f"{self.value:.1%}"
        return f"{self.value:,.0f}"

    def __str__(self) -> str:
        if self.value is None or self.basis is Basis.UNAVAILABLE:
            return f"{self.label}: not available ({self.basis.value})"
        value = self.formatted_value()
        if self.basis is Basis.MODELLED:
            return f"{self.label}: {value} (modelled estimate, not measured)"
        if not self.safe_to_quote:
            reason = self.quote_reason or "not approved for this claim"
            return f"{self.label}: {value} (measured; do not quote: {reason})"
        return f"{self.label}: {value} (measured)"

    @property
    def safe_to_quote(self) -> bool:
        default = self.basis is Basis.MEASURED and self.value is not None
        if self.quotable is None:
            return default
        return self.quotable and default

    def lineage_lines(self) -> tuple[str, ...]:
        lines: list[str] = []
        if self.population:
            lines.append(f"population: {self.population}")
        if self.numerator is not None and self.denominator is not None:
            lines.append(f"calculation: {self.numerator} / {self.denominator}")
        lines.append(f"basis: {self.basis.value}")
        lines.append(f"quote: {'yes' if self.safe_to_quote else 'no'}")
        if self.quote_reason:
            lines.append(f"reason: {self.quote_reason}")
        return tuple(lines)


@dataclass(frozen=True, slots=True)
class Call:
    outcome: CallOutcome
    intent_flagged: bool
