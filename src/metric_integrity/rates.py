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
        population = "all calls"
        quotable = False
        quote_reason = "denominator does not match the booking-intent success claim"
    else:
        base = booking_intent_calls(calls)
        label = "Booking rate vs calls expressing booking intent"
        population = "calls expressing booking intent"
        quotable = True
        quote_reason = None

    if base == 0:
        return Figure(
            None,
            Basis.UNAVAILABLE,
            label,
            display="rate",
            population=population,
            quotable=False,
            quote_reason="denominator population is empty",
        )

    return Figure(
        round(booked / base, 4),
        Basis.MEASURED,
        label,
        display="rate",
        population=population,
        numerator=booked,
        denominator=base,
        quotable=quotable,
        quote_reason=quote_reason,
    )
