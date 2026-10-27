"""Split one immutable source, transfer a shared profile, or drill a bolt axis.

All feature work is in an orthonormal cut frame. Booleans modify the *new*
components, never the source. Existing CADGen profiles and fasteners are reused.
"""

from dataclasses import asdict, dataclass
from itertools import combinations
import math

import cadquery as cq
import numpy as np

from Bolty import BoltSpec, build_bolt
from Gaiki import NutSpec, build_nut
from Otverstiya import through_hole_cutter
from generirovanie_pazov.generate_grooves import profile_prism, sample_profile

from .assembly_validation import overlap_volume, planar_contact_area, transform_part


class GeometryRejected(ValueError):
    """A bounded candidate failed; callers may try another plane/source."""


@dataclass(frozen=True)
class AssemblySettings:
    clearance: float = 0.2  # normal offset of a groove / radial clearance of a hole
    min_wall: float = 2.0
    volume_tolerance: float = 1e-5
    min_part_fraction: float = 0.15
    plane_attempts: int = 9
    feature_attempts: int = 8
    path_steps: int = 16

    def validate(self):
        if not math.isfinite(self.clearance) or not 0 <= self.clearance < 1:
            raise ValueError("clearance must be finite and 0 <= clearance < 1 mm")
        if any(not math.isfinite(x) or x <= 0 for x in (self.min_wall, self.volume_tolerance)):
            raise ValueError("min_wall and volume_tolerance must be positive and finite")
        if not math.isfinite(self.min_part_fraction) or not 0 < self.min_part_fraction < 0.5:
            raise ValueError("min_part_fraction must be between 0 and 0.5")
        if self.plane_attempts < 1 or self.feature_attempts < 1 or self.path_steps < 2:
            raise ValueError("plane/feature attempts >= 1, path_steps >= 2")


def require_solid(shape, label):
    if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 1e-8:
        raise GeometryRejected(f"{label}: expected one valid positive-volume solid")
    return shape.Solids()[0]


def difference_volume(first, second):
    # Empty Boolean results are valid zero-volume sets. OCC cannot subtract
    # an empty compound as an argument on every supported kernel version.
    if not first.Solids():
        return second.Volume() if second.Solids() else 0.0
    if not second.Solids():
        return first.Volume()
    return max(0.0, first.cut(second).Volume()) + max(0.0, second.cut(first).Volume())


def frame(normal):
    normal = np.asarray(normal, dtype=float)
    if normal.shape != (3,) or not np.isfinite(normal).all() or np.linalg.norm(normal) < 1e-10:
        raise GeometryRejected("Invalid split normal")
    z = normal / np.linalg.norm(normal)
    reference = np.eye(3)[np.argmin(np.abs(z))]
    x = np.cross(reference, z)
    x /= np.linalg.norm(x)
    return np.column_stack((x, np.cross(z, x), z))


@dataclass
class Split:
    original: cq.Shape  # cut coordinates; Z=0 is the interface
    lower: cq.Shape
    upper: cq.Shape
    rotation: np.ndarray  # cut coordinates -> source/world coordinates
    origin: np.ndarray
    checks: dict

    def world(self, shape):
        return transform_part(shape, self.rotation, self.origin)

    def metadata(self):
        return dict(origin=self.origin.tolist(), normal=self.rotation[:, 2].tolist(),
                    cut_to_world_rotation=self.rotation.tolist(), checks=self.checks)


def contact_patch(first, second, tolerance=1e-6):
    """Exact trimmed planar interface. Solid common may discard zero-volume faces."""
    patches=[]
    for a in first.Faces():
        if a.geomType() != "PLANE":continue
        n=a.normalAt()
        for b in second.Faces():
            if b.geomType() != "PLANE" or n.dot(b.normalAt()) > -0.999999:continue
            offset=(b.Center()-a.Center()).dot(n)
            if abs(offset)>tolerance:continue
            common=a.intersect(b.translate(tuple(-offset*n)))
            if common.Area()>1e-7:patches.extend(common.Faces())
    return cq.Compound.makeCompound(patches)


