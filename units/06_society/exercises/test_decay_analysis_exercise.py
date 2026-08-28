"""Auto-grader for the decay analysis data-analysis exercise (CP.5).

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's
implementation — it does *not* read or string-match the student's formula.

Checks
------
1.  **NotImplementedError guard** — fail immediately if hooks not filled in.
2.  **Half-life from fit** — log-linear fit extracts T ≈ 5.0 s from data.
3.  **Background subtraction** — subtracts background, clamps at zero.
4.  **Remaining fraction** — N/N0.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/06_society/exercises/test_decay_analysis_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/06_society/exercises/test_decay_analysis_exercise.py -v \
        --override-student-decay-analysis=units/06_society/exercises/decay_analysis_solution.py

    # Full self-check
    uv run pytest units/06_society/exercises/test_decay_analysis_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import Any, List

import pytest


def _load_decay_analysis_module(file_path: str) -> Any:
    """Import the decay analysis module from an arbitrary Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_decay_analysis", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_decay_analysis"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def decay_analysis_module(request: pytest.FixtureRequest) -> Any:
    """Return the decay analysis module under test.

    Uses ``--override-student-decay-analysis`` if provided; otherwise
    imports from the default ``decay_analysis_exercise`` module.
    """
    override = request.config.getoption("--override-student-decay-analysis")
    if override:
        return _load_decay_analysis_module(override)

    exercises_dir = Path(__file__).resolve().parent
    exercise_path = exercises_dir / "decay_analysis_exercise.py"
    return _load_decay_analysis_module(str(exercise_path))


# ===========================================================================
# Tests
# ===========================================================================


class TestDecayAnalysisExercise:
    """Auto-grader for the decay analysis exercise."""

    def test_half_life_implemented(self, decay_analysis_module: Any) -> None:
        """Fail immediately if the student hasn't filled in the hook."""
        try:
            decay_analysis_module.half_life_from_fit([0.0, 1.0], [100.0, 50.0])
        except NotImplementedError:
            pytest.fail(
                "Your half_life_from_fit() is still raising NotImplementedError. "
                "Replace the 'raise' line with the log-linear fit."
            )

    def test_background_subtract_implemented(self, decay_analysis_module: Any) -> None:
        """Fail immediately if background_subtracted_rate not implemented."""
        try:
            decay_analysis_module.background_subtracted_rate([100.0, 50.0], 20.0)
        except NotImplementedError:
            pytest.fail(
                "Your background_subtracted_rate() is still raising NotImplementedError."
            )

    def test_remaining_fraction_implemented(self, decay_analysis_module: Any) -> None:
        """Fail immediately if remaining_fraction not implemented."""
        try:
            decay_analysis_module.remaining_fraction(100.0, 50.0)
        except NotImplementedError:
            pytest.fail(
                "Your remaining_fraction() is still raising NotImplementedError."
            )

    def test_half_life_from_data(self, decay_analysis_module: Any) -> None:
        """Half-life from the provided dataset should be ~5.0 s."""
        T_est = decay_analysis_module.half_life_from_fit(
            decay_analysis_module.TIME_POINTS,
            decay_analysis_module.COUNT_RATES,
        )
        assert 4.0 < T_est < 6.0, (
            f"Estimated half-life = {T_est:.2f} s, "
            f"expected ~5.0 s (within 4.0–6.0 s)"
        )

    def test_half_life_known_data(self, decay_analysis_module: Any) -> None:
        """Half-life from ideal data should be exact."""
        t = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
        counts = [100.0 * (0.5 ** (ti / 5.0)) for ti in t]
        T_est = decay_analysis_module.half_life_from_fit(t, counts)
        assert T_est == pytest.approx(5.0, rel=0.01), (
            f"Half-life from ideal data = {T_est:.2f} s, expected 5.0 s"
        )

    def test_background_subtraction(self, decay_analysis_module: Any) -> None:
        """Background subtraction should reduce counts."""
        result = decay_analysis_module.background_subtracted_rate(
            decay_analysis_module.COUNT_RATES,
            decay_analysis_module.BACKGROUND_RATE,
        )
        for i in range(len(decay_analysis_module.COUNT_RATES)):
            expected = max(decay_analysis_module.COUNT_RATES[i] - decay_analysis_module.BACKGROUND_RATE, 0.0)
            assert result[i] == pytest.approx(expected, rel=0.01)

    def test_background_subtraction_no_negative(self, decay_analysis_module: Any) -> None:
        """Background subtraction should never produce negative counts."""
        result = decay_analysis_module.background_subtracted_rate([5.0, 10.0, 0.0], 20.0)
        for val in result:
            assert val >= 0.0

    def test_remaining_fraction(self, decay_analysis_module: Any) -> None:
        """Remaining fraction should be N/N0."""
        assert decay_analysis_module.remaining_fraction(100.0, 50.0) == pytest.approx(0.5)
        assert decay_analysis_module.remaining_fraction(100.0, 100.0) == pytest.approx(1.0)
        assert decay_analysis_module.remaining_fraction(100.0, 0.0) == pytest.approx(0.0)

    def test_background_subtracted_half_life(self, decay_analysis_module: Any) -> None:
        """Half-life from background-subtracted data should be ~5.0 s."""
        clean = decay_analysis_module.background_subtracted_rate(
            decay_analysis_module.COUNT_RATES,
            decay_analysis_module.BACKGROUND_RATE,
        )
        T_est = decay_analysis_module.half_life_from_fit(
            decay_analysis_module.TIME_POINTS, clean,
        )
        assert 4.0 < T_est < 6.0


# ===========================================================================
# Self-check
# ===========================================================================


def test_selfcheck_correct_passes(decay_analysis_module: Any) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    T_est = decay_analysis_module.half_life_from_fit(
        decay_analysis_module.TIME_POINTS,
        decay_analysis_module.COUNT_RATES,
    )
    assert 4.0 < T_est < 6.0

    clean = decay_analysis_module.background_subtracted_rate(
        decay_analysis_module.COUNT_RATES,
        decay_analysis_module.BACKGROUND_RATE,
    )
    assert clean[0] == pytest.approx(
        decay_analysis_module.COUNT_RATES[0] - decay_analysis_module.BACKGROUND_RATE,
        rel=0.01,
    )

    assert decay_analysis_module.remaining_fraction(100.0, 50.0) == pytest.approx(0.5)


def test_selfcheck_wrong_fails() -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong answer."""
    def wrong_fit(t: List[float], counts: List[float]) -> float:
        return 100.0

    T_est = wrong_fit([0.0, 1.0], [100.0, 50.0])
    assert abs(T_est - 5.0) > 2.0


def test_selfcheck_runner(request: pytest.FixtureRequest, decay_analysis_module: Any) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    assert decay_analysis_module.half_life_from_fit is not None
    assert decay_analysis_module.background_subtracted_rate is not None
    assert decay_analysis_module.remaining_fraction is not None