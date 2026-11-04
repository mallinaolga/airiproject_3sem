"""Reproducible common CADGen corpus. Run with the chosen checkout on PYTHONPATH."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil
import cadquery as cq
from cadgen.assembly_source import generate_source
from cadgen.assembly_geometry import require_solid, difference_volume

def save(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False))

def prepare(root):
    source=root/'sources';source.mkdir(parents=True,exist_ok=False)
    old=Path('examples/adaptive_joints')
    provenance=json.loads((old/'cadgen_overlap_provenance.json').read_text())
    shapes=[];manifest=[];failures=[]
    for i in range(1,101):
        name=f'model_{i:02d}';folder=source/name;folder.mkdir()
        if i<=10:
            for filename in ('original.step','original.stl','metadata.json'):
                shutil.copy2(old/name/filename,folder/filename)
            shape=cq.importers.importStep(str(folder/'original.step')).val()
            calls=next(p['extrude_calls'] for p in provenance['programs'] if p['model']==name)
            program='from cadgen.extrude import extrude\nr=None\n'+'\n'.join('r='+c['source'] for c in calls)+'\n'
            seed=None
        else:
            # Seeds are fixed before assembly outcomes exist. Rejections here
            # concern only invalid/duplicate sources, never assembly success.
            for attempt in range(100):
                seed=100000+i*100+attempt
                try:
                    shape,params,program=generate_source(seed,complexity='decomposition')
                    require_solid(shape,'benchmark source')
                    if any(abs(shape.Volume()-s.Volume())<1e-5 and difference_volume(shape,s)<1e-5 for s in shapes):
                        raise ValueError('duplicate source geometry')
                    break
                except Exception as error:
                    failures.append(dict(model=name,seed=seed,reason=str(error)));save(root/'generation_rejections.json',failures)
            else:raise RuntimeError(f'No valid distinct source for {name}')
            cq.exporters.export(shape,str(folder/'original.step'))
            cq.exporters.export(shape,str(folder/'original.stl'))
            save(folder/'metadata.json',dict(source=params,main_component_count=None,seed=seed))
            calls=[dict(line=n.lineno,source=ast.get_source_segment(program,n.value)) for n in ast.parse(program).body
                if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='r' for t in n.targets)
                and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='extrude']
            provenance['programs'].append(dict(model=name,extrude_calls=calls))
        require_solid(shape,'benchmark source')
        if any(abs(shape.Volume()-s.Volume())<1e-5 and difference_volume(shape,s)<1e-5 for s in shapes):
            raise ValueError(f'duplicate source: {name}')
        shapes.append(shape);(folder/'original.py').write_text(program)
        # Keep full history, so unsupported operations are not silently dropped.
        (folder/'history.py').write_text(program)
        manifest.append(dict(model=name,seed=seed,sha256=hashlib.sha256((folder/'original.step').read_bytes()).hexdigest(),volume=shape.Volume()))
        save(source/'manifest.json',manifest);save(source/'cadgen_overlap_provenance.json',provenance)
        print('SOURCE',name,seed,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();args.root.mkdir(parents=True,exist_ok=True);prepare(args.root)
