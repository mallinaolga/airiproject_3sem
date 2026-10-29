"""CLI comparison on existing CADGen sources, plus twelve constructive controls."""

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import time

import cadquery as cq

from .assembly_geometry import AssemblySettings
from .assembly_generator import save_json
from .auto_assembly import export_auto,renamed
from .constructive_geometry import ConstructiveSettings
from .constructive_decomposition import history_elements,decompose_constructive
from .constructive_assembly import assemble_constructive
from .decomposition import DecompositionSettings,Partition,validate_raw_partition
from .decomposition_export import export_geometry


def hashes(folder):
    return {str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob('*') if p.is_file()}


def normalize_result(row):
    """Distinguish a globally validated candidate from a usable disk export."""
    if 'validated_candidate_counts' in row:return row
    fields=('groove_elements','cylindrical_fits','bolts','screws')
    row['validated_candidate_counts']={k:row.get(k,0) for k in fields}
    row['candidate_connection_types']=row.get('connection_types',{})
    row['minimum_candidate_feature_mm']=row.get('minimum_installed_feature_mm')
    if not row['assembly_success']:
        row.update({k:0 for k in fields})
        row.update(connection_types={},minimum_installed_feature_mm=None)
    return row


def execute(state,target,parameters,geometry,design,program=None,only=None,profile=None,geometry_only=False):
    target=Path(target);target.mkdir(parents=True,exist_ok=False)
    decomp=DecompositionSettings()
    geometric=export_geometry(state,target/'geometry',decomp,parameters,program)
    save_json(target/'decomposition_report.json',dict(method='constructive_operation_volumes',
        components=state.checks.get('constructive_elements',{}),allocations=state.checks.get('constructive_allocations',[]),
        merges=state.checks.get('constructive_merges',[]),stops=state.stops,checks=state.checks))
    print('GEOMETRY',target.name,len(state.raw),'constituents',flush=True)
    def edge(a,b,options,entry=None):
        if entry:
            save_json(target/f'interface_{a}_{b}.json',entry)
            print('  INTERFACE',a,b,entry['status'],entry.get('options',0),flush=True)
    try:
        if not geometry_only:assemble_constructive(state,geometry,design,only=only,profile=profile,edge_callback=edge)
    except Exception as error:
        state.assembly.update(status='failed',success=False,reason=f'{type(error).__name__}: {error}')
    save_json(target/'assembly_report.json',state.assembly)
    assembly=None
    if state.assembly['success']:
        try:
            assembly=export_auto(state,42,parameters,program,target/'assembly',geometry,decomp,
                                 dict(decomposition='constructive',design_settings=asdict(design)))
        except Exception as error:
            if (target/'assembly').exists():(target/'assembly').rename(target/'failed_export')
            state.assembly.update(status='export_failed',success=False,reason=f'{type(error).__name__}: {error}')
            save_json(target/'assembly_report.json',state.assembly)
    features=[f for j in state.joints for f in j.parameters.get('features',[])]
    grooves=[f for f in features if f['type'] in ('groove','cylindrical_fit')]
    sizes=[]
    for f in grooves:
        if f['type']=='groove':sizes.extend([f['profile']['opening_width'],f['profile']['depth'],f['central_engagement_length']])
        else:sizes.extend([2*f['pin_radius'],f['depth']])
    counts=Counter(f['type'] for f in features)
    row=dict(model=target.name,components=len(state.raw),groove_elements=len(grooves),
        cylindrical_fits=counts['cylindrical_fit'],bolts=counts['bolted'],screws=counts['self_tapping_screw'],
        connection_types=dict(Counter(j.parameters['type'] for j in state.joints)),
        assembly_success=state.assembly['success'],assembly_status=state.assembly['status'],
        assembly_reason=state.assembly.get('reason'),geometric_partition_valid=geometric['checks']['geometric_partition_valid'],
        minimum_installed_feature_mm=min(sizes) if sizes else None,
        microscopic_features=any(v<.01 for v in sizes),unresolved_constructive_clusters=state.checks.get('unresolved_constructive_clusters',[]),
        raw_simple_components=sum(s.get('analysis',{}).get('recognition',{}).get('simple',False) for s in state.stops.values()),
        assembly_folder='assembly' if assembly else None,design_settings=asdict(design))
    normalize_result(row)
    save_json(target/'metadata.json',row)
    print(json.dumps(row,ensure_ascii=False),flush=True)
    return row


