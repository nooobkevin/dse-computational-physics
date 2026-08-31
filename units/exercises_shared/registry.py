"""Registry of per-unit exercise graders for ``tools/grade_exercise.py``.

Each unit ships one or more exercise test files under
``units/<unit>/exercises/``.  Every test file reads the student
implementation through a conftest override flag (e.g. ``--override-student``,
``--override-student-stars``).  This registry records, per unit:

* the exercise test file(s) to run,
* the conftest override flag each test file honours,
* the hidden solution file used for teacher self-checks (gitignored).

``tools/grade_exercise.py`` consults this registry to know which flag to pass
for each test file and which solution to grade against in ``--selfcheck``
mode.  The registry is authoritative; a unit not listed here falls back to
glob discovery (``test_*_exercise.py``) plus the shared ``--override-student``
flag when the conftest defines it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExerciseSpec:
    """One exercise test file inside a unit's ``exercises/`` directory."""

    test_file: str
    """Test file name, relative to the unit's ``exercises/`` directory."""

    override_flag: str
    """Pytest CLI flag the test file's conftest reads for the student file."""

    solution_file: str | None = None
    """Hidden solution file name (gitignored) that makes every test pass."""


UNIT_EXERCISES: dict[str, tuple[ExerciseSpec, ...]] = {
    "01_mechanics": (
        ExerciseSpec("test_exercise.py", "--override-student", "pendulum_solution.py"),
        ExerciseSpec(
            "test_kinematics_exercise.py", "--override-student", "kinematics_solution.py"
        ),
    ),
    "02_thermal": (
        ExerciseSpec("test_exercise.py", "--override-student", "gas_solution.py"),
    ),
    "03_waves": (
        ExerciseSpec("test_exercise.py", "--override-student", "wave_solution.py"),
    ),
    "04_em": (
        ExerciseSpec("test_exercise.py", "--override-student", "em_solution.py"),
    ),
    "05_engineering": (
        ExerciseSpec("test_exercise.py", "--override-student", "engineering_solution.py"),
        ExerciseSpec("test_orbital_exercise.py", "--override-student", "orbital_solution.py"),
        ExerciseSpec(
            "test_power_rating_exercise.py", "--override-student", "power_rating_solution.py"
        ),
    ),
    "06_society": (
        ExerciseSpec("test_exercise.py", "--override-student", "society_solution.py"),
        ExerciseSpec(
            "test_energy_exercise.py", "--override-student-energy", "energy_solution.py"
        ),
        ExerciseSpec(
            "test_decay_analysis_exercise.py",
            "--override-student-decay-analysis",
            "decay_analysis_solution.py",
        ),
    ),
    "07_quantum": (
        ExerciseSpec("test_exercise.py", "--override-student", "hydrogen_solution.py"),
    ),
    "08_astrophysics": (
        ExerciseSpec("test_exercise.py", "--override-student", "astrophysics_solution.py"),
        ExerciseSpec(
            "test_stars_exercise.py", "--override-student-stars", "stars_solution.py"
        ),
    ),
    "09_inquiry": (
        ExerciseSpec("test_exercise.py", "--override-student", "inquiry_solution.py"),
        ExerciseSpec(
            "test_design.py", "--override-design-student", "design_solution.py"
        ),
        ExerciseSpec(
            "test_data_analysis.py", "--override-data-student", "data_analysis_solution.py"
        ),
    ),
}

# Unit used by ``tools/grade_exercise.py --selfcheck``: a single-exercise
# unit whose solution file makes every test pass, so the CLI must print
# a 100% scorecard.
SELFCHECK_UNIT = "03_waves"