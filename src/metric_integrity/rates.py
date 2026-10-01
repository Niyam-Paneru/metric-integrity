from __future__ import annotations

from collections.abc import Sequence

from .models import Basis, Call, CallOutcome, Denominator, Figure


def booking_intent_calls(calls: Sequence[Call]) -> int:
    return sum(1 for call in calls if call.intent_flagged)


def answered_booking_intent_calls(calls: Sequence[Call]) -> int:
    return sum(
        1
        for call in calls
        if call.intent_flagged and call.outcome is not CallOutcome.NO_ANSWER
    )


def booked_calls(calls: Sequence[Call]) -> int:
    return sum(
        1
        for call in calls
        if call.intent_flagged and call.outcome is CallOutcome.BOOKED
    )


def booking_rate(calls: Sequence[Call], denominator: Denominator) -> Figure:
    booked = booked_calls(calls)

    if denominator is Denominator.ALL_CALLS:
        base = len(calls)
        label = "Booking rate vs all calls"
        # The arithmetic is observable, but this denominator is intentionally
        # not endorsed as the booking-intent success claim.
        basis = Basis.UNAVAILABLE
    else:
        base = booking_intent_calls(calls)
        label = "Booking rate vs calls expressing booking intent"
        basis = Basis.MEASURED

    if base == 0:
        return Figure(None, Basis.UNAVAILABLE, label, display="rate")

    return Figure(round(booked / base, 4), basis, label, display="rate")
