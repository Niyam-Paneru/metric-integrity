from metric_integrity import Basis, Figure


def test_only_measured_figure_is_quotable():
    assert Figure(0.5, Basis.MEASURED, "Measured").safe_to_quote
    assert not Figure(0.5, Basis.MODELLED, "Model").safe_to_quote
    assert not Figure(None, Basis.UNAVAILABLE, "Missing").safe_to_quote


def test_modelled_label_survives_formatting():
    text = str(Figure(4000.0, Basis.MODELLED, "Value"))
    assert "modelled estimate, not measured" in text
