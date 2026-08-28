# Scientific Inquiry — Concept Questions

These questions test your understanding of the scientific inquiry process
and data analysis techniques used in the exercise.  Answer them in a few
sentences each.

---

## Questions

### (a) Identifying variables

You are designing an experiment to investigate how the period of a simple
pendulum depends on its length.

1. What is the **independent variable**?
2. What is the **dependent variable**?
3. List at least **three control variables** that must be kept constant.

### (b) Why linearise?

You collect (L, T) data from a pendulum experiment.  The relationship
between T and L is non-linear: T = 2π √(L/g).

1. Why do we plot T² vs L instead of T vs L?
2. What quantity does the slope of the T² vs L graph represent?
3. What would the intercept be if the data were perfect?

### (c) Best-fit line vs passing through origin

When you fit a straight line to the T² vs L data, the best-fit line may
not pass exactly through the origin (0, 0), even though theory predicts
it should.

1. Why might the best-fit line not pass through the origin?
2. Should you force the line through the origin?  Explain the trade-off.
3. What does a non-zero intercept tell you about your data or experiment?

### (d) Percent error

You estimate g = 9.65 m/s² from your pendulum data.  The accepted value
is g = 9.81 m/s².

1. Compute the percent error of your estimate.
2. Is this a small or large error?  What might cause it?
3. How would the percent error change if you used a longer pendulum?

### (e) Systematic vs random error

Classify each of the following as **systematic** or **random** error:

1. Air resistance slowing the pendulum swing.
2. Parallax error when reading the angle from a protractor.
3. Human reaction time when starting/stopping a stopwatch.
4. The small-angle approximation (sin θ ≈ θ).
5. Pixel-tracking jitter in video analysis.

For each, explain whether it makes the measured period longer, shorter, or
unpredictable.

### (f) Evaluation and limitations

After completing your experiment and analysis, you are asked to evaluate
your investigation.

1. List at least **two limitations** of your experimental design.
2. Suggest **one improvement** to reduce the dominant source of error.
3. How confident are you in your estimated value of g?  What evidence
   supports your confidence?
4. If your percent error is large, does that mean the experiment was a
   failure?  Explain.

---

## Model Answers (teacher only)

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. **Independent variable**: Length of the pendulum (L).
2. **Dependent variable**: Period of oscillation (T).
3. **Control variables**: Mass of the bob, initial angular displacement
   (amplitude), air resistance (same environment), release method (no
   initial push), timing method.

### (b) Model answer

1. Plotting T² vs L linearises the relationship: T² = (4π²/g) × L is a
   straight line through the origin.  A straight line is easier to fit,
   analyse, and interpret than a curve.
2. The slope represents 4π²/g.  From the slope, we can estimate g:
   g = 4π² / slope.
3. The intercept should be zero (T² = 0 when L = 0).

### (c) Model answer

1. A non-zero intercept can arise from measurement errors (systematic
   offset in timing, incorrect length measurement), or from the fact that
   the pendulum has a finite bob size (effective length ≠ measured length).
2. Forcing through the origin is generally not recommended unless you are
   certain the relationship passes through (0, 0).  Forcing can bias the
   slope estimate.  It is better to fit freely and examine the intercept
   — if it is close to zero, the model is validated.
3. A non-zero intercept suggests either a systematic error in the
   measurements or that the assumed model (T² = (4π²/g) × L) is incomplete
   (e.g., the effective length includes the bob radius).

### (d) Model answer

1. Percent error = |9.65 - 9.81| / 9.81 × 100 ≈ 1.63%.
2. This is a relatively small error (~1.6%), suggesting the experiment was
   reasonably accurate.  Possible causes: air resistance, small-angle
   approximation error, timing precision, length measurement error.
3. A longer pendulum has a longer period, which reduces the relative
   effect of timing errors (fixed ±0.1 s reaction time is a smaller
   fraction of a longer period).  So percent error would likely decrease.

### (e) Model answer

| Source | Type | Effect on period |
|--------|------|-----------------|
| Air resistance | Systematic | Increases T (slows the pendulum) |
| Parallax error | Random | Unpredictable (random scatter) |
| Human reaction time | Random | Random scatter (±0.1–0.2 s) |
| Small-angle approximation | Systematic | True period is slightly longer than predicted |
| Pixel-tracking jitter | Random | Random noise in angle measurement |

### (f) Model answer

1. **Limitations**: (i) Small-angle approximation introduces systematic
   error; (ii) human reaction time limits timing precision; (iii) only
   one trial per length (no repeat measurements to estimate uncertainty).
2. **Improvement**: Use a photogate or light sensor with a data logger to
   measure the period automatically, eliminating human reaction time.
   Repeat measurements at each length to estimate random uncertainty.
3. Confidence is supported by: R² close to 1 (good linear fit), small
   percent error, and consistency with the theoretical model.  If R² is
   low or percent error is large, confidence is reduced.
4. No — a large percent error is not a failure.  It is an opportunity to
   identify sources of error, improve the experimental design, and learn
   about the limitations of the measurement.  Science progresses by
   understanding and reducing errors.
