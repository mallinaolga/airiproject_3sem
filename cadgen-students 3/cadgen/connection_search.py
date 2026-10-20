"""Bounded search for rigid contact, recess and insertion connections.

B-rep intersection rejects collisions. Planar contact uses face intersection;
curved support and straight approach paths are sampled, not a proof of continuous
assembly, mechanical retention, or manufacturing compatibility.
"""

from dataclasses import dataclass, field
import math

import cadquery as cq
import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Surface

from .assembly_validation import transform_part


@dataclass
class SearchSettings:
    contact_tolerance: float = 0.1
    volume_tolerance: float = 1e-5
    min_contact_area: float = 0.1
    min_engagement: float = 1.0
    max_poses: int = 32
    feature_limit: int = 12
    path_steps: int = 12


@dataclass
class Part:
    name: str
    shape: cq.Shape
    corners: list = field(default_factory=list)
    cylinders: list = field(default_factory=list)
    curves: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


def xyz(vector):
    return np.array(vector.toTuple(), dtype=float)


def unit(vector):
    length = np.linalg.norm(vector)
    if length < 1e-10:
        raise ValueError("Degenerate direction")
    return np.asarray(vector) / length


def frame(first, second):
    x = unit(first)
    y = unit(second - np.dot(second, x) * x)
    return np.column_stack((x, y, np.cross(x, y)))


def axis_frame(axis):
    axis = unit(axis)
    reference = np.eye(3)[np.argmin(np.abs(axis))]
    x = unit(np.cross(reference, axis))
    return np.column_stack((x, np.cross(axis, x), axis))


def surface_samples(face, grid=7):
    """Actual UV points inside the trimmed face, not tessellation centroids."""
    u0, u1, v0, v1 = face._uvBounds()
    points, normals = [], []
    for u in np.linspace(u0, u1, grid + 2)[1:-1]:
        for v in np.linspace(v0, v1, grid + 2)[1:-1]:
            try:
                normal, point = face.normalAt(float(u), float(v))
                if face.distance(cq.Vertex.makeVertex(*point.toTuple())) > 1e-5:
                    continue
                points.append(xyz(point))
                normals.append(xyz(normal))
            except (ValueError, RuntimeError):
                continue
    return np.asarray(points), np.asarray(normals)


def ellipsoid_fit(points):
    """Fit a quadric to a curved patch; only well-conditioned ellipsoids pass."""
    if len(points) < 15:
        return None
    origin = points.mean(axis=0)
    scale = max(np.linalg.norm(np.ptp(points, axis=0)), 1e-9)
    x, y, z = ((points - origin) / scale).T
    design = np.column_stack((x*x, y*y, z*z, 2*x*y, 2*x*z, 2*y*z,
                              2*x, 2*y, 2*z, np.ones(len(x))))
    _, singular, vt = np.linalg.svd(design, full_matrices=False)
    if singular[-2] < 1e-8:
        return None
    q = vt[-1]
    matrix = np.array([[q[0], q[3], q[4]], [q[3], q[1], q[5]],
                       [q[4], q[5], q[2]]])
    if np.linalg.cond(matrix) > 1e5:
        return None
    center = -np.linalg.solve(matrix, q[6:9])
    value = -(q[9] + np.dot(q[6:9], center))
    eigenvalues, axes = np.linalg.eigh(matrix / value)
    if np.min(eigenvalues) <= 0:
        return None
    radii = 1 / np.sqrt(eigenvalues)
    residual = np.abs(np.sum((((points-origin)/scale-center) @ axes / radii)**2,
                             axis=1) - 1)
    if max(residual) > 0.002:
        return None
    if np.linalg.det(axes) < 0:
        axes[:, -1] *= -1
    return {"center": center * scale + origin, "axes": axes, "radii": radii * scale}


