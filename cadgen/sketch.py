from __future__ import annotations

import json
import logging
import math
import random
from copy import deepcopy
from operator import itemgetter
from pathlib import Path

import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepBuilderAPI import (
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakePolygon,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_Transform,
)
from OCP.BRep import BRep_Tool
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet2d
from OCP.BRepTools import BRepTools, BRepTools_WireExplorer
from OCP.GC import GC_MakeArcOfCircle
from OCP.GeomAbs import GeomAbs_CurveType
from OCP.gp import gp_Ax1, gp_Ax2, gp_Circ, gp_Dir, gp_Pnt, gp_Trsf
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
from OCP.TopAbs import TopAbs_FACE, TopAbs_VERTEX, TopAbs_WIRE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS

from .base import BaseFactory, BaseOperation
from .registry import factories
from .utils import (
    argsort_points,
    float_to_string,
    get_point_on_sketch_and_radius_range,
    shape_to_area,
    shape_to_bbox,
)

logger = logging.getLogger(__name__)


class Sketch(BaseOperation):
    # prev_center: tuple[float, float] | None = None
    array_pattern_sketch: Sketch | None = None
    array_pattern_n: int | None = None
    array_pattern_radius: float | None = None
    array_pattern_dx: float | None = None
    array_pattern_dy: float | None = None
    array_pattern_nx: int | None = None
    array_pattern_ny: int | None = None
    array_pattern_type: str | None = None
    array_pattern_mode: str | None = None
    array_pattern_start_angle: float | None = None
    array_pattern_span: float | None = None
    corner_fillet: float | None = None
    corner_chamfer: float | None = None
    point: tuple[float, float] | None = None
    """
    wires = [{
            'type': 'polygon',
            'outer': True,
            'vertices': [[0, 0], [1, 1], ...]
            'edges': [
                {'type': 'line'},
                {'type': 'arc', 'point': [2, 2]}, ...]
        }, {
            'type': 'circle',
            'outer': False,
            'center': [1, 1],
            'radius': 2
        }, ...]
    """

    def __init__(
        self,
        wires,
        array_pattern_sketch: Sketch | None = None,
        array_pattern_n: int | None = None,
        array_pattern_radius: float | None = None,
        array_pattern_dx: float | None = None,
        array_pattern_dy: float | None = None,
        array_pattern_nx: int | None = None,
        array_pattern_ny: int | None = None,
        array_pattern_type: str | None = None,
        array_pattern_mode: str | None = None,
        array_pattern_start_angle: float | None = None,
        array_pattern_span: float | None = None,
        corner_fillet: float | None = None,
        corner_chamfer: float | None = None,
        point: tuple[float, float] | None = None,
    ):
        self.wires = wires
        self.corner_fillet = corner_fillet
        self.corner_chamfer = corner_chamfer
        self.array_pattern_sketch = array_pattern_sketch
        self.array_pattern_n = array_pattern_n
        self.array_pattern_radius = array_pattern_radius
        self.array_pattern_dx = array_pattern_dx
        self.array_pattern_dy = array_pattern_dy
        self.array_pattern_nx = array_pattern_nx
        self.array_pattern_ny = array_pattern_ny
        self.array_pattern_type = array_pattern_type
        self.array_pattern_mode = array_pattern_mode
        self.array_pattern_start_angle = array_pattern_start_angle
        self.array_pattern_span = array_pattern_span
        self.point = point

    # ------------------------------------------------------------------ 2D corner fillet
    #
    # Rounds the corners of the OUTER wire inside the sketch, emitted as
    # `.vertices().fillet(r)`.  This is deliberately a SKETCH feature rather
    # than a 3D edge fillet: 50.7% of the SFT model's build failures on clean
    # MCB are `.edges(PointOnEdgeSelector([...])).fillet/chamfer` dying with
    # `no_edges_for_fillet` / `BRep_API: command not done`, because the model
    # has to guess a 3D point that lands on the intended edge.  A sketch fillet
    # has no selector to get wrong -- the only failure axis is the scalar
    # radius, and that is closed-form clampable from the profile vertices.
    #
    # Empirical clamps (1507-config sweep, 895/895 = 1.000 valid+watertight
    # once obeyed, 0.681 on the adversarial sweep that violated them):
    #   * base wire must be ALL-STRAIGHT-EDGE -- a wire containing an arc has
    #     tangent (non-sharp) vertices and fails 5/5;
    #   * r <= 0.9 * rmax, rmax = min over edges of L/(cot(a/2)+cot(b/2))
    #     where a,b are the interior angles at that edge's endpoints
    #     (for a rectangle this reduces to min(w,h)/2).  The cliff at r/rmax
    #     = 1.0 is absolute: ~98% fail just above it;
    #   * never fillet the same face twice (arc-tangent vertices remain);
    #   * fillet BEFORE any mode='s' cut wire;
    #   * `.reset()` is mandatory between push/parray/rarray and `.vertices()`.

    @staticmethod
    def wire_is_all_straight(wire) -> bool:
        return (
            wire.get("type") not in ("circle", "spline")
            and bool(wire.get("edges"))
            and all(e["type"] == "line" for e in wire["edges"])
            and len(wire.get("vertices", [])) >= 3
        )

    @staticmethod
    def max_corner_fillet(wire) -> float:
        """
        Largest radius that fits every corner of a straight-edged wire.

        For edge (i, j) with interior angles th_i, th_j the two tangent points
        consume r*cot(th_i/2) and r*cot(th_j/2) of its length, so the binding
        constraint is r < L / (cot(th_i/2) + cot(th_j/2)).
        """
        if not Sketch.wire_is_all_straight(wire):
            return 0.0
        v = [np.asarray(p, dtype=float) for p in wire["vertices"]]
        n = len(v)
        if n < 3:
            return 0.0

        cots = []
        for i in range(n):
            a = v[(i - 1) % n] - v[i]
            b = v[(i + 1) % n] - v[i]
            na, nb = np.linalg.norm(a), np.linalg.norm(b)
            if na < 1e-9 or nb < 1e-9:
                return 0.0
            cos_t = float(np.clip(a @ b / (na * nb), -1.0, 1.0))
            theta = math.acos(cos_t)
            # a straight-through or fully reversed vertex cannot be rounded
            if theta < 1e-6 or abs(theta - math.pi) < 1e-6:
                return 0.0
            cots.append(1.0 / math.tan(theta / 2.0))

        rmax = float("inf")
        for i in range(n):
            j = (i + 1) % n
            length = float(np.linalg.norm(v[j] - v[i]))
            denom = cots[i] + cots[j]
            if denom <= 1e-9:
                continue
            rmax = min(rmax, length / denom)
        return 0.0 if not np.isfinite(rmax) else max(rmax, 0.0)

    @staticmethod
    def canonical_spline_points(points):
        """
        Put spline control points in the same winding the rest of the system
        uses: CLOCKWISE (shoelace signed area < 0).

        sketch_global_coords normalises every closed segment/arc path with
        `if _path_signed_area(edges) > 0.0: reverse`, i.e. it forces clockwise.
        A spline is not parsed as PathEdges so it bypasses that entirely, and a
        CCW spline next to CW polygons builds an oppositely-oriented face --
        which surfaces as `Extrude produced non-positive volume` and made
        0 of 100 spline profiles survive.
        """
        pts = [[float(x), float(y)] for x, y in points]
        n = len(pts)
        area = 0.0
        for i in range(n):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % n]
            area += x0 * y1 - x1 * y0
        return pts[::-1] if area > 0.0 else pts

    @staticmethod
    def max_corner_chamfer(wire) -> float:
        """
        Largest equal-distance chamfer that fits every corner.

        Two chamfers on the same edge each consume `c` of its length measured
        from their vertex, so the binding constraint is c < L/2 for the
        shortest edge.  The probe's failure mode here is SILENT -- over budget,
        OCC returns a solid whose isValid() is True but whose faces self-overlap
        so the mesh is NOT watertight (59 of 72 failures, no exception raised).
        That is why this is clamped up front rather than guarded by try/except.
        """
        if not Sketch.wire_is_all_straight(wire):
            return 0.0
        v = [np.asarray(p, dtype=float) for p in wire["vertices"]]
        n = len(v)
        if n < 3:
            return 0.0
        shortest = min(float(np.linalg.norm(v[(i + 1) % n] - v[i])) for i in range(n))
        return 0.45 * shortest  # 0.45 not 0.5: ratios in [0.50,0.55) failed 20/26

    def corner_chamfer_is_valid(self) -> bool:
        """The emitted `.vertices().chamfer(c)` will build watertight."""
        if not self.corner_chamfer or self.corner_chamfer <= 0:
            return False
        if self.corner_fillet:
            return False  # one corner treatment per profile
        if not self.wires or not self.wires[0].get("outer", False):
            return False
        if sum(1 for w in self.wires if w.get("outer", False)) != 1:
            return False
        if not Sketch.wire_is_all_straight(self.wires[0]):
            return False
        return self.corner_chamfer <= Sketch.max_corner_chamfer(self.wires[0]) + 1e-9

    @staticmethod
    def chamfered_vertices(wire, c: float):
        """
        The polygon that `.vertices().chamfer(c)` produces: every vertex is
        replaced by the two points at distance `c` along its adjacent edges.

        Computed geometrically rather than via OCC so `to_shape()` matches the
        emitted code exactly; an equal-distance 2D chamfer is exactly this.
        """
        v = [np.asarray(p, dtype=float) for p in wire["vertices"]]
        n = len(v)
        out = []
        for i in range(n):
            prev_dir = v[(i - 1) % n] - v[i]
            next_dir = v[(i + 1) % n] - v[i]
            np_, nn = np.linalg.norm(prev_dir), np.linalg.norm(next_dir)
            if np_ < 1e-12 or nn < 1e-12:
                return None
            out.append(v[i] + prev_dir / np_ * c)
            out.append(v[i] + next_dir / nn * c)
        return out

    def corner_fillet_is_valid(self) -> bool:
        """The emitted `.vertices().fillet(r)` will build."""
        if not self.corner_fillet or self.corner_fillet <= 0:
            return False
        if not self.wires or not self.wires[0].get("outer", False):
            return False
        # `.vertices()` selects the vertices of EVERY face in the sketch, so a
        # second outer wire would be filleted too -- only allow the single-face
        # case, where the outer wire is the one we clamped against.
        if sum(1 for w in self.wires if w.get("outer", False)) != 1:
            return False
        if not Sketch.wire_is_all_straight(self.wires[0]):
            return False
        return self.corner_fillet <= 0.9 * Sketch.max_corner_fillet(self.wires[0]) + 1e-9

    @staticmethod
    def wire_to_rectangle(wire):
        # -> (x, y, w, h) or None
        if wire.get("type") == "spline":
            return None
        vertices = wire["vertices"]
        if len(vertices) == 4:
            if set(e["type"] for e in wire["edges"]) == set(["line"]):
                x, y = zip(*vertices)
                if len(set(x)) == len(set(y)) == 2:
                    return (
                        (min(x) + max(x)) / 2,
                        (min(y) + max(y)) / 2,
                        max(x) - min(x),
                        max(y) - min(y),
                    )
        return None

    def to_string_one_sketch(
        self,
        plane,
        wires,
        skip_on_one_wire=False,
        short_mode=False,
        use_tag=False,
        emit_corner_fillet=False,
    ):
        context = [0, 0]
        s_short = ""
        # tag = "r.workplane(origin=r.val().Center())" if "faces" in plane else plane
        if not use_tag:
            tag = plane.split("=")[-1] if "faces" in plane else plane
        else:
            tag = plane.split("\n")[2].split("=")[0] if "faces" in plane else plane
        if tag.startswith(".copyWorkplane"):
            tag = "w0" + tag
        if not use_tag:
            s = f"{plane}.sketch()" if not short_mode else tag
        else:
            s = tag
            s += ".sketch()" if not short_mode else ""

        for i, wire in enumerate(wires):
            m = ",mode='s'" if not wire["outer"] else ""
            if wire["type"] == "spline":
                # Periodic closed spline.  The probe found two hard
                # requirements: the tangents argument must be POSITIONAL and
                # empty (`.spline(pts, [], True)`; passing None raises), and
                # `.assemble()` is mandatory before `.finalize()` or the
                # extrude dies with DispatchError.
                pts = ",".join(
                    f"({float_to_string(x)},{float_to_string(y)})"
                    for x, y in wire["points"]
                )
                t = f".spline([{pts}],[],True).assemble()"
                if i == 0:
                    s += t
                else:
                    s += f".reset().face({tag}.sketch(){t}{m})"
            elif wire["type"] == "circle":
                x, y = wire["center"]
                if not np.allclose([x, y], context):
                    context = [x, y]
                    s += f".push([({x},{y})])"
                r = wire["radius"]
                if short_mode:
                    s_short += f".circle({r}{m})"
                else:
                    s += f".circle({r}{m})"
            else:  # 'polygon'
                rectangle = self.wire_to_rectangle(wire)
                # rectangle
                if rectangle is not None:
                    x, y, w, h = rectangle
                    if not np.allclose([x, y], context):
                        context = [x, y]
                        x = float_to_string(x)
                        y = float_to_string(y)
                        s += f".push([({x},{y})])"
                    if short_mode:
                        s_short += f".rect({w},{h}{m})"
                    else:
                        s += f".rect({w},{h}{m})"
                else:
                    t = ""
                    for j, edge in enumerate(wire["edges"]):
                        if j == 0:
                            x, y = wire["vertices"][0]
                            u = f"({x},{y}),"
                        else:
                            u = ""

                        n_edges = len(wire["edges"])
                        x, y = wire["vertices"][(j + 1) % n_edges]
                        if edge["type"] == "line":
                            if j < n_edges - 1:
                                t += f".segment({u}({x},{y}))"
                            else:
                                t += ".close()"
                        else:  # 'arc'
                            mx, my = edge["point"]
                            t += f".arc({u}({mx},{my}),({x},{y}))"

                    t += ".assemble()"
                    if i == 0:
                        s += t
                    else:
                        s += f".reset().face({tag}.sketch(){t}{m})"

            # Round the outer profile's corners immediately after it is laid
            # down and BEFORE any mode='s' cut wire: filleting a multi-wire
            # face yields isValid()==False (measured 0/18), while
            # fillet-then-cut is valid+watertight.  `.reset()` afterwards is
            # required because `.vertices()` consumes the selection, and it
            # also forces the next primitive to re-emit its own `.push()`.
            if (
                i == 0
                and not short_mode
                and emit_corner_fillet
                and self.corner_fillet_is_valid()
            ):
                s += f".vertices().fillet({float_to_string(self.corner_fillet)}).reset()"
                context = [float("inf"), float("inf")]
            elif (
                i == 0
                and not short_mode
                and emit_corner_fillet
                and self.corner_chamfer_is_valid()
            ):
                s += (
                    f".vertices().chamfer({float_to_string(self.corner_chamfer)})"
                    ".reset()"
                )
                context = [float("inf"), float("inf")]

        if short_mode and s_short != "":
            return s_short
        else:
            return s

    def to_string(
        self,
        plane,
    ):
        s = self.to_string_one_sketch(
            plane,
            self.wires,
            skip_on_one_wire=self.array_pattern_sketch is not None,
            emit_corner_fillet=True,
        )
        # TODO think where this should go
        # if ".faces" in s:
        #     extent = abs(extent)
        #     if hole_outer_extent:
        #         hole_outer_extent = abs(hole_outer_extent)
        #     if hole_inner_extents:
        #         for i in range(len(hole_inner_extents)):
        #             hole_inner_extents[i] = abs(hole_inner_extents[i])

        point = self.point if self.point is not None else (0, 0)

        if self.array_pattern_sketch is not None:
            if self.array_pattern_mode == "s":
                self.array_pattern_sketch.wires[0]["outer"] = False
            array_pattern_string = self.to_string_one_sketch(
                plane,
                self.array_pattern_sketch.wires,
                skip_on_one_wire=True,
                short_mode=True,
            )
            self.array_pattern_sketch.wires[0]["outer"] = True
            reset = ".reset()" if "push" not in s else ""
            if point and tuple(point) != (0, 0):
                point_push = f".push([({point[0]},{point[1]})])"
                point = (0, 0)
            else:
                point_push = ""

            if self.array_pattern_type == "parray":
                s += f"{reset}{point_push}.parray({self.array_pattern_radius}, {self.array_pattern_start_angle}, {self.array_pattern_span}, {self.array_pattern_n})"
            elif self.array_pattern_type == "rarray":
                s += f"{reset}{point_push}.rarray({self.array_pattern_dx}, {self.array_pattern_dy}, {self.array_pattern_nx}, {self.array_pattern_ny})"
            if (
                "rect" in array_pattern_string or "circle" in array_pattern_string
            ) and "push" not in array_pattern_string:
                s += array_pattern_string
            else:
                array_pattern_string = self.to_string_one_sketch(
                    plane,
                    self.array_pattern_sketch.wires,
                    skip_on_one_wire=True,
                    use_tag=True,
                )
                s += f".face({array_pattern_string}.wires(), mode='{self.array_pattern_mode}')"

        s += ".finalize()"

        # check that solid
        logger.info("Sketch code: %s", s)
        if self.array_pattern_sketch is not None:
            pass
            # exec(
            #     f"import cadquery as cq\nw0=cq.Workplane('XY')\nw1=cq.Workplane('XY')\nr={s}",
            #     {},
            #     locals(),
            # )
            # w = locals()["r"].val()
            # mesh = compound_to_mesh(w)
            # assert len(mesh.split()) == 1, f"Mesh has {len(mesh.split())} parts"

        return s

    def cq_bounding_box(self, sketch):
        boxes = []
        for face in sketch.val()._faces.Faces():
            face_box = face.BoundingBox()
            boxes.append((face_box.xmin, face_box.ymin, face_box.xmax, face_box.ymax))

        xmin = min(boxes, key=lambda x: x[0])[0]
        ymin = min(boxes, key=lambda x: x[1])[1]
        xmax = max(boxes, key=lambda x: x[2])[2]
        ymax = max(boxes, key=lambda x: x[3])[3]
        return xmin, ymin, xmax, ymax

    def _fillet_outer_wire(self, wire_shape):
        """
        Apply the 2D corner fillet to an outer wire, mirroring what the emitted
        `.vertices().fillet(r)` does at runtime.

        to_shape() builds faces straight from OCC edges rather than through
        cadquery, so without this the generator's internal geometry (used for
        volume checks, normalisation and the code<->mesh IoU) would disagree
        with the code it writes.  BRepFilletAPI_MakeFillet2d is what
        cq.Sketch.fillet uses underneath; verified to agree analytically
        (60x40 rect, r=6, depth 10: 23690.5 vs 23691.0 exact).
        Returns the filleted outer wire, or the original on any failure.
        """
        try:
            face = BRepBuilderAPI_MakeFace(wire_shape).Face()
            mk = BRepFilletAPI_MakeFillet2d(face)
            explorer = TopExp_Explorer(face, TopAbs_VERTEX)
            seen: list[tuple[float, float]] = []
            while explorer.More():
                vertex = TopoDS.Vertex_s(explorer.Current())
                pnt = BRep_Tool.Pnt_s(vertex)
                key = (round(pnt.X(), 6), round(pnt.Y(), 6))
                if key not in seen:
                    seen.append(key)
                    mk.AddFillet(vertex, float(self.corner_fillet))
                explorer.Next()
            mk.Build()
            if not mk.IsDone():
                return wire_shape
            return BRepTools.OuterWire_s(TopoDS.Face_s(mk.Shape()))
        except Exception:  # noqa: BLE001 - fall back to the sharp profile
            logger.debug("corner fillet failed, keeping sharp corners", exc_info=True)
            return wire_shape

    def to_shape(self):
        # -> TopoDS_Compound
        compound = None
        face_builder: BRepBuilderAPI_MakeFace | None = None
        apply_fillet = self.corner_fillet_is_valid()
        apply_chamfer = self.corner_chamfer_is_valid()
        for i, wire in enumerate(self.wires):
            if apply_chamfer and i == 0:
                # `.vertices().chamfer(c)` == replacing each vertex with the two
                # points at distance c along its edges; build that polygon
                # directly so to_shape matches the emitted code exactly.
                pts = Sketch.chamfered_vertices(wire, float(self.corner_chamfer))
                if pts is not None:
                    wire = {
                        "type": "polygon",
                        "outer": True,
                        "vertices": [[float(p[0]), float(p[1])] for p in pts],
                        "edges": [{"type": "line"} for _ in pts],
                    }
            edges = self.wire_to_edges(wire)
            wire_builder = BRepBuilderAPI_MakeWire(edges[0])
            for edge in edges[1:]:
                wire_builder.Add(edge)

            if wire["outer"]:
                outer = wire_builder.Wire()
                if apply_fillet and i == 0:
                    outer = self._fillet_outer_wire(outer)
                face_builder = BRepBuilderAPI_MakeFace(outer)
            else:
                assert face_builder is not None, "face_builder is required"
                face_builder.Add(TopoDS.Wire_s(wire_builder.Wire().Reversed()))

            # make face if it is last inner wire
            if i == len(self.wires) - 1 or self.wires[i + 1]["outer"]:
                if compound is not None:
                    compound = BRepAlgoAPI_Fuse(compound, face_builder.Face()).Shape()
                else:
                    compound = face_builder.Face()
        return compound

    def transform(self, shift, scale):
        for wire in self.wires:
            if wire["type"] == "spline":
                for point in wire["points"]:
                    point[0] = (point[0] + shift[0]) * scale
                    point[1] = (point[1] + shift[1]) * scale
            elif wire["type"] == "circle":
                wire["center"][0] = (wire["center"][0] + shift[0]) * scale
                wire["center"][1] = (wire["center"][1] + shift[1]) * scale
                wire["radius"] = wire["radius"] * scale
            else:  # 'polygon'
                for vertex in wire["vertices"]:
                    vertex[0] = (vertex[0] + shift[0]) * scale
                    vertex[1] = (vertex[1] + shift[1]) * scale
                for edge in wire["edges"]:
                    if edge["type"] == "arc":
                        edge["point"][0] = (edge["point"][0] + shift[0]) * scale
                        edge["point"][1] = (edge["point"][1] + shift[1]) * scale

        # assert self.prev_center is not None
        # prev_center_x, prev_center_y = self.prev_center
        # prev_center_x = (prev_center_x + shift[0]) * scale
        # prev_center_y = (prev_center_y + shift[1]) * scale
        # self.prev_center = (prev_center_x, prev_center_y)

        if self.point is not None:
            point_x, point_y = self.point
            point_x = (point_x + shift[0]) * scale
            point_y = (point_y + shift[1]) * scale
            self.point = (point_x, point_y)

        # Transform sketch attributes
        if self.corner_fillet:
            self.corner_fillet *= scale
        if self.corner_chamfer:
            self.corner_chamfer *= scale
        if self.array_pattern_radius:
            self.array_pattern_radius *= scale
        if self.array_pattern_dx:
            self.array_pattern_dx *= scale
        if self.array_pattern_dy:
            self.array_pattern_dy *= scale

        if self.array_pattern_sketch:
            self.array_pattern_sketch.transform([0, 0], scale)

    def round(self):
        for wire in self.wires:
            if wire["type"] == "spline":
                for point in wire["points"]:
                    point[0] = round(point[0])
                    point[1] = round(point[1])
            elif wire["type"] == "circle":
                wire["center"][0] = round(wire["center"][0])
                wire["center"][1] = round(wire["center"][1])
                wire["radius"] = round(wire["radius"])
            else:  # 'polygon'
                for vertex in wire["vertices"]:
                    vertex[0] = round(vertex[0])
                    vertex[1] = round(vertex[1])
                for edge in wire["edges"]:
                    if edge["type"] == "arc":
                        edge["point"][0] = round(edge["point"][0])
                        edge["point"][1] = round(edge["point"][1])
        # assert self.prev_center is not None
        # self.prev_center = (round(self.prev_center[0]), round(self.prev_center[1]))

        if self.point is not None:
            self.point = (round(self.point[0]), round(self.point[1]))

        # Round sketch attributes.  The radius must stay a valid corner fillet
        # AFTER the vertices themselves are snapped to integers, so re-clamp
        # against the rounded profile and drop the fillet if it no longer fits
        # (the probe's `floor(0.9*rmax) < 1 -> skip` rule).
        if self.corner_fillet:
            self.corner_fillet = round(self.corner_fillet)
            if self.wires and Sketch.wire_is_all_straight(self.wires[0]):
                budget = math.floor(0.9 * Sketch.max_corner_fillet(self.wires[0]))
                self.corner_fillet = min(self.corner_fillet, budget)
            if self.corner_fillet < 1:
                self.corner_fillet = None
        if self.corner_chamfer:
            self.corner_chamfer = round(self.corner_chamfer)
            if self.wires and Sketch.wire_is_all_straight(self.wires[0]):
                self.corner_chamfer = min(
                    self.corner_chamfer,
                    math.floor(Sketch.max_corner_chamfer(self.wires[0])),
                )
            if self.corner_chamfer < 1:
                self.corner_chamfer = None
        if self.array_pattern_radius:
            self.array_pattern_radius = round(self.array_pattern_radius)
        if self.array_pattern_dx:
            self.array_pattern_dx = round(self.array_pattern_dx)
        if self.array_pattern_dy:
            self.array_pattern_dy = round(self.array_pattern_dy)

        if self.array_pattern_sketch:
            self.array_pattern_sketch.round()

    def reorder(self):
        n_wires = len(self.wires)
        bbox_corners = list()
        for wire in self.wires:
            outer_wire = deepcopy(wire)
            outer_wire["outer"] = True
            outer_face = Sketch([outer_wire]).to_shape()
            x_min, y_min, _, _, _, _ = shape_to_bbox(outer_face)
            bbox_corners.append([x_min, y_min])
        bbox_corners = np.array(bbox_corners)
        order = argsort_points(bbox_corners)

        # reorder outer wires by bottom left bbox corner
        # reorder inner wires by bottom left bbox corner
        wires = list()
        for i in order:
            if self.wires[i]["outer"]:
                wires.append(self.wires[i])
                inner_ids = list()
                for j in range(i + 1, len(self.wires)):
                    if self.wires[j]["outer"]:
                        break
                    inner_ids.append(j)
                if not len(inner_ids):
                    continue
                inner_order = argsort_points(bbox_corners[inner_ids])
                for j in inner_order:
                    wires.append(self.wires[inner_ids[j]])
        assert len(wires) == n_wires
        self.wires = wires

        # reorder vertices to start from bottom left
        for wire in self.wires:
            if wire["type"] == "circle":
                continue

            first = argsort_points(wire["vertices"])[0]
            n = len(wire["vertices"])
            wire["vertices"] = wire["vertices"][first:n] + wire["vertices"][:first]
            wire["edges"] = wire["edges"][first:n] + wire["edges"][:first]

    def orient(self):
        # all wires to be counterclockwise
        for wire in self.wires:
            if wire["type"] == "circle":
                continue

            points = list()
            for vertex, edge in zip(wire["vertices"], wire["edges"]):
                points.append(vertex)
                if edge["type"] == "arc":
                    points.append(edge["point"])

            points = np.array(points)
            x, y = points[:, 0], points[:, 1]
            # shoelace formula
            signed_area = np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))
            assert not np.isclose(signed_area, 0)
            if signed_area > 0:
                wire["vertices"] = wire["vertices"][::-1]
                wire["edges"] = wire["edges"][:-1][::-1] + [wire["edges"][-1]]

    @staticmethod
    def wire_to_edges(wire):
        edges = list()
        if wire["type"] == "spline":
            # Built through cadquery's own Edge.makeSpline -- the exact call
            # behind the emitted `.spline(pts, [], True)` -- so to_shape() and
            # the emitted code are identical by construction rather than by
            # a re-derivation that could drift.
            import cadquery as _cq

            pts = [_cq.Vector(float(x), float(y), 0.0) for x, y in wire["points"]]
            edges.append(_cq.Edge.makeSpline(pts, periodic=True).wrapped)
        elif wire["type"] == "circle":
            x, y = wire["center"]
            circ = gp_Circ(gp_Ax2(gp_Pnt(x, y, 0), gp_Dir(0, 0, 1)), wire["radius"])
            edges.append(BRepBuilderAPI_MakeEdge(circ).Edge())
        else:  # 'polygon'
            for j, edge in enumerate(wire["edges"]):
                x, y = wire["vertices"][j]
                xyz_first = gp_Pnt(x, y, 0)
                x, y = wire["vertices"][(j + 1) % len(wire["edges"])]
                xyz_last = gp_Pnt(x, y, 0)
                if edge["type"] == "line":
                    edge_builder = BRepBuilderAPI_MakeEdge(xyz_first, xyz_last)
                else:  # 'arc'
                    x, y = edge["point"]
                    xyz_middle = gp_Pnt(x, y, 0)
                    try:
                        arc_builder = GC_MakeArcOfCircle(
                            xyz_first, xyz_middle, xyz_last
                        )
                        arc_is_done = (
                            not hasattr(arc_builder, "IsDone")
                            or arc_builder.IsDone()
                        )
                        curve = arc_builder.Value() if arc_is_done else None
                    except Exception as e:
                        raise AssertionError("invalid arc") from e
                    if curve is None:
                        raise AssertionError("invalid arc")
                    edge_builder = BRepBuilderAPI_MakeEdge(curve)
                edges.append(edge_builder.Edge())
        return edges

    def try_fix_wire(self, wire, state):
        # skip inner wires if outer failed
        assert wire["outer"] or state["face"] is not None

        # remove zero edges
        if wire["type"] == "circle":
            assert not np.isclose(wire["radius"], 0)
        else:
            ids = [0]
            for i in range(1, len(wire["vertices"])):
                if not np.allclose(wire["vertices"][i], wire["vertices"][i - 1]):
                    ids.append(i)
            if len(ids) > 1:
                if np.allclose(wire["vertices"][0], wire["vertices"][ids[-1]]):
                    ids = ids[:-1]
            if len(ids) != len(wire["vertices"]):
                assert len(ids) > 1
                wire["vertices"] = itemgetter(*ids)(wire["vertices"])
                wire["edges"] = itemgetter(*ids)(wire["edges"])

        # skip wires with invalid arcs
        # they could be replaced with lines, but then probably need to orient again
        edges = self.wire_to_edges(wire)

        # check intersection of all edges
        for i in range(len(edges)):
            for j in range(i + 1, len(edges)):
                n = 0
                if j == i + 1:
                    n += 1
                if (j + 1) % len(edges) == i:
                    n += 1
                extrema = BRepExtrema_DistShapeShape(edges[i], edges[j])
                if np.isclose(extrema.Value(), 0):
                    assert n == extrema.NbSolution()
                else:
                    assert n == 0

        # skip invalid wires
        outer_wire = deepcopy(wire)
        outer_wire["outer"] = True
        outer_face = Sketch([outer_wire]).to_shape()
        outer_area = shape_to_area(outer_face)
        assert not np.isclose(outer_area, 0) and outer_area > 0

        new_face = Sketch(state["face_wires"] + [wire]).to_shape()

        # skip intersecting wires
        if not wire["outer"]:
            # todo: we should check distance between wires not areas of faces
            face_area = shape_to_area(state["face"])
            new_area = shape_to_area(new_face)
            assert not np.isclose(new_area, 0) and new_area > 0
            assert np.isclose(face_area - outer_area, new_area)

        state["face"] = new_face
        state["face_wires"].append(wire)

    def fix_one_sketch(self, wires):
        # skip zero edges, invalid wires, intersecting wires, intersecting faces
        compound, wires_cur = None, list()
        state = dict(face=None, face_wires=list())

        for i, wire in enumerate(wires):
            try:
                self.try_fix_wire(deepcopy(wire), state)
            except AssertionError:
                pass

            if i == len(wires) - 1 or wires[i + 1]["outer"]:
                if state["face"] is not None:
                    new_wires = wires_cur + state["face_wires"]  # type: ignore
                    new_compound = Sketch(new_wires).to_shape()

                    # skip intersecting faces
                    if compound is not None:
                        compound_area = shape_to_area(compound)
                        face_area = shape_to_area(
                            Sketch(state["face_wires"]).to_shape()
                        )
                        new_area = shape_to_area(new_compound)
                        if not np.isclose(compound_area + face_area, new_area):
                            continue

                    wires_cur = new_wires
                    compound = new_compound
                state["face"] = None
                state["face_wires"] = list()

        assert len(wires_cur) > 0
        return wires_cur

    def fix(self):
        # skip zero edges, invalid wires, intersecting wires, intersecting faces
        self.wires = self.fix_one_sketch(self.wires)
        if self.array_pattern_sketch is not None:
            self.array_pattern_sketch.wires = self.fix_one_sketch(
                self.array_pattern_sketch.wires
            )

    def to_dict(self) -> dict:
        return {
            "type": "Sketch",
            "wires": self.wires,
            "array_pattern_sketch": (
                self.array_pattern_sketch.to_dict()
                if self.array_pattern_sketch is not None
                else None
            ),
            "array_pattern_n": self.array_pattern_n,
            "array_pattern_radius": self.array_pattern_radius,
            "array_pattern_dx": self.array_pattern_dx,
            "array_pattern_dy": self.array_pattern_dy,
            "array_pattern_nx": self.array_pattern_nx,
            "array_pattern_ny": self.array_pattern_ny,
            "array_pattern_type": self.array_pattern_type,
            "array_pattern_mode": self.array_pattern_mode,
            "array_pattern_start_angle": self.array_pattern_start_angle,
            "array_pattern_span": self.array_pattern_span,
            "corner_fillet": self.corner_fillet,
            "corner_chamfer": self.corner_chamfer,
            "point": self.point,
        }

    @staticmethod
    def from_dict(entity: dict) -> "Sketch":
        assert (
            entity["type"] == "Sketch"
        ), f"Trying to build Sketch from type {entity['type']}"
        return Sketch(
            wires=entity["wires"],
            array_pattern_sketch=(
                Sketch.from_dict(entity["array_pattern_sketch"])
                if entity["array_pattern_sketch"] is not None
                else None
            ),
            array_pattern_n=entity["array_pattern_n"],
            array_pattern_radius=entity["array_pattern_radius"],
            array_pattern_dx=entity["array_pattern_dx"],
            array_pattern_dy=entity["array_pattern_dy"],
            array_pattern_nx=entity["array_pattern_nx"],
            array_pattern_ny=entity["array_pattern_ny"],
            array_pattern_type=entity["array_pattern_type"],
            array_pattern_mode=entity["array_pattern_mode"],
            array_pattern_start_angle=entity["array_pattern_start_angle"],
            array_pattern_span=entity["array_pattern_span"],
            corner_fillet=entity.get("corner_fillet"),
            corner_chamfer=entity.get("corner_chamfer"),
            point=entity["point"],
        )


