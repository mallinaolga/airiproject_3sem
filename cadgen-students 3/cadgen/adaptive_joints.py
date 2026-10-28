"""Bounded, scale-aware feature search on trimmed B-rep contact faces.

Only joint construction changes material. The input partition is never recut.
All profiles come from generate_grooves; placement proposals are not certificates.
"""

from collections import Counter
from dataclasses import replace
import math
import random

import cadquery as cq
import numpy as np
from OCP.BRepIntCurveSurface import BRepIntCurveSurface_Inter
from OCP.gp import gp_Dir, gp_Lin, gp_Pnt

from generirovanie_pazov.generate_grooves import PROFILE_TYPES
from .assembly_geometry import (GeometryRejected, Split, build_groove, build_bolted,
                                contact_patch, frame)
from .assembly_validation import overlap_volume, transform_part

# OCC linear confusion is 1e-7 mm. This is a CAD resolution limit, not a
# manufacturing minimum. No claim of strength or printability is made.
CAD_RESOLUTION = 5e-6
MAX_DESIGNS = 384
MAX_OPTIONS = 12
GROOVE_DESIGNS = 300  # reserve attempts for the hardware fallback


class JointSearchRejected(GeometryRejected):
    def __init__(self, report):
        self.report = report
        super().__init__("No validated adaptive joint within bounded search: " +
                         str(report.get("rejection_counts", {})))


def adaptive_clearance(requested, feature_size):
    if not math.isfinite(requested) or not 0 <= requested < 1:
        raise ValueError("clearance must satisfy 0 <= clearance < 1 mm")
    if feature_size <= CAD_RESOLUTION:
        raise GeometryRejected("Feature is below reliable CAD resolution")
    # Requested clearance is a ceiling, including the explicit zero case.
    return min(requested, .04*feature_size)


def local_settings(geometry, size, shapes):
    tolerance = min(geometry.volume_tolerance, min(s.Volume() for s in shapes)*1e-7,
                    size**3*1e-5)
    return replace(geometry,clearance=adaptive_clearance(geometry.clearance,size),
                   volume_tolerance=max(1e-18,tolerance))


def material_depth(shape, center, direction):
    """Distance to the first material exit, not to a remote bounding-box face."""
    direction = np.asarray(direction,float)
    origin = np.asarray([center[0],center[1],0.])
    probe = origin+direction*CAD_RESOLUTION
    if not shape.isInside(cq.Vector(*probe),1e-7):
        return 0.0
    ray = BRepIntCurveSurface_Inter()
    ray.Init(shape.wrapped,gp_Lin(gp_Pnt(*origin),gp_Dir(*direction)),1e-7)
    distances=[]
    while ray.More():
        value=float(ray.W())
        if value>CAD_RESOLUTION:
            distances.append(value)
        ray.Next()
    return min(distances,default=0.)


def contact_centers(face, count=12):
    """Trimmed-face grid plus tessellation seeds, ranked by boundary clearance.

    Boundary includes every inner wire: a centroid in a hole is never accepted.
    Sampling is bounded and does not guarantee a global maximum inscribed area.
    """
    box=face.BoundingBox()
    boundary=cq.Compound.makeCompound(face.Wires())
    candidates=[face.Center().toTuple()[:2]]
    for nx,ny in ((9,9),(17,5),(5,17)):
        for i in range(1,nx):
            for j in range(1,ny):
                candidates.append((box.xmin+box.xlen*i/nx,box.ymin+box.ylen*j/ny))
    vertices,triangles=face.tessellate(max(CAD_RESOLUTION,box.DiagonalLength*.03))
    for triangle in triangles[:256]:
        p=sum((np.array(vertices[i].toTuple()) for i in triangle))/3
        candidates.append(tuple(p[:2]))
    valid=[]
    for center in dict.fromkeys(candidates):
        vertex=cq.Vertex.makeVertex(*center,0.)
        if face.distance(vertex)>1e-7:
            continue
        radius=boundary.distance(vertex)
        if radius>CAD_RESOLUTION:
            valid.append((center,radius))
    valid.sort(key=lambda item:-item[1])
    selected=[]
    for center,radius in valid:
        if any(np.linalg.norm(np.array(center)-np.array(old)) < .65*min(radius,r)
               for old,r in selected):
            continue
        selected.append((center,radius))
        if len(selected)>=count:
            break
    return selected