def describe_part(name, shape, settings):
    if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0:
        raise ValueError("Expected one valid solid with positive volume")
    part = Part(name, shape)
    faces = shape.Faces()
    box = shape.BoundingBox()
    epsilon = max(min(box.xlen, box.ylen, box.zlen) * 1e-5, 1e-5)
    shared = {}
    for index, face in enumerate(faces):
        if face.geomType() == "PLANE":
            for edge in face.Edges():
                if edge.geomType() == "LINE":
                    shared.setdefault(edge.hashCode(), []).append((index, edge))
        else:
            try:
                points, normals = surface_samples(face)
                if len(points) < 4:
                    continue
                centered = points - points.mean(axis=0)
                curvature_sign = float(np.sum(centered * (normals-normals.mean(axis=0))))
                if face.geomType() == "CYLINDER":
                    cylinder = BRepAdaptor_Surface(face.wrapped).Cylinder()
                    direction = cylinder.Axis().Direction()
                    axis = np.array([direction.X(), direction.Y(), direction.Z()])
                    location = np.array([cylinder.Location().X(), cylinder.Location().Y(),
                                         cylinder.Location().Z()])
                    u0, u1, v0, v1 = face._uvBounds()
                    length = abs(v1-v0)
                    coverage = face.Area() / max(2*math.pi*cylinder.Radius()*length, 1e-9)
                    if coverage > 0.95 and abs(u1-u0) > 6.2:
                        part.cylinders.append({
                            "face": index, "inner": curvature_sign < 0,
                            "radius": cylinder.Radius(), "length": length, "axis": axis,
                            "center": location + axis * ((v0+v1)/2),
                        })
                fit = ellipsoid_fit(points) if face.geomType() != "CYLINDER" else None
                part.curves.append({
                    "face": index, "concave": curvature_sign < -1e-6,
                    "points": points, "normals": normals, "fit": fit,
                })
            except Exception as error:
                part.warnings.append(f"face {index}: {type(error).__name__}: {error}")

    for entries in shared.values():
        if len(entries) != 2:
            continue
        (ia, edge), (ib, other) = entries
        if ia == ib or not edge.isSame(other):
            continue
        na, nb = xyz(faces[ia].normalAt()), xyz(faces[ib].normalAt())
        if abs(np.dot(na, nb)) > 0.98:
            continue
        center = xyz(edge.Center())
        side = unit(na-nb) * epsilon
        inside = [shape.isInside(cq.Vector(*(center+s*side)), epsilon*0.01)
                  for s in (-1, 1)]
        if inside[0] != inside[1]:
            continue
        part.corners.append({
            "faces": [ia, ib], "normals": [na, nb], "center": center,
            "concave": all(inside), "length": edge.Length(),
            "direction": unit(xyz(edge.tangentAt(0.5))),
            "weight": min(faces[ia].Area(), faces[ib].Area()),
        })
    part.corners.sort(key=lambda x: x["weight"], reverse=True)
    return part


def candidate_poses(a, b, settings):
    """Interleave receiver roles and feature families; bound exact checks later."""
    groups = []
    for receiver, insert, swapped in ((a, b, False), (b, a, True)):
        corner_poses, cylinder_poses, curve_poses = [], [], []

        def emit(group, rotation, translation, kind, **evidence):
            # Every hypothesis moves B into the fixed coordinate system of A.
            if swapped:
                translation = -rotation.T @ translation
                rotation = rotation.T
            group.append(dict(rotation_matrix=rotation.tolist(), translation=translation.tolist(),
                              kind=kind, receiver="b" if swapped else "a", evidence=evidence))

        inner = [c for c in receiver.corners if c["concave"]][:settings.feature_limit]
        outer = [c for c in insert.corners if not c["concave"]][:settings.feature_limit]
        combinations = sorted(((i, j) for i in range(len(inner)) for j in range(len(outer))),
                              key=lambda p: (sum(p), p))
        for i, j in combinations:
            ca, cb = inner[i], outer[j]
            for reverse in (False, True):
                bn = cb["normals"][::-1] if reverse else cb["normals"]
                if abs(np.dot(*ca["normals"])-np.dot(*bn)) > 0.025:
                    continue
                rotation = frame(-ca["normals"][0], -ca["normals"][1]) @ frame(*bn).T
                translation = ca["center"] - rotation @ cb["center"]
                emit(corner_poses, rotation, translation, "multi_surface_contact",
                     receiver_faces=ca["faces"], insert_faces=cb["faces"])
        for ca in receiver.cylinders:
            if not ca["inner"]:
                continue
            for cb in insert.cylinders:
                if cb["inner"] or cb["radius"] > ca["radius"] + 1e-8:
                    continue
                engagement = min(ca["length"], cb["length"])
                if engagement < settings.min_engagement:
                    continue
                for sign in (1, -1):
                    rotation = axis_frame(ca["axis"]) @ axis_frame(sign*cb["axis"]).T
                    emit(cylinder_poses, rotation, ca["center"]-rotation@cb["center"],
                         "cylindrical_insertion", receiver_face=ca["face"],
                         insert_face=cb["face"], engagement=engagement,
                         radial_gap=ca["radius"]-cb["radius"])
        for ca in receiver.curves:
            if not ca["concave"] or ca["fit"] is None:
                continue
            for cb in insert.curves:
                if cb["concave"] or cb["fit"] is None:
                    continue
                fa, fb = ca["fit"], cb["fit"]
                if np.any(fb["radii"] > fa["radii"] + settings.contact_tolerance):
                    continue
                for signs in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)):
                    rotation = fa["axes"] @ np.diag(signs) @ fb["axes"].T
                    translation = fa["center"] - rotation @ fb["center"]
                    emit(curve_poses, rotation, translation, "curved_recess",
                         receiver_face=ca["face"], insert_face=cb["face"])
                    # Also seat a smaller oval towards the bottom of an open recess.
                    opening = ca["normals"].mean(axis=0)
                    if np.linalg.norm(opening) > 0.1:
                        opening = unit(opening)
                        host_depth = np.linalg.norm((fa["axes"].T @ opening)*fa["radii"])
                        insert_depth = np.linalg.norm((rotation @ fb["axes"]).T @ opening
                                                      * fb["radii"])
                        seated = translation - opening * max(0.0, host_depth-insert_depth)
                        emit(curve_poses, rotation, seated, "curved_recess",
                             receiver_face=ca["face"], insert_face=cb["face"])
        groups.extend([curve_poses, cylinder_poses, corner_poses])

    seen = set()
    for index in range(max((len(g) for g in groups), default=0)):
        for group in groups:
            if index >= len(group):
                continue
            pose = group[index]
            key = tuple(np.round(np.ravel(pose["rotation_matrix"]), 7)) + tuple(
                np.round(pose["translation"], 6))
            if key in seen:
                continue
            seen.add(key)
            yield pose


