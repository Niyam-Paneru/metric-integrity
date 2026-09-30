from __future__ import annotations

from metric_integrity import Basis, Call, CallOutcome, Denominator, Figure, Report


def sample() -> list[Call]:
    return [
        # 6 answered, intent expressed, 4 booked
        Call(CallOutcome.BOOKED, True, 1200.0),
        Call(CallOutcome.BOOKED, True, 1200.0),
        Call(CallOutcome.BOOKED, True, 1200.0),
        Call(CallOutcome.BOOKED, True, 1200.0),
        Call(CallOutcome.NOT_BOOKING_INTENT, True),
        Call(CallOutcome.NOT_BOOKING_INTENT, True),
        # 2 answered, intent, not booked
        Call(CallOutcome.NO_ANSWER, True),
        Call(CallOutcome.NO_ANSWER, True),
        # 6 never answered, intent expressed
        *[Call(CallOutcome.NO_ANSWER, True) for _ in range(6)],
        # 20 calls with no booking intent at all
        *[Call(CallOutcome.NOT_BOOKING_INTENT, False) for _ in range(20)],
    ]


# --- denominators ----------------------------------------------------------


def test_counts_are_correct() -> None:
    report = Report(sample())
    assert report.total_calls == 34
    assert report.booking_intent_calls == 14
    assert report.answered_booking_intent_calls == 6
    assert report.booked_calls == 4


def test_rate_uses_the_population_the_claim_is_about() -> None:
    report = Report(sample())
    assert report.booking_rate(Denominator.BOOKING_INTENT).value == 0.2857
    assert report.booking_rate(Denominator.ALL_CALLS).value == 0.1176


def test_the_two_denominators_give_different_answers() -> None:
    """If they agreed, the denominator choice would not matter and this module
    would be theatre."""
    report = Report(sample())
    intent = report.booking_rate(Denominator.BOOKING_INTENT)
    everything = report.booking_rate(Denominator.ALL_CALLS)
    assert intent.value != everything.value


def test_calls_without_intent_are_excluded_not_counted_as_failures() -> None:
    """20 info calls are not 20 booking failures."""
    report = Report(sample())
    assert report.booking_intent_calls == 14
    assert report.total_calls == 34


# --- basis labelling -------------------------------------------------------


def test_the_intent_denominator_is_measured() -> None:
    figure = Report(sample()).booking_rate(Denominator.BOOKING_INTENT)
    assert figure.basis is Basis.MEASURED
    assert figure.safe_to_quote


def test_the_all_calls_denominator_is_not_marked_measured() -> None:
    """The number that produces the impressive screenshot is not quotable."""
    figure = Report(sample()).booking_rate(Denominator.ALL_CALLS)
    assert figure.basis is Basis.UNAVAILABLE
    assert not figure.safe_to_quote


def test_a_modelled_figure_never_becomes_quotable() -> None:
    figure = Report(sample(), assumed_value_per_booking=1000.0).modelled_value()
    assert figure.value == 4000.0
    assert figure.basis is Basis.MODELLED
    assert not figure.safe_to_quote
    assert "modelled estimate, not measured" in str(figure)


def test_a_model_value_without_an_assumption_is_unavailable() -> None:
    figure = Report(sample()).modelled_value()
    assert figure.basis is Basis.UNAVAILABLE
    assert figure.value is None


# --- honest attribution ----------------------------------------------------


def test_recovered_revenue_is_unavailable_rather_than_invented() -> None:
    """No durable join exists, so the honest answer is 'we cannot know'."""
    report = Report(sample(), assumed_value_per_booking=1000.0)
    figure = report.recovered_value()
    assert figure.value is None
    assert figure.basis is Basis.UNAVAILABLE
    assert not figure.safe_to_quote


def test_limitations_name_the_specific_missing_join() -> None:
    limitations = Report(sample()).limitations()
    assert any("cannot be attributed" in limitation for limitation in limitations)
    assert any("assumption" in limitation for limitation in limitations)


# --- edge cases ------------------------------------------------------------


def test_no_calls_yields_unavailable_not_a_division_error() -> None:
    report = Report([])
    figure = report.booking_rate(Denominator.BOOKING_INTENT)
    assert figure.value is None
    assert figure.basis is Basis.UNAVAILABLE
    assert "not available" in str(figure)


def test_no_intent_calls_yields_unavailable() -> None:
    report = Report([Call(CallOutcome.NOT_BOOKING_INTENT, False)])
    assert report.booking_rate(Denominator.BOOKING_INTENT).value is None


def test_zero_or_negative_assumption_is_not_a_figure() -> None:
    assert Report(sample(), assumed_value_per_booking=0.0).modelled_value().value is None
    assert Report(sample(), assumed_value_per_booking=-5.0).modelled_value().value is None


def test_summary_is_readable_and_carries_the_labels() -> None:
    lines = Report(sample(), assumed_value_per_booking=1000.0).summary()
    text = "\n".join(lines)
    assert "Booked: 4" in text
    assert "(measured)" in text
    assert "modelled estimate, not measured" in text
    assert "not available" in text
    assert "Limitations:" in text
