from metric_integrity import Basis, Call, CallOutcome, Report


def test_unproven_attribution_returns_no_number():
    report = Report([Call(CallOutcome.BOOKED, True)], assumed_value_per_booking=1000.0)
    recovered = report.recovered_value()
    assert recovered.value is None
    assert recovered.basis is Basis.UNAVAILABLE


def test_assumption_stays_modelled():
    report = Report([Call(CallOutcome.BOOKED, True)], assumed_value_per_booking=1000.0)
    value = report.modelled_value()
    assert value.value == 1000.0
    assert value.basis is Basis.MODELLED
