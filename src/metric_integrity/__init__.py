"""Denominator-safe metrics.

A dashboard is an argument about reality made with arithmetic. Most misleading
dashboards are not lying. They are dividing by the wrong thing.

Three specific failures, all seen in production reporting:

1.  **Wrong denominator.** "We recovered 62% of missed calls" computed as
    `booked / every_call_including_wrong_number_lookups` is technically correct
    and commercially meaningless. The denominator must be the population the
    claim is about: *calls that expressed booking intent*.

2.  **Modelled values presented as measured.** A per-patient value taken from a
    configuration constant is an assumption. Multiply it by a real count and it
    becomes a number on a dashboard that nobody labels as an assumption. That is
    how a modelled figure becomes a quoted figure.

3.  **Attribution the data cannot support.** If a booking arrives tomorrow, you
    cannot prove it came from today's missed call without a real join. The
    honest output is a stated limitation, not a smaller made-up percentage.

The rule: a figure is only as good as its denominator, and an estimate must
never be able to reach a screen without its label.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Sequence


class Basis(str, Enum):
    """How a number came to exist. This travels with the number, always."""

    MEASURED = "measured"
    MODELLED = "modelled"
    UNAVAILABLE = "unavailable"


class Denominator(str, Enum):
    """The population a rate is actually about."""

    ALL_CALLS = "all_calls"
    BOOKING_INTENT = "booking_intent"


class CallOutcome(str, Enum):
    NO_ANSWER = "no_answer"
    BOOKED = "booked"
    NOT_BOOKING_INTENT = "not_booking_intent"


@dataclass(frozen=True, slots=True)
class Figure:
    """A number that knows what kind of number it is."""

    value: float | None
    basis: Basis
    label: str

    def __str__(self) -> str:
        if self.value is None or self.basis is Basis.UNAVAILABLE:
            return f"{self.label}: not available ({self.basis.value})"
        if self.basis is Basis.MODELLED:
            return f"{self.label}: {self.value:,.0f} (modelled estimate, not measured)"
        return f"{self.label}: {self.value:,.0f} (measured)"

    @property
    def safe_to_quote(self) -> bool:
        """Only measured figures may leave the system as a number.

        A modelled value is allowed to reach a screen. It is never allowed to
        reach a quote, an invoice, or a sales conversation.
        """
        return self.basis is Basis.MEASURED and self.value is not None


@dataclass(frozen=True, slots=True)
class Call:
    outcome: CallOutcome
    intent_flagged: bool
    treatment_value: float | None = None


class Report:
    """Builds every figure with its basis attached.

    There is no API here that returns a bare number. If you want a number for a
    document, you have to ask whether it is safe to quote, and it usually is not.
    """

    def __init__(self, calls: Sequence[Call], *, assumed_value_per_booking: float = 0.0):
        self._calls = tuple(calls)
        self._assumed_value = assumed_value_per_booking

    @property
    def total_calls(self) -> int:
        return len(self._calls)

    @property
    def booking_intent_calls(self) -> int:
        return sum(1 for c in self._calls if c.intent_flagged)

    @property
    def answered_booking_intent_calls(self) -> int:
        return sum(
            1 for c in self._calls if c.intent_flagged and c.outcome is not CallOutcome.NO_ANSWER
        )

    @property
    def booked_calls(self) -> int:
        return sum(
            1 for c in self._calls if c.intent_flagged and c.outcome is CallOutcome.BOOKED
        )

    def booking_rate(self, denominator: Denominator) -> Figure:
        """A rate is meaningless without naming its denominator.

        `ALL_CALLS` is reported but marked: it is the number that produces the
        impressive screenshot, and it is not the number that describes the
        business.
        """
        if denominator is Denominator.ALL_CALLS:
            base = self.total_calls
            label = "Booking rate vs all calls"
        else:
            base = self.booking_intent_calls
            label = "Booking rate vs calls expressing booking intent"

        if base == 0:
            return Figure(None, Basis.UNAVAILABLE, label)

        value = round(self.booked_calls / base, 4)
        basis = Basis.UNAVAILABLE if denominator is Denominator.ALL_CALLS else Basis.MEASURED
        return Figure(value, basis, label)

    def recovered_value(self) -> Figure:
        """Attribution, not measurement.

        Without a durable join from a later booking back to the call that
        triggered it, this cannot be computed. Returning a smaller invented
        number would be worse than returning nothing.
        """
        return Figure(
            None,
            Basis.UNAVAILABLE,
            "Recovered revenue attributed to recovered calls",
        )

    def modelled_value(self, per_booking_value: float | None = None) -> Figure:
        """An estimate, permanently labelled as one."""
        unit = self._assumed_value if per_booking_value is None else per_booking_value
        if unit <= 0:
            return Figure(None, Basis.UNAVAILABLE, "Modelled value of recovered bookings")
        return Figure(
            round(self.booked_calls * unit, 2),
            Basis.MODELLED,
            "Modelled value of recovered bookings",
        )

    def limitations(self) -> tuple[str, ...]:
        return (
            "A booking recorded later cannot be attributed to the call that "
            "prompted it without a durable cross-call join. This system does not "
            "have one, so recovered revenue is reported as unavailable.",
            "Per-booking treatment value is a configured assumption, not an "
            "observed figure. Any total derived from it is a model, not a measurement.",
            "Booking intent is inferred from the call record. Where intent was "
            "not flagged, those calls are excluded from the intent denominator "
            "rather than counted as failures.",
        )

    def summary(self) -> Sequence[str]:
        return [
            f"Total calls: {self.total_calls}",
            f"Calls expressing booking intent: {self.booking_intent_calls}",
            f"Answered: {self.answered_booking_intent_calls}",
            f"Booked: {self.booked_calls}",
            "",
            str(self.booking_rate(Denominator.BOOKING_INTENT)),
            str(self.booking_rate(Denominator.ALL_CALLS)),
            str(self.recovered_value()),
            str(self.modelled_value()),
            "",
            "Limitations:",
            *(f"  - {limitation}" for limitation in self.limitations()),
        ]
