"""Shared B-rep interfaces and configurable design limits for constructive mode."""

from dataclasses import dataclass,asdict
import math
import cadquery as cq
import numpy as np
from OCP.BRepIntCurveSurface import BRepIntCurveSurface_Inter
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.gp import gp_Lin,gp_Pnt,gp_Dir

from .assembly_geometry import GeometryRejected


@dataclass(frozen=True)
class ConstructiveSettings:
    max_shaft_length: float=50.
    min_screw_engagement: float=10.
    min_feature_size: float=.1
    service_overlap: float=.0005
    max_designs_per_pair: int=72
    max_options_per_pair: int=12
    max_assembly_states: int=128

    def validate(self):
        for name,value in asdict(self).items():
            if not math.isfinite(value) or value<=0:raise ValueError(name+' must be finite and positive')
        if self.min_screw_engagement>=self.max_shaft_length:
            raise ValueError('Screw engagement must be shorter than the maximum shaft')


def general_contact(first,second):
    faces=[]
    def bounds(face):
        box=Bnd_Box();BRepBndLib.AddOptimal_s(face.wrapped,box,False,False)
        return box.Get()
    left=[(f,bounds(f)) for f in first.Faces()];right=[(f,bounds(f)) for f in second.Faces()]
    for a,ab in left:
        for b,bb in right:
            if any(ab[i]>bb[i+3]+1e-6 or bb[i]>ab[i+3]+1e-6 for i in range(3)):continue
            if a.geomType()!=b.geomType():continue
            if a.distance(b)>1e-6:continue
            if a.geomType()=='PLANE' and a.normalAt().dot(b.normalAt())>-.99999:continue
            try:
                common=a.intersect(b)
                for face in common.Faces():
                    if face.Area()>1e-7:
                        if face.normalAt().dot(a.normalAt())<0:face=cq.Face(face.wrapped.Reversed())
                        faces.append(face)
            except (ValueError,RuntimeError):continue
    return cq.Compound.makeCompound(faces)


def axis_intervals(shape,point,direction):
    point=np.asarray(point,float);direction=np.asarray(direction,float);direction/=np.linalg.norm(direction)
    ray=BRepIntCurveSurface_Inter();ray.Init(shape.wrapped,gp_Lin(gp_Pnt(*point),gp_Dir(*direction)),1e-7)
    hits=[]
    while ray.More():hits.append(float(ray.W()));ray.Next()
    unique=[]
    for value in sorted(hits):
        if not unique or value-unique[-1]>1e-7:unique.append(value)
    result=[]
    for low,high in zip(unique,unique[1:]):
        if shape.isInside(cq.Vector(*(point+direction*(low+high)/2)),1e-7):result.append((low,high))
    return result


def positive_depth(shape,point,direction):
    return next((hi for lo,hi in axis_intervals(shape,point,direction) if lo<=1e-6 and hi>1e-6),0.)


def box_bounds(shape,margin):
    b=shape.BoundingBox()
    return [b.xmin-margin,b.ymin-margin,b.zmin-margin,b.xmax+margin,b.ymax+margin,b.zmax+margin]


def face_chord(face,center,axis):
    """Length of the actual connected trimmed-face chord through center."""
    b=face.BoundingBox();extent=b.DiagonalLength+1
    point=np.array([center[0],center[1],0.]);direction=np.eye(3)[axis]
    edge=cq.Edge.makeLine(cq.Vector(*(point-direction*extent)),cq.Vector(*(point+direction*extent)))
    common=face.intersect(edge);vertex=cq.Vertex.makeVertex(*point)
    return max((e.Length() for e in common.Edges() if e.distance(vertex)<1e-7),default=0.)
