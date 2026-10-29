"""Twelve small, explicit constructive fixtures; no random CADGen models."""

import cadquery as cq
import numpy as np
from cadgen.constructive_decomposition import Element,decompose_constructive,cylinder
from cadgen.decomposition import Partition,validate_raw_partition


def block(x,y,z,center=(0,0,0)):
    return cq.Workplane('XY').box(x,y,z).translate(center).val()


def fixed_pair(upper,lower):
    raw=dict(a=upper,b=lower);source=upper.fuse(lower).clean();state=Partition(source,raw)
    state.checks.update(validate_raw_partition(source,raw),method='constructive_operation_volumes',
        constructive_elements={n:dict(family='cylinder' if cylinder(s) else 'prism',cylinder=cylinder(s),axis=[0,0,1])
                               for n,s in raw.items()},geometric_analyses={},geometry_limits=[],
        decomposition_complete_within_search=True)
    state.stops={n:dict(reason='prescribed_pair_for_fastening_control',analysis=dict(recognition=dict(simple=True))) for n in raw}
    return state


def from_elements(shapes,axes):
    source=shapes[0]
    for shape in shapes[1:]:source=source.fuse(shape)
    elements=[Element(f'h{i+1}',s,np.array(axis,float)) for i,(s,axis) in enumerate(zip(shapes,axes))]
    return decompose_constructive(source,elements)


def cases():
    z=[0,0,1]
    key=block(14,6,20,(15,0,10)).fuse(block(6,12,20,(19,3,10))).clean()
    yield dict(name='01_cylinder_key',state=from_elements([cq.Solid.makeCylinder(10,20),key],[z,z]),expected=2)
    yield dict(name='02_whole_key',state=from_elements([key],[z]),expected=1)
    yield dict(name='03_coaxial_cylinders',state=from_elements([
        cq.Solid.makeCylinder(12,20),cq.Solid.makeCylinder(8,20,cq.Vector(0,0,20))],[z,z]),expected=2,only='cylindrical_fit')
    yield dict(name='04_crossed_cylinders',state=from_elements([
        cq.Solid.makeCylinder(15,40),cq.Solid.makeCylinder(5,23,cq.Vector(12,0,20),cq.Vector(1,0,0))],
        [z,[1,0,0]]),expected=2,only='cylindrical_fit_transverse_bolt')
    yield dict(name='05_four_corner_tongues',state=fixed_pair(block(100,80,20,(0,0,10)),block(100,80,20,(0,0,-10))),
        expected=2,only='four_pins',profile='rectangular')
    yield dict(name='06_four_bolts',state=fixed_pair(block(100,80,20,(0,0,10)),block(100,80,20,(0,0,-10))),expected=2,only='bolted')
    yield dict(name='07_two_long_grooves',state=fixed_pair(block(120,16,20,(0,0,10)),block(120,16,20,(0,0,-10))),
        expected=2,only='two_long_grooves',profile='rectangular')
    yield dict(name='08_open_sliding_joint',state=fixed_pair(block(120,16,20,(0,0,10)),block(120,16,20,(0,0,-10))),
        expected=2,only='two_long_grooves',profile='dovetail')
    yield dict(name='09_through_bolt_nut',state=fixed_pair(block(30,24,12,(0,0,6)),block(30,24,12,(0,0,-6))),expected=2,only='bolted')
    yield dict(name='10_blind_screw',state=fixed_pair(block(30,24,8,(0,0,4)),block(30,24,20,(0,0,-10))),expected=2,only='self_tapping_screw')
    holed=block(30,24,20,(0,0,10)).cut(cq.Solid.makeCylinder(4,20))
    yield dict(name='11_simple_with_hole',state=from_elements([holed],[z]),expected=1)
    yield dict(name='12_crossing_extrusions',state=from_elements([block(100,12,12),block(12,80,12)],[[1,0,0],[0,1,0]]),expected=2)