def planar_supports(a, b, settings):
    patches = []
    faces_a = [f for f in a.Faces() if f.geomType() == "PLANE"]
    faces_b = [f for f in b.Faces() if f.geomType() == "PLANE"]
    for fa in faces_a:
        normal = fa.normalAt()
        for fb in faces_b:
            if normal.dot(fb.normalAt()) > -0.995:
                continue
            offset = (fb.Center()-fa.Center()).dot(normal)
            if abs(offset) > settings.contact_tolerance:
                continue
            common = fa.intersect(fb.translate((-offset*normal).toTuple()))
            area = float(common.Area())
            if area >= settings.min_contact_area:
                patches.append(dict(normal=list(normal.toTuple()), area=area, gap=abs(offset)))
    return patches


def independent_normals(normals, angle=20):
    cosine = math.cos(math.radians(angle))
    return any(np.dot(x, y) < cosine for i, x in enumerate(normals) for y in normals[i+1:])


def curved_support(receiver, moved_insert, receiver_face, settings):
    curve = next((c for c in receiver.curves if c["face"] == receiver_face), None)
    if curve is None or not curve["concave"]:
        return None
    accepted = []
    for point, normal in zip(curve["points"], curve["normals"]):
        vertex = cq.Vertex.makeVertex(*point)
        for face in moved_insert.Faces():
            if face.distance(vertex) <= settings.contact_tolerance:
                if np.dot(xyz(face.normalAt(cq.Vector(*point))), normal) < -0.8:
                    accepted.append(normal)
                    break
    fraction = len(accepted) / max(len(curve["points"]), 1)
    if len(accepted) < 4 or fraction < 0.1 or not independent_normals(accepted):
        return None
    return dict(sampled_support_points=len(accepted), surface_sample_fraction=fraction,
                support_check="sampled_on_trimmed_curved_surface")