def halfspace(shape, upper, padding=1.0):
    bb = shape.BoundingBox()
    size = bb.DiagonalLength + max(abs(v) for v in (
        bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)) + padding
    return cq.Solid.makeBox(2*size, 2*size, size,
                            cq.Vector(-size, -size, 0 if upper else -size))


def split_model(original, origin, normal, settings):
    require_solid(original, "source")
    rotation = frame(normal)
    origin = np.asarray(origin, dtype=float)
    local = transform_part(original, rotation.T, -rotation.T@origin)
    lower = require_solid(local.intersect(halfspace(local, False)).clean(), "lower half")
    upper = require_solid(local.intersect(halfspace(local, True)).clean(), "upper half")
    fraction = min(lower.Volume(), upper.Volume()) / local.Volume()
    if fraction < settings.min_part_fraction:
        raise GeometryRejected("Split makes an insufficient-volume component")
    if min(-lower.BoundingBox().zmin, upper.BoundingBox().zmax) < 2*settings.min_wall:
        raise GeometryRejected("Insufficient material depth on one side of the split")
    overlap = overlap_volume(lower, upper)
    error = difference_volume(local, lower.fuse(upper))
    if overlap > settings.volume_tolerance or error > settings.volume_tolerance:
        raise GeometryRejected("Split does not reconstruct the source within CAD tolerance")
    return Split(local, lower, upper, rotation, origin,
                 dict(minimum_volume_fraction=fraction, reconstruction_error_volume=error,
                      intersection_volume=overlap, valid_single_solid_halves=True))


def candidate_planes(shape, rng, settings, connection):
    """Face normals and world axes, then oblique cuts; randomized offsets/order.

    Actual planar normals let rotated models retain flat bearing seats for
    bolts. Bounding-box axes alone cannot do that.
    """
    center = np.array(shape.Center().toTuple())
    axes = []
    normals = [np.array(f.normalAt().toTuple()) for f in sorted(
        shape.Faces(), key=lambda f: f.Area(), reverse=True) if f.geomType() == "PLANE"]
    for normal in normals + list(np.eye(3)):
        if not any(abs(np.dot(normal, other)) > 0.999999 for other in axes):
            axes.append(normal)
    rng.shuffle(axes)
    for i in range(settings.plane_attempts):
        normal = (axes[i % len(axes)] if i < len(axes) or connection == "bolted" else
                  np.array([rng.uniform(-1, 1) for _ in range(3)]))
        normal = normal / np.linalg.norm(normal)
        projections = [np.dot(np.array(v.Center().toTuple())-center, normal) for v in shape.Vertices()]
        # Smooth solids can have very few topological vertices: use bbox as
        # a conservative projection scale, not as a compatibility certificate.
        extent = max(max(projections, default=0)-min(projections, default=0),
                     shape.BoundingBox().DiagonalLength*0.2)
        origin = center + normal * rng.uniform(-0.12, 0.12) * extent
        yield origin, normal


def feature_centers(split, rng, attempts):
    bb = split.original.BoundingBox()
    # Center of mass may be in a void. Every candidate is checked by B-rep
    # containment, including the deterministic first proposal.
    yield (0.0, 0.0)
    for _ in range(attempts-1):
        yield (rng.uniform(bb.xmin*0.65, bb.xmax*0.65),
               rng.uniform(bb.ymin*0.65, bb.ymax*0.65))


def offset_prism(prism, clearance, extra_length=True):
    """True planar normal offset of the existing profile, including round arcs.

    No new definition of the six profiles is introduced here. Optional axial
    extension gives the same clearance at a closed pocket's end faces.
    """
    if clearance == 0:
        return prism
    ends = [f for f in prism.Faces() if abs(f.normalAt().y) > 0.999999]
    start = min(ends, key=lambda f: f.Center().y)
    wires = start.outerWire().offset2D(clearance, kind="arc")
    if len(wires) != 1:
        raise GeometryRejected("Profile offset did not produce one boundary")
    extra = clearance if extra_length else 0.0
    length = prism.BoundingBox().ylen
    return cq.Solid.extrudeLinear(wires[0], [], cq.Vector(0, length+2*extra, 0)).translate((0, -extra, 0))


