from metric_integrity import Call, CallOutcome, Denominator, Report


def sample():
    return [
        Call(CallOutcome.BOOKED, True),
        Call(CallOutcome.BOOKED, True),
        Call(CallOutcome.NO_ANSWER, True),
        *[Call(CallOutcome.NOT_BOOKING_INTENT, False) for _ in range(7)],
    ]


def test_denominator_choice_changes_the_answer():
    report = Report(sample())
    intent = report.booking_rate(Denominator.BOOKING_INTENT)
    all_calls = report.booking_rate(Denominator.ALL_CALLS)
    assert intent.value != all_calls.value


def test_zero_denominator_is_unavailable():
    report = Report([Call(CallOutcome.NOT_BOOKING_INTENT, False)])
    assert report.booking_rate(Denominator.BOOKING_INTENT).value is None