def evaluate_pose(a, b, pose, settings):
    """Recheck geometry: feature correspondence alone is not acceptance."""
    moved = transform_part(b.shape, pose["rotation_matrix"], pose["translation"])
    volume = max(0.0, float(a.shape.intersect(moved).Volume()))
    result = dict(pose, intersection_volume=volume, accepted=False)
    if volume > settings.volume_tolerance:
        result["reason"] = "collision"
        return result, moved
    if pose["kind"] == "cylindrical_insertion":
        r = np.asarray(pose["rotation_matrix"])
        t = np.asarray(pose["translation"])
        receiver = a if pose["receiver"] == "a" else b
        insert = b if receiver is a else a
        if receiver is b:
            t, r = -r.T @ t, r.T
        ca = next(c for c in receiver.cylinders if c["face"] == pose["evidence"]["receiver_face"])
        cb = next(c for c in insert.cylinders if c["face"] == pose["evidence"]["insert_face"])
        delta = r @ cb["center"] + t - ca["center"]
        offset = abs(np.dot(delta, ca["axis"]))
        radial_offset = np.linalg.norm(delta-np.dot(delta, ca["axis"])*ca["axis"])
        engagement = max(0.0, min(ca["length"]/2, offset+cb["length"]/2)
                         - max(-ca["length"]/2, offset-cb["length"]/2))
        if (abs(np.dot(ca["axis"], r@cb["axis"])) > 0.99999
                and ca["radius"]-cb["radius"]-radial_offset >= -1e-8
                and engagement >= settings.min_engagement):
            result.update(accepted=True, reason="cylindrical_insertion",
                          engagement=engagement, radial_gap=ca["radius"]-cb["radius"]-radial_offset)
            return result, moved
    patches = planar_supports(a.shape, moved, settings)
    if independent_normals([p["normal"] for p in patches]):
        result.update(accepted=True, reason="multi_surface_contact", contact_patches=patches)
        return result, moved
    if pose["kind"] == "curved_recess":
        if pose["receiver"] == "a":
            support = curved_support(a, moved, pose["evidence"]["receiver_face"], settings)
        else:
            r, t = np.asarray(pose["rotation_matrix"]), np.asarray(pose["translation"])
            in_b = transform_part(a.shape, r.T, -r.T@t)
            support = curved_support(b, in_b, pose["evidence"]["receiver_face"], settings)
        if support:
            result.update(accepted=True, reason="curved_recess", **support)
            return result, moved
    result["reason"] = "insufficient_contact_or_engagement"
    return result, moved


def approach_path(a, b, settings):
    """Finite samples, with a fully separated start. Does not prove continuity."""
    ba, bb = a.BoundingBox(), b.BoundingBox()
    travel = 1.1 * (ba.DiagonalLength + bb.DiagonalLength)
    directions = list(np.eye(3)) + list(-np.eye(3))
    normals = [xyz(f.normalAt()) for f in a.Faces() if f.geomType() == "PLANE"]
    for i, normal in enumerate(normals[:12]):
        directions.append(normal)
        for other in normals[i+1:12]:
            if np.linalg.norm(normal+other) > 0.1:
                directions.append(unit(normal+other))
    seen, errors = set(), []
    for direction in directions:
        key = tuple(np.round(direction, 5))
        if key in seen:
            continue
        seen.add(key)
        try:
            start = b.translate(tuple(direction * travel))
            if a.distance(start) <= settings.contact_tolerance:
                continue
            distances = sorted(set(np.linspace(0, travel, settings.path_steps+1)[1:])
                               | {travel*f for f in (0.001, 0.005, 0.01)}, reverse=True)
            if all(a.intersect(b.translate(tuple(direction*d))).Volume()
                   <= settings.volume_tolerance for d in distances):
                return dict(status="sampled_clear", withdrawal_direction=direction.tolist(),
                            travel=travel, checked_positions=len(distances)+1,
                            continuous_path_checked=False, errors=errors)
        except Exception as error:
            errors.append(f"{type(error).__name__}: {error}")
    return dict(status="not_found", continuous_path_checked=False, errors=errors)


def search_pair(a, b, settings):
    attempts, errors = [], []
    best_pose_only = None
    tested = 0
    for index, pose in enumerate(candidate_poses(a, b, settings)):
        if index >= settings.max_poses:
            break
        tested += 1
        try:
            result, moved = evaluate_pose(a, b, pose, settings)
            attempts.append(result["reason"])
            if not result["accepted"]:
                continue
            result["approach"] = approach_path(a.shape, moved, settings)
            result["mechanical_retention_checked"] = False
            if result["approach"]["status"] == "sampled_clear":
                return dict(status="connection_found", tested_poses=tested,
                            connection=result, errors=errors), moved
            best_pose_only = result
        except Exception as error:
            attempts.append("error")
            errors.append(f"{type(error).__name__}: {error}")
    from collections import Counter
    return dict(status="pose_only" if best_pose_only else ("error" if errors and
                    all(x == "error" for x in attempts) else "not_found"),
                tested_poses=tested, reasons=dict(Counter(attempts)),
                connection=best_pose_only, errors=errors), None
