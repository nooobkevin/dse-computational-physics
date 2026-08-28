"""physics_core.inquiry — scientific inquiry & data analysis toolkit.

This sub-package provides data-analysis engines that follow the same
abstract-base / Reference-subclass pattern as the simulation engines.
Students fill in the analysis hook (e.g. a model function or a least-squares
formula), while :class:`ReferenceLinearFit` provides the correct
least-squares linear regression implementation.

New in this CAF iteration
-------------------------
- :class:`EpidemicModel` / :class:`ReferenceEpidemicModel` — cellular
  automaton SIR epidemic simulation (CAF complex-systems topic).
"""

from __future__ import annotations

from physics_core.inquiry.analysis import LinearFit, ReferenceLinearFit
from physics_core.inquiry.complex_systems import (
    EpidemicModel,
    ReferenceEpidemicModel,
    basic_reproduction_number,
)

__all__ = [
    "LinearFit",
    "ReferenceLinearFit",
    "EpidemicModel",
    "ReferenceEpidemicModel",
    "basic_reproduction_number",
]
