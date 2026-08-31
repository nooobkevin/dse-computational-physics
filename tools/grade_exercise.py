"""Grade a unit's exercise test suite and print a partial-credit scorecard.

Usage:
    uv run python tools/grade_exercise.py <unit_dir> [--student PATH] [--solution PATH]
    uv run python tools/grade_exercise.py --selfcheck

For each exercise test file under ``<unit_dir>/exercises/`` (discovered via
``test_*_exercise.py`` plus the registry in ``units/exercises_shared/``),
runs pytest with ``--junitxml`` into a temp file, passing the unit's
conftest override flag (e.g. ``--override-student``) when a student or
solution file is supplied.  Parses the XML and prints a scorecard:

* per-test status lines (PASS/FAIL with the failure message's first line),
* totals (tests, passed, failed) and a percentage score.

Exit code 0 if every test passed, 1 otherwise.

``--selfcheck`` runs the CLI itself (via subprocess) against one unit's own
solution file and asserts the scorecard prints 100% — used by CI.
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "units" / "exercises_shared" / "registry.py"


@dataclass(frozen=True)
class ExerciseSpec:
    """One exercise test file inside a unit's ``exercises/`` directory.

    Mirrors ``units/exercises_shared/registry.py`` (loaded dynamically below).
    """

    test_file: str
    override_flag: str
    solution_file: str | None = None


def _load_registry() -> tuple[dict[str, tuple[ExerciseSpec, ...]], str]:
    """Import the exercise registry from ``units/exercises_shared/registry.py``."""
    spec = importlib.util.spec_from_file_location("_exercise_registry", REGISTRY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load registry module: {REGISTRY_PATH}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_exercise_registry"] = mod
    spec.loader.exec_module(mod)
    exercises = cast(dict[str, tuple[ExerciseSpec, ...]], getattr(mod, "UNIT_EXERCISES"))
    selfcheck_unit = cast(str, getattr(mod, "SELFCHECK_UNIT"))
    return exercises, selfcheck_unit


# ---------------------------------------------------------------------------
# Unit / test-file resolution
# ---------------------------------------------------------------------------


def resolve_unit_dir(unit_arg: str) -> Path:
    """Resolve a unit argument (name or path) to the unit directory."""
    candidate = Path(unit_arg)
    if candidate.is_dir():
        return candidate.resolve()
    direct = REPO_ROOT / "units" / unit_arg
    if direct.is_dir():
        return direct.resolve()
    raise FileNotFoundError(f"Unknown unit: {unit_arg!r} (no such directory under units/)")


def discover_test_files(
    unit_dir: Path, registry: dict[str, tuple[ExerciseSpec, ...]]
) -> list[Path]:
    """Return the exercise test files for a unit, registry entries first.

    Registry entries are authoritative (they cover files that do not match
    the ``test_*_exercise.py`` glob, e.g. unit 09's ``test_design.py``);
    any additional ``test_*_exercise.py`` files are appended.
    """
    exercises_dir = unit_dir / "exercises"
    files: list[Path] = []
    seen: set[str] = set()
    for spec in registry.get(unit_dir.name, ()):
        test_file = exercises_dir / spec.test_file
        if test_file.is_file() and spec.test_file not in seen:
            files.append(test_file)
            seen.add(spec.test_file)
    for test_file in sorted(exercises_dir.glob("test_*_exercise.py")):
        if test_file.name not in seen:
            files.append(test_file)
            seen.add(test_file.name)
    return files


def override_flag_for(
    unit_dir: Path, test_file: Path, registry: dict[str, tuple[ExerciseSpec, ...]]
) -> str | None:
    """Return the conftest override flag for a test file, if any.

    Registry lookup first; otherwise parse the unit's conftest for
    ``--override-*`` options — the shared ``--override-student`` flag wins
    when several exist.
    """
    for spec in registry.get(unit_dir.name, ()):
        if spec.test_file == test_file.name:
            return spec.override_flag
    conftest = unit_dir / "exercises" / "conftest.py"
    if not conftest.is_file():
        return None
    flags = sorted(
        {
            line.strip().strip('"')
            for line in conftest.read_text(encoding="utf-8").splitlines()
            if "--override-" in line
        }
    )
    if not flags:
        return None
    if len(flags) == 1:
        return flags[0]
    return "--override-student" if "--override-student" in flags else flags[0]


def solution_file_for(
    unit_dir: Path, test_file: Path, registry: dict[str, tuple[ExerciseSpec, ...]]
) -> Path | None:
    """Return the hidden solution file for a test file, if the registry knows one."""
    for spec in registry.get(unit_dir.name, ()):
        if spec.test_file == test_file.name and spec.solution_file is not None:
            return unit_dir / "exercises" / spec.solution_file
    return None


# ---------------------------------------------------------------------------
# pytest runner + JUnit XML parsing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TestResult:
    """One test case from the JUnit XML."""

    name: str
    classname: str
    passed: bool
    message: str | None


@dataclass(frozen=True)
class SuiteResult:
    """Aggregated results for one pytest run."""

    test_file: Path
    results: list[TestResult]
    total: int
    passed: int
    failed: int

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 0.0
        return 100.0 * self.passed / self.total


def run_pytest(test_file: Path, override_path: Path | None, flag: str | None) -> SuiteResult:
    """Run pytest for one test file with junitxml into a temp file."""
    with tempfile.TemporaryDirectory(prefix="grade_exercise_") as tmp:
        xml_path = Path(tmp) / "junit.xml"
        cmd: list[str] = [
            sys.executable,
            "-m",
            "pytest",
            str(test_file),
            "--junitxml",
            str(xml_path),
            "-p",
            "no:cacheprovider",
            "-q",
        ]
        if override_path is not None and flag is not None:
            cmd.append(f"{flag}={override_path}")
        proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if not xml_path.is_file():
            detail = (proc.stderr or proc.stdout or "").strip().splitlines()
            raise RuntimeError(
                f"pytest produced no JUnit XML for {test_file.name}: "
                + (detail[-1] if detail else "unknown error")
            )
        return parse_junit(xml_path, test_file)


def parse_junit(xml_path: Path, test_file: Path) -> SuiteResult:
    """Parse a JUnit XML file into a SuiteResult."""
    root = ET.parse(xml_path).getroot()
    results: list[TestResult] = []
    total = 0
    failed = 0
    for suite in root.iter("testsuite"):
        total += int(suite.attrib.get("tests", 0))
        failed += int(suite.attrib.get("failures", 0)) + int(suite.attrib.get("errors", 0))
        for case in suite.iter("testcase"):
            name = case.attrib.get("name", "<unnamed>")
            classname = case.attrib.get("classname", "")
            failure = case.find("failure")
            error = case.find("error")
            message: str | None = None
            if failure is not None:
                message = (failure.attrib.get("message") or failure.text or "").strip()
            elif error is not None:
                message = (error.attrib.get("message") or error.text or "").strip()
            results.append(
                TestResult(
                    name=name,
                    classname=classname,
                    passed=failure is None and error is None,
                    message=message,
                )
            )
    passed = total - failed
    return SuiteResult(
        test_file=test_file,
        results=results,
        total=total,
        passed=passed,
        failed=failed,
    )


# ---------------------------------------------------------------------------
# Scorecard output
# ---------------------------------------------------------------------------


def print_scorecard(suite: SuiteResult) -> None:
    """Print the per-test scorecard for one pytest run."""
    print(f"=== {suite.test_file.relative_to(REPO_ROOT)} ===")
    for result in suite.results:
        status = "PASS" if result.passed else "FAIL"
        print(f"  {status}  {result.name}")
        if result.message:
            first_line = result.message.splitlines()[0]
            print(f"       > {first_line}")
    print(
        f"  Total: {suite.total} | Passed: {suite.passed} | Failed: {suite.failed} | Score: {suite.percentage:.1f}%"
    )
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CliArgs:
    """Typed view of the parsed CLI arguments."""

    unit_dir: str | None
    student: str | None
    solution: str | None
    selfcheck: bool


def parse_args(argv: Sequence[str]) -> CliArgs:
    parser = argparse.ArgumentParser(
        prog="grade_exercise.py",
        description="Grade a unit's exercise test suite and print a scorecard.",
    )
    _ = parser.add_argument("unit_dir", nargs="?", help="Unit directory or name, e.g. 08_astrophysics")
    _ = parser.add_argument("--student", metavar="PATH", help="Student file to grade (overrides the default)")
    _ = parser.add_argument("--solution", metavar="PATH", help="Solution file to grade against")
    _ = parser.add_argument(
        "--selfcheck",
        action="store_true",
        help="Run the CLI against one unit's solution file and assert a 100 percent score",
    )
    ns = parser.parse_args(argv)
    return CliArgs(
        unit_dir=cast(str | None, ns.unit_dir),
        student=cast(str | None, ns.student),
        solution=cast(str | None, ns.solution),
        selfcheck=cast(bool, ns.selfcheck),
    )


def run_selfcheck(
    registry: dict[str, tuple[ExerciseSpec, ...]], selfcheck_unit: str
) -> int:
    """Run the CLI via subprocess against the selfcheck unit's solution."""
    unit_dir = resolve_unit_dir(selfcheck_unit)
    test_files = discover_test_files(unit_dir, registry)
    if len(test_files) != 1:
        print(f"SELFCHECK FAIL: {selfcheck_unit} must have exactly one exercise test file")
        return 1
    solution = solution_file_for(unit_dir, test_files[0], registry)
    if solution is None:
        print(f"SELFCHECK FAIL: no solution file registered for {selfcheck_unit}")
        return 1
    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        selfcheck_unit,
        "--solution",
        str(solution),
    ]
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    output = proc.stdout + proc.stderr
    print(output, end="")
    if proc.returncode != 0:
        print(f"SELFCHECK FAIL: CLI exited {proc.returncode} (expected 0)")
        return 1
    if "100.0%" not in output:
        print("SELFCHECK FAIL: scorecard did not print 100.0%")
        return 1
    print(f"SELFCHECK OK: {selfcheck_unit} solution graded at 100%")
    return 0


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    registry, selfcheck_unit = _load_registry()

    if args.selfcheck:
        return run_selfcheck(registry, selfcheck_unit)

    if args.unit_dir is None:
        print("grade_exercise.py: missing unit_dir argument", file=sys.stderr)
        return 2
    if args.student is not None and args.solution is not None:
        print("grade_exercise.py: --student and --solution are mutually exclusive", file=sys.stderr)
        return 2

    override_arg = args.student if args.student is not None else args.solution
    override_path = Path(override_arg) if override_arg is not None else None
    try:
        unit_dir = resolve_unit_dir(args.unit_dir)
    except FileNotFoundError as exc:
        print(f"grade_exercise.py: {exc}", file=sys.stderr)
        return 2

    test_files = discover_test_files(unit_dir, registry)
    if not test_files:
        print(
            f"grade_exercise.py: no exercise test files found under {unit_dir / 'exercises'}",
            file=sys.stderr,
        )
        return 2

    all_passed = True
    for test_file in test_files:
        flag = override_flag_for(unit_dir, test_file, registry)
        try:
            suite = run_pytest(test_file, override_path, flag)
        except RuntimeError as exc:
            print(f"grade_exercise.py: {exc}", file=sys.stderr)
            all_passed = False
            continue
        print_scorecard(suite)
        if suite.failed > 0:
            all_passed = False

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))