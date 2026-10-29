"""Operation-volume decomposition with local ownership of shared material.

History proposes logical elements. Every allocation is checked against B-rep;
no manufacturing/fastener feasibility participates in this stage.
"""

import ast
from dataclasses import dataclass,field
from itertools import combinations
from unittest.mock import patch

import cadquery as cq
import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Surface

from .assembly_geometry import GeometryRejected,difference_volume,frame,require_solid
from .assembly_validation import overlap_volume,transform_part
from .decomposition import Partition,validate_raw_partition,Budget
from .section_analysis import recognize,fill_bores,section,prism_from_section


@dataclass
class Element:
    id: str
    sweep: cq.Shape
    axis: np.ndarray
    history: dict=field(default_factory=dict)


def cylinder(shape):
    """Descriptor of a full cylindrical extrusion, not a round groove profile."""
    candidates=[]
    for f in shape.Faces():
        if f.geomType()!='CYLINDER':continue
        a=BRepAdaptor_Surface(f.wrapped)
        if a.LastUParameter()-a.FirstUParameter()<2*np.pi-1e-5:continue
        c=a.Cylinder();axis=np.array(c.Axis().Direction().Coord());origin=np.array(c.Location().Coord())
        radial=np.array(f.Center().toTuple())-origin
        # Face center of a full cylinder lies on its axis: normal sample is
        # evaluated on the actual surface instead.
        pt=a.Value((a.FirstUParameter()+a.LastUParameter())/2,(a.FirstVParameter()+a.LastVParameter())/2)
        p=np.array(pt.Coord());v=p-origin-axis*np.dot(p-origin,axis)
        if np.dot(f.normalAt(tuple(p)).toTuple(),v)<0:continue
        candidates.append(dict(radius=c.Radius(),axis=axis.tolist(),origin=origin.tolist()))
    return max(candidates,key=lambda c:c['radius']) if candidates else None


def history_elements(program,original,tolerance=1e-5):
    """Replay saved extrusion calls only; capture the actual operands of union.

    The original CADGen builder performs placement/overlap itself, unchanged.
    AST restricts the replay to literal extrusion arguments and the current r.
    No random factory or arbitrary original.py execution is involved.
    """
    from .extrude import extrude
    result=None;elements=[]
    nodes=[n for n in ast.parse(program).body if isinstance(n,ast.Assign)
           and any(isinstance(t,ast.Name) and t.id=='r' for t in n.targets)]
    for node in nodes:
        call=node.value
        if isinstance(call,ast.Constant) and call.value is None:continue
        if not isinstance(call,ast.Call) or not isinstance(call.func,ast.Name) or call.func.id!='extrude':
            raise GeometryRejected('History replay supports literal extrusion operations only')
        args=[result if isinstance(v,ast.Name) and v.id=='r' else ast.literal_eval(v) for v in call.args]
        kwargs={k.arg:ast.literal_eval(k.value) for k in call.keywords}
        captured=[];original_union=cq.Workplane.union
        def recording_union(workplane,body,*a,**kw):
            captured.append(body.val() if isinstance(body,cq.Workplane) else body)
            return original_union(workplane,body,*a,**kw)
        with patch.object(cq.Workplane,'union',recording_union):
            updated=extrude(*args,**kwargs)
        body=updated.val() if result is None else captured[-1]
        if not body.isValid() or not body.Solids():raise GeometryRejected('Invalid history sweep')
        axis={'XY':(0,0,1),'YZ':(1,0,0),'ZX':(0,1,0)}[args[2]]
        for subvolume,sweep in enumerate(body.Solids(),1):
            sweep=require_solid(sweep,'history extrusion component')
            elements.append(Element(f'h{len(elements)+1}',sweep,np.array(axis,float),
                dict(program_line=node.lineno,call=ast.get_source_segment(program,node),
                     operation_subvolume=subvolume,operation_solid_count=len(body.Solids()),
                     family='cylinder' if cylinder(sweep) else 'prism',
                     source_volume=sweep.Volume(),service_overlap_mm=.0005)))
        result=updated
    if result is None or difference_volume(original,result.val())>tolerance:
        raise GeometryRejected('History operands do not reproduce the provided original STEP')
    return elements


def combine(shapes):
    shapes=list(shapes)
    result=shapes[0]
    for s in shapes[1:]:result=result.fuse(s)
    return result.clean()


def constant_along(shape,axis):
    """External section along the construction direction; physical holes stay."""
    try:
        envelope,_,_=fill_bores(shape,Budget(1000))
        rotation=frame(axis);local=transform_part(envelope,rotation.T,np.zeros(3));b=local.BoundingBox()
        middle=(b.zmin+b.zmax)/2
        face=section(local,middle).translate((0,0,-middle))
        swept=prism_from_section(face,b.zmin,b.zlen)
        return difference_volume(local,swept)<=max(1e-5,envelope.Volume()*1e-8)
    except (ValueError,RuntimeError):
        # A failed analysis must never assert simplicity, or discard the
        # independently valid material partition.
        return False


