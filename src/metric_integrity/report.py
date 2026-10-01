from __future__ import annotations

from collections.abc import Sequence

from .models import Call, Denominator, Figure
from .rates import answered_booking_intent_calls, booked_calls, booking_intent_calls, booking_rate
from .valuation import modelled_value, recovered_value


class Report:
    def __init__(self, calls: Sequence[Call], *, assumed_value_per_booking: float = 0.0):
        self._calls = tuple(calls)
        self._assumed_value = assumed_value_per_booking

    @property
    def total_calls(self) -> int:
        return len(self._calls)

    @property
    def booking_intent_calls(self) -> int:
        return booking_intent_calls(self._calls)

    @property
    def answered_booking_intent_calls(self) -> int:
        return answered_booking_intent_calls(self._calls)

    @property
    def booked_calls(self) -> int:
        return booked_calls(self._calls)

    def booking_rate(self, denominator: Denominator) -> Figure:
        return booking_rate(self._calls, denominator)

    def recovered_value(self) -> Figure:
        return recovered_value()

    def modelled_value(self, per_booking_value: float | None = None) -> Figure:
        unit = self._assumed_value if per_booking_value is None else per_booking_value
        return modelled_value(self._calls, unit)

    def limitations(self) -> tuple[str, ...]:
        return (
            "A booking recorded later cannot be attributed to the call that prompted it "
            "without a durable cross-call join. This system does not have one, so recovered "
            "revenue is reported as unavailable.",
            "Per-booking treatment value is a configured assumption, not an observed figure. "
            "Any total derived from it is a model, not a measurement.",
            "Booking intent is inferred from the call record. Where intent was not flagged, "
            "those calls are excluded from the intent denominator rather than counted as failures.",
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
