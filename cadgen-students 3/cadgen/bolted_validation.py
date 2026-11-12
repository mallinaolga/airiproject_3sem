"""Check actual smooth bolt/nut geometry against the declared through fit."""
import math
from OCP.BRepAdaptor import BRepAdaptor_Surface
from Bolty import BoltSpec, build_bolt
from Gaiki import NutSpec, build_nut
from Otverstiya import through_hole_cutter
from .assembly_geometry import GeometryRejected, difference_volume
from .assembly_validation import overlap_volume, planar_contact_area


def _bore_radius(shape, x, y):
    radii = []
    for face in shape.Faces():
        if face.geomType() != "CYLINDER": continue
        cylinder = BRepAdaptor_Surface(face.wrapped).Cylinder()
        axis = cylinder.Axis()
        point, direction = axis.Location(), axis.Direction()
        if abs(abs(direction.Z())-1) < 1e-7 and math.hypot(point.X()-x, point.Y()-y) < 1e-6:
            radii.append(cylinder.Radius())
    if not radii:
        raise GeometryRejected("No coaxial cylindrical through-hole surface")
    return min(radii)


def validate_bolted(split, connection, settings):
    """Support single, grouped and constructive bolts using existing generators."""
    settings.validate()
    p = connection.parameters
    specs = p.get("features") or (p.get("bolts") if isinstance(p.get("bolts"), list) else [p])
    parts = dict(connection.components)
    expected_names = {"part_1", "part_2"} | {f"{kind}_{i}" for i in range(1, len(specs)+1) for kind in ("bolt", "nut")}
    if not specs or set(parts) != expected_names or len(parts) != len(connection.components):
        raise GeometryRejected("Bolted joint requires both bodies and every declared bolt/nut pair")
    paths = {moving: (fixed, directions) for moving, fixed, directions in connection.paths}
    order = {moving: i for i, (moving, _, _) in enumerate(connection.paths)}
    if set(paths) != expected_names-{"part_2"} or len(paths) != len(connection.paths):
        raise GeometryRejected("Incomplete bolted installation sequence")
    reports = []
    bb = split.original.BoundingBox()
    for index, spec in enumerate(specs, 1):
        bolt_name, nut_name = f"bolt_{index}", f"nut_{index}"
        bolt_spec, nut_spec = BoltSpec(**spec["bolt"]), NutSpec(**spec["nut"])
        constructive = "head_seat_z" in spec
        x, y, _ = spec["center_in_fastener_frame" if constructive else "center_in_cut_frame"]
        top = spec["head_seat_z"] if constructive else bb.zmax
        bottom = spec["lower_seat_z"] if constructive else bb.zmin
        gap = spec["clearance"] if constructive else spec["radial_clearance"]
        values = [x, y, top, bottom, gap, bolt_spec.shaft_length, bolt_spec.shaft_diameter,
                  nut_spec.hole_diameter, nut_spec.height]
        if not all(math.isfinite(v) for v in values) or not 0 <= gap < 1 or top <= bottom:
            raise GeometryRejected("Invalid bolted fit dimensions or clearance")
        hole = bolt_spec.shaft_diameter+2*gap
        if (spec["shaft_diameter"] != bolt_spec.shaft_diameter
                or (not constructive and (gap != settings.clearance or spec["hole_diameter"] != hole))
                or (constructive and gap > settings.clearance)):
            raise GeometryRejected("Declared bolt fit disagrees with dimensions or requested clearance")
        if (abs(nut_spec.hole_diameter-hole) > 1e-7
                or bolt_spec.shaft_length < top-bottom+nut_spec.height
                or min(bolt_spec.head_width, nut_spec.across_flats) <= hole):
            raise GeometryRejected("Incompatible bolt length, nut bore or bearing dimensions")
        expected = [(bolt_name, build_bolt(bolt_spec, adaptive=True).translate((x, y, top))),
                    (nut_name, build_nut(nut_spec, adaptive=True).translate((x, y, bottom-nut_spec.height)))]
        for name, shape in expected:
            if difference_volume(parts[name], shape) > settings.volume_tolerance:
                raise GeometryRejected(f"Bolt/nut geometry or coaxial placement mismatch: {name}")
        tool = through_hole_cutter(hole, bottom, top, (x, y))
        for name in ("part_1", "part_2"):
            if abs(_bore_radius(parts[name], x, y)-hole/2) > 1e-6:
                raise GeometryRejected("Actual bore diameter differs from declared clearance")
            if overlap_volume(parts[name], tool) > settings.volume_tolerance:
                raise GeometryRejected("Bolt hole is obstructed inside a body")
        head_area = planar_contact_area(parts["part_1"], parts[bolt_name], 1e-6)
        nut_area = planar_contact_area(parts["part_2"], parts[nut_name], 1e-6)
        if min(head_area, nut_area) < .05*bolt_spec.shaft_diameter**2:
            raise GeometryRejected("Head or nut lacks bearing contact with its body")
        for name, required, directions in (
                (bolt_name, {"part_1", "part_2"}, [(0, 0, 1)]),
                (nut_name, {"part_1", "part_2", bolt_name}, [(0, 0, -1)])):
            if not required.issubset(paths[name][0]) or paths[name][1] != directions:
                raise GeometryRejected("Invalid bolt/nut insertion direction or dependencies")
        if not order["part_1"] < order[bolt_name] < order[nut_name]:
            raise GeometryRejected("Bodies must precede bolts, and bolts must precede nuts")
        reports.append(dict(bolt=bolt_name, nut=nut_name, coaxiality_checked=True,
                            actual_radial_clearance=gap, head_bearing_area=head_area,
                            nut_bearing_area=nut_area, shaft_reaches_through_nut=True))
    return dict(bolted_fit_checks=reports, threaded=False)
