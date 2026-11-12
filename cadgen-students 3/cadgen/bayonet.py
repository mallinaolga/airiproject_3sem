"""Two-lug bayonet: axial entry, cylindrical arc channels, then rotation."""
from dataclasses import asdict, dataclass
import math
import cadquery as cq
import numpy as np

from .assembly_geometry import Connection, GeometryRejected, require_solid, difference_volume
from .assembly_validation import overlap_volume, transform_part


@dataclass(frozen=True)
class BayonetSpec:
    radius: float = 6.
    depth: float = 10.
    lug_projection: float = 2.
    lug_height: float = 2.
    lug_angle: float = 20.
    turn_angle: float = 60.

    def validate(self, settings):
        settings.validate()
        if any(not math.isfinite(v) or v <= 0 for v in asdict(self).values()):
            raise ValueError("Bayonet dimensions must be positive and finite")
        if self.radius <= 1 or self.depth <= self.lug_height+settings.clearance+settings.min_wall+1:
            raise GeometryRejected("Insufficient bayonet depth or roof material")
        angular_gap = math.degrees(math.asin(settings.clearance/(self.radius+self.lug_projection)))
        if not self.lug_angle+2*angular_gap < self.turn_angle < 180-self.lug_angle-2*angular_gap:
            raise GeometryRejected("Bayonet turn must separate the entry and locked lug positions")


def _sector(radius, height, z, start, angle):
    return cq.Solid.makeCylinder(radius, height, cq.Vector(0, 0, z),
                                 cq.Vector(0, 0, 1), angle).rotate((0, 0, 0), (0, 0, 1), start)


def _tools(spec, settings):
    spec.validate(settings)
    r, depth, c = spec.radius, spec.depth, settings.clearance
    outer = r+spec.lug_projection
    z = -depth+1
    delta = math.degrees(math.asin(c/outer))
    boss = cq.Solid.makeCylinder(r, depth, cq.Vector(0, 0, -depth))
    cavity = cq.Solid.makeCylinder(r+c, depth+c, cq.Vector(0, 0, -depth-c))
    lugs = []
    for azimuth in (0., 180.):
        start = azimuth-spec.lug_angle/2
        lug = _sector(outer, spec.lug_height, z, start, spec.lug_angle).cut(
            cq.Solid.makeCylinder(r-.5, spec.lug_height, cq.Vector(0, 0, z)))
        lugs.append(lug)
        entry = _sector(outer+c, -z+c, z-c, start-delta, spec.lug_angle+2*delta)
        turn = _sector(outer+c, spec.lug_height+2*c, z-c, start-delta,
                       spec.turn_angle+spec.lug_angle+2*delta)
        cavity = cavity.fuse(entry, turn)
    entry_feature = boss.fuse(*lugs).clean()
    locked_feature = entry_feature.rotate((0, 0, 0), (0, 0, 1), spec.turn_angle)
    return locked_feature, cavity.clean(), z, delta


def build_bayonet(split, settings, spec=None):
    spec = spec or BayonetSpec()
    feature, cavity, z, delta = _tools(spec, settings)
    # Conservative complete envelopes certify the floor, side wall and anchor.
    envelope = cq.Solid.makeCylinder(spec.radius+spec.lug_projection+settings.clearance+settings.min_wall,
        spec.depth+settings.clearance+settings.min_wall,
        cq.Vector(0, 0, -spec.depth-settings.clearance-settings.min_wall))
    anchor = cq.Solid.makeCylinder(spec.radius+settings.min_wall, settings.min_wall)
    if envelope.cut(split.lower).Volume() > settings.volume_tolerance:
        raise GeometryRejected("Bayonet socket lacks side wall or floor material")
    if anchor.cut(split.upper).Volume() > settings.volume_tolerance:
        raise GeometryRejected("Bayonet boss lacks anchor material")
    donor = require_solid(split.upper.fuse(feature).clean(), "bayonet donor")
    receiver = require_solid(split.lower.cut(cavity).clean(), "bayonet receiver")
    parameters = dict(type="bayonet", joint_type="bayonet", spec=asdict(spec),
        clearance=settings.clearance, clearance_meaning="radial and axial; flank clearance at most c",
        angular_clearance_degrees=delta, insertion_method="axial_then_rotation",
        insertion_direction_in_cut_frame=[0, 0, -1], axis_in_cut_frame=[0, 0, 1],
        rotation_origin_in_cut_frame=[0, 0, 0], turn_angle_degrees=spec.turn_angle,
        insertion_depth=spec.depth, lug_count=2,
        lugs=[dict(entry_angle_degrees=a, locked_angle_degrees=a+spec.turn_angle,
                   z_min=z, height=spec.lug_height, outer_radius=spec.radius+spec.lug_projection)
              for a in (0., 180.)],
        final_pose=dict(rotation_degrees_from_entry=spec.turn_angle, axial_translation=0.),
        local_material_margin=settings.min_wall, global_minimum_wall_certified=False,
        self_locking=False, reverse_rotation_allowed=True, physical_strength_checked=False,
        constrained_dof=["straight_axial_withdrawal_at_locked_angle"],
        remaining_unfixed_dof=["reverse_rotation_then_axial_withdrawal"],
        insertion="axial_then_rotation")
    return Connection([("part_1", donor), ("part_2", receiver)],
                      split.lower.intersect(cavity).cut(feature), parameters, [])


