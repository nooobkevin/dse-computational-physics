"""Tests for physics_core.inquiry.analysis — LinearFit and ReferenceLinearFit."""

import math
from typing import Optional

import numpy as np
import pytest

from physics_core.inquiry.analysis import (
    LinearFit,
    ReferenceLinearFit,
    percent_error,
    propagate_uncertainty,
)
from physics_core.inquiry.complex_systems import (
    CrowdModel,
    ForestFireModel,
    ReferenceCrowdModel,
    ReferenceForestFire,
)


class TestLinearFit:
    """Tests for the abstract base."""

    def test_model_raises_not_implemented(self) -> None:
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        with pytest.raises(NotImplementedError):
            fit.model(0.5)

    def test_step_is_noop(self) -> None:
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        fit.step()  # should not raise
        fit.step(0.01)  # should not raise

    def test_state_returns_defaults(self) -> None:
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        s = fit.state
        assert s["slope"] == pytest.approx(0.0)
        assert s["intercept"] == pytest.approx(0.0)
        assert s["r_squared"] == pytest.approx(0.0)

    def test_position_raises_not_implemented(self) -> None:
        """position() calls model() internally, so it should raise."""
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        with pytest.raises(NotImplementedError):
            fit.position()

    def test_energy_returns_defaults(self) -> None:
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        e = fit.energy()
        assert e["r_squared"] == pytest.approx(0.0)
        assert e["residual_sum_squares"] == pytest.approx(0.0)

    def test_shape_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="same shape"):
            LinearFit(
                x_data=np.array([0.0, 1.0, 2.0]),
                y_data=np.array([0.0, 1.0]),
            )

    def test_too_few_points_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 2"):
            LinearFit(
                x_data=np.array([0.0]),
                y_data=np.array([0.0]),
            )


