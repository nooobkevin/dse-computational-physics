# Pendulum Exercise — Concept Questions (M5)

These questions test your understanding of the physics behind the pendulum
simulation you just implemented.  Answer them in a few sentences each.

---

## Questions

### (a) Estimating *g* from the measured period

You run your pendulum simulation with `length = 1.0 m` and measure an
oscillation period of `T = 2.01 s`.

1. Use the small-angle formula to estimate the gravitational acceleration
   *g* from these values.
2. Compute the percent error compared to the standard value *g* = 9.81 m/s².
3. Report your result with the appropriate number of significant figures.

### (b) Sources of error

In a real (physical) pendulum experiment, the measured period often differs
from the theoretical prediction.  List **at least three** sources of error
and explain how each one affects the measured period (does it make *T*
longer, shorter, or unpredictable?).

Consider:
- Air resistance / drag
- Parallax error when reading the angle
- The small-angle approximation
- Human reaction time when timing with a stopwatch
- Pixel-tracking noise (if using video analysis)

### (c) Explicit Euler vs. Velocity-Verlet

Your simulation can use either the Explicit Euler scheme or the
Velocity-Verlet scheme.  When you run the pendulum with Euler at a
moderate time-step (e.g. `dt = 0.01 s`), the total energy drifts upward
over time.  With Verlet at the same `dt`, the energy stays nearly constant.

1. Why does Explicit Euler cause energy drift?
2. Why does Velocity-Verlet conserve energy much better?
3. What would happen if you used a very small `dt` (e.g. `dt = 0.0001 s`)
   with Euler — would the drift disappear?  Explain.

*Hint: think about whether each method is **symplectic** (preserves phase-space
area) and whether the numerical trajectory obeys a conserved quantity.*

### (d) Small-angle approximation

The small-angle formula for the period is `T = 2π √(L/g)`, which assumes
`sin(θ) ≈ θ`.

1. For what range of initial amplitudes is this approximation valid?
   (State a quantitative condition, e.g. "θ₀ < X rad" or "error < Y%".)
2. If you start the pendulum at `θ₀ = 0.5 rad` (≈ 29°), will the true
   period be longer or shorter than the small-angle prediction?  Why?
3. At what amplitude does the small-angle approximation overestimate or
   underestimate the period by more than 1%?

---

## Model Answers (teacher only)

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. From `T = 2π √(L/g)`, solving for *g*:

       g = (4π² L) / T²
       g = (4π² × 1.0) / (2.01)²
       g ≈ 39.478 / 4.0401 ≈ 9.77 m/s²

2. Percent error vs 9.81:

       % error = |9.77 - 9.81| / 9.81 × 100 ≈ 0.41%

3. Significant figures: *T* = 2.01 has 3 sig figs, *L* = 1.0 has 2 sig figs.
   The result should be reported to 2 sig figs: *g* ≈ 9.8 m/s² (or 9.77 m/s²
   if keeping 3 sig figs from *T*).  The percent error is 0.4%.

### (b) Model answer

| Source | Effect on period | Explanation |
|--------|-----------------|-------------|
| Air resistance / drag | Increases *T* (slows the pendulum) | Drag opposes motion, reducing the effective restoring force and increasing the period. |
| Parallax error | Random / systematic | Misreading the angle from the side introduces random error in amplitude measurement; if consistently off, it biases the period measurement. |
| Small-angle approximation | Systematic — true period is slightly longer | The true period for a physical pendulum is longer than `2π√(L/g)` because `sin(θ) < θ` for θ > 0, reducing the restoring torque. |
| Human reaction time | Random error, typically ±0.1–0.2 s | Starting/stopping the stopwatch late adds random scatter.  Averaging over many periods reduces this. |
| Pixel-tracking noise | Random error in amplitude/position | Sub-pixel jitter in video tracking introduces noise in the measured angle, which propagates to period estimates. |

### (c) Model answer

1. **Explicit Euler** updates position and velocity using the *current*
   acceleration only.  This is a first-order method that does not respect
   the geometric structure of Hamiltonian systems.  The numerical trajectory
   does not lie on the constant-energy surface; instead it systematically
   drifts to higher energy (the method is not symplectic — it expands
   phase-space area).

2. **Velocity-Verlet** is a symplectic integrator: it preserves phase-space
   area and approximately conserves a "shadow Hamiltonian" close to the true
   Hamiltonian.  As a result, the total energy oscillates around the true
   value but does not systematically drift, even over long integration times.

3. With a very small `dt`, Euler's energy drift per step is smaller, but it
   is still systematic — the energy will still drift upward, just more
   slowly.  The drift does **not** disappear; it scales as O(dt).  Verlet's
   energy error oscillates with amplitude O(dt²) but does not drift, so
   Verlet is always preferable for long simulations.

### (d) Model answer

1. The small-angle approximation `sin(θ) ≈ θ` is accurate to within ~1% for
   `θ₀ < 0.14 rad` (≈ 8°).  A common rule of thumb is `θ₀ < 0.1 rad` (≈ 6°)
   for < 0.5% error.

2. The true period is **longer** than the small-angle prediction.  For
   `θ₀ = 0.5 rad`, `sin(θ) < θ`, so the restoring torque is weaker than the
   linear approximation, making the pendulum swing more slowly.

3. The error exceeds 1% for `θ₀ > 0.14 rad` (≈ 8°).  The exact threshold
   depends on the required precision; the period can be expressed as a
   series: `T_true = T_small × (1 + θ₀²/16 + 11θ₀⁴/3072 + ...)`.  The
   first correction term `θ₀²/16` exceeds 0.01 when `θ₀ > 0.4 rad`, but
   the full numerical error (including higher terms) reaches 1% at about
   `θ₀ ≈ 0.14 rad`.