def profile_gaps(prism, cavity, clearance):
    """Measure the constructed profile's actual side surfaces, not just parameters."""
    boundary = cq.Compound.makeCompound(cavity.Faces())
    measured = []
    for face in prism.Faces():
        u0, u1, v0, v1 = face._uvBounds()
        normal, point = face.normalAt((u0+u1)/2, (v0+v1)/2)
        if abs(normal.y) > 0.999999 or normal.z > 0.999999:
            continue  # end caps and the opening shared with the donor
        expected = point + normal*clearance
        if boundary.distance(cq.Vertex.makeVertex(*expected.toTuple())) > 1e-6:
            raise GeometryRejected("Profile's actual normal-offset surface does not match clearance")
        gap = boundary.distance(cq.Vertex.makeVertex(*point.toTuple()))
        if abs(gap-clearance) > 1e-6:
            raise GeometryRejected("Profile surface gap differs from the requested clearance")
        measured.append(float(gap))
    if not measured:
        raise GeometryRejected("No profile surfaces available for clearance verification")
    return measured


@dataclass
class Connection:
    components: list  # (name, shape in the cut frame)
    removed: cq.Shape  # expected technological void, measured inside source
    parameters: dict
    paths: list  # (moving name, stationary names, withdrawal directions)


def build_groove(split, rng, settings, profile="rectangular", *, centers=None, footprint=None):
    bb = split.original.BoundingBox()
    last_reason = "No supported feature placement"
    for x, y in (feature_centers(split, rng, settings.feature_attempts) if centers is None else centers):
        try:
            sampled = sample_profile(rng, profile)
            depth = -split.lower.BoundingBox().zmin * rng.uniform(0.20, 0.35)
            width = bb.xlen * rng.uniform(0.18, 0.3)
            if footprint:
                width = min(width, footprint["width"])
                depth = min(depth, footprint["depth"])
            scale = min(width/sampled.max_width, depth/sampled.depth)
            values = asdict(sampled)
            for key in values:
                if key != "kind" and values[key] is not None:
                    values[key] *= scale
            selected = type(sampled)(**values)
            sliding = selected.kind in ("dovetail", "t")
            core_length = bb.ylen*rng.uniform(0.22, 0.38)
            if footprint:
                core_length = min(core_length, footprint["length"])
            if min(selected.opening_width, selected.depth, core_length) < settings.min_wall:
                raise GeometryRejected("Feature too small for minimum wall setting")
            length = (2*(max(abs(bb.ymin-y), abs(bb.ymax-y))+settings.min_wall)
                      if sliding else core_length)
            pin_tool = profile_prism(selected, length).translate((x, y, 0))
            cavity = offset_prism(pin_tool, settings.clearance)
            measured_gaps = profile_gaps(pin_tool, cavity, settings.clearance)
            # A local envelope certifies floor/side material; for sliding slots
            # open ends are intentional, so test the central engagement region.
            core = profile_prism(selected, core_length).translate((x, y, 0))
            envelope = offset_prism(core, settings.clearance+settings.min_wall)
            envelope = envelope.intersect(halfspace(split.original, False))
            if envelope.cut(split.lower).Volume() > settings.volume_tolerance:
                raise GeometryRejected("Insufficient floor/side material around groove")
            anchor = cq.Solid.makeBox(selected.max_width+2*settings.min_wall,
                                     core_length+2*settings.min_wall, settings.min_wall,
                                     cq.Vector(x-selected.max_width/2-settings.min_wall,
                                               y-core_length/2-settings.min_wall, 0))
            if anchor.cut(split.upper).Volume() > settings.volume_tolerance:
                raise GeometryRejected("Insufficient material anchoring the protrusion")
            tongue = pin_tool.intersect(split.lower).clean()
            require_solid(tongue, "transferred tongue")
            if not sliding and pin_tool.cut(split.lower).Volume() > settings.volume_tolerance:
                raise GeometryRejected("Closed-pocket protrusion leaves the original body")
            if tongue.cut(cavity).Volume() > settings.volume_tolerance:
                raise GeometryRejected("Groove does not contain the shared protrusion")
            donor = require_solid(split.upper.fuse(tongue).clean(), "protrusion component")
            receiver = require_solid(split.lower.cut(cavity).clean(), "groove component")
            if min(donor.Volume(), receiver.Volume()) < split.original.Volume()*settings.min_part_fraction:
                raise GeometryRejected("Connection removes too much material")
            removed = split.lower.intersect(cavity).cut(tongue)
            directions = [(0, 1, 0), (0, -1, 0)] if sliding else [(0, 0, 1)]
            parameters = dict(
                type="groove", profile=asdict(selected), center_in_cut_frame=[x, y, 0],
                tool_length=length, central_engagement_length=core_length,
                clearance=settings.clearance, clearance_meaning="normal_offset_of_profile",
                measured_profile_surface_gaps=measured_gaps,
                axial_end_clearance=None if sliding else settings.clearance,
                round_radial_clearance=settings.clearance if selected.kind == "round" else None,
                round_diametral_clearance=2*settings.clearance if selected.kind == "round" else None,
                open_ends="both" if sliding else "closed_pocket",
                insertion="longitudinal_slide" if sliding else "normal_to_split",
                transferred_volume=tongue.Volume(), profile_containment_checked=True,
                material_check="central envelope and anchor containment; valid single-solid outputs",
                global_minimum_wall_certified=False)
            return Connection([("part_1", donor), ("part_2", receiver)], removed, parameters,
                              [("part_1", ["part_2"], directions)])
        except (GeometryRejected, ValueError, RuntimeError) as error:
            last_reason = str(error)
    raise GeometryRejected(f"groove/{profile}: {last_reason}")