def check_bayonet_motion(donor, receiver, parameters, settings):
    spec = BayonetSpec(**parameters["spec"])
    spec.validate(settings)
    turn = spec.turn_angle
    travel = spec.depth+2*settings.min_wall
    entry = donor.rotate((0, 0, 0), (0, 0, 1), -turn)
    if entry.translate((0, 0, travel)).distance(receiver) <= 1e-6:
        raise GeometryRejected("Bayonet insertion start is not separated")
    translations = np.linspace(travel, 0, settings.path_steps+1).tolist()
    angles = np.linspace(0, turn, settings.path_steps+1).tolist()
    axial_volumes = [overlap_volume(entry.translate((0, 0, d)), receiver) for d in translations]
    turn_volumes = [overlap_volume(entry.rotate((0, 0, 0), (0, 0, 1), a), receiver) for a in angles]
    if any(v > settings.volume_tolerance for v in axial_volumes):
        raise GeometryRejected("Bayonet axial insertion collides")
    if any(v > settings.volume_tolerance for v in turn_volumes):
        raise GeometryRejected("Bayonet rotation or final position collides")
    lift = settings.clearance+spec.lug_height/2
    retained = overlap_volume(donor.translate((0, 0, lift)), receiver)
    if retained <= settings.volume_tolerance:
        raise GeometryRejected("Bayonet locked position does not block axial withdrawal")
    return dict(status="sampled_clear", continuous_path_proven=False,
        axial_stage=dict(translations=translations, rotation_degrees_from_final=-turn,
                         intersection_volumes=axial_volumes),
        rotation_stage=dict(angles_degrees_from_entry=angles, intersection_volumes=turn_volumes),
        locked_axial_withdrawal_blocked=True, axial_lock_probe=lift,
        axial_lock_intersection_volume=retained,
        reverse_rotation_and_withdrawal="same checked poses in reverse; sampled_clear")


def validate_bayonet(split, connection, settings):
    p = connection.parameters
    if connection.paths:
        raise GeometryRejected("Bayonet must not be represented as a linear-only path")
    expected = build_bayonet(split, settings, BayonetSpec(**p["spec"]))
    if p != expected.parameters:
        raise GeometryRejected("Bayonet kinematic metadata does not match its dimensions")
    parts = dict(connection.components)
    if len(connection.components) != 2 or set(parts) != {"part_1", "part_2"}:
        raise GeometryRejected("Bayonet requires two integral components")
    for name, shape in expected.components:
        if difference_volume(parts[name], shape) > settings.volume_tolerance:
            raise GeometryRejected(f"Bayonet coaxiality, lug/channel or position mismatch: {name}")
    return check_bayonet_motion(parts["part_1"], parts["part_2"], p, settings)


def pair_sequence(parts, raw, joints, settings):
    """Explicit two-body motion adapter, not a general rotational planner."""
    if len(joints) != 1 or len(raw) != 2 or len(parts) != 2:
        raise GeometryRejected("Unverified bayonet sequence: only an isolated two-body pair is supported")
    joint = joints[0]
    p = joint.parameters
    rotation = np.asarray(p["cut_to_world_rotation"])
    origin = np.asarray(p["cut_origin"])
    moving, fixed = joint.owners
    local = lambda s: transform_part(s, rotation.T, -rotation.T@origin)
    checks = check_bayonet_motion(local(parts[moving]), local(parts[fixed]), p, settings)
    sequence = [dict(step=0, component=fixed, action="place_base", stationary_components=[], coordinate_frame="source_world"),
        dict(step=1, component=moving, action="axial_then_rotation", stationary_components=[fixed],
             coordinate_frame="source_world", axis=(rotation@np.array([0., 0., 1.])).tolist(),
             rotation_origin=origin.tolist(), insertion_direction=(-rotation[:, 2]).tolist(),
             stages=[checks["axial_stage"], checks["rotation_stage"]], continuous_path_proven=False)]
    return sequence, dict(method="bayonet_pair_sampled_motion", motion_checks=checks,
                         continuous_path_proven=False, technical_limit_reached=False)
