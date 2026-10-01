from metric_integrity import Basis, Figure


def test_only_measured_figure_is_quotable():
    assert Figure(0.5, Basis.MEASURED, "Measured").safe_to_quote
    assert not Figure(0.5, Basis.MODELLED, "Model").safe_to_quote
    assert not Figure(None, Basis.UNAVAILABLE, "Missing").safe_to_quote


def test_modelled_label_survives_formatting():
    text = str(Figure(4000.0, Basis.MODELLED, "Value"))
    assert "modelled estimate, not measured" in text

def test_rate_figure_renders_as_percentage():
    text = str(Figure(0.2857, Basis.MEASURED, "Booking rate", display="rate"))
    assert "28.6%" in text
    assert "(measured)" in text


def test_unknown_display_format_is_rejected():
    import pytest

    with pytest.raises(ValueError, match="unsupported_figure_display"):
        Figure(1.0, Basis.MEASURED, "Value", display="mystery")

