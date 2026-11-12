"""Two integral mating bodies with a symbolic, geometrically smooth thread."""
import math

from Otverstiya import through_hole_cutter
from .assembly_geometry import (Connection, GeometryRejected, difference_volume,
                                feature_centers, require_solid)


def _positive(value, name):
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")


def build_threaded(split, rng, settings, *, centers=None, diameter=None, pitch=None,
                   engagement_length=6.):
    """Fuse a boss into A and cut a blind socket into B; no separate hardware."""
    settings.validate()
    diameter = 6. if diameter is None else diameter
    _positive(diameter, "Nominal diameter")
    _positive(engagement_length, "Engagement length")
    if pitch is not None:
        _positive(pitch, "Nominal pitch")
    if engagement_length < settings.min_wall:
        raise GeometryRejected("Engagement length below the local geometric minimum")
    c, wall, depth = settings.clearance, settings.min_wall, engagement_length
    last = "No feasible integral threaded pair"
    for xy in (feature_centers(split, rng, settings.feature_attempts) if centers is None else centers):
        if len(xy) != 2 or not all(math.isfinite(v) for v in xy):
            raise ValueError("Center must contain two finite coordinates")
        try:
            envelope = through_hole_cutter(diameter+2*c+2*wall, -depth-c-wall, 0, xy)
            anchor = through_hole_cutter(diameter+2*wall, 0, wall, xy)
            if envelope.cut(split.lower).Volume() > settings.volume_tolerance:
                raise GeometryRejected("Threaded socket lacks side wall or blind floor material")
            if anchor.cut(split.upper).Volume() > settings.volume_tolerance:
                raise GeometryRejected("Threaded boss lacks anchor material")
            boss = through_hole_cutter(diameter, -depth, 0, xy)
            cavity = through_hole_cutter(diameter+2*c, -depth-c, 0, xy)
            donor = require_solid(split.upper.fuse(boss).clean(), "integral threaded donor")
            receiver = require_solid(split.lower.cut(cavity).clean(), "threaded receiver")
            return Connection([("part_1", donor), ("part_2", receiver)],
                split.lower.intersect(cavity).cut(boss),
                dict(type="threaded", joint_type="threaded", threaded=True,
                     thread_representation="symbolic", thread_geometry=False,
                     nominal_diameter=diameter, nominal_pitch=pitch,
                     hole_diameter=diameter+2*c, clearance=c,
                     clearance_meaning="radial and socket floor",
                     engagement_length=depth, socket_depth=depth+c,
                     minimum_geometric_engagement=wall, integral_protrusion=True,
                     additional_components=[], participating_components=["part_1", "part_2"],
                     center_in_cut_frame=[*xy, 0], axis_in_cut_frame=[0, 0, 1],
                     insertion_direction_in_cut_frame=[0, 0, -1],
                     insertion_method="screw-like/helical", helical_motion_checked=False,
                     geometry_path_kind="smooth_proxy_linear_insertion",
                     local_material_margin=wall, global_minimum_wall_certified=False,
                     thread_retention_modeled=False, self_retaining=False,
                     remaining_unfixed_dof=["axial_withdrawal", "rotation_about_axis"],
                     physical_strength_checked=False),
                [("part_1", ["part_2"], [(0, 0, 1)])])
        except GeometryRejected as error:
            last = str(error)
    raise GeometryRejected(last)


def validate_threaded(split, connection, settings):
    """Check actual two-body geometry, not merely declared coaxiality."""
    parts = dict(connection.components)
    if len(connection.components) != 2 or set(parts) != {"part_1", "part_2"}:
        raise GeometryRejected("Threaded requires exactly two integral bodies and no hardware")
    p = connection.parameters
    expected = build_threaded(split, None, settings,
        centers=[p["center_in_cut_frame"][:2]], diameter=p["nominal_diameter"],
        pitch=p.get("nominal_pitch"), engagement_length=p["engagement_length"])
    if p != expected.parameters or connection.paths != expected.paths:
        raise GeometryRejected("Symbolic threaded dimensions, metadata or insertion path mismatch")
    for name, shape in expected.components:
        require_solid(parts[name], name)
        if difference_volume(parts[name], shape) > settings.volume_tolerance:
            raise GeometryRejected(f"Threaded coaxiality, diameter, depth or placement mismatch: {name}")
    return dict(threaded=True, thread_geometry=False, thread_representation="symbolic",
                threaded_fit_checks=dict(coaxiality_checked=True, integral_boss_checked=True,
                    blind_socket_checked=True, component_count=2, actual_radial_clearance=p["clearance"],
                    geometric_engagement_length=p["engagement_length"], local_material_checked=True),
                helical_motion_checked=False, geometric_path_scope="smooth_proxy_only")
