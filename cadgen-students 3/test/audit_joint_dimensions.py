"""Read-only dimensional audit of existing assemblies; no joint/model generation."""

import argparse
import json
import math
from pathlib import Path

import cadquery as cq
import numpy as np
from OCP.BRep import BRep_Tool
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.BRepIntCurveSurface import BRepIntCurveSurface_Inter
from OCP.gp import gp_Dir, gp_Lin, gp_Pnt

from cadgen.adaptive_joints import contact_centers, material_depth
from cadgen.assembly_geometry import contact_patch
from cadgen.assembly_validation import transform_part


def dimensions(shape):
    # Ignore cached visualization tessellation, which can underestimate a
    # thin curved contact face at the old STL meshing tolerance.
    box=Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped,box,False,False)
    lo_x,lo_y,lo_z,hi_x,hi_y,hi_z=box.Get()
    return [hi_x-lo_x,hi_y-lo_y,hi_z-lo_z]


def first_material_interval(shape,point,direction):
    """First material interval along a ray, classified between exact intersections.

    This is a local sample, never a minimum wall certificate. Intervals shorter
    than twenty model/linear tolerances are explicitly not certified.
    """
    point=np.asarray(point,float);direction=np.asarray(direction,float)
    direction/=np.linalg.norm(direction)
    tolerance=max([1e-7]+[BRep_Tool.Tolerance_s(v.wrapped) for v in shape.Vertices()])
    ray=BRepIntCurveSurface_Inter()
    ray.Init(shape.wrapped,gp_Lin(gp_Pnt(*point),gp_Dir(*direction)),1e-8)
    hits=[0.]
    while ray.More():
        value=float(ray.W())
        if value>1e-10:hits.append(value)
        ray.Next()
    hits.sort();unique=[]
    for value in hits:
        if not unique or value-unique[-1]>1e-9:unique.append(value)
    for start,end in zip(unique,unique[1:]):
        if end-start<=1e-9:continue
        middle=point+direction*((start+end)/2)
        if shape.isInside(cq.Vector(*middle),1e-8):
            length=end-start
            certified=length>=20*tolerance
            return dict(thickness_mm=length if certified else None,observed_interval_mm=[start,end],
                below_confidence_limit=not certified,model_linear_tolerance_mm=tolerance,
                reason="local B-rep ray interval" if certified else "interval below twenty model tolerances")
    return dict(thickness_mm=None,observed_interval_mm=None,below_confidence_limit=False,
                model_linear_tolerance_mm=tolerance,reason="no certified material interval on this ray")


def chord(face,center,axis):
    """Trimmed-face chord through the selected point, not a bounding-box claim."""
    b=face.BoundingBox();extent=b.DiagonalLength+1
    a=np.array([*center,0.],float);offset=np.array([1.,0.,0.]) if axis==0 else np.array([0.,1.,0.])
    edge=cq.Edge.makeLine(cq.Vector(*(a-offset*extent)),cq.Vector(*(a+offset*extent)))
    common=face.intersect(edge)
    vertex=cq.Vertex.makeVertex(*a)
    lengths=[e.Length() for e in common.Edges() if e.distance(vertex)<=1e-7]
    return max(lengths) if lengths else None


def load_shapes(folder,entries):
    return {c["name"]:transform_part(cq.importers.importStep(str(folder/c["step"])).val(),
                                     c["rotation_matrix"],c["translation"]) for c in entries}