def configurations(split, owners):
    """Every planar patch, both transfer roles, and in-plane orientations."""
    patches=contact_patch(split.lower,split.upper)
    for face_index,face in enumerate(sorted(patches.Faces(),key=lambda f:-f.Area())):
        if face.Area()<=CAD_RESOLUTION**2:
            continue
        origin=np.asarray(face.Center().toTuple())
        normal=np.asarray(face.normalAt().toTuple())
        for reverse in (False,True):
            base=frame(-normal if reverse else normal)
            # Tangents of straight boundary edges supplement the frame axes.
            angles=[0.,math.pi/2]
            for edge in sorted(face.Edges(),key=lambda e:-e.Length()):
                if edge.geomType() != "LINE":
                    continue
                tangent=base.T@np.array(edge.tangentAt().toTuple())
                angle=math.atan2(tangent[1],tangent[0])
                if not any(abs(math.sin(angle-other))<1e-5 for other in angles):
                    angles.append(angle)
                if len(angles)>=4:
                    break
            for angle in angles:
                c,s=math.cos(angle),math.sin(angle)
                rotation=base@np.array([[c,-s,0.],[s,c,0.],[0.,0.,1.]])
                local=lambda shape:transform_part(shape,rotation.T,-rotation.T@origin)
                lower,upper=(split.upper,split.lower) if reverse else (split.lower,split.upper)
                candidate=Split(local(split.original),local(lower),local(upper),split.rotation@rotation,
                                split.origin+split.rotation@origin,split.checks)
                local_face=local(face)
                yield candidate,owners[::-1] if reverse else owners,local_face,dict(
                    patch=face_index,face_area=face.Area(),roles_reversed=reverse,
                    angle_radians=angle,normal_world=candidate.rotation[:,2].tolist())


