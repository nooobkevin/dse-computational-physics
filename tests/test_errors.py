"""Tests for physics_core.errors — error helpers and significant figures."""

import pytest

from physics_core.errors import (
    absolute_error,
    format_value_with_error,
    percent_error,
    relative_error,
    sig_figs,
)


class TestAbsoluteError:
    def test_positive(self) -> None:
        assert absolute_error(5.0, 3.0) == 2.0

    def test_negative(self) -> None:
        assert absolute_error(-5.0, -3.0) == 2.0

    def test_exact(self) -> None:
        assert absolute_error(3.0, 3.0) == 0.0


class TestRelativeError:
    def test_typical(self) -> None:
        assert relative_error(5.0, 4.0) == pytest.approx(0.25)

    def test_zero_true_raises(self) -> None:
        with pytest.raises(ZeroDivisionError):
            relative_error(1.0, 0.0)


class TestPercentError:
    def test_typical(self) -> None:
        assert percent_error(5.0, 4.0) == pytest.approx(25.0)

    def test_zero_true_raises(self) -> None:
        with pytest.raises(ZeroDivisionError):
            percent_error(1.0, 0.0)


class TestSigFigs:
    def test_positive(self) -> None:
        assert sig_figs(12345, 3) == 12300.0

    def test_small(self) -> None:
        assert sig_figs(0.0012345, 2) == pytest.approx(0.0012)

    def test_zero(self) -> None:
        assert sig_figs(0.0, 3) == 0.0

    def test_negative_n_raises(self) -> None:
        with pytest.raises(ValueError, match="n must be >= 1"):
            sig_figs(1.0, 0)

    def test_negative_value(self) -> None:
        assert sig_figs(-12345, 2) == -12000.0


class TestFormatValueWithError:
    def test_typical(self) -> None:
        result = format_value_with_error(1.23456, 0.056)
        # err rounded to 1 sig fig = 0.06, value rounded to 2 d.p. = 1.23
        assert result == "1.23 ± 0.06"

    def test_large_error(self) -> None:
        result = format_value_with_error(123.4, 5.6)
        # err rounded to 1 sig fig = 6, value rounded to 0 d.p. = 123
        assert result == "123 ± 6"

    def test_small_error(self) -> None:
        result = format_value_with_error(0.001234, 0.000056)
        # err rounded to 1 sig fig = 0.00006, value to 5 d.p.
        assert result == "0.00123 ± 0.00006"

    def test_err_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="err must be > 0"):
            format_value_with_error(1.0, 0.0)

    def test_err_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="err must be > 0"):
            format_value_with_error(1.0, -1.0)