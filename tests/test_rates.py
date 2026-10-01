from metric_integrity import Call, CallOutcome, Denominator
from metric_integrity.rates import answered_booking_intent_calls, booked_calls, booking_intent_calls, booking_rate


def sample():
    return [
        Call(CallOutcome.BOOKED, True),
        Call(CallOutcome.NO_ANSWER, True),
        Call(CallOutcome.NOT_BOOKING_INTENT, False),
    ]


def test_count_helpers_keep_populations_separate():
    calls = sample()
    assert booking_intent_calls(calls) == 2
    assert answered_booking_intent_calls(calls) == 1
    assert booked_calls(calls) == 1


def test_intent_rate_is_measured_against_intent_population():
    figure = booking_rate(sample(), Denominator.BOOKING_INTENT)
    assert figure.value == 0.5
    assert figure.safe_to_quote


def test_all_call_rate_is_not_promoted_to_primary_measured_claim():
    figure = booking_rate(sample(), Denominator.ALL_CALLS)
    assert figure.value == round(1 / 3, 4)
    assert not figure.safe_to_quote
