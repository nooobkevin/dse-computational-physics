"""Astrophysics and Relativity domain — Doppler shift, Hubble's law, stellar classification,
special relativity, and H-R diagram physics."""

from physics_core.astrophysics.doppler import DopplerShift, ReferenceDopplerShift
from physics_core.astrophysics.hr_diagram import HRDiagram, ReferenceHRDiagram, SAMPLE_STARS
from physics_core.astrophysics.hubble import HubbleLaw, SPECTRAL_CLASSES
from physics_core.astrophysics.relativity import RelativityEngine, ReferenceRelativityEngine

__all__ = [
    "DopplerShift",
    "ReferenceDopplerShift",
    "HubbleLaw",
    "SPECTRAL_CLASSES",
    "RelativityEngine",
    "ReferenceRelativityEngine",
    "HRDiagram",
    "ReferenceHRDiagram",
    "SAMPLE_STARS",
]