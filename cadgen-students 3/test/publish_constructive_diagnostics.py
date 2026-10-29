"""Publish saved decompositions and observe bounded joint searches unchanged.

No decomposition, CADGen factory or assembly search is run here. sys.settrace
observes locals of the existing local-search functions; it neither replaces
builders nor changes their parameters, budgets, return values or exceptions.
"""

import argparse
from collections import Counter
from dataclasses import asdict,is_dataclass
import hashlib
from itertools import combinations
import json
import linecache
from pathlib import Path
import re
import shutil
import sys

import cadquery as cq
import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Surface

from cadgen import constructive_joint_design as design_module
from cadgen.assembly_geometry import AssemblySettings,difference_volume,frame
from cadgen.assembly_validation import transform_part
from cadgen.auto_assembly import layout,renamed
from cadgen.constructive_geometry import ConstructiveSettings,general_contact
from cadgen.joint_design import materialize
from cadgen.validate_constructive_results import load_parts


PROJECT=Path(__file__).resolve().parents[1]
SOURCE=PROJECT/'generations/assemblies/constructive_verified'
CHECKPOINT=PROJECT/'generations/assemblies/constructive_geometry_checked'
TARGET=PROJECT/'examples/constructive_diagnostics'
FAILED=(1,2,5,6,7,9)
ALIASES={'self_tapping_screw':'blind_bolt','screws':'blind_bolts','screw':'blind_bolt',
         'min_screw_engagement':'min_blind_bolt_engagement',
         'second_part_engagement_mm':'second_part_engagement_mm'}


def terminology(text):
    if text in ALIASES:return ALIASES[text]
    for old,new in [('self_tapping_screw','blind_bolt'),('Blind screw','Blind bolt'),
                    ('blind screw','blind bolt'),('Screw engagement','Blind bolt engagement'),
                    ('screw_','blind_bolt_')]:text=text.replace(old,new)
    return text


def clean(value):
    if isinstance(value,str):return terminology(value)
    if isinstance(value,(bool,int,float)) or value is None:return value
    if isinstance(value,np.generic):return value.item()
    if isinstance(value,np.ndarray):return value.tolist()
    if isinstance(value,(list,tuple)):return [clean(v) for v in value]
    if isinstance(value,dict):return {ALIASES.get(str(k),terminology(str(k))):clean(v) for k,v in value.items()}
    if is_dataclass(value):return clean(asdict(value))
    raise TypeError(type(value).__name__)


def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(clean(value),indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def box(shape):
    b=shape.BoundingBox()
    return dict(dimensions_mm=[b.xlen,b.ylen,b.zlen],bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax])


def export_stl(parts,path,explode=False):
    parts=dict(parts);shifts=layout(parts,8) if explode else {}
    bodies=[s.translate(tuple(shifts[n])) if explode else s for n,s in parts.items()]
    cq.exporters.export(cq.Compound.makeCompound(bodies),str(path),tolerance=.1,angularTolerance=.15)
    assert Path(path).stat().st_size<10_000_000,path


def copy_data(src,dst,names=None):
    dst=Path(dst);dst.parent.mkdir(parents=True,exist_ok=True)
    if src.suffix=='.json':
        value=json.loads(src.read_text());save(dst,renamed(value,names) if names else value)
    else:shutil.copy2(src,dst)


def classification(gm,parts):
    result=[]
    for record in gm['raw_components']:
        name=record['name'];stop=gm['stopping_conditions'][name]
        recognition=stop.get('analysis',{}).get('recognition',{})
        result.append(dict(record,**box(parts[name]),simple=recognition.get('simple',False),
            classification='simple_confirmed' if recognition.get('simple') else 'simplicity_not_confirmed',
            recognition=recognition,stopping_condition=stop,
            constructive_element=gm['checks']['constructive_elements'].get(name)))
    return result


