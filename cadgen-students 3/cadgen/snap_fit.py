"""Integral cantilever latch with sampled, prescribed bending geometry (mm)."""
from dataclasses import asdict, dataclass
import math

import cadquery as cq
import numpy as np

from .assembly_geometry import Connection, GeometryRejected, difference_volume, require_solid
from .assembly_validation import overlap_volume, transform_part


def _bend(u):
    return u*u*(3-u)/2


@dataclass(frozen=True)
class SnapFitSpec:
    length: float = 12.
    thickness: float = 1.
    width: float = 4.
    hook_height: float = 1.2
    ramp_angle_degrees: float = 30.
    max_deflection: float = 2.
    relief_depth: float = 2.2

    @property
    def ramp_length(self):
        return self.hook_height/math.tan(math.radians(self.ramp_angle_degrees))

    def required_deflection(self, clearance):
        return (self.hook_height-clearance)/_bend((self.length-self.ramp_length)/self.length)

    def validate(self, settings):
        settings.validate()
        if any(not math.isfinite(v) or v <= 0 for v in asdict(self).values()):
            raise ValueError("Snap-fit dimensions must be positive and finite")
        if not 5 <= self.ramp_angle_degrees <= 75:
            raise GeometryRejected("Snap-fit ramp angle outside geometric design limits")
        if self.length/self.thickness < 6:
            raise GeometryRejected("Tongue too short or too thick for the prescribed slender-beam model")
        if self.length-self.ramp_length-settings.clearance < settings.min_wall:
            raise GeometryRejected("Insufficient retaining shoulder roof thickness")
        if self.hook_height <= settings.clearance:
            raise GeometryRejected("No positive hook engagement behind the shoulder")
        delta = self.required_deflection(settings.clearance)
        if delta > self.max_deflection or delta/self.length > .2:
            raise GeometryRejected("Required deflection exceeds geometric design limits")
        if delta > self.relief_depth:
            raise GeometryRejected("Insufficient free relief space for tongue deflection")


def tongue_shape(spec, deflection=0.):
    """Piecewise planar approximation to x=-delta*u²*(3-u)/2, clamped at z=0.

    This is an assumed displacement field, not a material/force simulation.
    Cross sections retain their width and thickness; the hook moves with them.
    """
    shoulder = spec.length-spec.ramp_length
    nodes = sorted(set(np.linspace(0, spec.length, 17).tolist()+[shoulder]))
    shift = lambda s: deflection*_bend(s/spec.length)
    points = [(-spec.thickness/2-shift(s), -s) for s in nodes]
    for s in reversed(nodes):
        hook = spec.hook_height*(spec.length-s)/spec.ramp_length if s >= shoulder else 0.
        points.append((spec.thickness/2+hook-shift(s), -s))
        if s == shoulder:
            points.append((spec.thickness/2-shift(s), -s))
    return require_solid(cq.Workplane("XZ").polyline(points).close()
                         .extrude(spec.width/2, both=True).val().clean(), "deformed tongue")


def _box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1-x0, y1-y0, z1-z0, cq.Vector(x0, y0, z0))


def build_snap_fit(split, settings, spec=None):
    spec = spec or SnapFitSpec()
    spec.validate(settings)
    c, wall = settings.clearance, settings.min_wall
    left = -spec.thickness/2-spec.relief_depth-c
    right = spec.thickness/2+c
    half_width = spec.width/2+c
    floor = -spec.length-c
    roof = -spec.length+spec.ramp_length+c
    envelope = _box(left-wall, right+spec.hook_height+wall,
                    -half_width-wall, half_width+wall, floor-wall, 0)
    anchor = _box(-spec.thickness/2-wall, spec.thickness/2+wall,
                  -half_width-wall, half_width+wall, 0, wall)
    if envelope.cut(split.lower).Volume() > settings.volume_tolerance:
        raise GeometryRejected("Snap-fit receiver lacks wall or floor material")
    if anchor.cut(split.upper).Volume() > settings.volume_tolerance:
        raise GeometryRejected("Snap-fit tongue lacks anchor material")
    slot = _box(left, right, -half_width, half_width, floor, 0)
    # Open the pocket towards +X so the hook is accessible for manual release.
    pocket = _box(left, split.lower.BoundingBox().xmax+1,
                  -half_width, half_width, floor, roof)
    cavity = slot.fuse(pocket).clean()
    tongue = tongue_shape(spec)
    donor = require_solid(split.upper.fuse(tongue).clean(), "snap-fit donor")
    receiver = require_solid(split.lower.cut(cavity).clean(), "snap-fit receiver")
    parameters = dict(type="snap_fit", joint_type="snap_fit", spec=asdict(spec),
        clearance=c, required_deflection=spec.required_deflection(c),
        engagement_depth=spec.hook_height-c, shoulder_z=roof,
        integral_protrusion=True, additional_components=[],
        participating_components=["part_1", "part_2"],
        insertion_direction_in_cut_frame=[0, 0, -1], deformation_direction_in_cut_frame=[-1, 0, 0],
        insertion_method="approach_cam_deflection_pass_shoulder_recover_seat",
        deformation_model="piecewise_linear_samples_of_cubic_cantilever_displacement",
        uniform_deformation_samples=17, additional_hook_shoulder_section=True,
        final_pose=dict(translation=[0, 0, 0], deflection=0.),
        release_method="press_hook_through_positive_x_service_opening_then_withdraw",
        release_actuator_checked=False, material=None, physical_elasticity_checked=False,
        physical_strength_checked=False, continuous_path_proven=False,
        constrained_dof=["straight_axial_withdrawal_without_deflection"],
        remaining_unfixed_dof=["withdrawal_after_controlled_deflection"],
        local_material_margin=wall, global_minimum_wall_certified=False)
    return Connection([("part_1", donor), ("part_2", receiver)],
                      split.lower.intersect(cavity).cut(tongue), parameters, [])


