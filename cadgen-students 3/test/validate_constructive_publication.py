"""Audit the publication without rerunning decomposition or joint generation."""

import hashlib
import json
from pathlib import Path
import re

import cadquery as cq
import numpy as np
import trimesh

from publish_constructive_diagnostics import TARGET,SOURCE,PROJECT,sha,save,terminology,load_parts
from cadgen.decomposition import validate_raw_partition


def main():
    manifest=json.loads((TARGET/'SOURCE_MANIFEST.json').read_text())
    for name,expected in manifest['algorithm_sources_sha256'].items():
        assert sha(PROJECT/name)==expected,('Algorithm/test changed',name)
    for name,expected in manifest['copied_sha256'].items():
        assert sha(TARGET/name)==expected,('Copied geometry changed',name)
    protected=json.loads(Path('/workspace/airi-constructive-protected.json').read_text())
    for name,expected in protected.items():assert sha(PROJECT/name)==expected,('Old example changed',name)
    count=simple=pair_count=attempt_count=static_views=valid_views=0;checks=[];all_stls=[]
    for model in sorted(TARGET.glob('model_*')):
        m=json.loads((model/'metadata.json').read_text());old=json.loads((SOURCE/model.name/'metadata.json').read_text())
        assert m['complete_assembly_success']==old['assembly_success']
        expected=old['components'];assert m['main_component_count']==expected
        assert len(m['geometric_components'])==expected
        assert {c['name'] for c in m['geometric_components']}=={f'part_{i}' for i in range(1,expected+1)}
        original=cq.importers.importStep(str(model/'original.step')).val()
        raw=load_parts(model,m['raw_components'])
        raw_checks=validate_raw_partition(original,raw)
        assert sha(model/'split_assembled.stl')==sha(SOURCE/model.name/'geometry/geometric_partition.stl')
        count+=len(raw);simple+=sum(c['simple'] for c in m['geometric_components'])
        for c in m['geometric_components']:
            saved=json.loads((SOURCE/model.name/'geometry/metadata.json').read_text())['stopping_conditions'][c['name']]['analysis']['recognition']
            assert c['simple']==saved['simple']
        processed=model/('assembly' if old['assembly_success'] else 'partial_assembly')
        if processed.exists():
            pm=json.loads((processed/'metadata.json').read_text())
            baseline=SOURCE/model.name/('assembly' if old['assembly_success'] else 'failed_export')
            original_pm=json.loads((baseline/'metadata.json').read_text())
            assert pm['complete_assembly_success']==old['assembly_success']
            for c in original_pm['components']:
                for field in ('stl','step'):
                    assert sha(baseline/c[field])==sha(processed/terminology(c[field]))
            for filename in ('assembly.stl','assembly.step','parts_exploded.stl','exploded.step'):
                if (baseline/filename).exists():assert sha(baseline/filename)==sha(processed/filename)
        index=json.loads((model/'joint_diagnostics/index.json').read_text());seen=set()
        names=m['component_id_map']
        original_trials=json.loads((SOURCE/model.name/'assembly_report.json').read_text())['trials']
        required={tuple(sorted(names.get(n,n) for n in t['components'])) for t in original_trials}
        for pair in index['pairs']:
            folder=model/pair['folder'];d=json.loads((folder/'attempts.json').read_text());key=tuple(sorted(d['components']))
            assert key not in seen;seen.add(key);pair_count+=1
            assert len(d['attempts'])==d.get('search_report',{}).get('attempts',0)
            assert len(d['attempts'])<=d['design_settings']['max_designs_per_pair']
            assert sum(t['local_validation_passed'] for t in d['attempts'])==d.get('search_report',{}).get('valid_designs',0)
            for t in d['attempts']:
                attempt_count+=1
                assert t['owners'][0] in key and t['owners'][1] in key
                assert t['builder_role_to_published_part']==dict(zip(('part_1','part_2'),t['owners']))
                if t['local_validation_passed']:assert t['static_geometry_passed'] and t['builder_succeeded']
            if d['locally_valid_returned_options']:
                assert any(v['local_geometry_and_sampled_pair_path_passed'] for v in d['representative_views'])
            for v in d['representative_views']:
                assert (folder/(v['stem']+'_assembled.stl')).exists()
                assert (folder/(v['stem']+'_exploded.stl')).exists()
                if v['local_geometry_and_sampled_pair_path_passed']:valid_views+=1
                else:static_views+=1;assert v['static_geometry_passed']
        assert required<=seen,(model.name,'Missing original neighbour')
        checks.append(dict(model=model.name,components=len(raw),simple=sum(c['simple'] for c in m['geometric_components']),
                           neighbour_pairs=len(seen),raw_partition=raw_checks))
    assert count==69 and simple==51
    broken=[]
    for path in TARGET.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if target.startswith(('http://','https://','#')):continue
            if not (path.parent/target).exists():broken.append((str(path),target))
    assert not broken,broken
    for path in TARGET.rglob('*'):
        if not path.is_file():continue
        assert path.suffix.lower() in ('.json','.md','.step','.stl'),path
        assert path.stat().st_size<100_000_000,path
        if path.suffix=='.stl':
            assert path.stat().st_size<10_000_000,path
            mesh=trimesh.load(str(path),force='mesh')
            assert len(mesh.faces)>0 and np.isfinite(mesh.vertices).all() and mesh.volume>0,path
            all_stls.append(dict(path=str(path.relative_to(TARGET)),bytes=path.stat().st_size,triangles=len(mesh.faces)))
        if path.suffix in ('.json','.md'):
            text=path.read_text()
            assert 'self_tapping_screw' not in text,path
            assert not re.search('саморез',text,re.IGNORECASE),path
    result=dict(status='passed',models=checks,components=count,simple_confirmed=simple,simplicity_not_confirmed=count-simple,
        neighbour_pairs=pair_count,observed_attempts=attempt_count,locally_valid_representative_pairs=valid_views,
        static_only_representative_pairs=static_views,readable_stl_count=len(all_stls),stl_files=all_stls,
        copied_geometry_checksums_verified=len(manifest['copied_sha256']),
        unchanged_algorithm_and_test_files=len(manifest['algorithm_sources_sha256']),unchanged_old_example_files=len(protected),
        all_markdown_links_valid=True,new_CADGen_sources_generated=False,algorithms_modified=False)
    save(TARGET/'PUBLICATION_VALIDATION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('models','stl_files')},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
