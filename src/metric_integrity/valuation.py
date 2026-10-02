from __future__ import annotations

from collections.abc import Sequence
from math import isfinite

from .models import Basis, Call, CallOutcome, Figure


def recovered_value() -> Figure:
    return Figure(
        None,
        Basis.UNAVAILABLE,
        "Recovered revenue attributed to recovered calls",
        population="later bookings attributable to recovered calls",
        quotable=False,
        quote_reason="missing durable attribution join",
    )


def modelled_value(calls: Sequence[Call], per_booking_value: float) -> Figure:
    population = "booked calls expressing booking intent"
    if not isfinite(per_booking_value) or per_booking_value <= 0:
        return Figure(
            None,
            Basis.UNAVAILABLE,
            "Modelled value of booked calls",
            population=population,
            quotable=False,
            quote_reason="positive finite per-booking assumption required",
        )

    booked = sum(
        1
        for call in calls
        if call.intent_flagged and call.outcome is CallOutcome.BOOKED
    )
    return Figure(
        round(booked * per_booking_value, 2),
        Basis.MODELLED,
        "Modelled value of booked calls",
        population=population,
        quotable=False,
        quote_reason="value uses a configured per-booking assumption",
    )
