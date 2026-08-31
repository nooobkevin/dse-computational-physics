# Unit 01: Mechanics 力學 — S4

## Learning Outcomes 學習目標
- **Kinematics** 運動學: use SUVAT equations and interpret s–t, v–t, a–t graphs.
- **Projectile motion** 拋體運動: independence of horizontal/vertical motion; effect of air resistance.
- **SHM & circular motion** 簡諧運動與圓周運動: SHM as projection of uniform circular motion.
- **Damping & resonance** 阻尼與共振: underdamped/critical/overdamped regimes; resonance curve.
- **Numerical methods** 數值方法: compare Euler vs Verlet energy drift.
- **MVA** 運動影片分析: estimate *g* from a tracked pendulum period.

## Key Formulas 核心公式
| Formula | Meaning |
|---|---|
| $v = \frac{\Delta s}{\Delta t},\ a = \frac{\Delta v}{\Delta t}$ | velocity, acceleration |
| $v^2 = u^2 + 2as$ | SUVAT (no time) |
| $x(t) = R\cos(\omega t)$ | SHM displacement |
| $T = 2\pi\sqrt{L/g}$ | pendulum period |
| $\alpha = -\frac{g}{L}\theta - b\,\omega$ | damped angular accel. |
| $KE = \tfrac{1}{2}mv^2,\ PE = mgh$ | mechanical energy |

## Lesson Flow 課堂流程
1. **Watch** 觀看: `ShmProjection.mp4`, `DampedSHM.mp4`, `Resonance.mp4`, `IntegratorConvergence.mp4`, `ProjectileDt.mp4`, `ProjectileDrag.mp4`, `PlanetFreeFall.mp4`.
2. **Interact** 互動: teacher app `--mode pendulum|circular|projectile` (pendulum = MVA, estimates *g*).
3. **Code** 編程: `pendulum_exercise.py` (fill `angular_acceleration`) or `kinematics_exercise.py` (5 SUVAT hooks).

## Simulation Commands 指令
```bash
uv sync
uv run python units/01_mechanics/teacher_app/main.py --mode pendulum
bash units/01_mechanics/manim/render.sh shm_projection -ql   # Docker
uv run pytest units/01_mechanics/exercises/test_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/01_mechanics/exercises/test_exercise.py -v` (auto-grader).
- **Quiz** 小測: `uv run pytest units/01_mechanics/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/01_mechanics/exercises/quiz_solution.py uv run pytest units/01_mechanics/exercises/test_quiz.py` (expect 10 passes).