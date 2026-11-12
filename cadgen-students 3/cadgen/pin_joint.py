"""Separate, removable cylindrical pin in two coaxial through holes (mm)."""

import math

from Otverstiya import through_hole_cutter
from .assembly_geometry import (Connection, GeometryRejected, difference_volume,
                                require_solid, feature_centers)


def _geometry(split, settings, diameter, center):
    settings.validate()
    if len(center) != 2 or not all(math.isfinite(v) for v in (*center, diameter)) or diameter <= 0:
        raise ValueError("Pin diameter must be positive; center must contain two finite coordinates")
    hole_diameter = diameter + 2 * settings.clearance
    bounds = []
    for half in (split.upper, split.lower):
        bb = half.BoundingBox()
        if bb.zlen < settings.min_wall:
            raise GeometryRejected("Insufficient pin engagement in a component")
        envelope = through_hole_cutter(hole_diameter + 2 * settings.min_wall,
                                       bb.zmin, bb.zmax, center)
        if envelope.cut(half).Volume() > settings.volume_tolerance:
            raise GeometryRejected("Pin holes lack a full material column and minimum side wall")
        bounds.append((bb.zmin, bb.zmax))
    low, high = bounds[1][0], bounds[0][1]
    if abs(bounds[0][0]) > 1e-6 or abs(bounds[1][1]) > 1e-6:
        raise GeometryRejected("Pin requires adjoining halves at the cut plane")
    cutter = through_hole_cutter(hole_diameter, low - 1, high + 1, center)
    pin = through_hole_cutter(diameter, low, high, center)
    return cutter, pin, bounds


def build_pin(split, rng, settings, *, diameter=4.0, center=None):
    """Use the existing split unchanged, drilling both halves with one tool.

    Conservative full columns reject curved seats, voids and thin side walls.
    A clearance fit does not retain the pin axially or prevent axial rotation.
    """
    settings.validate()
    if not math.isfinite(diameter) or diameter <= 0:
        raise ValueError("Pin diameter must be finite and positive")
    last = "No pin placement"
    for xy in ([center] if center is not None else feature_centers(split, rng, settings.feature_attempts)):
        try:
            tool, pin, bounds = _geometry(split, settings, diameter, xy)
            upper = require_solid(split.upper.cut(tool).clean(), "pin upper")
            lower = require_solid(split.lower.cut(tool).clean(), "pin lower")
            require_solid(pin, "separate pin")
            return Connection(
                [("part_1", upper), ("part_2", lower), ("pin_1", pin)],
                split.original.intersect(tool),
                dict(type="pinned", integral_protrusion=False, diameter=diameter,
                     hole_diameter=diameter + 2 * settings.clearance,
                     clearance=settings.clearance, clearance_meaning="radial",
                     center_in_cut_frame=[*xy, 0], axis_in_cut_frame=[0, 0, 1],
                     pin_length=bounds[0][1] - bounds[1][0],
                     engagement_lengths=[b-a for a,b in bounds],
                     local_material_margin=settings.min_wall,
                     insertion="axial_pin_insertion", insertion_direction_in_cut_frame=[0, 0, -1],
                     additional_components=["pin_1"],
                     hardware_directions_local={"pin_1": [[0, 0, 1]]},
                     constrained_dof=["transverse_translation_after_clearance_take_up"],
                     remaining_unfixed_dof=["axial_translation", "rotation_about_axis"],
                     self_retaining=False, physical_strength_checked=False),
                [("part_1", ["part_2"], [(0, 0, 1)]),
                 ("pin_1", ["part_1", "part_2"], [(0, 0, 1)])])
        except GeometryRejected as error:
            last = str(error)
    raise GeometryRejected(last)


def validate_pin(split, connection, settings):
    """Reconstruct expected geometry, checking actual bores and separate hardware.

    This also detects changed placement, length, radius or extra/missing hardware;
    metadata alone is never accepted as proof of coaxiality.
    """
    p = connection.parameters
    if any(not math.isfinite(p[key]) for key in ("diameter", "hole_diameter", "pin_length", "clearance")):
        raise GeometryRejected("Nonfinite pin dimensions")
    parts = dict(connection.components)
    if len(connection.components) != 3 or set(parts) != {"part_1", "part_2", "pin_1"}:
        raise GeometryRejected("Pin joint requires exactly two bodies and one separate pin")
    if (p.get("axis_in_cut_frame") != [0, 0, 1]
            or p.get("insertion_direction_in_cut_frame") != [0, 0, -1]
            or connection.paths != [("part_1", ["part_2"], [(0, 0, 1)]),
                                    ("pin_1", ["part_1", "part_2"], [(0, 0, 1)])]):
        raise GeometryRejected("Invalid pin axis or insertion sequence")
    tool, pin, bounds = _geometry(split, settings, p["diameter"], p["center_in_cut_frame"][:2])
    if (p["clearance"] != settings.clearance
            or abs(p["hole_diameter"] - p["diameter"] - 2*settings.clearance) > 1e-8
            or abs(p["pin_length"] - (bounds[0][1]-bounds[1][0])) > 1e-8):
        raise GeometryRejected("Inconsistent pin dimensions or clearance")
    expected = {"part_1": split.upper.cut(tool), "part_2": split.lower.cut(tool), "pin_1": pin}
    for name, shape in expected.items():
        if difference_volume(parts[name], shape) > settings.volume_tolerance:
            raise GeometryRejected(f"Pin coaxiality, dimensions or placement mismatch: {name}")
    return dict(coaxial_holes_checked=True, pin_dimensions_checked=True,
                local_side_wall_checked=True, engagement_checked=True,
                physical_strength_checked=False)