def audit_model(folder):
    meta=json.loads((folder/"metadata.json").read_text())
    model_name=folder.parent.name if folder.name=="assembly" else folder.name
    raw=load_shapes(folder,meta["raw_components"])
    final=load_shapes(folder,meta["components"])
    inverse={v:k for k,v in meta["component_id_map"].items()}
    rows=[]
    for joint in meta["joints"]:
        p=joint["parameters"];selection=joint["selection"];profile=p["profile"]
        assert p["type"]=="groove"
        donor,receiver=joint["components"]
        rotation=np.array(p["cut_to_world_rotation"]);origin=np.array(p["cut_origin"])
        local=lambda shape:transform_part(shape,rotation.T,-rotation.T@origin)
        upper,lower=local(raw[donor]),local(raw[receiver])
        finished_upper,finished_lower=local(final[donor]),local(final[receiver])
        center=p["center_in_cut_frame"][:2];x,y=center
        patch=contact_patch(upper,lower)
        vertex=cq.Vertex.makeVertex(x,y,0.)
        faces=[f for f in patch.Faces() if abs(f.normalAt().z)>.999999
               and abs(f.Center().z)<1e-6 and f.distance(vertex)<=1e-7]
        if not faces:raise ValueError(f"No actual selected contact face: {model_name}/{joint['id']}")
        face=min(faces,key=lambda f:abs(f.Area()-selection["face_area"]))
        assert abs(face.Area()-selection["face_area"])<=max(1e-6,face.Area()*1e-6)
        radius=cq.Compound.makeCompound(face.Wires()).distance(vertex)
        w=profile["opening_width"];max_w=max(w,profile.get("bottom_width") or 0.)
        depth=profile["depth"];length=p["central_engagement_length"];gap=p["clearance"]
        before_receiver=material_depth(lower,center,(0,0,-1))
        before_donor=material_depth(upper,center,(0,0,1))
        samples=[]
        for position,r in contact_centers(face,16):
            rd=material_depth(lower,position,(0,0,-1));dd=material_depth(upper,position,(0,0,1))
            if min(rd,dd)>0:samples.append(dict(center=list(position),boundary_distance_mm=r,
                                               receiver_depth_mm=rd,donor_depth_mm=dd))
        floor_origin=[x,y,-depth/2]
        walls={
            "receiver_floor":first_material_interval(finished_lower,floor_origin,(0,0,-1)),
            "receiver_left":first_material_interval(finished_lower,floor_origin,(-1,0,0)),
            "receiver_right":first_material_interval(finished_lower,floor_origin,(1,0,0)),
            "donor_anchor":first_material_interval(finished_upper,[x,y,0.],(0,0,1))}
        for label,direction in (("receiver_end_minus",(0,-1,0)),("receiver_end_plus",(0,1,0))):
            walls[label]=(dict(thickness_mm=None,reason="intentional open sliding end")
                          if p["open_ends"]=="both" else first_material_interval(finished_lower,floor_origin,direction))
        chord_x,chord_y=chord(face,center,0),chord(face,center,1)
        rejected=[]
        search=selection["adaptive_search"]
        if "file" in search:search=json.loads((folder/search["file"]).read_text())
        for candidate in search.get("rejected_designs",[]):
            if all(candidate.get(key)==selection.get(key) for key in
                   ("patch","roles_reversed","angle_radians","profile","sample")):
                if np.linalg.norm(np.array(candidate.get("center",[1e9,1e9]))-np.array(center))<1e-8:
                    rejected.append(candidate)
        row=dict(model=model_name,joint_id=joint["id"],donor=donor,receiver=receiver,
            previous_decomposition_names=[inverse[donor],inverse[receiver]],
            donor_dimensions_xyz_mm=dimensions(final[donor]),receiver_dimensions_xyz_mm=dimensions(final[receiver]),
            donor_before_dimensions_xyz_mm=dimensions(raw[donor]),receiver_before_dimensions_xyz_mm=dimensions(raw[receiver]),
            profile=profile,profile_opening_width_mm=w,profile_max_width_mm=max_w,
            profile_depth_mm=depth,engagement_length_mm=length,tool_length_mm=p["tool_length"],
            # Exact nominal axis extents of a normal offset profile, before
            # clipping the cutter to the real receiver. Sliding length is a
            # central engagement length, not the full open cutter length.
            nominal_cavity_width_mm=max_w+2*gap,nominal_cavity_depth_mm=depth+gap,
            nominal_cavity_engagement_length_mm=length+2*gap,
            clearance_mm=gap,measured_profile_surface_gaps_mm=p["measured_profile_surface_gaps"],
            contact_face_dimensions_xy_mm=dimensions(face)[:2],contact_face_area_mm2=face.Area(),
            pair_contact_area_mm2=patch.Area(),pair_contact_faces=len(patch.Faces()),
            pair_contact_dimensions_xyz_world_mm=dimensions(contact_patch(raw[donor],raw[receiver])),
            center_in_cut_frame_mm=[x,y,0.],cut_to_world_rotation=p["cut_to_world_rotation"],cut_origin=p["cut_origin"],
            boundary_distance_at_center_mm=radius,face_chords_at_center_xy_mm=[chord_x,chord_y],
            receiver_depth_before_mm=before_receiver,donor_depth_before_mm=before_donor,
            recorded_material_depths_mm=selection["available_material_depths"],
            sampled_available_material=samples,wall_samples_after=walls,
            requested_envelope_margin_mm=p["local_material_margin"],
            global_minimum_wall_certified=False,
            ratios=dict(profile_width_over_contact_chord_x=max_w/chord_x if chord_x else None,
                engagement_length_over_contact_chord_y=length/chord_y if chord_y else None,
                profile_depth_over_receiver_material=depth/before_receiver if before_receiver else None,
                nominal_cavity_width_over_contact_chord_x=(max_w+2*gap)/chord_x if chord_x else None,
                nominal_cavity_length_over_contact_chord_y=(length+2*gap)/chord_y if chord_y else None,
                nominal_cavity_depth_over_receiver_material=(depth+gap)/before_receiver if before_receiver else None),
            selected_scale_factor=selection["scale_factor"],initial_footprint=selection["footprint"],
            initial_radius_inferred_mm=selection["footprint"]["width"]/(1.05*selection["scale_factor"]),
            matching_rejected_designs=rejected,selection_without_search={k:v for k,v in selection.items() if k!="adaptive_search"},
            assembly_sequence_verified=meta["checks"]["assembly_sequence_checked"],
            minimum_profile_dimension_mm=min(w,depth,length),
            below_001_mm=(w<.01 or depth<.01))
        # Persist the formula's cause, separate from a proof of optimal size.
        row["size_cause"]=("receiver_depth" if before_receiver*.35<=radius*.6*(1+1e-5)
                            else "contact_boundary_radius")
        row["minimum_nominal_cavity_dimension_mm"]=min(row["nominal_cavity_width_mm"],
            row["nominal_cavity_depth_mm"],row["nominal_cavity_engagement_length_mm"])
        row["nominal_full_cutter_length_mm"]=p["tool_length"]+2*gap
        row["sliding_receiver_middepth_span_mm"]=None
        if p["open_ends"]=="both":
            segments=[first_material_interval(lower,floor_origin,d) for d in ((0,1,0),(0,-1,0))]
            row["sliding_receiver_middepth_intervals"]=segments
            if all(seg["observed_interval_mm"] and seg["observed_interval_mm"][0]<1e-7 for seg in segments):
                row["sliding_receiver_middepth_span_mm"]=sum(seg["observed_interval_mm"][1] for seg in segments)
        rows.append(row)
        print(model_name,joint["id"],"SMALL" if row["below_001_mm"] else "ok",flush=True)
    return rows


