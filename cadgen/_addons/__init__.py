"""Bundled CadQuery extensions used by CADGen geometry.

Derived from the local cadquery_addons package by Daniel Ignatyev.
Only attach_at and circular_pattern are included; selectors come from CADGen.
"""

from .attach_array import _wp_attach_at
from .circular_pattern import _wp_circular_pattern

__all__ = ["_wp_attach_at", "_wp_circular_pattern"]