def propose_adaptive_joints(split, owners, name, seed, geometry, connection="auto", profile="auto", excluded=()):
    from .joint_design import make_joint

    geometry.validate()
    if connection not in ("auto","groove","bolted","combined"):
        raise ValueError("Unknown connection type")
    if profile not in ("auto",*PROFILE_TYPES):
        raise ValueError("Unknown profile")
    report=dict(adaptive=True,design_limit=MAX_DESIGNS,groove_design_limit=GROOVE_DESIGNS,option_limit=MAX_OPTIONS,
                designs_tried=0,exhaustive=False,rejected_designs=[],rejection_counts={},
                evaluated_profiles=[],valid_designs=0,technical_limit_reached=False)
    failures=Counter();options=[]
    configs=[]
    for local,roles,face,description in configurations(split,owners):
        centers=contact_centers(face,max(4,geometry.feature_attempts*2))
        if not centers:
            failures["No interior contact samples above CAD resolution"]+=1
            continue
        placements=[]
        for center,radius in centers:
            lower_depth=material_depth(local.lower,center,(0,0,-1))
            upper_depth=material_depth(local.upper,center,(0,0,1))
            if min(lower_depth,upper_depth)<=CAD_RESOLUTION:
                continue
            placements.append((center,radius,lower_depth,upper_depth))
        configs.append((local,roles,description,placements))
    report["interface_configurations"]=len(configs)
    curved=any(f.geomType()!="PLANE" for f in split.original.Faces())
    preferences=(["round","rectangular","v","trapezoid","dovetail","t"] if curved else
                 ["rectangular","round","v","trapezoid","dovetail","t"])
    profiles=[profile] if profile!="auto" else preferences

    def record(error,design):
        reason=f"{type(error).__name__}: {error}"
        failures[reason]+=1
        # Keep precise parameters for every attempted design, up to the bound.
        report["rejected_designs"].append(dict(design,reason=reason))

    def accept(local,roles,result,selected_geometry,design):
        joint=make_joint(local,result,roles,name,10. if result.parameters["type"]=="groove" else 2.,
                         dict(design,reason="actual B-rep material, validated offset and sampled insertion"),
                         selected_geometry)
        if any(overlap_volume(joint.zone,z)>selected_geometry.volume_tolerance for z in excluded):
            raise GeometryRejected("Joint conflicts with an existing feature")
        options.append(joint)
        report["valid_designs"]+=1

    # Fair allocation across planes/roles/orientations. Each profile gets a
    # chance; smaller variants and alternative placements follow any failure.
    if connection in ("auto","groove","combined"):
        for local,roles,description,placements in configs:
            for kind in profiles:
                profile_start=report["designs_tried"]
                profile_quota=max(1,GROOVE_DESIGNS//max(1,len(configs))//len(profiles))
                if report["designs_tried"]>=GROOVE_DESIGNS:
                    break
                report["evaluated_profiles"].append(kind)
                found=False
                # Shrink features without shrinking the surrounding components.
                for center_index,(center,radius,depth,anchor_depth) in enumerate(placements):
                    for factor in (1.,.5,.2,.08):
                        if (report["designs_tried"]>=GROOVE_DESIGNS or
                                report["designs_tried"]-profile_start>=profile_quota):
                            break
                        width=radius*1.05*factor
                        length=radius*1.25*factor
                        feature_depth=min(depth*.35,radius*.6)*factor
                        size=min(width,feature_depth,length,anchor_depth*.5)
                        if size<=CAD_RESOLUTION:
                            continue
                        settings=local_settings(geometry,size,(local.lower,local.upper))
                        footprint=dict(width=width,length=length,depth=feature_depth,anchor_depth=anchor_depth*.4)
                        design=dict(description,profile=kind,center=list(center),sample=center_index,
                                    footprint=footprint,clearance=settings.clearance,scale_factor=factor,
                                    available_material_depths=[depth,anchor_depth])
                        report["designs_tried"]+=1
                        try:
                            result=build_groove(local,random.Random(f"adaptive:{seed}:{kind}"),settings,kind,
                                                centers=[center],footprint=footprint,adaptive=True)
                            accept(local,roles,result,settings,design)
                            found=True
                            break
                        except (ValueError,RuntimeError) as error:
                            record(error,design)
                    if found or report["designs_tried"]-profile_start>=profile_quota:
                        break
                # Keep all profiles represented when feasible. Full-assembly
                # selection balances directions below instead of keeping only
                # the first successful preferred profile.
    # In auto mode bolts are a fallback, never a higher-scoring substitute.
    if connection in ("bolted","combined") or (connection=="auto" and not options):
        for local,roles,description,placements in configs:
            for center,radius,depth,anchor_depth in placements:
                found=False
                for factor in (1.,.5,.2,.08):
                    if report["designs_tried"]>=MAX_DESIGNS:
                        break
                    diameter=min(radius*.7,min(depth,anchor_depth)*.8)*factor
                    if diameter<=CAD_RESOLUTION:
                        continue
                    settings=local_settings(geometry,diameter,(local.lower,local.upper))
                    design=dict(description,type="bolted",center=list(center),diameter=diameter,
                                clearance=settings.clearance)
                    report["designs_tried"]+=1
                    try:
                        result=build_bolted(local,random.Random(seed),settings,centers=[center],
                                            adaptive=True,diameter=diameter)
                        # Match the established one/multi-bolt export recipe.
                        bolt=result.parameters
                        result.parameters=dict(type="bolted",bolts=[bolt],bolt_count=1,
                            radial_clearance=settings.clearance,diametral_clearance=2*settings.clearance,
                            adaptive=True,local_material_margin=bolt["local_material_margin"],
                            volume_tolerance_used=settings.volume_tolerance,threaded=False)
                        accept(local,roles,result,settings,design)
                        found=True
                        break
                    except (ValueError,RuntimeError) as error:
                        record(error,design)
                if found:
                    break
    # Preserve distinct withdrawal directions before filling with profile
    # alternatives. Cap is explicit; this is not exhaustive joint enumeration.
    ordered=[];groups={}
    for option in options:
        key=tuple(round(v,5) for v in option.directions[0])
        groups.setdefault(key,[]).append(option)
    while groups and len(ordered)<MAX_OPTIONS:
        for key in list(groups):
            ordered.append(groups[key].pop(0))
            if not groups[key]:
                del groups[key]
            if len(ordered)>=MAX_OPTIONS:
                break
    report.update(rejection_counts=dict(failures),evaluated_profiles=list(dict.fromkeys(report["evaluated_profiles"])),
                  technical_limit_reached=report["designs_tried"]>=MAX_DESIGNS,
                  per_configuration_profile_budget=max(1,GROOVE_DESIGNS//max(1,len(configs))//len(profiles)),
                  placement_search_bounded=True,
                  returned_options=len(ordered),options_truncated=len(options)>len(ordered))
    if connection=="combined":
        # Combined means both features, never silently relabel a single groove.
        report["rejection_counts"]["Adaptive combined joint not implemented; request groove or bolted"]=1
        raise JointSearchRejected(report)
    if not ordered:
        raise JointSearchRejected(report)
    for option in ordered:
        option.selection["adaptive_search"]=report
    return ordered
