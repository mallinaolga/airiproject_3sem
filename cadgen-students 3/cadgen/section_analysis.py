"""Recognize a translation extrusion by B-rep set equality, not face count.

Analysis copies may fill verified straight internal bores. The source and
partition solids are never changed by this module. Finite directions are tried;
failure to recognize an extrusion is not proof that none exists.
"""

import math

import cadquery as cq
import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Surface

from .assembly_geometry import difference_volume, frame
from .assembly_validation import transform_part


def canonical(vector):
    v = np.asarray(vector, dtype=float)
    if v.shape != (3,) or not np.isfinite(v).all() or np.linalg.norm(v) < 1e-10:
        raise ValueError("invalid analysis direction")
    v = v / np.linalg.norm(v)
    return -v if next((x for x in v if abs(x) > 1e-7), 1) < 0 else v


def directions(shape, history=None):
    options = list((history or {}).get("directions", []))
    for f in shape.Faces():
        if f.geomType() == "CYLINDER":
            options.append(BRepAdaptor_Surface(f.wrapped).Cylinder().Axis().Direction().Coord())
    options.extend(f.normalAt().toTuple() for f in sorted(shape.Faces(), key=lambda f: -f.Area())
                   if f.geomType() == "PLANE")
    _, inertia = np.linalg.eigh(np.array(cq.Shape.matrixOfInertia(shape)))
    options.extend(inertia.T)
    result = []
    for v in options:
        v = canonical(v)
        if not any(abs(np.dot(v, old)) > .999999 for old in result):
            result.append(v)
        if len(result) == 16:
            break
    # A long prism can have dozens of side normals larger than either cap.
    # Never let that ordering evict its extrusion axis: for a translation
    # extrusion it is a principal inertia direction (apart from degeneracy).
    # At most three extra axes; the shared operation budget still applies.
    for v in inertia.T:
        v = canonical(v)
        if not any(abs(np.dot(v,old)) > .999999 for old in result):
            result.append(v)
    return result


def fill_bores(shape, budget):
    """Fill inward cylindrical walls or fully wall-supported closed-wire bores.

    A partial external scallop/recess must not be mistaken for a hole. V bounds
    keep blind-hole depth and stepped-bore segments separate. Booleans affect
    this temporary analysis envelope only.
    """
    result, filled, errors = shape, [], []
    for f in shape.Faces():
        if f.geomType() != "CYLINDER":
            continue
        a = BRepAdaptor_Surface(f.wrapped)
        if a.LastUParameter()-a.FirstUParameter() < 2*math.pi-1e-6:
            continue
        c = a.Cylinder()
        p = np.array(a.Value((a.FirstUParameter()+a.LastUParameter())/2,
                             (a.FirstVParameter()+a.LastVParameter())/2).Coord())
        origin, axis = np.array(c.Location().Coord()), np.array(c.Axis().Direction().Coord())
        radial = p-origin-axis*np.dot(p-origin, axis)
        if np.dot(np.array(f.normalAt(tuple(p)).toTuple()), radial) >= 0:
            continue
        budget.use()
        try:
            start = origin+axis*a.FirstVParameter()
            plug = cq.Solid.makeCylinder(c.Radius(), a.LastVParameter()-a.FirstVParameter(),
                                         cq.Vector(*start), cq.Vector(*axis))
            candidate = result.fuse(plug).clean()
            if len(candidate.Solids()) == 1 and candidate.isValid():
                result = candidate
                filled.append(dict(radius=c.Radius(), axis=axis.tolist(), start=start.tolist(),
                                   depth=a.LastVParameter()-a.FirstVParameter()))
        except Exception as error:
            errors.append(f"{type(error).__name__}: {error}")
    # A noncircular straight bore has a closed opening wire and a congruent
    # exit or blind end. Require its entire lateral boundary to be supported
    # by actual cavity walls: two coincident openings alone are insufficient.
    planar = [f for f in result.Faces() if f.geomType() == "PLANE"]
    for entrance in planar:
        inward = -np.array(entrance.normalAt().toTuple())
        for wire in entrance.innerWires():
            opening = cq.Face.makeFromWires(wire)
            for end in planar:
                if abs(np.dot(end.normalAt().toTuple(),inward)) < .999999:
                    continue
                depth = np.dot(np.array(end.Center().toTuple())-np.array(entrance.Center().toTuple()),inward)
                if depth < 1e-5:
                    continue
                budget.use()
                shifted = opening.translate(tuple(inward*depth))
                if not any(abs(cq.Face.makeFromWires(w).Area()-opening.Area()) < 1e-5
                           and shifted.intersect(cq.Face.makeFromWires(w)).Area() > opening.Area()-1e-5
                           for w in end.Wires()):
                    continue
                try:
                    plug = cq.Solid.extrudeLinear(wire,[],cq.Vector(*(inward*depth)))
                    sides = [f for f in plug.Faces() if not
                             (f.geomType()=="PLANE" and abs(np.dot(f.normalAt().toTuple(),inward))>.999999)]
                    if plug.intersect(result).Volume() > 1e-5:
                        continue
                    if any(side.Area()-side.intersect(result).Area() > max(1e-5,side.Area()*1e-7)
                           for side in sides):
                        continue
                    candidate = result.fuse(plug).clean()
                    if len(candidate.Solids())==1 and candidate.isValid():
                        result = candidate
                        filled.append(dict(kind="closed_wire_bore",axis=inward.tolist(),depth=float(depth)))
                        break
                except Exception as error:
                    errors.append(f"{type(error).__name__}: {error}")
    return result, filled, errors