def build_bolted(split, rng, settings, *, centers=None):
    bb = split.original.BoundingBox()
    last_reason = "No accessible through column"
    for x, y in (feature_centers(split, rng, settings.feature_attempts) if centers is None else centers):
        try:
            diameter = rng.choice((4.0, 5.0, 6.0))
            head_width, nut_height = diameter+4.0, 4.0
            outer_radius = head_width/(2*math.cos(math.pi/6))
            pad = through_hole_cutter(2*(outer_radius+settings.min_wall), bb.zmin, bb.zmax, (x, y))
            if pad.cut(split.original).Volume() > settings.volume_tolerance:
                raise GeometryRejected("No full material column and flat accessible bearing seats")
            hole_diameter = diameter+2*settings.clearance
            tool = through_hole_cutter(hole_diameter, bb.zmin-1, bb.zmax+1, (x, y))
            upper = require_solid(split.upper.cut(tool).clean(), "drilled upper component")
            lower = require_solid(split.lower.cut(tool).clean(), "drilled lower component")
            if min(upper.Volume(), lower.Volume()) < split.original.Volume()*settings.min_part_fraction:
                raise GeometryRejected("Bolt channel removes too much material")
            lengths = [split.upper.BoundingBox().zmax, -split.lower.BoundingBox().zmin]
            expected_holes = [math.pi*(hole_diameter/2)**2*d for d in lengths]
            actual_holes = [split.upper.Volume()-upper.Volume(), split.lower.Volume()-lower.Volume()]
            if any(abs(a-e) > settings.volume_tolerance for a, e in zip(actual_holes, expected_holes)):
                raise GeometryRejected("Coaxial hole is not fully through both halves")
            spec = BoltSpec("hex_head", bb.zlen+nut_height+2, diameter, head_width, 4.0, 0.0, 0.0)
            bolt = build_bolt(spec).translate((x, y, bb.zmax))
            nut_spec = NutSpec(hole_diameter, head_width, nut_height, 0.5)
            nut = build_nut(nut_spec).translate((x, y, bb.zmin-nut_height))
            head_area = planar_contact_area(upper, bolt, 1e-6)
            nut_area = planar_contact_area(lower, nut, 1e-6)
            if min(head_area, nut_area) < 1.0:
                raise GeometryRejected("Insufficient bearing contact for head or nut")
            parameters = dict(
                type="bolted", axis_in_cut_frame=[0, 0, 1], center_in_cut_frame=[x, y, 0],
                shaft_diameter=diameter, hole_diameter=hole_diameter,
                radial_clearance=settings.clearance, diametral_clearance=2*settings.clearance,
                nut_radial_clearance=settings.clearance, bolt=asdict(spec), nut=asdict(nut_spec),
                main_body_thickness=bb.zlen, engagement_in_halves=lengths,
                coaxial_holes_checked=True, hole_removed_volumes=actual_holes,
                expected_hole_removed_volumes=expected_holes,
                head_bearing_area=head_area, nut_bearing_area=nut_area,
                head_cannot_pass_hole=head_width > hole_diameter,
                tip_beyond_nut=2.0, threaded=False, thread_retention_modeled=False,
                material_check="full column contains bearing radius plus min_wall",
                global_minimum_wall_certified=False)
            return Connection([("part_1", upper), ("part_2", lower), ("bolt_1", bolt), ("nut_1", nut)],
                              split.original.intersect(tool), parameters,
                              [("part_1", ["part_2"], [(0, 0, 1)]),
                               ("bolt_1", ["part_1", "part_2"], [(0, 0, 1)]),
                               ("nut_1", ["part_1", "part_2", "bolt_1"], [(0, 0, -1)])])
        except (GeometryRejected, ValueError, RuntimeError) as error:
            last_reason = str(error)
    raise GeometryRejected(f"bolted: {last_reason}")


