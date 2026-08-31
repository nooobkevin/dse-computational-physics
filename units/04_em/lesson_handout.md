# Unit 04: Electricity and Magnetism 電與磁 — S4

## Learning Outcomes 學習目標
- **Current & resistance** 電流與電阻: $R = V/I$; ohmic vs non-ohmic I–V curves.
- **Circuits** 電路: KCL ($\Sigma I = 0$), KVL ($\Sigma V = 0$); series/parallel; power.
- **Electrostatics** 靜電學: Coulomb's law; field lines; $E = F/q$, $E = V/d$.
- **Magnetic fields** 磁場: $F = BIl\sin\theta$, $F = BQv\sin\theta$; right-hand rule.
- **Circular motion in B** 磁場中的圓周運動: $r = mv/(qB)$.
- **Electric motor** 電動機: torque $\tau = NBIAsin\phi$; commutator.

## Key Formulas 核心公式
| Formula | Meaning |
|---|---|
| $R = \frac{V}{I}$ | Ohm's law |
| $P = VI = I^2R = V^2/R$ | electrical power |
| $F = \frac{Q_1Q_2}{4\pi\varepsilon_0 r^2}$ | Coulomb's law |
| $E = \frac{V}{d}$ | uniform field |
| $F = BIl\sin\theta$ | force on conductor |
| $F = BQv\sin\theta$ | Lorentz force |
| $r = \frac{mv}{qB}$ | orbit radius |
| $\tau = NBIAsin\phi$ | motor torque |

## Lesson Flow 課堂流程
1. **Watch** 觀看: `ElectricFieldLines.mp4`, `PotentialGradient.mp4`, `CircuitComparison.mp4`, `MagneticForce.mp4`, `ElectricMotor.mp4`.
2. **Interact** 互動: teacher app `--mode field|circuit|magnet|solenoid|vi_graph|parallel|motor` (fully synthetic).
3. **Code** 編程: `em_exercise.py` (fill `field`, `potential`, `resolve`, `magnetic_force`, `orbit_radius`).

## Simulation Commands 指令
```bash
uv sync
uv run python units/04_em/teacher_app/main.py --mode motor
bash units/04_em/manim/render.sh magnetic_force -ql   # Docker
uv run pytest units/04_em/exercises/test_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/04_em/exercises/test_exercise.py -v` (auto-grader).
- **Quiz** 小測: `uv run pytest units/04_em/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/04_em/exercises/quiz_solution.py uv run pytest units/04_em/exercises/test_quiz.py` (expect 10 passes).