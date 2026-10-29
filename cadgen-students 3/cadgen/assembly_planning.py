"""Whole-construction validation and bounded reverse-disassembly search."""

from itertools import combinations
import cadquery as cq
import numpy as np

from .assembly_geometry import GeometryRejected, difference_volume, require_solid, sampled_path, contact_patch
from .assembly_validation import overlap_volume


def union(shapes):
    shapes=[s for s in shapes if s.Solids()]
    if not shapes:return cq.Compound.makeCompound([])
    result=shapes[0]
    for shape in shapes[1:]:result=result.fuse(shape)
    return result


def assembly_graph(raw,joints,geometry,contact_function=None):
    contact_function=contact_function or contact_patch
    contacts=[]
    for a,b in combinations(raw,2):
        patch=contact_function(raw[a],raw[b])
        if patch.Area()<=1e-6 or not patch.Faces():continue
        face=max(patch.Faces(),key=lambda f:f.Area())
        contacts.append(dict(components=[a,b],area=patch.Area(),position=list(face.Center().toTuple()),
                             normal=list(face.normalAt().toTuple()),
                             selected_joint=next((j.id for j in joints if set(j.owners)=={a,b}),None)))
    reached={next(iter(raw))}
    while True:
        previous=len(reached)
        for joint in joints:
            if reached.intersection(joint.owners):reached.update(joint.owners)
        if len(reached)==previous:break
    if len(reached)!=len(raw):raise GeometryRejected("Selected joint graph is disconnected")
    for joint in joints:
        if not any(set(c["components"])==set(joint.owners) for c in contacts):
            raise GeometryRejected("A joint joins components without a real B-rep interface")
    return dict(vertices=list(raw),contacts=contacts,selected_edges=[j.metadata() for j in joints],connected=True)


def find_sequence(parts,raw,joints,geometry,max_states):
    main=set(raw)
    hardware={name:j for j in joints for name,_ in j.hardware}
    visited=set()
    attempts=[]
    limited=False

    def withdrawal(name,remaining):
        if name in hardware:
            joint=hardware[name]
            if "_bolt_" in name and any(n in remaining and "_nut_" in n for n,_ in joint.hardware):
                return []
            custom=joint.parameters.get("hardware_directions_world",{}).get(name)
            if custom is not None:return [np.asarray(d,float) for d in custom]
            return [joint.axis if "_bolt_" in name or "_screw_" in name else -joint.axis]
        if any(name in j.owners and any(n in remaining for n,_ in j.hardware) for j in joints):
            return []
        constraints=[]
        for j in joints:
            if name not in j.owners:continue
            other=j.owners[1-j.owners.index(name)]
            if other not in remaining:continue
            sign=1 if name==j.owners[0] else -1
            constraints.append([sign*v for v in j.directions])
        if not constraints:return list(np.eye(3))+list(-np.eye(3))
        return [v for v in constraints[0] if all(
            any(np.dot(v,w)>0.99999 for w in allowed) for allowed in constraints[1:])]

    def solve(remaining):
        nonlocal limited
        if len(remaining)==1:
            last=next(iter(remaining))
            return [] if last in main else None
        if remaining in visited:return None
        if len(visited)>=max_states:
            limited=True;return None
        visited.add(remaining)
        ordered=sorted(remaining,key=lambda n:(n in main,sum(n in j.owners and all(o in remaining for o in j.owners) for j in joints),n))
        for moving in ordered:
            directions=withdrawal(moving,remaining)
            if not directions:continue
            fixed=sorted(remaining-{moving})
            path=sampled_path(parts[moving],[parts[n] for n in fixed],directions,geometry)
            attempts.append(dict(moving=moving,stationary=fixed,status=path["status"]))
            if path["status"]!="sampled_clear":continue
            tail=solve(remaining-{moving})
            if tail is not None:
                return [dict(component=moving,stationary_components=fixed,path=path)]+tail
        return None

    disassembly=solve(frozenset(parts))
    if disassembly is None:
        raise GeometryRejected("technical_limit_reached: assembly sequence states" if limited else
                               "No collision-sampled complete assembly sequence")
    removed={s["component"] for s in disassembly}
    base=next(n for n in parts if n not in removed)
    sequence=[dict(step=0,component=base,action="place_base",stationary_components=[],coordinate_frame="source_world")]
    installed=[base]
    for entry in reversed(disassembly):
        path=entry["path"]
        direction=np.array(path["withdrawal_direction_in_cut_frame"])
        sequence.append(dict(step=len(sequence),component=entry["component"],action="linear_insertion",
            coordinate_frame="source_world",
            stationary_components=list(installed),start_translation=(direction*path["travel"]).tolist(),
            final_translation=[0,0,0],insertion_direction=(-direction).tolist(),
            checked_positions=path["checked_positions"],distances=path["distances"],
            continuous_path_proven=False))
        installed.append(entry["component"])
    return sequence,dict(states_explored=len(visited),state_limit=max_states,trials=attempts,
                         continuous_path_proven=False,technical_limit_reached=limited)


def validate_partition(original,raw,parts,joints,geometry,max_states):
    for name,shape in list(raw.items())+list(parts.items()):require_solid(shape,name)
    raw_overlap={f"{a}/{b}":overlap_volume(raw[a],raw[b]) for a,b in combinations(raw,2)}
    if any(v>geometry.volume_tolerance for v in raw_overlap.values()):raise GeometryRejected("Raw partition overlaps")
    error=difference_volume(original,union(raw.values()))
    if error>geometry.volume_tolerance:raise GeometryRejected("Raw partition fails source reconstruction")
    overlaps={f"{a}/{b}":overlap_volume(parts[a],parts[b]) for a,b in combinations(parts,2)}
    if any(v>geometry.volume_tolerance for v in overlaps.values()):raise GeometryRejected("Final components collide")
    main=union(parts[n] for n in raw)
    # Main geometry is compared independently of external hardware.
    voids=[]
    for joint in joints:
        removed=union(joint.removals)
        added=union(joint.additions)
        voids.append(removed.cut(added) if added.Solids() else removed)
    expected=union(voids) if voids else original.cut(original)
    actual=original.cut(main)
    if main.cut(original).Volume()>geometry.volume_tolerance or difference_volume(expected,actual)>geometry.volume_tolerance:
        raise GeometryRejected("Main geometry changed outside declared joint voids")
    sequence,planning=find_sequence(parts,raw,joints,geometry,max_states)
    return dict(raw_reconstruction_error_volume=error,raw_intersection_volumes=raw_overlap,
                final_intersection_volumes=overlaps,main_geometry_preserved=True,
                allowed_removed_volume=expected.Volume(),actual_removed_volume=actual.Volume(),
                main_added_volume=main.cut(original).Volume(),assembly_sequence_checked=True,
                planning=planning,continuous_path_proven=False,threaded=False,
                mechanical_retention_checked=False),sequence
