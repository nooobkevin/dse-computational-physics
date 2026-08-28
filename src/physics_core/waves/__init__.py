"""Wave motion simulation engine for the HKDSE Physics toolkit.

Provides an abstract base :class:`WaveSim` with physics hooks that raise
``NotImplementedError``, and a :class:`ReferenceWaveSim` that supplies the
correct analytical wave physics.

The engine models traveling and standing waves on a discrete spatial grid.
"""
