"""Reload constructive exports and verify solids, placements and saved motions.

This is a file-level audit, not a strength calculation or continuous collision
proof. The manufacturing-void check compares the saved volume and the spatial
envelopes of declared joints; individual recipes are checked during creation.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path

import cadquery as cq
import numpy as np
import trimesh

from Bolty import BoltSpec,build_bolt
from .assembly_geometry import difference_volume,require_solid
from .assembly_validation import overlap_volume,transform_part
from .assembly_generator import save_json
from .decomposition import validate_raw_partition
from .joint_design import combine


def load_parts(folder,records):
    return {r['name']:require_solid(transform_part(cq.importers.importStep(str(folder/r['step'])).val(),
            r['rotation_matrix'],r['translation']),r['name']) for r in records}


def verify_model(folder,source=None,tolerance=1e-5):
    folder=Path(folder);g=folder/'geometry'
    gm=json.loads((g/'metadata.json').read_text())
    original=cq.importers.importStep(str(g/'original.step')).val()
    raw=load_parts(g,gm['raw_components'])
    checks=validate_raw_partition(original,raw,tolerance)
    if source:
        expected=cq.importers.importStep(str(Path(source)/folder.name/'original.step')).val()
        assert difference_volume(original,expected)<=tolerance,'Source geometry changed'
    result=dict(model=folder.name,geometric_components=len(raw),geometry_checks=checks,
                minimum_component_bbox_mm=min(min(s.BoundingBox().xlen,s.BoundingBox().ylen,s.BoundingBox().zlen)
                                               for s in raw.values()))
    status=json.loads((folder/'assembly_report.json').read_text())
    result['assembly_success']=status['success']
    stl_count=0
    for path in sorted(folder.rglob('*.stl')):
        if 'failed_export' in path.parts:continue
        mesh=trimesh.load(str(path),force='mesh')
        assert len(mesh.faces) and np.isfinite(mesh.vertices).all() and mesh.volume>0,path
        stl_count+=1
    result['readable_stl_files']=stl_count
    if not status['success']:
        assert not (folder/'assembly').exists(),'Failed assembly exported as ready'
        result['assembly_reason']=status.get('reason')
        return result
    a=folder/'assembly';am=json.loads((a/'metadata.json').read_text())
    assert am['success']
    parts=load_parts(a,am['components'])
    for left,right in combinations(parts,2):
        assert overlap_volume(parts[left],parts[right])<=tolerance,(left,right,'final collision')
    main=combine(parts[r['name']] for r in am['components'] if r['role']=='main')
    assert main.cut(original).Volume()<=tolerance,'Main material added outside source'
    removed=original.cut(main)
    allowed=am['checks'].get('allowed_removed_volume',0.)
    # Integrated volumes can drift when STEP reconstruction retrims curved
    # faces. This tolerance concerns the scalar integral, not collisions or
    # the spatial test against the declared modification envelopes below.
    volume_integral_tolerance=max(tolerance,original.Volume()*1e-7)
    assert abs(removed.Volume()-allowed)<=volume_integral_tolerance,'Void volume changed in export'
    zones=[];feature_sizes=[];hardware_checked=0
    used_hardware=set()
    design=am['request']['design_settings']
    for joint in am['joints']:
        p=joint['parameters'];r=np.array(p['cut_to_world_rotation']);origin=np.array(p['cut_origin'])
        for b in p['feature_zones_local']:
            box=cq.Solid.makeBox(b[3]-b[0],b[4]-b[1],b[5]-b[2],cq.Vector(*b[:3]))
            zones.append(transform_part(box,r,origin))
        for f in p['features']:
            assert 0<=f['clearance']<1,'Invalid clearance'
            if f['type']=='groove':
                feature_sizes.extend([f['profile']['opening_width'],f['profile']['depth'],f['central_engagement_length']])
            elif f['type']=='cylindrical_fit':
                feature_sizes.extend([2*f['pin_radius'],f['depth']])
                assert abs(f['hole_radius']-f['pin_radius']-f['clearance'])<1e-7
            else:
                assert f['shaft_length']<=design['max_shaft_length']+1e-7
                fr=np.array(f.get('fastener_to_joint_rotation',np.eye(3)))
                fo=np.array(f.get('fastener_origin_in_joint',[0,0,0]))
                world_r=r@fr;world_o=r@fo+origin
                center=np.array(f['center_in_fastener_frame'])+np.array([0,0,f['head_seat_z']])
                expected=build_bolt(BoltSpec(**f['bolt']),adaptive=True).translate(tuple(center))
                expected=transform_part(expected,world_r,world_o)
                matches=[n for n in joint['hardware'] if n not in used_hardware
                         and n.startswith(('bolt_','screw_')) and difference_volume(expected,parts[n])<=tolerance]
                assert len(matches)==1,'Saved hardware does not match shaft/head dimensions'
                used_hardware.add(matches[0]);hardware_checked+=1
                if f['type']=='self_tapping_screw':
                    engagement=f['second_part_engagement_mm']
                    assert engagement>=design['min_screw_engagement']-1e-7
                    x,y,_=f['center_in_fastener_frame']
                    probe=cq.Solid.makeCylinder((f['shaft_diameter']+2*f['clearance'])/2,engagement,
                                               cq.Vector(x,y,-engagement))
                    probe=transform_part(probe,world_r,world_o)
                    assert probe.cut(raw[joint['components'][1]]).Volume()<=tolerance,'Engagement crosses air'
    if zones:
        assert removed.cut(combine(zones)).Volume()<=tolerance,'Changes outside declared joint envelopes'
    if feature_sizes:assert min(feature_sizes)>=design['min_feature_size']-1e-7,'Below design floor'
    sequence=am['assembly_sequence'];installed=set();sampled=0
    for step in sequence:
        name=step['component'];assert name in parts and name not in installed
        assert set(step['stationary_components'])==installed
        if step['action']!='place_base':
            assert step['action']=='linear_insertion','Unsupported motion in audit'
            direction=-np.array(step['insertion_direction'])
            for distance in step['distances']:
                moving=parts[name].translate(tuple(direction*distance))
                assert all(overlap_volume(moving,parts[n])<=tolerance for n in installed),(name,distance)
                sampled+=1
        installed.add(name)
    assert installed==set(parts),'Incomplete saved assembly sequence'
    for file,count in [('assembly.step',len(parts)),('exploded.step',len(parts)),('split_exploded.step',len(raw))]:
        read=cq.importers.importStep(str(a/file))
        assert len(read.solids().vals())==count and all(s.isValid() for s in read.solids().vals())
        if file=='assembly.step':
            # Preserve touching solids as separate operands, just as the STEP
            # assembly does. Fusing them can alter coincident boundary topology.
            assert difference_volume(read.val(),cq.Compound.makeCompound(list(parts.values())))<=tolerance
    result.update(final_components=len(parts),hardware_dimensions_checked=hardware_checked,
                  checked_path_positions=sampled,minimum_feature_mm=min(feature_sizes) if feature_sizes else None,
                  microscopic_features=any(v<.01 for v in feature_sizes),continuous_path_proven=False,
                  mechanical_strength_checked=False,volume_integral_tolerance=volume_integral_tolerance,
                  void_volume_integral_drift=abs(removed.Volume()-allowed))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    parser.add_argument('--source',type=Path)
    args=parser.parse_args()
    rows=[]
    for folder in sorted(args.folder.iterdir()):
        if not (folder/'geometry/metadata.json').exists():continue
        row=verify_model(folder,args.source);rows.append(row)
        print(json.dumps(row,ensure_ascii=False),flush=True)
    assert rows,'No geometric exports to validate'
    save_json(args.folder/'file_validation.json',dict(status='passed',models=rows,
        audit_scope='Reloaded STEP/STL, solids, source reconstruction, pairwise collisions, void envelopes/volume, hardware dimensions, all saved trajectory samples',
        continuous_path_proven=False,individual_void_recipes_replayed=False))


if __name__=='__main__':main()
