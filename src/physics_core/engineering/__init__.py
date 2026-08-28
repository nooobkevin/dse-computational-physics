"""Engineering domain — optical fibres, lasers, motors, and transformers."""

from physics_core.engineering.optics import OpticalFibre, ReferenceOpticalFibre
from physics_core.engineering.lasers import Laser, ReferenceLaser
from physics_core.engineering.motors import Motor, ReferenceMotor, Transformer, ReferenceTransformer

__all__ = [
    "OpticalFibre",
    "ReferenceOpticalFibre",
    "Laser",
    "ReferenceLaser",
    "Motor",
    "ReferenceMotor",
    "Transformer",
    "ReferenceTransformer",
]