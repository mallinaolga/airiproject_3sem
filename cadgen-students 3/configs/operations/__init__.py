"""Factory presets for individual CAD operations used in tests."""

from .array_pattern import cad_factory as array_pattern_factory
from .chamfer import cad_factory as chamfer_factory
from .extrude import cad_factory as extrude_factory
from .fillet import cad_factory as fillet_factory
from .gear import cad_factory as gear_factory
from .hole import cad_factory as hole_factory
from .loft import cad_factory as loft_factory
from .orto_cut import cad_factory as orto_cut_factory
from .revolve import cad_factory as revolve_factory
from .sweep import cad_factory as sweep_factory

__all__ = [
    "array_pattern_factory",
    "chamfer_factory",
    "extrude_factory",
    "fillet_factory",
    "gear_factory",
    "hole_factory",
    "loft_factory",
    "orto_cut_factory",
    "revolve_factory",
    "sweep_factory",
]
