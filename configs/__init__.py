"""Predefined CADGen factory configurations."""

from .datasets.py_configs.eo_r_ap_h_l import cad_factory as DATASET_LOFT_FACTORY
from .datasets.py_configs.eo_r_ap_h_s import cad_factory as DATASET_SWEEP_FACTORY
from .operations import (
    array_pattern_factory,
    chamfer_factory,
    extrude_factory,
    fillet_factory,
    gear_factory,
    hole_factory,
    loft_factory,
    revolve_factory,
    sweep_factory,
)

__all__ = [
    "DATASET_LOFT_FACTORY",
    "DATASET_SWEEP_FACTORY",
    "array_pattern_factory",
    "chamfer_factory",
    "extrude_factory",
    "fillet_factory",
    "gear_factory",
    "hole_factory",
    "loft_factory",
    "revolve_factory",
    "sweep_factory",
]