def prepare():
    TARGET.mkdir(parents=True,exist_ok=False)
    manifest={};rows=[]
    for folder in sorted(SOURCE.glob('model_*')):
        target=TARGET/folder.name;target.mkdir()
        g=folder/'geometry';gm=json.loads((g/'metadata.json').read_text())
        row=json.loads((folder/'metadata.json').read_text());parts=load_parts(g,gm['raw_components'])
        for old,new in [('original.stl','original.stl'),('original.step','original.step'),
                        ('split_exploded.stl','split_exploded.stl'),('geometric_partition.stl','split_assembled.stl')]:
            copy_data(g/old,target/new);manifest[str((target/new).relative_to(TARGET))]=sha(g/old)
        for c in gm['raw_components']:
            for field in ('stl','step'):
                copy_data(g/c[field],target/c[field]);manifest[str((target/c[field]).relative_to(TARGET))]=sha(g/c[field])
        names=gm['component_id_map']
        copy_data(folder/'assembly_report.json',target/'assembly_report.json',names)
        copy_data(folder/'decomposition_report.json',target/'decomposition_report.json',names)
        status=('complete_validated' if row['assembly_success'] else
                'partial_validated_export_failed' if row['assembly_status']=='export_failed' else 'assembly_not_found')
        metadata=dict(gm,publication_status=status,complete_assembly_success=row['assembly_success'],
            assembly_success=row['assembly_success'],assembly_status=row['assembly_status'],
            original_assembly_status=row['assembly_status'],assembly_reason=row.get('assembly_reason'),
            geometric_components=classification(gm,parts),geometric_component_count=len(parts),
            original_files_copied_without_regeneration=True,source_run='constructive_verified',
            stage_separation='Root part_N files are geometric components BEFORE fasteners; processed files have their own folder.',
            units='mm',installed_joint_counts={k:v if row['assembly_success'] else 0
                for k,v in row.get('validated_candidate_counts',{}).items()},
            candidate_joint_counts=row.get('validated_candidate_counts',{}))
        save(target/'metadata.json',metadata)
        processed=folder/('assembly' if row['assembly_success'] else 'failed_export')
        if processed.exists():
            out=target/('assembly' if row['assembly_success'] else 'partial_assembly');out.mkdir()
            pm=json.loads((processed/'metadata.json').read_text())
            files={c[k] for c in pm['components'] for k in ('stl','step')}
            files.update(f for f in ('assembly.stl','assembly.step','parts_exploded.stl','exploded.step') if (processed/f).exists())
            for file in sorted(files):copy_data(processed/file,out/terminology(file))
            pm.update(publication_status=status,complete_assembly_success=row['assembly_success'])
            save(out/'metadata.json',pm)
        rows.append(dict(model=folder.name,components=len(parts),simple=sum(c['simple'] for c in metadata['geometric_components']),status=status))
    save(TARGET/'SOURCE_MANIFEST.json',dict(source='generations/assemblies/constructive_verified',copied_sha256=manifest,
        algorithm_sources_sha256=json.loads(Path('/workspace/airi-publication-frozen-code.json').read_text())))
    save(TARGET/'models.json',dict(models=rows))
    print('COPIED',len(rows),'models',sum(r['components'] for r in rows),'geometric parts',flush=True)


def face_info(face):
    info=dict(type=face.geomType(),area_mm2=face.Area(),center_world_mm=list(face.Center().toTuple()),**box(face))
    if face.geomType()=='PLANE':
        n=np.array(face.normalAt().toTuple());r=frame(n);o=np.array(face.Center().toTuple())
        local=transform_part(face,r.T,-r.T@o)
        info.update(normal_world=n.tolist(),local_dimensions_mm=box(local)['dimensions_mm'][:2])
    elif face.geomType()=='CYLINDER':
        a=BRepAdaptor_Surface(face.wrapped);c=a.Cylinder()
        info.update(radius_mm=c.Radius(),axis_world=list(c.Axis().Direction().Coord()),
                    angular_span_radians=a.LastUParameter()-a.FirstUParameter(),axial_span_mm=a.LastVParameter()-a.FirstVParameter())
    return info


