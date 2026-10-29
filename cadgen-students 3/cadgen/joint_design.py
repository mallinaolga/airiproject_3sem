"""Geometry-ranked joints on actual cut interfaces; shared legacy builders."""

from dataclasses import dataclass, replace
from itertools import combinations
import random

import cadquery as cq
import numpy as np

from .assembly_geometry import (Connection, GeometryRejected, Split, build_bolted,
    build_groove, require_solid, validate_connection, contact_patch)
from .assembly_validation import overlap_volume, transform_part


@dataclass
class Joint:
    id: str
    owners: tuple  # upper/donor, lower/receiver; updated when a child is split
    additions: tuple
    removals: tuple
    hardware: list
    zone: cq.Shape
    parameters: dict
    directions: tuple
    axis: np.ndarray
    score: float
    selection: dict

    def metadata(self):
        b = self.zone.BoundingBox()
        return dict(id=self.id, components=list(self.owners), parameters=self.parameters,
                    score=self.score, selection=self.selection,
                    protected_zone_bounds=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax],
                    possible_withdrawal_directions=[v.tolist() for v in self.directions],
                    hardware=[name for name, _ in self.hardware])


def combine(shapes):
    shapes = [s for s in shapes if s.Solids()]
    if not shapes:
        return cq.Compound.makeCompound([])
    result = shapes[0]
    for s in shapes[1:]:
        result = result.fuse(s)
    return result


def orient_interface(split):
    patch = contact_patch(split.lower,split.upper)
    if patch.BoundingBox().xlen <= patch.BoundingBox().ylen:
        return split, patch
    rz = np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]])
    convert = lambda s: transform_part(s, rz.T, np.zeros(3))
    updated = Split(convert(split.original), convert(split.lower), convert(split.upper),
                    split.rotation@rz, split.origin, split.checks)
    return updated, contact_patch(updated.lower,updated.upper)


def interface_centers(patch):
    centers = []
    for f in sorted(patch.Faces(), key=lambda face: face.Area(), reverse=True):
        p = f.Center()
        b = f.BoundingBox()
        centers.extend([(p.x,p.y),
                        (p.x-b.xlen*.23,p.y), (p.x+b.xlen*.23,p.y),
                        (p.x,p.y-b.ylen*.28), (p.x,p.y+b.ylen*.28),
                        (p.x-b.xlen*.36,p.y), (p.x+b.xlen*.36,p.y),
                        (p.x-b.xlen*.23,p.y-b.ylen*.23),
                        (p.x+b.xlen*.23,p.y+b.ylen*.23)])
    return list(dict.fromkeys(centers))


def connection_zone(split, result, margin):
    if result.parameters.get("feature_zones_local"):
        boxes=[cq.Solid.makeBox(b[3]-b[0],b[4]-b[1],b[5]-b[2],cq.Vector(*b[:3]))
               for b in result.parameters["feature_zones_local"]]
        return split.world(cq.Compound.makeCompound(boxes))
    first, second = [s for _, s in result.components[:2]]
    altered = [first.cut(split.upper), split.upper.cut(first), second.cut(split.lower), split.lower.cut(second)]
    altered += [s for _, s in result.components[2:]]
    b = cq.Compound.makeCompound([s for s in altered if s.Solids()]).BoundingBox()
    box = cq.Solid.makeBox(b.xlen+2*margin, b.ylen+2*margin, b.zlen+2*margin,
                          cq.Vector(b.xmin-margin,b.ymin-margin,b.zmin-margin))
    return split.world(box)


