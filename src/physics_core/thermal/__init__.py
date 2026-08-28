"""Thermal physics / kinetic theory module for the physics toolkit.

Provides:
- GasSim (abstract base) + ReferenceGasSim (correct physics)
- Maxwell-Boltzmann distribution helpers
- RandomWalk engine (seeded deterministic random walk)
"""

from physics_core.thermal.random_walk import RandomWalk

__all__ = ["RandomWalk"]