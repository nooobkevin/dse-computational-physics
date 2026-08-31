# Unit 03: Waves 波動 — S4

## Learning Outcomes 學習目標
- **Nature of waves** 波的性質: $v = f\lambda$; transverse vs longitudinal; energy $\propto A^2$.
- **Superposition & standing waves** 疊加與駐波: two counter-propagating waves → nodes.
- **Young's double-slit** 楊氏雙縫: $d\sin\theta = n\lambda$; fringe spacing $\Delta y = \lambda D/d$.
- **Polarisation** 偏振: Malus's law $I = I_0\cos^2\theta$.
- **EM spectrum** 電磁波譜: bands radio → gamma; visible 400–700 nm.
- **Ultrasound** 超聲波: pulse-echo ranging $d = vt/2$.

## Key Formulas 核心公式
| Formula | Meaning |
|---|---|
| $v = f\lambda$ | wave speed |
| $y(x,t) = A\sin(kx - \omega t)$ | traveling wave |
| $I \propto A^2$ | intensity vs amplitude |
| $d\sin\theta = n\lambda$ | double-slit maxima |
| $I = I_0\cos^2\theta$ | Malus's law |
| $I = I_0/r^2$ | inverse-square law |
| $d = \frac{vt}{2}$ | ultrasound echo distance |

## Lesson Flow 課堂流程
1. **Watch** 觀看: `SuperpositionStanding.mp4`, `WaveSpeedIntensity.mp4`, `YoungSlit.mp4`, `Polarisation.mp4`, `UltrasoundRanging.mp4`, `EMSpectrum.mp4`.
2. **Interact** 互動: teacher app `--mode traveling|standing|interference|inverse_square` (fully synthetic).
3. **Code** 編程: `wave_exercise.py` (fill `displacement(self, x, t)`).

## Simulation Commands 指令
```bash
uv sync
uv run python units/03_waves/teacher_app/main.py --mode interference
bash units/03_waves/manim/render.sh polarisation -ql   # Docker
uv run pytest units/03_waves/exercises/test_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/03_waves/exercises/test_exercise.py -v` (auto-grader).
- **Quiz** 小測: `uv run pytest units/03_waves/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/03_waves/exercises/quiz_solution.py uv run pytest units/03_waves/exercises/test_quiz.py` (expect 10 passes).