def make_joint(split, result, owners, name, score, selection, geometry):
    validate_connection(split, result, geometry)
    upper, lower = [s for _, s in result.components[:2]]
    additions = tuple(split.world(a.cut(b)) for a,b in ((upper,split.upper),(lower,split.lower)))
    removals = tuple(split.world(a.cut(b)) for a,b in ((split.upper,upper),(split.lower,lower)))
    hardware = [(name+"_"+n,split.world(s)) for n,s in result.components[2:]]
    dirs = tuple(split.rotation@np.asarray(v,float) for v in result.paths[0][2])
    params = dict(result.parameters, cut_to_world_rotation=split.rotation.tolist(),
                  cut_origin=split.origin.tolist())
    zone=connection_zone(split,result,result.parameters.get("local_material_margin",geometry.min_wall))
    local_zone=transform_part(zone,split.rotation.T,-split.rotation.T@split.origin)
    b=local_zone.BoundingBox();body=split.original.BoundingBox()
    future_levels=set(round(f.Center().z,5) for f in split.original.Faces()
        if f.geomType()=="PLANE" and abs(f.normalAt().z)>.99999
        and body.zmin+geometry.min_wall<f.Center().z<body.zmax-geometry.min_wall
        and abs(f.Center().z)>geometry.min_wall)
    crossings=sum(b.zmin<z<b.zmax for z in future_levels)
    return Joint(name, owners, additions, removals, hardware,zone,params,dirs,
                 split.rotation[:,2],score-2.5*crossings,
                 dict(selection,future_parallel_transitions_protected=crossings))


def bolt_group(split, centers, seed, geometry, desired, excluded=()):
    accepted, failures = [], []
    for index, center in enumerate(centers):
        if len(accepted) >= desired:
            break
        if any(np.linalg.norm(np.array(center)-np.array(c)) < 24 for c,_ in accepted):
            continue
        try:
            result = build_bolted(split,random.Random(f"bolts:{seed}:{index}"),geometry,centers=[center])
            zone=connection_zone(split,result,geometry.min_wall)
            if any(overlap_volume(zone,old)>geometry.volume_tolerance for old in excluded):
                raise GeometryRejected("bolt position conflicts with another protected joint")
            accepted.append((center,result))
        except Exception as error:
            failures.append(str(error))
    if not accepted:
        raise GeometryRejected("No accessible bolt column: "+str(failures[-1:]))
    removed = combine(r.removed for _,r in accepted)
    upper = require_solid(split.upper.cut(removed).clean(),"multi-bolt upper")
    lower = require_solid(split.lower.cut(removed).clean(),"multi-bolt lower")
    components=[("part_1",upper),("part_2",lower)]
    paths=[("part_1",["part_2"],[(0,0,1)])]
    specs=[]
    for index,(_,result) in enumerate(accepted,1):
        for n,s in result.components[2:]:
            components.append((n.replace("_1",f"_{index}"),s))
        paths.extend([(f"bolt_{index}",["part_1","part_2"],[(0,0,1)]),
                      (f"nut_{index}",["part_1","part_2",f"bolt_{index}"],[(0,0,-1)])])
        specs.append(result.parameters)
    return Connection(components,removed,dict(type="bolted",bolts=specs,bolt_count=len(specs),
        radial_clearance=geometry.clearance,diametral_clearance=2*geometry.clearance,
        requested_geometric_bolt_count=desired,feasible_columns=len(accepted),threaded=False),paths)


def propose_joints(split, owners, name, seed, geometry, connection="auto", profile="auto", excluded=(), *, adaptive=True):
    if adaptive and connection!="combined":
        from .adaptive_joints import propose_adaptive_joints
        return propose_adaptive_joints(split,owners,name,seed,geometry,connection,profile,excluded)
    return legacy_joints(split,owners,name,seed,geometry,connection,profile,excluded)


