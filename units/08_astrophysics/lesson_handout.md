# Unit 08: Astrophysics and Relativity 天文物理與相對論 — S6

## Learning Outcomes 學習目標
- **Parallax** 視差: distance $d = 1/p$; light year, AU, parsec.
- **Blackbody & H-R diagram** 黑體與赫羅圖: Wien's law; Stefan–Boltzmann $L = 4\pi R^2\sigma T^4$.
- **Doppler redshift** 都卜勒紅移: $\Delta\lambda/\lambda_0 = v_r/c$; Hubble's law $v = H_0 d$.
- **Dark matter** 暗物質: flat vs Keplerian rotation curves.
- **Time dilation & length contraction** 時間膨脹與長度收縮: $\Delta t = \Delta t_0/\sqrt{1-v^2/c^2}$.
- **Big Bang evidence** 大爆炸證據: redshift + CMB ($T = 2.725$ K).

## Key Formulas 核心公式
| Formula | Meaning |
|---|---|
| $d = \frac{1}{p}$ | parallax distance (pc) |
| $L = 4\pi R^2\sigma T^4$ | Stefan–Boltzmann |
| $\lambda_{peak} = \frac{b}{T}$ | Wien's law |
| $\frac{\Delta\lambda}{\lambda_0} = \frac{v_r}{c}$ | Doppler redshift |
| $v = H_0\,d$ | Hubble's law |
| $\Delta t = \frac{\Delta t_0}{\sqrt{1-v^2/c^2}}$ | time dilation |
| $l = l_0\sqrt{1-v^2/c^2}$ | length contraction |

## Lesson Flow 課堂流程
1. **Watch** 觀看: `DopplerRedshift.mp4`, `HubbleLawScene.mp4`, `SpacetimeDiagram.mp4`, `HRDiagramScene.mp4`, `BigBangEvidence.mp4` (+ `StellarLifecycle.mp4` enrichment).
2. **Interact** 互動: teacher app `--mode doppler|hubble|relativity|parallax` (+ `lifecycles` enrichment).
3. **Code** 編程: `astrophysics_exercise.py` (Doppler hooks) or `stars_exercise.py` (relativity + stars hooks).

## Simulation Commands 指令
```bash
uv sync
uv run python units/08_astrophysics/teacher_app/main.py --mode relativity
bash units/08_astrophysics/manim/render.sh spacetime_diagram -ql   # Docker
uv run pytest units/08_astrophysics/exercises/test_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/08_astrophysics/exercises/test_exercise.py -v` (also `test_stars_exercise.py`).
- **Quiz** 小測: `uv run pytest units/08_astrophysics/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/08_astrophysics/exercises/quiz_solution.py uv run pytest units/08_astrophysics/exercises/test_quiz.py` (expect 10 passes).