def controls(output,geometry,design):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'test'))
    from constructive_controls import cases
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
    rows=[]
    for case in cases():
        row=execute(case['state'],output/case['name'],dict(generator='synthetic_constructive_control',case=case['name']),
                    geometry,design,only=case.get('only'),profile=case.get('profile'))
        row['expected_components']=case['expected'];rows.append(row)
        assert row['components']==case['expected'] and row['assembly_success'],row
    save_json(output/'report.json',dict(status='passed',models=rows))
    write_readme(output,rows,controls=True)
    return rows


def compare(source,output,geometry,design,models=None,geometry_only=False,reuse_geometry=None):
    source=Path(source).resolve();output=Path(output).resolve()
    output.mkdir(parents=True,exist_ok=False);before=hashes(source)
    provenance=json.loads((source/'cadgen_overlap_provenance.json').read_text())
    programs={p['model']:'from cadgen.extrude import extrude\nr=None\n'+'\n'.join(
        'r='+c['source'] for c in sorted(p['extrude_calls'],key=lambda c:c['line']))+'\n' for p in provenance['programs']}
    rows=[];report=dict(status='running',source=str(source),models=rows,
        random_source_generation_performed=False,original_geometries_modified=False,
        decomposition_algorithm_sha256=hashlib.sha256((Path(__file__).parent/'constructive_decomposition.py').read_bytes()).hexdigest())
    save_json(output/'report.json',report)
    model_order={value:index for index,value in enumerate(models or range(1,11))}
    for folder in sorted(source.glob('model_*'),key=lambda p:model_order.get(int(p.name[-2:]),99)):
        if models and int(folder.name[-2:]) not in models:continue
        started=time.monotonic();metadata=json.loads((folder/'metadata.json').read_text())
        original=cq.importers.importStep(str(folder/'original.step')).val();program=programs[folder.name]
        state=None
        try:
            if reuse_geometry:
                checkpoint=Path(reuse_geometry)
                saved=json.loads((checkpoint/'report.json').read_text())
                if saved.get('decomposition_algorithm_sha256')!=report['decomposition_algorithm_sha256']:
                    raise ValueError('Cached decomposition was created by a different geometry algorithm')
                cache=checkpoint/folder.name/'geometry';gm=json.loads((cache/'metadata.json').read_text())
                inverse={v:k for k,v in gm['component_id_map'].items()}
                from .assembly_validation import transform_part
                raw={inverse[c['name']]:transform_part(cq.importers.importStep(str(cache/c['step'])).val(),
                        c['rotation_matrix'],c['translation']) for c in gm['raw_components']}
                state=Partition(original,raw,stops=renamed(gm['stopping_conditions'],inverse),
                    cuts=gm['cuts'],checks=renamed(gm['checks'],inverse))
                validate_raw_partition(original,raw)
                elements=state.checks['constructive_elements']
                print('CACHED GEOMETRY',folder.name,len(raw),'constituents',flush=True)
            else:
                elements=history_elements(program,original)
                state=decompose_constructive(original,elements)
                print('HISTORY',folder.name,len(elements),'extrusions',flush=True)
            row=execute(state,output/folder.name,metadata['source'],geometry,design,program,geometry_only=geometry_only)
            row.update(history_operations=len(next(p['extrude_calls'] for p in provenance['programs']
                if p['model']==folder.name)),decomposition_success=True,geometry_only=geometry_only)
        except Exception as error:
            row=dict(model=folder.name,assembly_success=False,decomposition_success=False,
                     reason=f'{type(error).__name__}: {error}')
            target=output/folder.name
            # Do not lose a valid raw decomposition merely because construction
            # or export of its fasteners failed.
            if state is None:
                state=Partition(original,{'unresolved':original},stops={'unresolved':dict(reason='unresolved_history',detail=row['reason'])})
                state.checks.update(validate_raw_partition(original,state.raw),method='unresolved_history',
                    all_leaves_constant_section=False,decomposition_complete_within_search=False)
            if state.original is original and not (target/'geometry').exists():
                target.mkdir(exist_ok=True);export_geometry(state,target/'geometry',DecompositionSettings(),metadata['source'],program)
                row['components']=len(state.raw)
            if (target/'geometry/metadata.json').exists():
                gm=json.loads((target/'geometry/metadata.json').read_text());row['components']=gm['main_component_count']
            save_json((target if target.exists() else output)/f'{folder.name}_failure.json',row)
            print('FAILED',json.dumps(row,ensure_ascii=False),flush=True)
        row.update(previous_components=metadata['main_component_count'],elapsed_seconds=round(time.monotonic()-started,3))
        rows.append(row);save_json(output/'report.json',report)
    assert hashes(source)==before,'Published examples changed'
    report.update(status='complete',source_checksums=before,source_unchanged=True)
    save_json(output/'report.json',report);write_readme(output,rows)
    return rows


