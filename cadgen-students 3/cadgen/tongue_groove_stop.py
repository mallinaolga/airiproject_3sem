"""Rectangular longitudinal channel with an integral terminal material stop."""
from dataclasses import asdict
import math

from generirovanie_pazov.generate_grooves import Profile, profile_prism
from .assembly_geometry import (Connection, GeometryRejected, build_groove, offset_prism,
                                halfspace, require_solid, difference_volume)
from .assembly_validation import overlap_volume


def _channel(profile, start, end, x, clearance):
    prism = profile_prism(profile, end-start).translate((x, (start+end)/2, 0))
    return offset_prism(prism, clearance, extra_length=False)


def build_tongue_groove_stop(split, rng, settings, *, centers=None):
    """Reuse a rectangular tenon; open its receiver towards -Y only.

    Insertion is +Y. The channel ends exactly at the tenon's leading face.
    Clearance applies to the floor and side walls, not the bearing stop face.
    """
    base = build_groove(split, rng, settings, "rectangular", centers=centers)
    profile = Profile(**base.parameters["profile"])
    x, y, _ = base.parameters["center_in_cut_frame"]
    length = base.parameters["central_engagement_length"]
    end = y+length/2
    entry = split.lower.BoundingBox().ymin
    # A continuous material envelope includes floor, side walls and the stop.
    # The entrance is intentionally open; all other boundaries remain solid.
    envelope = _channel(profile, entry, end+settings.min_wall, x,
                        settings.clearance+settings.min_wall)
    envelope = envelope.intersect(halfspace(split.original, False))
    if envelope.cut(split.lower).Volume() > settings.volume_tolerance:
        raise GeometryRejected("Insufficient floor, side wall or stop thickness along channel")
    cutter = _channel(profile, entry-1, end, x, settings.clearance)
    donor = base.components[0][1]
    receiver = require_solid(split.lower.cut(cutter).clean(), "stopped channel receiver")
    tongue = donor.cut(split.upper)
    parameters = dict(
        type="tongue_groove_stop", joint_type="tongue_groove_stop", profile=asdict(profile),
        center_in_cut_frame=[x, y, 0], central_engagement_length=length,
        clearance=settings.clearance, clearance_meaning="side_and_floor_normal_offset",
        measured_profile_surface_gaps=base.parameters["measured_profile_surface_gaps"],
        entry_y=entry, stop_y=end, stop_thickness=settings.min_wall,
        stop_geometry=dict(kind="integral_terminal_wall", plane_normal=[0, -1, 0],
                           plane_origin=[x, end, 0], bearing_width=profile.opening_width,
                           bearing_depth=profile.depth),
        stop_contact_clearance=0., local_material_margin=settings.min_wall,
        open_ends="negative_y_only", insertion="longitudinal_slide",
        insertion_method="linear_slide_to_stop", insertion_direction_in_cut_frame=[0, 1, 0],
        constrained_dof=["positive_y_translation_at_stop", "transverse_x_after_clearance_take_up"],
        remaining_unfixed_dof=["negative_y_withdrawal", "positive_z_lift"],
        self_retaining=False, physical_strength_checked=False,
        global_minimum_wall_certified=False)
    result = Connection([("part_1", donor), ("part_2", receiver)],
                      split.lower.intersect(cutter).cut(tongue), parameters,
                      [("part_1", ["part_2"], [(0, -1, 0)])])
    result.parameters["stop_checks"] = validate_tongue_groove_stop(split, result, settings)
    return result


def validate_tongue_groove_stop(split, connection, settings):
    settings.validate()
    p = connection.parameters
    if (not all(math.isfinite(v) for v in [p["central_engagement_length"], p["entry_y"],
            p["stop_y"], p["stop_thickness"], *p["center_in_cut_frame"]])
            or p["central_engagement_length"] <= 0
            or p["entry_y"] != split.lower.BoundingBox().ymin):
        raise GeometryRejected("Invalid stopped-channel dimensions")
    if len(connection.components) != 2 or {n for n, _ in connection.components} != {"part_1", "part_2"}:
        raise GeometryRejected("Stopped groove requires exactly two integral components")
    donor, receiver = dict(connection.components)["part_1"], dict(connection.components)["part_2"]
    profile = Profile(**p["profile"])
    profile.validate()
    if profile.kind != "rectangular" or p["joint_type"] != "tongue_groove_stop":
        raise GeometryRejected("Stopped groove must have a rectangular tongue")
    x, y, _ = p["center_in_cut_frame"]
    length = p["central_engagement_length"]
    end = y+length/2
    if (p["clearance"] != settings.clearance or p["stop_y"] != end
            or p["stop_thickness"] != settings.min_wall
            or p["insertion_direction_in_cut_frame"] != [0, 1, 0]
            or connection.paths != [("part_1", ["part_2"], [(0, -1, 0)])]):
        raise GeometryRejected("Invalid stop dimensions, position or insertion direction")
    tongue = profile_prism(profile, length).translate((x, y, 0))
    cutter = _channel(profile, p["entry_y"]-1, end, x, settings.clearance)
    envelope = _channel(profile, p["entry_y"], end+settings.min_wall, x,
                        settings.clearance+settings.min_wall).intersect(halfspace(split.original, False))
    if envelope.cut(split.lower).Volume() > settings.volume_tolerance:
        raise GeometryRejected("Insufficient material around stopped channel")
    # Measure only the tongue's leading face against the opposing stop face.
    contact = 0.
    for a in tongue.Faces():
        if a.geomType() != "PLANE" or a.normalAt().y < .999999: continue
        for b in receiver.Faces():
            if (b.geomType() == "PLANE" and b.normalAt().y < -.999999
                    and abs(b.Center().y-end) < 1e-6):
                contact += a.intersect(b).Area()
    expected_area = profile.opening_width*profile.depth
    if abs(contact-expected_area) > max(1e-6, expected_area*1e-7):
        raise GeometryRejected("Stop missing or misplaced: no complete leading-face contact")
    for actual, expected in ((donor, split.upper.fuse(tongue)), (receiver, split.lower.cut(cutter))):
        if difference_volume(actual, expected) > settings.volume_tolerance:
            raise GeometryRejected("Stopped groove geometry differs from declared channel or tongue")
    probes = [min(.01, settings.min_wall/10), settings.min_wall/2]
    volumes = [overlap_volume(tongue.translate((0, distance, 0)), receiver) for distance in probes]
    if any(v <= settings.volume_tolerance for v in volumes):
        raise GeometryRejected("Stop does not block forward travel")
    return dict(stop_contact_area=contact, stop_position_checked=True,
                local_channel_wall_checked=True, forward_stop_checked=True,
                forward_probe_distances=probes, forward_probe_intersection_volumes=volumes,
                physical_strength_checked=False)