def legacy_joints(split, owners, name, seed, geometry, connection="auto", profile="auto", excluded=()):
    split, patch = orient_interface(split)
    b = patch.BoundingBox()
    area = patch.Area()
    aspect = b.ylen/max(b.xlen,1e-8)
    centers = interface_centers(patch)[:geometry.feature_attempts]
    curved = sum(f.Area() for f in split.original.Faces() if f.geomType() != "PLANE") / split.original.Area()
    if profile != "auto":
        profiles=[profile]
    elif aspect > 2.2:
        profiles=["dovetail","t","rectangular","trapezoid","v","round"]
    elif curved > .2:
        profiles=["round","rectangular","v","trapezoid","dovetail","t"]
    elif b.xlen < 22:
        profiles=["v","trapezoid","rectangular","round","dovetail","t"]
    else:
        profiles=["rectangular","trapezoid","round","v","dovetail","t"]
    footprint=dict(width=b.xlen*.32,length=b.ylen*.38,
                   depth=min(-split.lower.BoundingBox().zmin*.27,16))
    options, rejected = [], []
    groove = None
    groove_zone = None
    prefer_bolt = aspect < 1.6 and area > 700
    selection=dict(interface_area=area,interface_aspect=aspect,curved_area_fraction=curved,
                   profile_preference=profiles,reason="geometry rank plus actual material/path feasibility")

    def add(result, score):
        joint=make_joint(split,result,owners,name,score,selection,geometry)
        if any(overlap_volume(joint.zone,z)>geometry.volume_tolerance for z in excluded):
            raise GeometryRejected("placement conflicts with a previous protected joint zone")
        options.append(joint)
        return joint

    if connection in ("auto","groove","combined"):
        for preference,kind in enumerate(profiles):
            for index,center in enumerate(centers):
                try:
                    result=build_groove(split,random.Random(f"groove:{seed}:{kind}:{index}"),geometry,kind,
                                        centers=[center],footprint=footprint)
                    selected=add(result,5.5-preference*.25)
                    groove,groove_zone=result,selected.zone
                    break
                except Exception as error:
                    rejected.append(dict(type="groove",profile=kind,reason=str(error)))
            if groove:
                break
    if connection in ("auto","bolted","combined"):
        try:
            desired=max(1,int(b.ylen/30)) if area>700 else 1
            bolted=bolt_group(split,centers,seed,geometry,min(desired,len(centers)),excluded)
            add(bolted,7.0 if prefer_bolt else 4.8)
        except Exception as error:
            rejected.append(dict(type="bolted",reason=str(error)))
    if groove and connection in ("auto","combined") and groove.parameters["profile"]["kind"] in ("dovetail","t"):
        # A bolt is useful here as a conditional slide stop. It is NOT added
        # automatically to a normal-insertion groove.
        modified=replace(split,upper=groove.components[0][1],lower=groove.components[1][1])
        for center in centers:
            try:
                bolted=bolt_group(modified,[center],seed,geometry,1,[*excluded,groove_zone])
                bz=connection_zone(modified,bolted,geometry.min_wall)
                if overlap_volume(bz,groove_zone)>geometry.volume_tolerance:
                    raise GeometryRejected("bolt intersects groove protection envelope")
                paths=[groove.paths[0]]+bolted.paths[1:]
                combined=Connection(bolted.components,combine([groove.removed,bolted.removed]),
                    dict(type="combined",groove=groove.parameters,bolts=bolted.parameters["bolts"],
                         bolt_count=bolted.parameters["bolt_count"],threaded=False,
                         reason="longitudinal guide plus accessible conditional slide stop"),paths)
                add(combined,8.0)
                break
            except Exception as error:
                rejected.append(dict(type="combined",reason=str(error)))
    elif connection in ("auto","combined"):
        rejected.append(dict(type="combined",reason="No eligible longitudinal guide needing a conditional slide stop"))
    if connection != "auto":
        options=[o for o in options if o.parameters["type"]==connection]
    for option in options:
        option.selection=dict(option.selection,investigated_types=["groove","bolted","combined"],
                              rejected_designs=rejected,alternative_scores=[
                                  dict(type=o.parameters["type"],score=o.score) for o in options])
    if not options:
        raise GeometryRejected("No feasible joint design: "+str(rejected[-8:]))
    return sorted(options,key=lambda option:-option.score)


def materialize(raw, joints, geometry):
    parts=dict(raw)
    for joint in joints:
        for i,owner in enumerate(joint.owners):
            if owner not in parts:
                raise GeometryRejected("Joint endpoint is not a current component")
            if joint.removals[i].Solids():
                parts[owner]=parts[owner].cut(joint.removals[i])
            if joint.additions[i].Solids():
                parts[owner]=parts[owner].fuse(joint.additions[i])
            parts[owner]=require_solid(parts[owner].clean(),owner)
        for name,shape in joint.hardware:
            parts[name]=require_solid(shape,name)
    return parts