def section(shape, z):
    size = shape.BoundingBox().DiagonalLength*3+1
    wire = cq.Workplane("XY", origin=(0, 0, z)).rect(2*size, 2*size).val()
    return shape.intersect(cq.Face.makeFromWires(wire))


def outer_section(shape, z):
    """Planar bounded contours, ignoring enclosed interior wires only."""
    faces = [cq.Face.makeFromWires(f.outerWire()).translate((0,0,-z))
             for f in section(shape,z).Faces()]
    return cq.Compound.makeCompound(faces)


def contour_difference(a, b):
    aa, bb = a.Area(), b.Area()
    common = a.intersect(b).Area()
    return max(0., aa+bb-2*common)/max(aa, bb, 1e-9)


def levels(local, epsilon):
    result = []
    for z in sorted(f.Center().z for f in local.Faces()
                    if f.geomType() == "PLANE" and abs(f.normalAt().z) > .999999):
        if not result or abs(z-result[-1]) > epsilon*.001:
            result.append(z)
    return result


def prism_from_section(profile, bottom, height):
    solids = []
    for f in profile.Faces():
        wire = f.outerWire()
        solids.append(cq.Solid.extrudeLinear(wire, f.innerWires(), cq.Vector(0,0,height)).translate((0,0,bottom)))
    return cq.Compound.makeCompound(solids)


def recognize(shape, budget, history=None):
    """Test full-volume equality with an extrusion of an actual midsection.

    Each direction uses the complete height, so a short unsampled step cannot
    pass through equal probe areas. Enclosed sectional holes are retained in
    the sweep; recognized variable-depth/transverse bores are filled beforehand.
    """
    envelope, bores, errors = fill_bores(shape, budget)
    center = np.array(envelope.Center().toTuple())
    axes = []
    tolerance = max(1e-5, envelope.Volume()*1e-8)
    for normal in directions(envelope, history):
        budget.use(2)
        r = frame(normal)
        local = transform_part(envelope, r.T, -r.T@center)
        bb = local.BoundingBox()
        epsilon = max(bb.DiagonalLength*1e-5, 1e-5)
        zs = levels(local, epsilon)
        axis = dict(normal=normal, rotation=r, center=center, local=local, levels=zs,
                    epsilon=epsilon, extent=(bb.zmin,bb.zmax))
        axes.append(axis)
        try:
            mid = (bb.zmin+bb.zmax)/2
            profile = section(local, mid).translate((0,0,-mid))
            # This exact reconstruction also covers arbitrary noncircular
            # holes parallel to the extrusion axis.
            swept = prism_from_section(profile, bb.zmin, bb.zlen)
            error = difference_volume(local, swept)
            if error <= tolerance:
                return dict(simple=True, reason="constant_outer_section", normal=normal.tolist(),
                            extrusion_length=bb.zlen, reconstruction_error_volume=error,
                            tolerance_volume=tolerance, ignored_bores=bores, errors=errors), axes
        except Exception as error:
            errors.append(f"{type(error).__name__}: {error}")
    return dict(simple=False, reason="no_constant_section_direction_verified", ignored_bores=bores,
                directions_tested=len(axes), errors=errors), axes