def audit(source,output):
    source=Path(source).resolve();all_rows=[]
    for model in sorted(p for p in source.glob("model_*") if p.is_dir()):
        folder=model/"assembly" if (model/"assembly").is_dir() else model
        all_rows.extend(audit_model(folder))
    all_rows.sort(key=lambda r:r["minimum_nominal_cavity_dimension_mm"])
    assert len(all_rows)==76
    for row in all_rows:
        assert len(row["wall_samples_after"])==6
        for values in (row["donor_dimensions_xyz_mm"],row["receiver_dimensions_xyz_mm"],row["contact_face_dimensions_xy_mm"]):
            assert all(math.isfinite(v) and v>0 for v in values)
        assert math.isclose(row["receiver_depth_before_mm"],row["recorded_material_depths_mm"][0],rel_tol=1e-5,abs_tol=1e-7)
        assert math.isclose(row["donor_depth_before_mm"],row["recorded_material_depths_mm"][1],rel_tol=1e-5,abs_tol=1e-7)
    result=dict(schema_version=1,units="mm",source=str(source),joints_count=len(all_rows),
        small_joints_count=sum(r["below_001_mm"] for r in all_rows),
        geometry_generation_performed=False,algorithm_changed=False,joints=all_rows,
        wall_note="Local line samples only; no global minimum wall certified. Thin intervals below twenty model tolerances are not certified.")
    Path(output).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",default="generations/assemblies/adaptive_joints_final")
    parser.add_argument("--output",default="/tmp/airi_joint_dimensions.json")
    args=parser.parse_args()
    audit(args.source,args.output)