def failure_category(reason,built=False,static=False,label=''):
    s=reason.lower()
    if 'no sampled assembly path' in s:return 'no_pair_insertion_direction'
    if 'sequence' in s:return 'no_complete_assembly_order'
    if 'protected zones' in s or 'conflict' in s:return 'joint_conflict'
    if 'limit' in s or 'budget' in s:return 'search_limit'
    if built:return 'geometric_validation_failed'
    if 'bolt' in terminology(label) or 'bolted' in label:return 'bolt_creation_failed'
    if 'cylind' in label:return 'cylindrical_fit_creation_failed'
    return 'groove_creation_failed'


class Observer:
    """Frame-local observation of exactly the attempts made by the algorithm."""
    def __init__(self):
        self.attempts=[];self.active={};self.stack=[];self.skips=[];self.static_examples={};self.failure=None

    def trace(self,f,event,arg):
        try:return self.observe(f,event,arg)
        except Exception as error:
            self.failure=f'{type(error).__name__}: {error}'
            raise

    def observe(self,f,event,arg):
        module=f.f_globals.get('__name__','');name=f.f_code.co_name
        relevant=(module in ('cadgen.constructive_joint_design','cadgen.constructive_fasteners','cadgen.assembly_geometry'))
        if not relevant:return None
        if event=='call':
            if module=='cadgen.constructive_joint_design' and name=='attempt':
                v=f.f_locals
                limited=(v['attempts']>=v['design'].max_designs_per_pair or
                    (v['role_limited'] and v['attempts']-v['role_start']>=v['role_budget']))
                if limited:
                    self.skips.append(dict(label=v['label'],owners=list(v['owners']),reason='attempt budget before builder invocation'))
                    return None
                split=v['split'];row=dict(id=f'attempt_{len(self.attempts)+1:03d}',label=v['label'],
                    owners=list(v['owners']),cut_to_world_rotation=split.rotation.tolist(),cut_origin_mm=split.origin.tolist(),
                    feature_proposals=[],builder_calls=[],builder_succeeded=False,static_geometry_passed=False,
                    local_validation_passed=False)
                self.attempts.append(row);self.active[id(f)]=row;self.stack.append((f,row))
            elif self.stack and name=='accept':
                row=self.stack[-1][1];v=f.f_locals
                row['builder_succeeded']=True;row['_connection']=v['result'];row['_split']=v['split']
                row['built_parameters']=clean(v['result'].parameters)
            elif self.stack and name=='build_groove':
                row=self.stack[-1][1];v=f.f_locals
                row['builder_calls'].append(dict(function='build_groove',values=dict(
                    centers=clean(v.get('centers')),profile=clean(v.get('exact_profile')),
                    footprint=clean(v.get('footprint')),clearance_mm=v['settings'].clearance)))
            return self.trace
        if not self.stack:return self.trace
        row=self.stack[-1][1];v=f.f_locals
        if (name=='_grooves' and event=='line' and 'selected' in v and 'local_length' in v
                and linecache.getline(f.f_code.co_filename,f.f_lineno).lstrip().startswith('if min(selected.opening_width')):
            p=v['selected'];key=(v.get('x'),v.get('y'),p.opening_width,p.depth,v['local_length'])
            if key!=row.get('_last_feature'):
                row['_last_feature']=key
                row['feature_proposals'].append(dict(type='groove',profile=asdict(p),center_in_cut_frame_mm=[v['x'],v['y'],0.],
                    width_mm=p.opening_width,depth_mm=p.depth,length_mm=v['local_length'],
                    available_receiver_depth_mm=v.get('rd'),available_donor_depth_mm=v.get('dd'),
                    face_chord_x_mm=v.get('chord_x'),face_chord_y_mm=v.get('chord_y'),depth_factor=v['depth_factor']))
        if event=='return' and name in ('_grooves','cylindrical_fit','fasten','_transverse'):
            fields=('layout','kind','depth_factor','depth_scale','crossed','centers','diameter','radius','depth','gap','floor',
                    'rd','dd','x','y','length','engagement','receiver_depth','donor_depth','top','bottom')
            row['builder_calls'].append(dict(function=name,returned_connection=arg is not None,
                values={k:clean(v[k]) for k in fields if k in v}))
        if name=='validate_connection' and event=='return':
            row['static_geometry_passed']='paths' in v
            row['static_checks']={k:clean(v[k]) for k in ('intersections','added','void_error') if k in v}
            if 'path' in v:row['last_path_check']=clean(v['path'])
        if name=='accept' and event=='return' and 'joint' in v:
            if v.get('options') and v['options'][-1] is v['joint']:
                row['local_validation_passed']=True;row['joint']=clean(v['joint'].metadata())
        if id(f) in self.active:
            if event=='exception':row['reason']=f'{arg[0].__name__}: {arg[1]}'
            if event=='return':
                if row['local_validation_passed']:
                    row.pop('reason',None);row['outcome']='local_valid'
                else:
                    row['reason']=row.get('reason','Builder did not produce a locally valid joint')
                    row['outcome']=failure_category(row['reason'],row['builder_succeeded'],row['static_geometry_passed'],row['label'])
                if row['static_geometry_passed'] and not row['local_validation_passed']:
                    kind='groove' if 'groove' in str(row.get('built_parameters',{}).get('type')) else 'bolt_or_fit'
                    if kind not in self.static_examples:
                        self.static_examples[kind]=(row['_connection'],row['_split'],row['id'])
                for key in ('_connection','_split','_before','_last_feature'):row.pop(key,None)
                del self.active[id(f)];self.stack.pop()
        return self.trace


