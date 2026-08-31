# Unit 05: Physics and Engineering 工程物理 — S5

## Learning Outcomes 學習目標
- **Electromagnetic induction** 電磁感應: flux $\Phi = BA\cos\theta$; Faraday $\varepsilon = -\Delta\Phi/\Delta t$; Lenz's law.
- **Transformer** 變壓器: $V_p/V_s = N_p/N_s$; power conservation; efficiency.
- **Domestic electricity** 家居電力: $I = P/V$; fuse selection; kWh cost.
- **Orbital motion** 軌道運動: $F = GMm/r^2$; $v_{orb} = \sqrt{GM/r}$; $v_{esc} = \sqrt{2GM/r}$.
- **Bernoulli** 伯努利: $P + \rho gh + \tfrac{1}{2}\rho v^2 = \text{const}$; pitot tube.
- **Energy conservation** 能量守恆: $U = -GMm/r$; KE/GPE/total.

## Key Formulas 核心公式
| Formula | Meaning |
|---|---|
| $\Phi = BA\cos\theta$ | magnetic flux |
| $\varepsilon = -\frac{\Delta\Phi}{\Delta t}$ | Faraday's law |
| $\frac{V_p}{V_s} = \frac{N_p}{N_s}$ | transformer ratio |
| $I = \frac{P}{V}$ | operating current |
| $F = \frac{GMm}{r^2}$ | gravitation |
| $v_{orb} = \sqrt{\frac{GM}{r}}$ | orbital velocity |
| $v_{esc} = \sqrt{\frac{2GM}{r}}$ | escape velocity |
| $P + \rho gh + \tfrac{1}{2}\rho v^2 = \text{const}$ | Bernoulli |

## Lesson Flow 課堂流程
1. **Watch** 觀看: `OrbitalMotion.mp4`, `BernoulliPitot.mp4`, `ElectromagneticInduction.mp4`, `TransformerScene.mp4`, `MotorEffect.mp4`.
2. **Interact** 互動: teacher app `--mode transformer|orbital|induction` (+ `fibre` enrichment).
3. **Code** 編程: `orbital_exercise.py` (5 hooks) or `power_rating_exercise.py` (I, fuse, kWh, cost).

## Simulation Commands 指令
```bash
uv sync
uv run python units/05_engineering/teacher_app/main.py --mode orbital
bash units/05_engineering/manim/render.sh orbital_motion -ql   # Docker
uv run pytest units/05_engineering/exercises/test_orbital_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/05_engineering/exercises/test_orbital_exercise.py -v` (also `test_power_rating_exercise.py`).
- **Quiz** 小測: `uv run pytest units/05_engineering/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/05_engineering/exercises/quiz_solution.py uv run pytest units/05_engineering/exercises/test_quiz.py` (expect 10 passes).