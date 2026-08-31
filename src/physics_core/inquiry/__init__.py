"""physics_core.inquiry — scientific inquiry & data analysis toolkit.

This sub-package provides data-analysis engines that follow the same
abstract-base / Reference-subclass pattern as the simulation engines.
Students fill in the analysis hook (e.g. a model function or a least-squares
formula), while :class:`ReferenceLinearFit` provides the correct
least-squares linear regression implementation.

Complex systems
---------------
- :class:`EpidemicModel` / :class:`ReferenceEpidemicModel` — deterministic
  cellular-automaton SIR epidemic simulation (CAF complex-systems topic).
- :class:`ForestFireModel` / :class:`ReferenceForestFire` — deterministic
  forest-fire cellular automaton with wind-biased spread.
- :class:`CrowdModel` / :class:`ReferenceCrowdModel` — deterministic
  agent-based crowd evacuation with panic-dependent congestion.
"""

from __future__ import annotations

from physics_core.inquiry.analysis import LinearFit, ReferenceLinearFit
from physics_core.inquiry.complex_systems import (
    CrowdModel,
    EpidemicModel,
    ForestFireModel,
    ReferenceCrowdModel,
    ReferenceEpidemicModel,
    ReferenceForestFire,
    basic_reproduction_number,
)

__all__ = [
    "LinearFit",
    "ReferenceLinearFit",
    "EpidemicModel",
    "ReferenceEpidemicModel",
    "ForestFireModel",
    "ReferenceForestFire",
    "CrowdModel",
    "ReferenceCrowdModel",
    "basic_reproduction_number",
]