def write_readme(output,rows,controls=False):
    lines=['# Конструктивная декомпозиция и крепления', '',
        'Геометрия проверяется до проектирования креплений. Неудачи сборки не меняют декомпозицию. '
        'Траектории дискретные; прочность, реальное резьбовое удержание и непрерывная бесстолкновительность не доказаны.', '',
        '| Модель | Было деталей | Стало | Пазовых элементов | Болтов | Саморезов | Полностью собрана | Файлы |',
        '|---|---:|---:|---:|---:|---:|---|---|']
    for row in sorted(rows,key=lambda r:r["model"]):
        name=row['model'];target=output/name;views=[]
        if (target/'geometry').is_dir():
            views.extend([f'[исходник]({name}/geometry/original.stl)',f'[разбиение]({name}/geometry/split_exploded.stl)'])
        if row['assembly_success']:
            views.extend([f'[детали с креплениями]({name}/assembly/parts_exploded.stl)',
                          f'[сборка STL]({name}/assembly/assembly.stl)',f'[STEP]({name}/assembly/assembly.step)'])
        lines.append(f"| {name} | {row.get('previous_components','—')} | {row.get('components','?')} | "
            f"{row.get('groove_elements',0) if row['assembly_success'] else 0} | "
            f"{row.get('bolts',0) if row['assembly_success'] else 0} | {row.get('screws',0) if row['assembly_success'] else 0} | "
            f"{'да' if row['assembly_success'] else 'нет'} | {' · '.join(views)} |")
    lines.extend(['','Подробные варианты распределения перекрытий — `decomposition_report.json`, '
        'кандидаты и отказы креплений — `interface_*.json`, глобальная проверка — `assembly_report.json`. '
        'Папка `assembly/` создаётся только после проверки полного порядка сборки всех деталей и крепежа.',''])
    for row in sorted(rows,key=lambda r:r['model']):
        name=row['model'];target=output/name
        lines.extend([f'## {name}',''])
        gm=json.loads((target/'geometry/metadata.json').read_text())
        lines.extend(['До креплений: '+ ' · '.join(
            f"[{c['name']} STL]({name}/geometry/{c['stl']}) / [STEP]({name}/geometry/{c['step']})"
            for c in gm['raw_components']),''])
        if row['assembly_success']:
            am=json.loads((target/'assembly/metadata.json').read_text())
            lines.extend(['После креплений: '+ ' · '.join(
                f"[{c['name']} STL]({name}/assembly/{c['stl']}) / [STEP]({name}/assembly/{c['step']})"
                for c in am['components']),f'[Метаданные сборки]({name}/assembly/metadata.json)',''])
        else:
            lines.extend([f"Сборка: `{row['assembly_status']}`. {row.get('assembly_reason') or ''}",
                f'[Причины отказа и варианты]({name}/assembly_report.json)',''])
            if (target/'failed_export/parts_exploded.stl').exists():
                lines.extend([f'[Кандидат, не прошедший проверку экспорта]({name}/failed_export/parts_exploded.stl). '
                    'Это диагностический файл, не готовая сборка.',''])
    (output/'README.md').write_text('\n'.join(lines),encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=Path('examples/adaptive_joints'))
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--controls',action='store_true')
    parser.add_argument('--geometry-only',action='store_true',help='Persist the geometric partition without searching joints')
    parser.add_argument('--models',type=int,nargs='+')
    parser.add_argument('--reuse-geometry',type=Path,help='Validated geometric checkpoint; never reclassify or repartition it')
    parser.add_argument('--max-shaft-length',type=float,default=50.)
    parser.add_argument('--min-screw-engagement',type=float,default=10.)
    parser.add_argument('--min-feature-size',type=float,default=.1)
    parser.add_argument('--max-designs-per-pair',type=int,default=72)
    parser.add_argument('--max-assembly-states',type=int,default=128)
    parser.add_argument('--clearance',type=float,default=.2)
    parser.add_argument('--path-steps',type=int,default=16)
    args=parser.parse_args();geometry=AssemblySettings(clearance=args.clearance,path_steps=args.path_steps);geometry.validate()
    design=ConstructiveSettings(max_shaft_length=args.max_shaft_length,min_screw_engagement=args.min_screw_engagement,
        min_feature_size=args.min_feature_size,max_designs_per_pair=args.max_designs_per_pair,max_assembly_states=args.max_assembly_states)
    design.validate()
    if args.controls:controls(args.output,geometry,design)
    else:compare(args.source,args.output,geometry,design,args.models,args.geometry_only,args.reuse_geometry)


if __name__=='__main__':main()
