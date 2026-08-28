"""Electromagnetism domain — electric fields, circuits, and magnetic fields."""

from physics_core.em.electrostatics import ElectricField, ReferenceElectricField
from physics_core.em.circuits import Circuit, ReferenceCircuit
from physics_core.em.magnetism import MagneticField, ReferenceStraightWire, ReferenceSolenoid

__all__ = [
    "ElectricField",
    "ReferenceElectricField",
    "Circuit",
    "ReferenceCircuit",
    "MagneticField",
    "ReferenceStraightWire",
    "ReferenceSolenoid",
]