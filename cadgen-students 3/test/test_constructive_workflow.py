import json
import cadquery as cq
from cadgen.constructive_workflow import compare
from cadgen.assembly_geometry import AssemblySettings
from cadgen.constructive_geometry import ConstructiveSettings
from cadgen.extrude import extrude


def test_model_100_and_explicit_history_are_processed(tmp_path):
    source=tmp_path/'sources';source.mkdir();programs=[]
    for number in (100,1):
        folder=source/f'model_{number:02d}';folder.mkdir()
        shape=extrude(None,(0,0,0),'XY','rect(20,20)',10).val()
        cq.exporters.export(shape,str(folder/'original.step'))
        (folder/'metadata.json').write_text(json.dumps(dict(source={'test':True},main_component_count=1)))
        (folder/'history.py').write_text("r=None\nr=extrude(r,(0,0,0),'XY','rect(20,20)',10)\n")
        programs.append(dict(model=folder.name,extrude_calls=[]))
    (source/'cadgen_overlap_provenance.json').write_text(json.dumps(dict(programs=programs)))
    rows=compare(source,tmp_path/'result',AssemblySettings(),ConstructiveSettings())
    assert [r['model'] for r in rows]==['model_01','model_100']
    assert all(r['decomposition_success'] and r['assembly_success'] for r in rows)
    assert all(r['history_operations']==1 and r['components']==1 for r in rows)