class SketchFactory(BaseFactory):
    try:
        sketches_root = Path(
            "/mnt/virtual_ai0001071-04018_A100-MT-nfs1/NFS1-cad-3d-SR008/CAD/cadexp/datasets/sketchgraphs/sg_sketches"
        )
        sketches = json.loads((sketches_root / "valid_files.json").read_text())
        long_sketches = json.loads((sketches_root / "long_sketches.json").read_text())
    except:
        logger.info("Sketchgraph folder not found.")
    sketches_root: Path
    sketches: list[str | Path]
    long_sketches: list[str | Path]

    def __init__(
        self,
        min_n_commands,
        max_n_commands,
        n_outer_probabilities,
        rotation_probability,
        array_pattern_probability=0.0,
        array_pattern_sketch_min_n_commands=1,
        array_pattern_sketch_max_n_commands=1,
        array_pattern_sketch_min_rel_scale=0.01,
        array_pattern_cut_probability=1,
        parray_probability=0.5,
        corner_fillet_probability=0.0,
        corner_chamfer_probability=0.0,
        spline_profile_probability=0.0,
        corner_fillet_min_rel=0.10,
        corner_fillet_max_rel=0.90,
        from_sketchgraph: bool = False,
        from_sketchgraph_probability: float | None = None,
    ):
        # n_commands: number of rotated rectangles / circles
        # n_outer_probabilities: number of outer wires probablities
        # rotation_probability: probablity to rotate rectangle
        self.min_n_commands = min_n_commands
        self.max_n_commands = max_n_commands
        self.n_outer_probabilities = n_outer_probabilities
        self.rotation_probability = rotation_probability
        self.array_pattern_probability = array_pattern_probability
        self.array_pattern_sketch_min_n_commands = array_pattern_sketch_min_n_commands
        self.array_pattern_sketch_max_n_commands = array_pattern_sketch_max_n_commands
        self.array_pattern_sketch_min_rel_scale = array_pattern_sketch_min_rel_scale
        self.array_pattern_cut_probability = array_pattern_cut_probability
        self.parray_probability = parray_probability
        # 2D corner rounding of the outer profile.  Off by default so
        # existing configs are unchanged; enable per-config.
        self.corner_fillet_probability = corner_fillet_probability
        self.corner_chamfer_probability = corner_chamfer_probability
        # convert a straight outer profile into a smooth periodic spline
        self.spline_profile_probability = spline_profile_probability
        # radius as a fraction of the profile's own corner budget
        self.corner_fillet_min_rel = corner_fillet_min_rel
        self.corner_fillet_max_rel = corner_fillet_max_rel
        self.from_sketchgraph = from_sketchgraph
        self.from_sketchgraph_probability = from_sketchgraph_probability

    @staticmethod
    def make_rectangle_face(x, y, w, h, angle):
        polygon = BRepBuilderAPI_MakePolygon()
        polygon.Add(gp_Pnt(x - w / 2, y - h / 2, 0))
        polygon.Add(gp_Pnt(x + w / 2, y - h / 2, 0))
        polygon.Add(gp_Pnt(x + w / 2, y + h / 2, 0))
        polygon.Add(gp_Pnt(x - w / 2, y + h / 2, 0))
        polygon.Close()
        wire = polygon.Wire()

        if not np.isclose(angle, 0):
            trsf = gp_Trsf()
            rotation_axis = gp_Ax1(gp_Pnt(x, y, 0), gp_Dir(0, 0, 1))
            trsf.SetRotation(rotation_axis, angle)
            wire = TopoDS.Wire_s(BRepBuilderAPI_Transform(wire, trsf, True).Shape())

        face = BRepBuilderAPI_MakeFace(wire).Face()
        return face

    @staticmethod
    def make_circle_face(x, y, radius):
        circ = gp_Circ(gp_Ax2(gp_Pnt(x, y, 0), gp_Dir(0, 0, 1)), radius)
        edge = BRepBuilderAPI_MakeEdge(circ).Edge()
        wire = BRepBuilderAPI_MakeWire(edge).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        return face

    def try_update_compound(self, compound, state, only_cuts=False, zero_center=False):
        # try add a rectangle or circle to existing face
        r_min, r_max = 0.01, 0.5
        if np.random.randint(2) < 1:
            xy = list(state["prev_center"])
        else:
            xy = np.random.uniform(-1, 1, 2).tolist()
        if zero_center:
            xy = [0, 0]

        if (np.random.randint(2) < 1 or only_cuts) and compound is not None:
            algo = BRepAlgoAPI_Cut
            # try to be inside bounding box
            if np.random.randint(2) < 1:
                x_min, y_min, _, x_max, y_max, _ = shape_to_bbox(compound)
                if not x_min < xy[0] < x_max:
                    xy[0] = np.random.uniform(x_min, x_max)  # type: ignore
                if not y_min < xy[1] < y_max:
                    xy[1] = np.random.uniform(y_min, y_max)  # type: ignore
                r_max = min(x_max - xy[0], xy[0] - x_min, y_max - xy[1], xy[1] - y_min)
        else:
            algo = BRepAlgoAPI_Fuse

        r_max = max(r_min, r_max)
        use_sketchgraph = getattr(
            self,
            "_active_from_sketchgraph",
            self.from_sketchgraph,
        )
        if not use_sketchgraph:
            if np.random.randint(2) < 1:
                radius = np.random.uniform(r_min, r_max)
                face = self.make_circle_face(xy[0], xy[1], radius)
            else:
                wh = np.random.uniform(r_min, r_max * 2, 2)
                if np.random.rand() < self.rotation_probability:
                    angle = np.random.uniform(0, np.pi)
                else:
                    angle = 0
                face = self.make_rectangle_face(xy[0], xy[1], wh[0], wh[1], angle)
        else:
            if not getattr(self, "sketches", None) and not getattr(
                self, "long_sketches", None
            ):
                raise RuntimeError(
                    "Sketchgraph sampling requested, but sketchgraph files were not "
                    "loaded. Check SketchFactory.sketches_root or set "
                    "from_sketchgraph=False."
                )
            # Only external SketchGraphs sampling needs these libraries.
            # Keep the procedural generator independent of them.
            import cadlib.core as clc
            import cadlib.features as clf
            from cadaxt.core import CADAxtProfile
            from sg_parser.sample_sketch import sample_profile_from_sketch_dict

            face = None
            bbox = np.random.uniform(r_min, r_max) * 2
            while face is None:
                try:
                    if np.random.uniform() > 0.10:
                        sketchgraph_file = (
                            self.sketches_root / random.choice(self.sketches)
                            if self.sketches
                            else None
                        )
                    else:
                        sketchgraph_file = Path(random.choice(self.long_sketches))

                    sample = sample_profile_from_sketch_dict(sketchgraph_file)
                    profile = CADAxtProfile(
                        **list(sample["profiles"].values())[0], transform={}
                    )
                    face = clc.CAD().ocp.move_lower_left(
                        clc.CAD().ocp.rescale_to_area(
                            clf.Profile.from_dict(
                                data=profile.model_dump(),
                                sketch_plane=clc.CoordSystem(),
                            ).profile2face(),
                            bbox**2,
                        ),
                        xy[0] - bbox / 2,
                        xy[1] - bbox / 2,
                    )
                except Exception:
                    continue

        if compound is None:
            compound = face
        else:
            new_compound = algo(compound, face).Shape()
            unifier = ShapeUpgrade_UnifySameDomain(new_compound, True, True, True)
            unifier.Build()
            new_compound = unifier.Shape()
            new_area = shape_to_area(new_compound)
            # check that not everything is deleted
            assert not np.isclose(new_area, 0)
            # check that something is changed
            assert not np.isclose(
                shape_to_area(BRepAlgoAPI_Cut(face, new_compound).Shape()), 0
            ) or not np.isclose(
                shape_to_area(BRepAlgoAPI_Cut(new_compound, face).Shape()), 0
            )
            compound = new_compound

        return compound, dict(prev_center=xy)

    @staticmethod
    def compound_to_wires(compound):
        face_explorer = TopExp_Explorer(compound, TopAbs_FACE)  # type: ignore
        wires = list()
        while face_explorer.More():
            face = face_explorer.Current()
            face_wires, bbox_sizes = list(), list()
            wire_explorer = TopExp_Explorer(face, TopAbs_WIRE)  # type: ignore
            while wire_explorer.More():
                wire = TopoDS.Wire_s(wire_explorer.Current())
                x_min, y_min, _, x_max, y_max, _ = shape_to_bbox(
                    BRepBuilderAPI_MakeFace(wire).Face()  # type: ignore
                )
                bbox_size = max(x_max - x_min, y_max - y_min)
                face_wires.append(wire)
                bbox_sizes.append(bbox_size)
                wire_explorer.Next()

            for i, wire_id in enumerate(np.argsort(bbox_sizes)[::-1]):
                outer = i == 0
                wires.append(dict(wire=face_wires[wire_id], outer=outer))
            face_explorer.Next()
        return wires

    @staticmethod
    def sample_wires(wires):
        # max_n_outer_wires = np.random.randint(1, self.max_n_outer_wires + 1)
        # p = self.n_outer_probabilities
        # max_n_outer_wires = np.random.choice(len(p), p=p) + 1
        max_n_outer_wires = 1
        n_outer_wires = 0
        i = -1
        for i, wire in enumerate(wires):
            if wire["outer"]:
                n_outer_wires += 1
            if n_outer_wires > max_n_outer_wires:
                i = i - 1
                break
        return wires[: i + 1]

    @staticmethod
    def wires_to_sketch(wires, state):
        sketch = list()
        for wire in wires:
            edges = list()
            edge_explorer = BRepTools_WireExplorer(wire["wire"])
            while edge_explorer.More():
                edge = TopoDS.Edge_s(edge_explorer.Current())
                curve = BRepAdaptor_Curve(edge)
                u_first = curve.FirstParameter()
                u_last = curve.LastParameter()
                # edge = topods.Edge(edge_explorer.Current())
                # curve, u_first, u_last = BRep_Tool.Curve(edge)
                xy_first = curve.Value(u_first)
                xy_first = [xy_first.X(), xy_first.Y()]

                xy_middle = curve.Value((u_first + u_last) / 2)
                xy_middle = [xy_middle.X(), xy_middle.Y()]
                xy_last = curve.Value(u_last)
                xy_last = [xy_last.X(), xy_last.Y()]
                edges.append(
                    dict(
                        curve=curve,
                        xy_first=xy_first,
                        xy_middle=xy_middle,
                        xy_last=xy_last,
                    )
                )
                edge_explorer.Next()

            assert len(edges) > 0
            if len(edges) == 1:  # circle
                edge = edges[0]
                curve_type = edge["curve"].GetType()
                assert curve_type == GeomAbs_CurveType.GeomAbs_Circle
                assert np.allclose(edge["xy_first"], edge["xy_last"])
                circ = edge["curve"].Circle()

                radius = circ.Radius()
                center = circ.Location()
                center = [center.X(), center.Y()]
                sketch.append(
                    dict(
                        type="circle", outer=wire["outer"], center=center, radius=radius
                    )
                )
            else:  # polygon
                # if end if 1s edge is not begin or end ot the 2nd, than reverse 1st
                if not np.allclose(
                    edges[0]["xy_last"], edges[1]["xy_first"]
                ) and not np.allclose(edges[0]["xy_last"], edges[1]["xy_last"]):
                    xy = edges[0]["xy_first"]
                    edges[0]["xy_first"] = edges[0]["xy_last"]
                    edges[0]["xy_last"] = xy
                vertices = [edges[0]["xy_first"]]
                segments = list()
                for edge in edges:
                    assert not np.allclose(edge["xy_first"], edge["xy_last"])
                    # if end of begin edge is not end of previous, than reverse this
                    if not np.allclose(edge["xy_first"], vertices[-1]):
                        xy = edge["xy_first"]
                        edge["xy_first"] = edge["xy_last"]
                        edge["xy_last"] = xy
                    assert np.allclose(edge["xy_first"], vertices[-1])
                    vertices.append(edge["xy_last"])
                    if (
                        edge["curve"].GetType() == GeomAbs_CurveType.GeomAbs_Line
                    ):  # line
                        segments.append(dict(type="line"))
                    else:  # arc
                        segments.append(dict(type="arc", point=edge["xy_middle"]))
                assert np.allclose(vertices[0], vertices[-1])
                sketch.append(
                    dict(
                        type="polygon",
                        outer=wire["outer"],
                        vertices=vertices[:-1],
                        edges=segments,
                    )
                )
        sketch = Sketch(sketch)
        # sketch.prev_center = state["prev_center"]
        return sketch

    def generate_one_sketch(
        self, min_n_commands, max_n_commands, only_cuts=False, zero_center=False
    ):
        prev_center = (0, 0)
        if self.from_sketchgraph_probability is None:
            active_from_sketchgraph = self.from_sketchgraph
        else:
            active_from_sketchgraph = (
                np.random.random() < self.from_sketchgraph_probability
            )

        # construct Sketch from random rectangles and circles
        compound = None
        state = dict(prev_center=prev_center)
        n_commands = np.random.randint(min_n_commands, 1 + max_n_commands)

        previous_active = getattr(self, "_active_from_sketchgraph", None)
        self._active_from_sketchgraph = active_from_sketchgraph
        try:
            for _ in range(n_commands):
                try:
                    compound, state = self.try_update_compound(
                        compound, state, only_cuts=only_cuts, zero_center=zero_center
                    )
                except AssertionError:
                    pass
        finally:
            if previous_active is None:
                delattr(self, "_active_from_sketchgraph")
            else:
                self._active_from_sketchgraph = previous_active

        wires = self.compound_to_wires(compound)
        wires = self.sample_wires(wires)
        sketch = self.wires_to_sketch(wires, state)
        logger.info("Generated sketch: %s", sketch.__dict__)

        return sketch

    def generate(self, zero_center=False):
        do_array_pattern = np.random.random() < self.array_pattern_probability

        array_pattern_sketch = None
        array_pattern_start_angle = None
        array_pattern_span = None
        array_pattern_radius = None
        array_pattern_mode = None
        array_pattern_sketch = None
        array_pattern_n = None
        array_pattern_type = None
        array_pattern_dx = None
        array_pattern_dy = None
        array_pattern_nx = None
        array_pattern_ny = None
        min_extent = None
        point = (0, 0)
        sketch: Sketch | None = None

        if do_array_pattern:
            logger.info("Array pattern enabled")
            array_pattern_sketch = self.generate_one_sketch(
                self.array_pattern_sketch_min_n_commands,
                self.array_pattern_sketch_max_n_commands,
                zero_center=True,
            )
            array_pattern_n = np.random.randint(2, 40)
            array_pattern_start_angle = np.random.randint(0, 360)
            array_pattern_span = (
                360 if np.random.random() < 0.2 else np.random.randint(0, 360)
            )

            array_pattern_type = (
                "parray" if np.random.random() < self.parray_probability else "rarray"
            )
            array_pattern_mode = (
                "s"
                if np.random.uniform() < self.array_pattern_cut_probability
                or array_pattern_type == "rarray"
                else "a"
            )
            logger.info(
                f"Array pattern: type={array_pattern_type}, n={array_pattern_n}, mode={array_pattern_mode}, start_angle={array_pattern_start_angle}, span={array_pattern_span}"
            )

            if array_pattern_type == "parray":
                sketch = self.generate_one_sketch(
                    1, 1 + self.max_n_commands, only_cuts=True, zero_center=zero_center
                )
                point, min_extent, max_extent = get_point_on_sketch_and_radius_range(
                    sketch
                )
                if array_pattern_mode == "s":

                    array_pattern_radius = np.random.uniform(
                        (
                            min_extent
                            if min_extent > 0.5 * max_extent
                            else 0.5 * max_extent
                        ),
                        max_extent * 0.95,
                    )
                    k = array_pattern_span / 360
                    possible_tseconds = (
                        2
                        * array_pattern_radius
                        * np.sin(np.pi * k / np.arange(2, array_pattern_n + 1))
                    )
                    # tmp = possible_tseconds[
                    #     possible_tseconds > self.array_pattern_sketch_min_rel_scale
                    # ]
                    tmp = possible_tseconds
                    # creating more space so it is not narrowly stacked
                    tsecond = (
                        tmp[-2]
                        if len(tmp) > 2
                        else tmp[-1] if len(tmp) > 1 else tmp[-1]
                    )
                    array_pattern_n = len(tmp)

                    t = min(
                        1 - array_pattern_radius / max_extent,
                        tsecond,
                    )
                    array_pattern_sketch_rel_scale = tsecond
                    # array_pattern_sketch_rel_scale = np.random.uniform(
                    #     self.array_pattern_sketch_min_rel_scale, t
                    # )
                else:
                    t = np.random.uniform(0.1, 0.7)
                    array_pattern_radius = np.random.uniform(
                        max_extent * (1 - 0.5 * t), max_extent * (1 + 0.5 * t)
                    )
                    array_pattern_sketch_rel_scale = t

            elif array_pattern_type == "rarray":
                xmin, ymin, _, xmax, ymax, _ = shape_to_bbox(
                    array_pattern_sketch.to_shape()
                )
                bbox_extents = [xmax - xmin, ymax - ymin]

                tmp = self.rotation_probability
                self.rotation_probability = 0
                sketch = self.generate_one_sketch(
                    1,
                    1 + self.max_n_commands,
                    only_cuts=True,
                    zero_center=zero_center,  # 1
                )  # self.min_n_commands, self.max_n_commands
                point, min_extent, max_extent = get_point_on_sketch_and_radius_range(
                    sketch
                )
                self.rotation_probability = tmp

                rect = (
                    sketch.wire_to_rectangle(sketch.wires[0])
                    if sketch.wires[0]["type"] == "polygon"
                    else None
                )
                if len(sketch.wires) == 1 and rect is not None:
                    x, y, w, h = rect
                    mi, ma = min(
                        w - 2 * abs(point[0] - x), h - 2 * abs(point[1] - y)
                    ), max(w - 2 * (point[0] - x), h - 2 * abs(point[1] - y))
                    n_mi = np.random.randint(1, 5)
                    n_ma = np.random.randint(2, 10)
                    dmi = mi / (n_mi)
                    dma = ma / (n_ma)

                    if mi == h - 2 * abs(point[1] - y):
                        array_pattern_dx = np.random.uniform(0.8 * dma, dma)
                        array_pattern_dy = np.random.uniform(0.8 * dmi, dmi)
                        array_pattern_nx = n_ma
                        array_pattern_ny = n_mi
                    else:
                        array_pattern_dx = np.random.uniform(0.8 * dmi, dmi)
                        array_pattern_dy = np.random.uniform(0.8 * dma, dma)
                        array_pattern_nx = n_mi
                        array_pattern_ny = n_ma

                    alpha_x = 0.8 * array_pattern_dx / bbox_extents[0]
                    alpha_y = 0.8 * array_pattern_dy / bbox_extents[1]
                else:
                    array_pattern_radius = max_extent
                    mi = ma = array_pattern_radius * 1.5
                    n_mi = np.random.randint(1, 5)
                    n_ma = np.random.randint(2, 10)
                    dmi = mi / (n_mi)
                    dma = ma / (n_ma)
                    array_pattern_dx = np.random.uniform(0.8 * dma, dma)
                    array_pattern_dy = np.random.uniform(0.8 * dmi, dmi)
                    array_pattern_nx = n_ma
                    array_pattern_ny = n_mi
                    alpha_x = 0.8 * array_pattern_dx / bbox_extents[0]
                    alpha_y = 0.8 * array_pattern_dy / bbox_extents[1]

                array_pattern_sketch_rel_scale = min(alpha_x, alpha_y)

            array_pattern_sketch.transform([0, 0], array_pattern_sketch_rel_scale)  # type: ignore

            # TODO maybe remove this whole part during sketch disentanglement
            # if do_hole:
            #     if do_outer_hole:
            #         assert (
            #             array_pattern_radius is not None and min_extent is not None
            #         ), "array_pattern_radius and min_extent are required"
            #         outer_hole_radius = np.random.uniform(
            #             array_pattern_radius, 0.95 * min_extent
            #         )
            #     inner_holes_radii = get_inner_holes_radii(
            #         array_pattern_radius, n_inner_holes
            #     )

        else:
            sketch = self.generate_one_sketch(
                self.min_n_commands, self.max_n_commands, zero_center=zero_center
            )

        assert sketch is not None
        sketch.array_pattern_sketch = array_pattern_sketch
        sketch.array_pattern_n = array_pattern_n
        sketch.array_pattern_start_angle = array_pattern_start_angle
        sketch.array_pattern_span = array_pattern_span
        sketch.array_pattern_radius = array_pattern_radius
        sketch.array_pattern_dx = array_pattern_dx
        sketch.array_pattern_dy = array_pattern_dy
        sketch.array_pattern_nx = array_pattern_nx
        sketch.array_pattern_ny = array_pattern_ny
        sketch.array_pattern_type = array_pattern_type
        sketch.array_pattern_mode = array_pattern_mode
        sketch.point = point[:2]
        self._maybe_make_spline_profile(sketch)
        self._maybe_add_corner_fillet(sketch)
        self._maybe_add_corner_chamfer(sketch)

        return sketch

    def _maybe_add_corner_fillet(self, sketch: "Sketch") -> None:
        """
        Round the outer profile's corners, sampled as a fraction of that
        profile's own corner budget so the radius is always feasible.

        Sampling relatively (not absolutely) is what keeps this valid across
        the whole size range: the probe found the r/rmax cliff at 1.0 is
        absolute and scale-invariant, so any absolute radius range would fail
        on small profiles and be invisible on large ones.
        """
        if np.random.random() >= self.corner_fillet_probability:
            return
        if not sketch.wires or not sketch.wires[0].get("outer", False):
            return
        if not Sketch.wire_is_all_straight(sketch.wires[0]):
            return
        # `.vertices()` would also round a second face's corners
        if sum(1 for w in sketch.wires if w.get("outer", False)) != 1:
            return

        rmax = Sketch.max_corner_fillet(sketch.wires[0])
        if rmax <= 0:
            return
        budget = 0.9 * rmax
        radius = budget * np.random.uniform(
            self.corner_fillet_min_rel, self.corner_fillet_max_rel
        )
        if radius <= 0:
            return
        sketch.corner_fillet = float(radius)
        if not sketch.corner_fillet_is_valid():
            sketch.corner_fillet = None

    def _maybe_make_spline_profile(self, sketch: "Sketch") -> None:
        """
        Replace a straight-edged outer profile with a smooth periodic spline
        through the same points.

        Motivation: the SFT model, given a profile it cannot express, degenerates
        into tracing the outline point-by-point -- truncated steps carry a median
        356 `.segment()` calls / 6523 chars against 356 chars for accepted steps,
        and `unterminated string literal` is the top cause of zero-output parts
        (41.8%).  The corpus contains no spline at all (0 of 4000 samples) and
        tops out at 80 segments, so there is nothing to learn a compact curve
        from.  One `.spline([...],[],True)` expresses in a few control points
        what would otherwise need hundreds of segments.

        Reusing the already-sampled polygon points keeps the shape sane; the
        conversion is reverted if the resulting face does not build.
        """
        if np.random.random() >= self.spline_profile_probability:
            return
        if not sketch.wires or not sketch.wires[0].get("outer", False):
            return
        wire = sketch.wires[0]
        if not Sketch.wire_is_all_straight(wire):
            return
        pts = wire.get("vertices") or []
        if len(pts) < 4:  # a spline through <4 points is not meaningfully curved
            return

        original = sketch.wires[0]
        sketch.wires[0] = {
            "type": "spline",
            "outer": True,
            "points": Sketch.canonical_spline_points(pts),
        }
        try:
            shape = sketch.to_shape()
            if shape is None or shape_to_area(shape) <= 0:
                raise ValueError("degenerate spline face")
        except Exception:  # noqa: BLE001 - self-intersecting spline, keep polygon
            sketch.wires[0] = original

    def _maybe_add_corner_chamfer(self, sketch: "Sketch") -> None:
        """Bevel the outer profile's corners; skipped if it already has a fillet."""
        if sketch.corner_fillet:
            return
        if np.random.random() >= self.corner_chamfer_probability:
            return
        if not sketch.wires or not sketch.wires[0].get("outer", False):
            return
        if not Sketch.wire_is_all_straight(sketch.wires[0]):
            return
        if sum(1 for w in sketch.wires if w.get("outer", False)) != 1:
            return
        cmax = Sketch.max_corner_chamfer(sketch.wires[0])
        if cmax <= 0:
            return
        sketch.corner_chamfer = float(
            cmax * np.random.uniform(
                self.corner_fillet_min_rel, self.corner_fillet_max_rel
            )
        )
        if not sketch.corner_chamfer_is_valid():
            sketch.corner_chamfer = None

    @staticmethod
    def from_dict(entity: dict) -> "SketchFactory":
        return SketchFactory(
            min_n_commands=entity["min_n_commands"],
            max_n_commands=entity["max_n_commands"],
            n_outer_probabilities=entity["n_outer_probabilities"],
            rotation_probability=entity["rotation_probability"],
            array_pattern_probability=entity.get("array_pattern_probability", 0.0),
            array_pattern_sketch_min_n_commands=entity.get(
                "array_pattern_sketch_min_n_commands", 1
            ),
            array_pattern_sketch_max_n_commands=entity.get(
                "array_pattern_sketch_max_n_commands", 1
            ),
            array_pattern_sketch_min_rel_scale=entity.get(
                "array_pattern_sketch_min_rel_scale", 0.01
            ),
            array_pattern_cut_probability=entity.get(
                "array_pattern_cut_probability", 1
            ),
            parray_probability=entity.get("parray_probability", 0.5),
            corner_fillet_probability=entity.get("corner_fillet_probability", 0.0),
            corner_chamfer_probability=entity.get("corner_chamfer_probability", 0.0),
            spline_profile_probability=entity.get("spline_profile_probability", 0.0),
            corner_fillet_min_rel=entity.get("corner_fillet_min_rel", 0.10),
            corner_fillet_max_rel=entity.get("corner_fillet_max_rel", 0.90),
            from_sketchgraph=entity.get("from_sketchgraph", False),
            from_sketchgraph_probability=entity.get(
                "from_sketchgraph_probability",
                None,
            ),
        )

    def to_dict(self) -> dict:
        return {
            "type": "SketchFactory",
            "min_n_commands": self.min_n_commands,
            "max_n_commands": self.max_n_commands,
            "n_outer_probabilities": self.n_outer_probabilities,
            "rotation_probability": self.rotation_probability,
            "array_pattern_probability": self.array_pattern_probability,
            "array_pattern_sketch_min_n_commands": self.array_pattern_sketch_min_n_commands,
            "array_pattern_sketch_max_n_commands": self.array_pattern_sketch_max_n_commands,
            "array_pattern_sketch_min_rel_scale": self.array_pattern_sketch_min_rel_scale,
            "array_pattern_cut_probability": self.array_pattern_cut_probability,
            "parray_probability": self.parray_probability,
            "corner_fillet_probability": self.corner_fillet_probability,
            "corner_chamfer_probability": self.corner_chamfer_probability,
            "spline_profile_probability": self.spline_profile_probability,
            "corner_fillet_min_rel": self.corner_fillet_min_rel,
            "corner_fillet_max_rel": self.corner_fillet_max_rel,
            "from_sketchgraph": self.from_sketchgraph,
            "from_sketchgraph_probability": self.from_sketchgraph_probability,
        }


factories.register("sketch", SketchFactory)
