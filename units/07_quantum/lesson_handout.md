# Unit 07: Quantum Physics 量子物理 — S6

## Learning Outcomes 學習目標
- **Rutherford scattering** 盧瑟福散射: impact parameter $b$ → scattering angle $\theta$; nuclear model.
- **Photoelectric effect** 光電效應: $E = hf$; work function $\phi$; threshold $f_0$; $K_{max} = hf - \phi$.
- **Bohr hydrogen** 波耳氫原子: $E_n = -13.6/n^2$ eV; line spectra; ionisation.
- **Wave–particle duality** 波粒二象性: de Broglie $\lambda = h/p$; square well $E_n = n^2h^2/(8mL^2)$.
- **Superposition & uncertainty** 疊加與不確定原理: $|\psi\rangle = a|0\rangle + b|1\rangle$; $\Delta x\Delta p \ge \hbar/2$.
- **Laser** 雷射: population inversion; stimulated emission.

## Key Formulas 核心公式
| Formula | Meaning |
|---|---|
| $E = hf$ | photon energy |
| $K_{max} = hf - \phi$ | photoelectric balance |
| $E_n = -\frac{13.6}{n^2}\ \text{eV}$ | Bohr energy levels |
| $\frac{1}{\lambda} = R_H\left(\frac{1}{n_f^2} - \frac{1}{n_i^2}\right)$ | transition wavelength |
| $\lambda = \frac{h}{p}$ | de Broglie wavelength |
| $E_n = \frac{n^2h^2}{8mL^2}$ | square-well energy |
| $\Delta x\,\Delta p \ge \frac{\hbar}{2}$ | Heisenberg UP |

## Lesson Flow 課堂流程
1. **Watch** 觀看: `RutherfordScattering.mp4`, `HydrogenSpectra.mp4`, `SuperpositionState.mp4`, `EnergyLevels.mp4`, `Photoelectric.mp4`, `WavefunctionProbability.mp4`.
2. **Interact** 互動: teacher app `--mode rutherford|hydrogen|well|photoelectric|de_broglie|laser|uncertainty` (fully synthetic).
3. **Code** 編程: `hydrogen_exercise.py` (energy_level, transition_wavelength, ionisation_energy) or `quantum_exercise.py` (square-well energy).

## Simulation Commands 指令
```bash
uv sync
uv run python units/07_quantum/teacher_app/main.py --mode hydrogen
bash units/07_quantum/manim/render.sh rutherford_scattering -ql   # Docker
uv run pytest units/07_quantum/exercises/test_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/07_quantum/exercises/test_exercise.py -v` (add `-k Bohr` / `-k QuantumWell`).
- **Quiz** 小測: `uv run pytest units/07_quantum/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/07_quantum/exercises/quiz_solution.py uv run pytest units/07_quantum/exercises/test_quiz.py` (expect 10 passes).