def _valid(parts):
    return bool(parts) and all(s.isValid() and len(s.Solids())==1 and s.Volume()>1e-8 for s in parts.values())


def _local_overlap_cut(overlap,axis,fraction):
    rotation=frame(axis);local=transform_part(overlap,rotation.T,np.zeros(3));b=local.BoundingBox()
    level=b.zmin+b.zlen*fraction;pad=b.DiagonalLength+1
    cutter=cq.Solid.makeBox(b.xlen+2,b.ylen+2,b.zlen+2,
                           cq.Vector(b.xmin-1,b.ymin-1,level))
    upper=local.intersect(cutter)
    return transform_part(upper,rotation,np.zeros(3))


def decompose_constructive(original,elements,tolerance=1e-5):
    original=require_solid(original,'source');parts={};records=[];provenance={}
    for element in elements:
        sweep=element.sweep.intersect(original).clean()
        if not parts:
            parts[element.id]=require_solid(sweep,element.id);provenance[element.id]=[element]
            continue
        occupied=combine(parts.values());overlap=sweep.intersect(occupied)
        added=sweep.cut(occupied).clean()
        if added.Volume()<=tolerance:
            records.append(dict(operation=element.id,status='redundant_or_contained',added_volume=added.Volume()))
            continue
        # A larger coaxial cylinder placed midway along a shaft is a genuine
        # radius step, not a separate annular sleeve. Give its full interval
        # to the large cylinder and retain connected natural shaft segments.
        new_cylinder=cylinder(element.sweep)
        stepped=dict(parts);stepped_provenance=dict(provenance);split_steps=[];step_sweep=sweep
        for name,body in list(parts.items()):
            old_element=provenance[name][0];old_cylinder=cylinder(old_element.sweep)
            if new_cylinder and old_cylinder:
                if new_cylinder['radius']<=old_cylinder['radius']+1e-6:continue
                axis=np.array(old_cylinder['axis']);delta=np.array(new_cylinder['origin'])-np.array(old_cylinder['origin'])
                if abs(np.dot(axis,new_cylinder['axis']))<.99999 or np.linalg.norm(np.cross(delta,axis))>1e-6:continue
                reason='natural coaxial radius-step intervals'
            elif not new_cylinder and not old_cylinder:
                axis=old_element.axis
                if abs(np.dot(axis,element.axis))<.99999:continue
                if not constant_along(body,axis) or not constant_along(sweep,axis):continue
                reason='natural parallel prismatic section-step intervals'
            else:continue
            remainder=body.cut(sweep).clean();segments=remainder.Solids()
            if len(segments)<2:continue
            if not all(constant_along(s,axis) for s in segments):continue
            if new_cylinder and not all(cylinder(s) for s in segments):continue
            # End caps consisting solely of CADGen's placement overlap are
            # retained with the adjacent step, never exported as tiny parts.
            r=frame(axis)
            service_limit=2*element.history.get('service_overlap_mm',.0005)+1e-7
            thin=[s for s in segments if transform_part(s,r.T,np.zeros(3)).BoundingBox().zlen<=service_limit]
            if thin:step_sweep=step_sweep.fuse(combine(thin)).clean()
            segments=[s for s in segments if s not in thin]
            del stepped[name];del stepped_provenance[name];children=[]
            for i,segment in enumerate(segments,1):
                child=f'{name}_s{i}';stepped[child]=segment;stepped_provenance[child]=provenance[name];children.append(child)
            split_steps.append(dict(parent=name,segments=children,reason=reason,
                                    service_end_caps_absorbed=len(thin)))
        if split_steps:
            stepped[element.id]=step_sweep
            if _valid(stepped) and difference_volume(occupied.fuse(sweep),combine(stepped.values()))<=tolerance:
                intersections=max((overlap_volume(a,b) for a,b in combinations(stepped.values(),2)),default=0.)
                if intersections<=tolerance:
                    parts=stepped;provenance=stepped_provenance;provenance[element.id]=[element]
                    records.append(dict(operation=element.id,
                                        selected='natural_coaxial_step_ownership' if new_cylinder else 'natural_prismatic_step_ownership',
                                        steps=split_steps,overlap_volume=overlap.Volume(),added_volume=added.Volume(),
                                        alternative_rejected='annular/shell sleeve would hide the natural section transition'))
                    continue
        alternatives=[]
        def offer(label,values,priority):
            reason=None
            if not _valid(values):reason='would disconnect or erase a logical element'
            else:
                error=difference_volume(occupied.fuse(sweep),combine(values.values()))
                intersections=max((overlap_volume(a,b) for a,b in combinations(values.values(),2)),default=0.)
                if error>tolerance or intersections>tolerance:reason='material ownership fails exact reconstruction'
            preserved=0
            if reason is None:
                for name,body in values.items():
                    candidate=element if name==element.id else provenance[name][0]
                    if difference_volume(body,candidate.sweep.intersect(original))<=tolerance:
                        preserved+=4 if cylinder(candidate.sweep) else 1
            alternatives.append(dict(strategy=label,valid=reason is None,reason=reason,priority=preserved+priority*.01,preserved_primitive_score=preserved,
                                      parts=values if reason is None else None))
        offer('preserve_existing_elements',dict(parts,**{element.id:added}),3)
        reverse={n:s.cut(sweep).clean() for n,s in parts.items()}
        if all(s.Volume()>tolerance for s in reverse.values()):
            offer('preserve_new_element',dict(reverse,**{element.id:sweep}),2)
        # A local halflap divides only the shared volume. It never sends a
        # global cutting plane through unrelated parts of either extrusion.
        if not any(a['valid'] for a in alternatives) and overlap.Volume()>tolerance:
            axes=[np.cross(element.axis,old.axis) for group in provenance.values() for old in group]
            axes.extend(np.eye(3));seen=[]
            for axis in axes:
                if np.linalg.norm(axis)<1e-6:continue
                axis=axis/np.linalg.norm(axis)
                if any(abs(np.dot(axis,old))>.99999 for old in seen):continue
                seen.append(axis)
                for fraction in (.5,.35,.65):
                    assigned_new=_local_overlap_cut(overlap,axis,fraction)
                    assigned_old=overlap.cut(assigned_new)
                    values={n:s.cut(assigned_new).clean() for n,s in parts.items()}
                    values[element.id]=sweep.cut(assigned_old).clean()
                    offer(f'local_overlap_halflap:{axis.tolist()}:{fraction}',values,1)
        feasible=[a for a in alternatives if a['valid']]
        if not feasible:
            # Keep inseparable additions with their actual neighbouring
            # component rather than creating arbitrary disconnected shards.
            adjacent=sorted(parts,key=lambda n:-overlap_volume(parts[n],sweep))
            owner=adjacent[0];merged=parts[owner].fuse(added).clean()
            require_solid(merged,'unresolved constructive cluster')
            parts[owner]=merged;provenance[owner].append(element)
            selected='retain_inseparable_cluster'
        else:
            selected=max(feasible,key=lambda a:a['priority'])
            parts=selected['parts'];selected=selected['strategy'];provenance[element.id]=[element]
        records.append(dict(operation=element.id,selected=selected,overlap_volume=overlap.Volume(),
            added_volume=added.Volume(),alternatives=[{k:v for k,v in a.items() if k!='parts'} for a in alternatives]))
    # Merge only redundant parallel operations of the same construction family
    # whose union is constant along that SAME construction direction. A
    # cylinder and a key remain distinct even if their combined contour sweeps.
    merges=[];changed=True
    while changed:
        changed=False
        for a,b in combinations(tuple(parts),2):
            ea,eb=provenance[a][0],provenance[b][0]
            if abs(np.dot(ea.axis,eb.axis))<.99999:continue
            fa=ea.history.get('family','cylinder' if cylinder(ea.sweep) else 'prism')
            fb=eb.history.get('family','cylinder' if cylinder(eb.sweep) else 'prism')
            if fa!=fb:continue
            combined=parts[a].fuse(parts[b]).clean()
            if len(combined.Solids())!=1:continue
            try:simple=constant_along(combined,ea.axis)
            except Exception:simple=False
            if simple:
                parts[a]=combined;del parts[b];provenance[a]+=provenance.pop(b)
                merges.append(dict(components=[a,b],reason='same construction direction and verified constant external section'))
                changed=True;break
    state=Partition(original,parts)
    state.checks.update(validate_raw_partition(original,parts,tolerance))
    descriptions={}
    for name,shape in parts.items():
        group=provenance[name]
        try:recognition=recognize(shape,Budget(2000))[0]
        except (ValueError,RuntimeError) as error:
            recognition=dict(simple=False,reason='recognition_error',errors=[f'{type(error).__name__}: {error}'])
        history=group[0];descriptor=cylinder(history.sweep)
        try:along=constant_along(shape,history.axis)
        except Exception:along=False
        state.stops[name]=dict(reason='constructive_element' if len(group)==1 else 'constructive_cluster',
            analysis=dict(recognition=recognition),history_elements=[e.id for e in group],
            construction_axis=history.axis.tolist(),constant_along_construction=along,
            note='Attachment trimming is retained; this label is not a claim of constant section when recognition is false.')
        descriptions[name]=dict(history_elements=[e.id for e in group],family=history.history.get('family','cylinder' if descriptor else 'prism'),
            axis=history.axis.tolist(),cylinder=descriptor,operations=[e.history for e in group],
            trimmed_by_attachment=difference_volume(shape,history.sweep)>tolerance)
    state.checks.update(constructive_elements=descriptions,constructive_allocations=records,
        constructive_merges=merges,geometric_analyses={},geometry_limits=[],
        all_leaves_constant_section=all(s['analysis']['recognition']['simple'] for s in state.stops.values()),
        decomposition_complete_within_search=not any(len(provenance[n])>1 and not state.stops[n]['constant_along_construction'] for n in parts),
        unresolved_constructive_clusters=[n for n in parts if len(provenance[n])>1 and not state.stops[n]['constant_along_construction']],
        method='constructive_operation_volumes',
        global_planes_through_neighbours_used=False,service_overlaps_kept_in_material=True)
    return state
