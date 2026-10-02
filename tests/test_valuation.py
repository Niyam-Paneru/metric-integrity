import pytest

from metric_integrity import Basis, Call, CallOutcome
from metric_integrity.valuation import modelled_value, recovered_value


def test_recovered_value_refuses_unsupported_attribution():
    figure = recovered_value()
    assert figure.value is None
    assert figure.basis is Basis.UNAVAILABLE


def test_modelled_value_keeps_modelled_basis():
    calls = [Call(CallOutcome.BOOKED, True), Call(CallOutcome.NO_ANSWER, True)]
    figure = modelled_value(calls, 750.0)
    assert figure.value == 750.0
    assert figure.basis is Basis.MODELLED
    assert not figure.safe_to_quote


@pytest.mark.parametrize("assumption", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_assumption_yields_unavailable_value(assumption):
    figure = modelled_value([Call(CallOutcome.BOOKED, True)], assumption)
    assert figure.value is None
    assert figure.basis is Basis.UNAVAILABLE
    assert not figure.safe_to_quote
