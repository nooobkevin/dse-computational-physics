"""Engineering domain — orbital mechanics, fluid dynamics, induction, optical fibres, motors, and transformers."""

from physics_core.engineering.optics import OpticalFibre, ReferenceOpticalFibre
from physics_core.engineering.motors import Motor, ReferenceMotor, Transformer, ReferenceTransformer
from physics_core.engineering.orbital import OrbitSim, ReferenceOrbitalBody
from physics_core.engineering.fluid import FluidFlow, ReferenceFluidFlow
from physics_core.engineering.induction import InductionCoil, ReferenceInductionCoil

__all__ = [
    "OpticalFibre",
    "ReferenceOpticalFibre",
    "Motor",
    "ReferenceMotor",
    "Transformer",
    "ReferenceTransformer",
    "OrbitSim",
    "ReferenceOrbitalBody",
    "FluidFlow",
    "ReferenceFluidFlow",
    "InductionCoil",
    "ReferenceInductionCoil",
]