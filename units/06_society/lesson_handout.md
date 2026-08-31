# Unit 06: Physics and Society 物理與社會 — S5

## Learning Outcomes 學習目標
- **Radioactive decay** 放射性衰變: random nature; activity $A \propto N$; half-life from graph.
- **Radiation types** 輻射種類: alpha/beta/gamma penetrating & ionising power.
- **Chain reaction** 鏈式反應: neutron multiplication factor $k$; critical mass.
- **Mass–energy** 質能關係: $\Delta E = \Delta mc^2$; electron-volt & atomic mass unit.
- **Energy sources** 能源: solar $P = S\cdot A\cdot\eta$; wind $P = \tfrac{1}{2}\eta\rho Av^3$.
- **Radioisotope uses** 放射性同位素應用: radiotherapy, tracers, imaging.

## Key Formulas 核心公式
| Formula | Meaning |
|---|---|
| $N = N_0\,2^{-t/T}$ | decay curve (half-life form) |
| $p = 1 - e^{-\lambda dt}$ | decay probability (Monte Carlo) |
| $\Delta E = \Delta m\,c^2$ | mass–energy (1 amu ≈ 931.5 MeV) |
| $P = S\cdot A\cdot\eta$ | solar power |
| $P = \tfrac{1}{2}\eta\rho\pi r^2 v^3$ | wind power |
| $A = \lambda N$ | activity |

## Lesson Flow 課堂流程
1. **Watch** 觀看: `RadioactiveDecay.mp4`, `RadiationPenetration.mp4`, `ChainReaction.mp4`, `EnergySources.mp4`, `RadioisotopeUses.mp4`.
2. **Interact** 互動: teacher app `--mode decay|radiation|reactor|energy` (fully synthetic).
3. **Code** 編程: `society_exercise.py` (`decay_probability`), `energy_exercise.py` (mass-energy, solar, wind), or `decay_analysis_exercise.py` (half-life fit).

## Simulation Commands 指令
```bash
uv sync
uv run python units/06_society/teacher_app/main.py --mode decay
bash units/06_society/manim/render.sh energy_sources -ql   # Docker
uv run pytest units/06_society/exercises/test_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/06_society/exercises/test_exercise.py -v` (also `test_energy_exercise.py`, `test_decay_analysis_exercise.py`).
- **Quiz** 小測: `uv run pytest units/06_society/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/06_society/exercises/quiz_solution.py uv run pytest units/06_society/exercises/test_quiz.py` (expect 10 passes).