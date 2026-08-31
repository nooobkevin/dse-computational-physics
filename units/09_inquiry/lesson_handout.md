# Unit 09: Scientific Inquiry in Physics 物理科學探究 — S4–S6

## Learning Outcomes 學習目標
- **Data analysis** 數據分析: linearisation ($1/x$, $1/x^2$); best-fit line; slope → physical quantity.
- **Uncertainty & outliers** 不確定度與離群值: error bars; IQR outlier detection; percent uncertainty.
- **Complex systems** 複雜系統: SIR epidemic, forest fire, crowd evacuation cellular automata.
- **Engineering design** 工程設計: pendulum-clock design loop (Design, Build, Test, Analyse, Improve).
- **Investigation report** 探究報告: structure a full scientific investigation.
- **AI & safety evaluation** AI 與安全評估: critically evaluate AI-generated analysis; hazard identification.

## Key Formulas 核心公式
| Formula | Meaning |
|---|---|
| $T^2 = \frac{4\pi^2}{g}L$ | pendulum linearisation → g |
| $y = mx + c$ | best-fit line |
| $\text{percent uncertainty} = \frac{\Delta x}{x}\times100\%$ | relative error |
| $s = \tfrac{1}{2}gt^2$ | free-fall linearisation |
| SIR: $\frac{dS}{dt} = -\beta SI$ | epidemic model |
| $T = 2\pi\sqrt{L/g}$ | pendulum period (design) |

## Lesson Flow 課堂流程
1. **Watch** 觀看: `Linearisation.mp4`, `LinearisationTransforms.mp4`, `Uncertainty.mp4`, `UncertaintyRepeated.mp4`, `Conclusion.mp4`, `EpidemicSpread.mp4`, `ForestFire.mp4`, `CrowdControl.mp4`, `EngineeringDesign.mp4`.
2. **Interact** 互動: teacher app `--mode analysis|experiment|epidemic|fire|crowd|design`.
3. **Code** 編程: `inquiry_exercise.py` (linear fit), `design_exercise.py` (fit_slope, recommended_length), or `data_analysis_exercise.py` (to_si, remove_outliers, estimate_g).

## Simulation Commands 指令
```bash
uv sync
uv run python units/09_inquiry/teacher_app/main.py --mode epidemic
bash units/09_inquiry/manim/render.sh epidemic -ql   # Docker
uv run pytest units/09_inquiry/exercises/test_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/09_inquiry/exercises/test_exercise.py -v` (also `test_design.py`, `test_data_analysis.py`).
- **Quiz** 小測: `uv run pytest units/09_inquiry/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/09_inquiry/exercises/quiz_solution.py uv run pytest units/09_inquiry/exercises/test_quiz.py` (expect 10 passes).