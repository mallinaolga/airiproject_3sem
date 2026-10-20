import cadquery as cq


def _wp_circular_pattern(
    self: cq.Workplane,
    point: tuple[float, float, float],
    span: float,
    n: int,
    expr: str,
    combine: str = "a",
) -> cq.Workplane:
    from OCP.BRep import BRep_Tool
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.BRepTools import BRepTools
    from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
    from OCP.gp import gp_Pnt

    from ..selectors import PointOnFaceSelector

    face = self.faces(PointOnFaceSelector([point[0], point[1], point[2]])).val()

    umin, umax, _, _ = BRepTools.UVBounds_s(face.wrapped)

    gp_pnt = gp_Pnt(*point)
    geom_surf = BRep_Tool.Surface_s(face.wrapped)
    proj = GeomAPI_ProjectPointOnSurf(gp_pnt, geom_surf)
    u, v = proj.Parameters(1)
    surf_adapt = BRepAdaptor_Surface(face.wrapped)

    parameter_range = umax - umin
    total_parameter_range = parameter_range * span / 360

    range_for_one = (
        total_parameter_range / (n - 1) if span < 360 else total_parameter_range / n
    )

    final_parameters = []
    next_parameter = u
    for _ in range(n):
        next_parameter += range_for_one
        if next_parameter > umax:
            next_parameter -= umax
        final_parameters.append(next_parameter)

    points = [surf_adapt.Value(param, v) for param in final_parameters]
    points = [(p.X(), p.Y(), p.Z()) for p in points]

    return self.attach_at(points, expr, combine=combine)


setattr(cq.Workplane, "circular_pattern", _wp_circular_pattern)