def sampled_path(moving, stationary, directions, settings):
    fixed = cq.Compound.makeCompound(stationary)
    travel = 1.2*(fixed.BoundingBox().DiagonalLength+moving.BoundingBox().DiagonalLength)
    distances = sorted(set(np.linspace(0, travel, settings.path_steps+1).tolist())
                       | {travel*f for f in (0.0001, 0.001, 0.005, 0.01, 0.02, 0.05)}, reverse=True)
    trials = []
    for direction in directions:
        vector = np.asarray(direction, dtype=float)
        vector /= np.linalg.norm(vector)
        start = moving.translate(tuple(vector*travel))
        if fixed.distance(start) <= 1e-6:
            trials.append(dict(direction=vector.tolist(), reason="start_not_separated"))
            continue
        collision = None
        for distance in distances:
            volume = overlap_volume(fixed, moving.translate(tuple(vector*distance)))
            if volume > settings.volume_tolerance:
                collision = dict(distance=distance, intersection_volume=volume)
                break
        if collision is None:
            return dict(status="sampled_clear", withdrawal_direction_in_cut_frame=vector.tolist(),
                        travel=travel, checked_positions=len(distances), distances=distances,
                        continuous_path_proven=False, failed_trials=trials)
        trials.append(dict(direction=vector.tolist(), reason="collision", **collision))
    return dict(status="not_found", continuous_path_proven=False, failed_trials=trials)


def validate_connection(split, connection, settings):
    parts = dict(connection.components)
    for name, shape in parts.items():
        require_solid(shape, name)
    intersections = {f"{a}/{b}": overlap_volume(parts[a], parts[b])
                     for a, b in combinations(parts, 2)}
    if any(v > settings.volume_tolerance for v in intersections.values()):
        raise GeometryRejected(f"Assembled components intersect: {intersections}")
    union = parts["part_1"].fuse(parts["part_2"])
    added = max(0.0, union.cut(split.original).Volume())
    missing = split.original.cut(union)
    void_error = difference_volume(missing, connection.removed)
    if added > settings.volume_tolerance or void_error > settings.volume_tolerance:
        raise GeometryRejected("Main geometry changed outside the declared technological void")
    paths = {}
    for moving, fixed, directions in connection.paths:
        path = sampled_path(parts[moving], [parts[n] for n in fixed], directions, settings)
        if path["status"] != "sampled_clear":
            raise GeometryRejected(f"No sampled assembly path for {moving}: {path['failed_trials']}")
        path["withdrawal_direction_world"] = (split.rotation @ np.array(
            path["withdrawal_direction_in_cut_frame"])).tolist()
        path["stationary_components"] = fixed
        paths[moving] = path
    return dict(valid_single_solid_components=True, intersection_volumes=intersections,
                added_main_body_volume=added, removed_main_body_volume=missing.Volume(),
                expected_removed_volume=connection.removed.Volume(),
                technological_void_error_volume=void_error, main_geometry_preserved=True,
                paths=paths, continuous_path_proven=False,
                mechanical_retention_checked=False, thread_retention_modeled=False)
