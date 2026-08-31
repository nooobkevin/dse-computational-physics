# Unit 02: Thermal Physics 熱學 — S4

## Learning Outcomes 學習目標
- **Kinetic theory** 分子動力論: temperature as average molecular KE.
- **Gas laws** 氣體定律: Boyle, pressure, Charles; combine to $pV/T = \text{const}$.
- **Absolute zero** 絕對零度: determine by p–T extrapolation.
- **Maxwell–Boltzmann** 麥克斯韋–玻爾茲曼: interpret speed distribution vs temperature.
- **Random walk** 隨機行走: RMS displacement grows as $\sqrt{N}$ (diffusion).
- **Specific heat** 比熱容: fit $Q$ vs $\Delta T$ to find $c$.

## Key Formulas 核心公式
| Formula | Meaning |
|---|---|
| $KE_{avg} = \frac{3}{2}kT$ | avg KE per molecule |
| $c = \frac{Q}{m\Delta T}$ | specific heat capacity |
| $pV = NkT$ | ideal gas law (sim units) |
| $pV = nRT$ | ideal gas law (real) |
| $P \propto 1/V,\ P \propto T,\ V \propto T$ | empirical gas laws |
| $r_{RMS} = s\sqrt{N}$ | random-walk RMS |
| $T(K) = T(°C) + 273.15$ | Kelvin–Celsius |

## Lesson Flow 課堂流程
1. **Watch** 觀看: `RandomWalkScene.mp4`, `MaxwellBoltzmann.mp4`, `PressureStatistical.mp4`, `IntegratorConvergence.mp4`.
2. **Interact** 互動: teacher app `--mode gas` (MB overlay, live pressure) and `--mode gas_laws` (Boyle + absolute-zero extrapolation).
3. **Code** 編程: `gas_exercise.py` (fill `_collide_wall`, `_collide_particle`) or `specific_heat_exercise.py` (fit → c).

## Simulation Commands 指令
```bash
uv sync
uv run python units/02_thermal/teacher_app/main.py --mode gas_laws
bash units/02_thermal/manim/render.sh random_walk -ql   # Docker
uv run pytest units/02_thermal/exercises/test_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/02_thermal/exercises/test_exercise.py -v` (gas + `-k TestSpecificHeat`).
- **Quiz** 小測: `uv run pytest units/02_thermal/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/02_thermal/exercises/quiz_solution.py uv run pytest units/02_thermal/exercises/test_quiz.py` (expect 10 passes).