class TestReferenceLinearFit:
    """Tests for the reference implementation."""

    def test_recovers_known_slope_intercept(self) -> None:
        """Fit a clean synthetic line y = 2x + 1."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        assert fit.slope() == pytest.approx(2.0, abs=1e-6)
        assert fit.intercept() == pytest.approx(1.0, abs=1e-6)

    def test_r_squared_perfect(self) -> None:
        """R² should be exactly 1 for noiseless data."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        assert fit.correlation_squared() == pytest.approx(1.0, abs=1e-10)

    def test_recovers_negative_slope(self) -> None:
        """Fit a line with negative slope y = -3x + 5."""
        x = np.array([0.0, 1.0, 2.0, 3.0])
        y = -3.0 * x + 5.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        assert fit.slope() == pytest.approx(-3.0, abs=1e-6)
        assert fit.intercept() == pytest.approx(5.0, abs=1e-6)

    def test_records_residuals(self) -> None:
        """Residuals should be zero for noiseless data."""
        x = np.array([0.0, 1.0, 2.0])
        y = 1.5 * x + 0.5
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        res = fit.residuals()
        assert np.allclose(res, 0.0, atol=1e-10)

    def test_model_evaluates(self) -> None:
        """model(x) should return slope*x + intercept."""
        x = np.array([0.0, 1.0, 2.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        assert fit.model(3.0) == pytest.approx(7.0, abs=1e-6)
        assert fit.model(-1.0) == pytest.approx(-1.0, abs=1e-6)

    def test_position_returns_arrays(self) -> None:
        """position() should return (x_fit, y_fit) arrays of length 200."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        x_fit, y_fit = fit.position()
        assert len(x_fit) == 200
        assert len(y_fit) == 200
        # y_fit should be approximately 2*x_fit + 1
        assert np.allclose(y_fit, 2.0 * x_fit + 1.0, atol=1e-6)

    def test_energy_returns_goodness_of_fit(self) -> None:
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        e = fit.energy()
        assert e["r_squared"] == pytest.approx(1.0, abs=1e-10)
        assert e["residual_sum_squares"] == pytest.approx(0.0, abs=1e-10)

    def test_step_is_noop(self) -> None:
        x = np.array([0.0, 1.0, 2.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        slope_before = fit.slope()
        fit.step()
        assert fit.slope() == pytest.approx(slope_before)

    def test_state_returns_fit_params(self) -> None:
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        s = fit.state
        assert s["slope"] == pytest.approx(2.0, abs=1e-6)
        assert s["intercept"] == pytest.approx(1.0, abs=1e-6)
        assert s["r_squared"] == pytest.approx(1.0, abs=1e-10)


class TestHelpers:
    """Tests for standalone helper functions."""

    def test_percent_error_standard(self) -> None:
        err = percent_error(estimated=9.77, accepted=9.81)
        expected = abs(9.77 - 9.81) / 9.81 * 100.0
        assert err == pytest.approx(expected)

    def test_percent_error_exact(self) -> None:
        err = percent_error(estimated=9.81, accepted=9.81)
        assert err == pytest.approx(0.0)

    def test_percent_error_zero_accepted_raises(self) -> None:
        with pytest.raises(ZeroDivisionError):
            percent_error(estimated=1.0, accepted=0.0)

    def test_propagate_uncertainty_noiseless(self) -> None:
        """With noiseless data, uncertainty should be very small."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        slope_err, intercept_err = propagate_uncertainty(
            slope=2.0, intercept=1.0, x_data=x, y_data=y
        )
        # Noiseless data → residuals are zero → s² = 0 → uncertainties are 0
        assert slope_err == pytest.approx(0.0, abs=1e-10)
        assert intercept_err == pytest.approx(0.0, abs=1e-10)

    def test_propagate_uncertainty_noisy(self) -> None:
        """With noisy data, uncertainties should be non-zero."""
        rng = np.random.default_rng(42)
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0 + rng.normal(0, 0.1, size=len(x))
        slope_err, intercept_err = propagate_uncertainty(
            slope=2.0, intercept=1.0, x_data=x, y_data=y
        )
        assert slope_err > 0.0
        assert intercept_err > 0.0

    def test_propagate_uncertainty_too_few_points(self) -> None:
        x = np.array([0.0, 1.0])
        y = np.array([0.0, 1.0])
        with pytest.raises(ValueError, match="at least 3"):
            propagate_uncertainty(slope=1.0, intercept=0.0, x_data=x, y_data=y)

    def test_propagate_uncertainty_collinear(self) -> None:
        """Identical x values should cause delta <= 0."""
        x = np.array([1.0, 1.0, 1.0])
        y = np.array([0.0, 1.0, 2.0])
        with pytest.raises(ValueError, match="non-positive"):
            propagate_uncertainty(slope=1.0, intercept=0.0, x_data=x, y_data=y)


class TestEpidemicModel:
    """Tests for the cellular-automaton epidemic model."""

    def test_abstract_raises(self) -> None:
        """Abstract base should raise NotImplementedError on step()."""
        from physics_core.inquiry.complex_systems import EpidemicModel

        m = EpidemicModel(rows=10, cols=10, p_infect=0.3, p_recover=0.1, seed=42)
        with pytest.raises(NotImplementedError):
            m.step()

    def test_initial_state(self) -> None:
        """Initial state: centre infected, rest susceptible."""
        m = get_ref_epidemic(rows=10, cols=10)
        s, i, r = m.sir_counts()
        assert s == 99
        assert i == 1
        assert r == 0

    def test_infection_spreads(self) -> None:
        """Infection spreads from the centre seed."""
        m = get_ref_epidemic(rows=50, cols=50, p_infect=0.5, p_recover=0.05)
        history = m.run(200)
        max_i = max(h[1] for h in history)
        assert max_i > 1, "Infection should spread from initial seed"

    def test_r_monotonic(self) -> None:
        """Recovered count must be non-decreasing."""
        m = get_ref_epidemic(rows=30, cols=30, p_infect=0.4, p_recover=0.08)
        history = m.run(150)
        r_counts = [h[2] for h in history]
        for i in range(1, len(r_counts)):
            assert r_counts[i] >= r_counts[i - 1], (
                f"R dropped at step {i}: {r_counts[i - 1]} -> {r_counts[i]}"
            )

    def test_deterministic_same_seed(self) -> None:
        """Same seed produces identical trajectory."""
        m1 = get_ref_epidemic(rows=30, cols=30, p_infect=0.3, p_recover=0.1)
        m2 = get_ref_epidemic(rows=30, cols=30, p_infect=0.3, p_recover=0.1)
        h1 = m1.run(100)
        h2 = m2.run(100)
        for i, (a, b) in enumerate(zip(h1, h2)):
            assert a == b, f"Trajectory diverged at step {i}: {a} vs {b}"

    def test_no_infection_when_p_infect_zero(self) -> None:
        """p_infect=0 means no spread beyond the initial seed."""
        m = get_ref_epidemic(rows=20, cols=20, p_infect=0.0, p_recover=0.1)
        history = m.run(50)
        peak_i = max(h[1] for h in history)
        assert peak_i <= 1, (
            f"With p_infect=0, max I should be <= 1, got {peak_i}"
        )

    def test_run_returns_including_initial(self) -> None:
        """run(steps) returns steps+1 entries, starting with initial state."""
        m = get_ref_epidemic(rows=10, cols=10)
        h = m.run(50)
        assert len(h) == 51
        assert h[0] == (99, 1, 0)

    def test_grid_property_returns_copy(self) -> None:
        """grid property returns a copy, not a reference."""
        m = get_ref_epidemic(rows=10, cols=10)
        g = m.grid
        g[0, 0] = 99
        assert m.grid[0, 0] != 99

    def test_small_grid_raises(self) -> None:
        """Grids smaller than 3x3 raise ValueError."""
        with pytest.raises(ValueError):
            get_ref_epidemic(rows=2, cols=10)

    def test_invalid_p_infect_raises(self) -> None:
        with pytest.raises(ValueError):
            get_ref_epidemic(p_infect=-0.1)

    def test_invalid_p_recover_raises(self) -> None:
        with pytest.raises(ValueError):
            get_ref_epidemic(p_recover=1.5)

    def test_basic_reproduction_number(self) -> None:
        """R0 computation is correct."""
        from physics_core.inquiry.complex_systems import basic_reproduction_number

        r0 = basic_reproduction_number(0.5, 0.1)
        assert r0 == pytest.approx(20.0)
        # When p_recover is zero, R0 is infinite
        import math
        assert basic_reproduction_number(0.3, 0.0) == math.inf

    def test_history_accessor(self) -> None:
        """history() returns the per-step S/I/R counts."""
        m = get_ref_epidemic(rows=10, cols=10, p_infect=0.5, p_recover=0.05)
        m.run(10)
        h = m.history()
        assert len(h) == 11  # initial + 10 steps


def get_ref_epidemic(
    rows: int = 50,
    cols: int = 50,
    p_infect: float = 0.3,
    p_recover: float = 0.1,
    seed: int = 42,
):
    """Helper: create a ReferenceEpidemicModel for testing."""
    from physics_core.inquiry.complex_systems import ReferenceEpidemicModel

    return ReferenceEpidemicModel(
        rows=rows, cols=cols, p_infect=p_infect, p_recover=p_recover, seed=seed
    )


class TestForestFire:
    """Tests for the forest-fire cellular automaton."""

    def test_abstract_raises(self) -> None:
        """Abstract base should raise NotImplementedError on step()."""
        m = ForestFireModel(rows=10, cols=10, p_ignite=0.3, seed=42)
        with pytest.raises(NotImplementedError):
            m.step()

    def test_initial_state(self) -> None:
        """Initial state: centre burning, no burned cells yet."""
        m = get_ref_fire(rows=20, cols=20)
        trees, burning, burned = m.fire_counts()
        assert burning == 1
        assert burned == 0
        assert trees > 0

    def test_deterministic_same_seed(self) -> None:
        """Same seed produces an identical fire trajectory."""
        m1 = get_ref_fire(rows=30, cols=40, p_ignite=0.4, wind_bias=0.3)
        m2 = get_ref_fire(rows=30, cols=40, p_ignite=0.4, wind_bias=0.3)
        h1 = m1.run(60)
        h2 = m2.run(60)
        for i, (a, b) in enumerate(zip(h1, h2)):
            assert a == b, f"Trajectory diverged at step {i}: {a} vs {b}"

    def test_single_ignition_eventually_burns_out(self) -> None:
        """A single ignition burns out: burning → 0 with burned > 0."""
        m = get_ref_fire(rows=30, cols=30, p_ignite=0.4, seed=5)
        history = m.run(30 * 30)
        trees, burning, burned = history[-1]
        assert burning == 0, f"Fire never died out: {burning} burning"
        assert burned > 0, "Fire should have consumed some trees"

    def test_wind_biases_direction(self) -> None:
        """Wind shifts the burned centroid toward the downwind direction."""
        east = get_ref_fire(
            rows=40, cols=60, p_ignite=0.4, wind_direction=0,
            wind_bias=0.5, seed=11,
        )
        west = get_ref_fire(
            rows=40, cols=60, p_ignite=0.4, wind_direction=2,
            wind_bias=0.5, seed=11,
        )
        east.run(30)
        west.run(30)

        def centroid(model: ReferenceForestFire) -> float:
            mask = (model.grid == 2) | (model.grid == 3)  # burning | burned
            r_, c_ = np.where(mask)
            return float(c_.mean()) if len(c_) else float("nan")

        assert centroid(east) > centroid(west), (
            f"East wind should push the fire east (col centroid "
            f"{centroid(east):.2f} vs {centroid(west):.2f})"
        )

    def test_run_returns_including_initial(self) -> None:
        """run(steps) returns steps+1 entries, starting with the initial state."""
        m = get_ref_fire(rows=10, cols=10)
        h = m.run(20)
        assert len(h) == 21
        assert h[0][1] == 1  # one burning cell at t=0

    def test_grid_property_returns_copy(self) -> None:
        """grid property returns a copy, not a reference."""
        m = get_ref_fire(rows=10, cols=10)
        g = m.grid
        g[0, 0] = 99
        assert m.grid[0, 0] != 99

    def test_small_grid_raises(self) -> None:
        """Grids smaller than 3x3 raise ValueError."""
        with pytest.raises(ValueError):
            get_ref_fire(rows=2, cols=10)

    def test_invalid_p_ignite_raises(self) -> None:
        with pytest.raises(ValueError):
            get_ref_fire(p_ignite=1.5)

    def test_invalid_wind_direction_raises(self) -> None:
        with pytest.raises(ValueError):
            get_ref_fire(wind_direction=4)
        with pytest.raises(ValueError):
            get_ref_fire(wind_direction=-1)

    def test_history_accessor(self) -> None:
        """history() returns the per-step fire counts."""
        m = get_ref_fire(rows=10, cols=10)
        m.run(10)
        h = m.history()
        assert len(h) == 11  # initial + 10 steps


class TestCrowdModel:
    """Tests for the agent-based crowd-evacuation model."""

    def test_abstract_raises(self) -> None:
        """Abstract base should raise NotImplementedError on step()."""
        c = CrowdModel(n_agents=5, seed=42)
        with pytest.raises(NotImplementedError):
            c.step()

    def test_initial_state(self) -> None:
        """Initially no one has exited and all agents are inside the hall."""
        c = get_ref_crowd(n_agents=10, seed=42)
        mean_speed, exited, pressure = c.crowd_metrics()
        assert exited == 0
        assert c.positions.shape == (10, 2)
        assert np.all(c.positions >= 0)
        assert np.all(c.positions[:, 0] <= c.hall_width)
        assert np.all(c.positions[:, 1] <= c.hall_height)

    def test_deterministic_same_seed(self) -> None:
        """Same seed produces an identical agent trajectory."""
        c1 = get_ref_crowd(n_agents=20, seed=7)
        c2 = get_ref_crowd(n_agents=20, seed=7)
        for _ in range(60):
            c1.step()
            c2.step()
            assert np.array_equal(c1.positions, c2.positions)

    def test_all_agents_eventually_exit(self) -> None:
        """With enough steps every agent reaches the exit."""
        c = get_ref_crowd(n_agents=25, seed=7)
        c.run(3000)
        assert np.all(c.exited)

    def test_all_exit_under_high_panic(self) -> None:
        """Even an evacuating crowd under high panic fully clears."""
        c = ReferenceCrowdModel(
            n_agents=40, base_speed=1.0, panic=1.2, seed=9
        )
        c.run(3000)
        assert np.all(c.exited)

    def test_crowding_slows_mean_speed(self) -> None:
        """A crowded hall slows mean speed vs an empty hall."""
        empty = get_ref_crowd(
            n_agents=1,
            init_positions=np.array([[5.0, 3.0]]),
            seed=1,
        )
        empty.step()
        empty_speed = empty.crowd_metrics()[0]

        rng = np.random.default_rng(3)
        cluster = np.column_stack(
            [
                rng.uniform(4.5, 5.5, 20),
                rng.uniform(2.5, 3.5, 20),
            ]
        )
        crowded = get_ref_crowd(
            n_agents=20, init_positions=cluster, seed=1
        )
        crowded.step()
        crowd_speed = crowded.crowd_metrics()[0]

        assert crowd_speed < empty_speed, (
            f"Crowding should slow mean speed "
            f"({crowd_speed:.3f} vs empty {empty_speed:.3f})"
        )

    def test_higher_panic_faster_exit_but_higher_pressure(self) -> None:
        """Panic gives a faster initial rush but a larger door bottleneck."""
        low = get_ref_crowd(
            n_agents=60, base_speed=0.9, panic=0.0, exit_size=0.8, seed=9
        )
        high = get_ref_crowd(
            n_agents=60, base_speed=0.9, panic=1.2, exit_size=0.8, seed=9
        )
        h_low = low.run(800)
        h_high = high.run(800)

        # Both fully evacuate.
        assert h_low[-1][1] == 60
        assert h_high[-1][1] == 60

        # At the initial rush (step 18) high panic exits faster...
        assert h_high[18][1] > h_low[18][1]
        # ...while piling up a bigger crowd at the door.
        assert h_high[18][2] > h_low[18][2]

    def test_run_returns_including_initial(self) -> None:
        """run(steps) returns steps+1 metric rows, starting with the initial."""
        c = get_ref_crowd(n_agents=10, seed=42)
        h = c.run(20)
        assert len(h) == 21
        mean_speed, exited, pressure = h[0]
        assert exited == 0

    def test_invalid_n_agents_raises(self) -> None:
        with pytest.raises(ValueError):
            get_ref_crowd(n_agents=0)

    def test_invalid_panic_raises(self) -> None:
        with pytest.raises(ValueError):
            get_ref_crowd(n_agents=5, panic=-0.1)

    def test_init_positions_outside_hall_raises(self) -> None:
        with pytest.raises(ValueError):
            get_ref_crowd(
                n_agents=5,
                init_positions=np.array(
                    [[50.0, 3.0], [5.0, 3.0], [5.0, 3.0], [5.0, 3.0], [5.0, 3.0]]
                ),
            )

    def test_metric_types(self) -> None:
        """crowd_metrics returns (float, int, int)."""
        c = get_ref_crowd(n_agents=10, seed=42)
        c.step()
        mean_speed, exited, pressure = c.crowd_metrics()
        assert isinstance(mean_speed, float)
        assert isinstance(exited, int)
        assert isinstance(pressure, int)


def get_ref_fire(
    rows: int = 50,
    cols: int = 50,
    p_ignite: float = 0.3,
    wind_direction: int = 0,
    wind_bias: float = 0.0,
    burn_duration: int = 1,
    tree_density: float = 0.85,
    seed: int = 42,
) -> ReferenceForestFire:
    """Helper: create a ReferenceForestFire for testing."""
    return ReferenceForestFire(
        rows=rows,
        cols=cols,
        p_ignite=p_ignite,
        wind_direction=wind_direction,
        wind_bias=wind_bias,
        burn_duration=burn_duration,
        tree_density=tree_density,
        seed=seed,
    )


def get_ref_crowd(
    n_agents: int = 20,
    hall_width: float = 10.0,
    hall_height: float = 6.0,
    exit_size: float = 1.0,
    base_speed: float = 1.0,
    panic: float = 0.0,
    neighbour_radius: float = 0.8,
    agent_radius: float = 0.12,
    exit_radius: float = 1.0,
    exit_on: str = "right",
    seed: int = 42,
    init_positions: Optional[np.ndarray] = None,
) -> ReferenceCrowdModel:
    """Helper: create a ReferenceCrowdModel for testing."""
    return ReferenceCrowdModel(
        n_agents=n_agents,
        hall_width=hall_width,
        hall_height=hall_height,
        exit_size=exit_size,
        base_speed=base_speed,
        panic=panic,
        neighbour_radius=neighbour_radius,
        agent_radius=agent_radius,
        exit_radius=exit_radius,
        exit_on=exit_on,
        seed=seed,
        init_positions=init_positions,
    )