def selected_model_joints(folder,names):
    processed=folder/('assembly' if (folder/'assembly').exists() else 'failed_export')
    if not processed.exists():return []
    return renamed(json.loads((processed/'metadata.json').read_text())['joints'],names)


def diagnose_model(number):
    name=f'model_{number:02d}';folder=SOURCE/name;target=TARGET/name
    gm=json.loads((folder/'geometry/metadata.json').read_text());names=gm['component_id_map']
    # Reload the very checkpoint used by the original search, not a new cut.
    cache=CHECKPOINT/name/'geometry';cm=json.loads((cache/'metadata.json').read_text())
    parts=load_parts(cache,cm['raw_components']);descriptions=cm['checks']['constructive_elements']
    published=load_parts(folder/'geometry',gm['raw_components'])
    assert all(difference_volume(parts[n],published[n])<=1e-5 for n in parts),'Checkpoint geometry mismatch'
    original=json.loads((folder/'assembly_report.json').read_text())
    trials={tuple(sorted(names.get(n,n) for n in t['components'])):renamed(t,names) for t in original['trials']}
    geometry=AssemblySettings();design=ConstructiveSettings()
    out=target/'joint_diagnostics';out.mkdir(exist_ok=False)
    rows=[]
    for a,b in combinations(parts,2):
        patch=general_contact(parts[a],parts[b]);area=patch.Area();distance=parts[a].distance(parts[b])
        key=tuple(sorted((a,b)))
        if area<=1e-7 and distance>1e-6 and key not in trials:continue
        pair=out/f'{a}__{b}';pair.mkdir();export_stl({a:parts[a],b:parts[b]},pair/'pair_exploded.stl',True)
        contact=dict(area_mm2=area,minimum_distance_mm=distance,faces=[face_info(f) for f in patch.Faces()],
            definition='shared_trimmed_BRep_faces' if area>1e-7 else 'boundary_touch_without_verified_contact_area')
        observer=Observer();options=[];error=None
        if area>1e-7:
            old_trace=sys.gettrace()
            try:
                sys.settrace(observer.trace)
                options=design_module.propose_constructive(parts,a,b,descriptions,geometry,design)
            except Exception as exc:error=dict(reason=f'{type(exc).__name__}: {exc}',report=getattr(exc,'report',None))
            finally:sys.settrace(old_trace)
            if observer.failure:raise RuntimeError('Diagnostic observer failed: '+observer.failure)
        else:error=dict(reason='No verified shared B-rep face; algorithm does not call a joint builder for this boundary touch')
        report=(options[0].selection['constructive_search'] if options else (error or {}).get('report')) or {}
        signatures={json.dumps(clean(j.parameters),sort_keys=True) for j in options}
        for t in observer.attempts:
            if t['local_validation_passed']:
                t['retained_in_returned_options']=json.dumps(t['joint']['parameters'],sort_keys=True) in signatures
        reps=[];families=set()
        for index,j in enumerate(options,1):
            p=j.parameters;family=('groove' if p['type']=='distributed_grooves' else p['type'])
            if family in families:continue
            families.add(family);stem=f'valid_candidate_{index:02d}'
            modified=materialize({a:parts[a],b:parts[b]},[j],geometry)
            export_stl(modified,pair/f'{stem}_assembled.stl');export_stl(modified,pair/f'{stem}_exploded.stl',True)
            reps.append(dict(stem=stem,local_geometry_and_sampled_pair_path_passed=True,
                global_assembly_success=original['success'],joint=j.metadata()))
        for connection,split,attempt in observer.static_examples.values():
            stem='static_only_'+attempt;modified={n:split.world(s) for n,s in connection.components}
            export_stl(modified,pair/f'{stem}_assembled.stl');export_stl(modified,pair/f'{stem}_exploded.stl',True)
            reps.append(dict(stem=stem,attempt=attempt,static_geometry_passed=True,
                             local_geometry_and_sampled_pair_path_passed=False,global_assembly_success=False))
        unreachable=[names.get(n,n) for n in original.get('unreachable_components',[])]
        global_reason=(f'Original complete search stopped before joint combinations/order: no connected graph; unreachable {unreachable}'
            if unreachable else 'Original full in-memory order passed, but STEP export failed' if original['success'] and (folder/'failed_export').exists()
            else 'Original full assembly passed' if original['success'] else original.get('reason'))
        # Original report says success=False after export, but retained planning
        # and failed_export metadata still record the successful in-memory order.
        if (folder/'failed_export').exists():global_reason='Full in-memory assembly and order passed; subsequent STEP roundtrip failed; model is partial, not fully successful'
        result=dict(model=name,components=[a,b],contact=contact,part_dimensions_mm={n:box(parts[n])['dimensions_mm'] for n in (a,b)},
            original_pair_trial=trials.get(key),diagnostic_replay=True,geometry_unchanged=True,
            algorithms_unchanged=True,settings=asdict(geometry),design_settings=asdict(design),
            attempts=observer.attempts,pre_filter_and_search_rejections=report.get('rejected',[]),
            budget_skipped_calls=observer.skips,search_report=report,error=error,
            locally_valid_returned_options=len(options),representative_views=reps,
            global_model_status=json.loads((folder/'metadata.json').read_text())['assembly_status'],
            why_local_options_are_not_complete_model=global_reason,
            original_global_rejections=renamed(original.get('global_rejections',[]),names),
            remaining_scope='Local replay only; no new global assembly or part decomposition was run. No continuous path or strength proof.')
        save(pair/'attempts.json',result)
        rows.append(dict(components=[a,b],folder=str(pair.relative_to(target)),contact_area_mm2=area,
            verified_contact_faces=len(patch.Faces()),attempts=len(observer.attempts),valid_options=len(options),
            failure_categories=dict(Counter(t['outcome'] for t in observer.attempts))))
        print(name,a,b,'area',round(area,6),'attempts',len(observer.attempts),'valid',len(options),flush=True)
    save(out/'index.json',dict(model=name,pairs=rows,all_boundary_neighbours_included=True))
    print('DONE',name,len(rows),'pairs',flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepare',action='store_true');p.add_argument('--models',nargs='+',type=int)
    args=p.parse_args()
    if args.prepare:prepare()
    for n in args.models or []:diagnose_model(n)


if __name__=='__main__':main()
