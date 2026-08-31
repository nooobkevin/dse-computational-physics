"""Electromagnetism domain — electric fields, circuits, and magnetic fields."""

from physics_core.em.motor import (
    CoilTorque,
    DCMotor,
    ReferenceCoilTorque,
    ReferenceDCMotor,
    ReferenceDCMotorConstant,
    ReferenceWireForce,
    WireForce,
)
from physics_core.em.electrostatics import ElectricField, ReferenceElectricField
from physics_core.em.circuits import Circuit, ReferenceCircuit
from physics_core.em.magnetism import (
    MagneticField,
    MovingCharge,
    ReferenceBarMagnet,
    ReferenceMovingCharge,
    ReferenceSolenoid,
    ReferenceStraightWire,
)

__all__ = [
    "ElectricField",
    "ReferenceElectricField",
    "Circuit",
    "ReferenceCircuit",
    "MagneticField",
    "MovingCharge",
    "ReferenceBarMagnet",
    "ReferenceMovingCharge",
    "ReferenceSolenoid",
    "ReferenceStraightWire",
    "WireForce",
    "ReferenceWireForce",
    "CoilTorque",
    "ReferenceCoilTorque",
    "DCMotor",
    "ReferenceDCMotor",
    "ReferenceDCMotorConstant",
]