def motion_samples(spec, settings):
    """Cam-driven bending, sliding under the shoulder, recovery and seating."""
    c = settings.clearance
    full = spec.required_deflection(c)
    shoulder = spec.length-spec.ramp_length
    count = settings.path_steps+1
    poses = []
    def append(stage, offset, delta):
        poses.append(dict(stage=stage, axial_translation=float(offset), deflection=float(delta)))
    for d in np.linspace(spec.length+2*settings.min_wall, spec.length, count):
        append("approach", d, 0.)
    for d in np.linspace(spec.length, shoulder, count):
        hook = spec.hook_height*(spec.length-d)/spec.ramp_length
        delta = max(0., hook-c)/_bend(d/spec.length)
        append("cam_deflection", d, delta)
    for d in np.linspace(shoulder, c, count):
        append("pass_shoulder", d, full)
    for delta in np.linspace(full, 0., count):
        append("recover", c, delta)
    for d in np.linspace(c, 0., count):
        append("seat", d, 0.)
    return poses


def check_snap_motion(donor, receiver, parameters, settings):
    spec = SnapFitSpec(**parameters["spec"])
    spec.validate(settings)
    relaxed = tongue_shape(spec)
    body = require_solid(donor.cut(relaxed).clean(), "snap-fit rigid base")
    shapes = {}
    poses = motion_samples(spec, settings)
    for pose in poses:
        delta = pose["deflection"]
        key = round(delta, 12)
        if key not in shapes:
            shapes[key] = require_solid(body.fuse(tongue_shape(spec, delta)).clean(), "bent donor")
        moving = shapes[key].translate((0, 0, pose["axial_translation"]))
        volume = overlap_volume(moving, receiver)
        pose["intersection_volume"] = volume
        if volume > settings.volume_tolerance:
            raise GeometryRejected(f"Snap-fit {pose['stage']} collision at {pose}")
    start = donor.translate((0, 0, poses[0]["axial_translation"]))
    if start.distance(receiver) <= 1e-6:
        raise GeometryRejected("Snap-fit approach start is not separated")
    lift = settings.clearance+spec.ramp_length/4
    retained = overlap_volume(donor.translate((0, 0, lift)), receiver)
    if retained <= settings.volume_tolerance:
        raise GeometryRejected("Snap-fit has no geometric axial engagement")
    # Reverse the actual verified states: unload, press in the pocket, withdraw.
    return dict(status="sampled_deformation_clear", poses=poses,
                maximum_sampled_deflection=max(p["deflection"] for p in poses),
                straight_withdrawal_blocked=True, retention_probe=lift,
                retention_intersection_volume=retained,
                release=dict(status="sampled_clear", poses=list(reversed(poses)),
                             requires_external_actuation=True, actuator_access_checked=False),
                continuous_path_proven=False, physical_elasticity_checked=False,
                physical_strength_checked=False)


def validate_snap_fit(split, connection, settings):
    parts = dict(connection.components)
    if len(connection.components) != 2 or set(parts) != {"part_1", "part_2"}:
        raise GeometryRejected("Snap-fit requires exactly two integral bodies")
    if connection.paths:
        raise GeometryRejected("Snap-fit cannot use rigid linear-only installation")
    expected = build_snap_fit(split, settings, SnapFitSpec(**connection.parameters["spec"]))
    if expected.parameters != connection.parameters:
        raise GeometryRejected("Snap-fit geometry/kinematics metadata mismatch")
    for name, shape in expected.components:
        if difference_volume(parts[name], shape) > settings.volume_tolerance:
            raise GeometryRejected(f"Snap-fit tongue, shoulder or final position mismatch: {name}")
    return check_snap_motion(parts["part_1"], parts["part_2"], connection.parameters, settings)


def pair_sequence(parts, raw, joints, settings):
    if len(joints) != 1 or len(raw) != 2 or len(parts) != 2:
        raise GeometryRejected("Unverified snap-fit sequence: only an isolated two-body pair is supported")
    joint = joints[0]
    p = joint.parameters
    rotation, origin = np.asarray(p["cut_to_world_rotation"]), np.asarray(p["cut_origin"])
    local = lambda s: transform_part(s, rotation.T, -rotation.T@origin)
    moving, fixed = joint.owners
    checks = check_snap_motion(local(parts[moving]), local(parts[fixed]), p, settings)
    sequence = [dict(step=0, component=fixed, action="place_base", stationary_components=[]),
        dict(step=1, component=moving, action="prescribed_cantilever_deflection",
             stationary_components=[fixed], coordinate_frame="source_world",
             insertion_direction=(-rotation[:, 2]).tolist(),
             deformation_direction=(-rotation[:, 0]).tolist(),
             cut_to_world_rotation=rotation.tolist(), cut_origin=origin.tolist(),
             poses_in_cut_frame=checks["poses"], physical_elasticity_checked=False,
             continuous_path_proven=False)]
    return sequence, dict(method="snap_fit_pair_sampled_deformation", motion_checks=checks,
                         continuous_path_proven=False, physical_elasticity_checked=False,
                         technical_limit_reached=False)
