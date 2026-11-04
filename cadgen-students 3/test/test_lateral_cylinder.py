"""Regression for a radial saddle, loaded in its original assembly frame."""
import json
from pathlib import Path
import cadquery as cq
import numpy as np
import pytest
from cadgen.assembly_geometry import AssemblySettings, validate_connection, difference_volume
from cadgen.assembly_validation import transform_part
from cadgen.constructive_geometry import ConstructiveSettings, general_contact
from cadgen.constructive_joint_design import lateral_cylinder_grooves

ROOT=Path(__file__).resolve().parents[1]

def pair():
    root=ROOT/'examples/constructive_diagnostics/model_01'
    meta=json.loads((root/'metadata.json').read_text())
    parts={c['name']:transform_part(cq.importers.importStep(str(root/c['step'])).val(),
        c['rotation_matrix'],c['translation']) for c in meta['raw_components'] if c['name'] in ('part_5','part_6')}
    return parts['part_6'],parts['part_5']

@pytest.mark.parametrize('short',[False,True])
def test_radial_saddle_geometry_and_insertion(short,tmp_path):
    donor,receiver=pair();geometry=AssemblySettings()
    split,result=lateral_cylinder_grooves(donor,receiver,general_contact(receiver,donor),geometry,ConstructiveSettings(),short=short)
    checks=validate_connection(split,result,geometry)
    assert checks['main_geometry_preserved']
    assert result.parameters['feature_count']==(4 if short else 2)
    assert 0<result.parameters['clearance']<1
    for f in result.parameters['features']:
        assert f['profile']['opening_width']>=.5
        assert f['central_engagement_length']>=(8 if short else 20)
    assert np.dot(split.rotation[:,2],(0,0,1))>.99999
    for name,part in result.components:
        path=tmp_path/f'{name}.step';cq.exporters.export(part,str(path))
        loaded=cq.importers.importStep(str(path)).val()
        assert loaded.isValid() and len(loaded.Solids())==1
        assert difference_volume(part,loaded)<geometry.volume_tolerance


def test_small_cylinder_rejected():
    donor,receiver=pair()
    with pytest.raises(ValueError,match='too small'):
        lateral_cylinder_grooves(donor.scale(.1),receiver.scale(.1),
            general_contact(receiver.scale(.1),donor.scale(.1)),AssemblySettings(),ConstructiveSettings())


def test_detection_is_rotation_invariant():
    donor,receiver=pair()
    donor=donor.rotate((0,0,0),(1,1,0),37).translate((14,-8,11))
    receiver=receiver.rotate((0,0,0),(1,1,0),37).translate((14,-8,11))
    split,result=lateral_cylinder_grooves(donor,receiver,general_contact(receiver,donor),AssemblySettings(),ConstructiveSettings())
    assert validate_connection(split,result,AssemblySettings())['main_geometry_preserved']
    assert result.parameters['feature_count']==2


def test_search_uses_geometry_without_model_or_part_identifiers():
    from cadgen.constructive_joint_design import propose_constructive
    donor,receiver=pair()
    options=propose_constructive({'saddle':donor,'shaft':receiver},'saddle','shaft',{},
        AssemblySettings(),ConstructiveSettings(),only='lateral_cylinder_grooves')
    assert options[0].parameters['type']=='lateral_cylinder_grooves'
    assert options[0].parameters['layout']=='two_long_grooves'
    assert options[0].selection['constructive_search']['attempts']<=72
