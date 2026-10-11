import pytest

from metric_integrity import Call, CallOutcome, Denominator
from metric_integrity.rates import booking_rate


def sample():
    return [
        Call(CallOutcome.BOOKED, True),
        Call(CallOutcome.NO_ANSWER, True),
        Call(CallOutcome.NOT_BOOKING_INTENT, False),
    ]


@pytest.mark.parametrize("invalid", [None, "", "all_calls", "booking_intent", 0, object()])
def test_unknown_denominator_cannot_be_reported_as_quotable(invalid):
    with pytest.raises(ValueError, match="unsupported_booking_rate_denominator"):
        booking_rate(sample(), invalid)


def test_both_supported_denominators_remain_distinct():
    all_calls = booking_rate(sample(), Denominator.ALL_CALLS)
    intent = booking_rate(sample(), Denominator.BOOKING_INTENT)

    assert (all_calls.numerator, all_calls.denominator) == (1, 3)
    assert (intent.numerator, intent.denominator) == (1, 2)
    assert not all_calls.safe_to_quote
    assert intent.safe_to_quote
