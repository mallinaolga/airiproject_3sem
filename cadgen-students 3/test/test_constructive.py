"""Logical ownership, distributed features, true cylinders and hardware limits."""

from dataclasses import replace
import unittest
import cadquery as cq
import numpy as np

from constructive_controls import cases,fixed_pair,block
from cadgen.assembly_geometry import AssemblySettings,GeometryRejected,Split,difference_volume
from cadgen.constructive_assembly import assemble_constructive
from cadgen.constructive_geometry import ConstructiveSettings
from cadgen.constructive_decomposition import history_elements,decompose_constructive
from cadgen.constructive_fasteners import fasten


class ConstructiveControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results={}
        for case in cases():
            state=case['state']
            assemble_constructive(state,AssemblySettings(path_steps=8),only=case.get('only'),profile=case.get('profile'))
            cls.results[case['name']]=(case,state)

    def check(self,index):
        name=next(n for n in self.results if n.startswith(f'{index:02d}_'))
        case,state=self.results[name]
        self.assertEqual(len(state.raw),case['expected'])
        self.assertTrue(state.checks['geometric_partition_valid'])
        self.assertTrue(state.assembly['success'],state.assembly)
        return state

    def test_cylinder_and_key_remain_two_whole_elements(self):self.check(1)
    def test_whole_key_is_one_element(self):self.check(2)
    def test_coaxial_fit_is_full_cylinder(self):
        state=self.check(3)
        f=state.joints[0].parameters['features'][0]
        self.assertEqual(f['type'],'cylindrical_fit');self.assertTrue(f['full_cylinder_not_round_profile'])
        self.assertGreater(f['pin_radius'],3)
    def test_crossed_cylinders_have_fit_and_transverse_bolt(self):
        state=self.check(4);j=state.joints[0]
        self.assertEqual(j.parameters['type'],'cylindrical_fit_transverse_bolt')
        self.assertGreater(len(j.hardware),1)
        self.assertTrue(j.parameters['features'][0]['crossed_axes'])
    def test_four_spread_tongues(self):
        state=self.check(5);p=state.joints[0].parameters
        self.assertEqual(p['feature_count'],4)
        self.assertEqual(p['layout'],'four_pins')
        self.assertEqual(len({tuple(f['center_in_cut_frame']) for f in p['features']}),4)
    def test_four_bolts_are_a_first_class_layout(self):
        state=self.check(6);self.assertEqual(state.joints[0].parameters['bolts'],4)
    def test_long_grooves_do_not_use_inscribed_circle_length(self):
        state=self.check(7);features=state.joints[0].parameters['features']
        self.assertEqual(len(features),2)
        self.assertTrue(all(f['central_engagement_length']>80 for f in features))
        self.assertTrue(all(f['central_engagement_length']>20*f['profile']['opening_width'] for f in features))
    def test_open_dovetails_have_longitudinal_checked_path(self):
        state=self.check(8)
        self.assertTrue(all(f['open_ends']=='both' for f in state.joints[0].parameters['features']))
        self.assertTrue(state.checks['assembly_sequence_checked'])
    def test_through_holes_use_nuts_without_ten_mm_rule(self):
        state=self.check(9)
        self.assertTrue(any('_nut_' in n for j in state.joints for n,_ in j.hardware))
        self.assertTrue(all(f['second_part_engagement_mm'] is None for j in state.joints for f in j.parameters['features']))
    def test_blind_screw_has_ten_mm_actual_engagement(self):
        state=self.check(10)
        self.assertTrue(all(f['second_part_engagement_mm']>=10 for j in state.joints for f in j.parameters['features']))
        self.assertTrue(all(f['shaft_length']<=50 for j in state.joints for f in j.parameters['features']))
        self.assertFalse(any('_nut_' in n for j in state.joints for n,_ in j.hardware))
    def test_hole_does_not_split_simple_element(self):
        state=self.check(11);self.assertEqual(len(state.raw),1)
        bore=cq.Solid.makeCylinder(4,20)
        self.assertLess(next(iter(state.raw.values())).intersect(bore).Volume(),1e-5)
    def test_crossed_extrusions_are_locally_allocated(self):
        state=self.check(12)
        self.assertFalse(state.checks['global_planes_through_neighbours_used'])
        self.assertIn('local_overlap_halflap',state.checks['constructive_allocations'][0]['selected'])
    def test_every_success_has_complete_main_and_hardware_sequence(self):
        for _,state in self.results.values():
            expected=set(state.raw)|{n for j in state.joints for n,_ in j.hardware}
            self.assertEqual({s['component'] for s in state.sequence},expected)
    def test_geometry_ignores_impossible_hardware_settings(self):
        case=next(c for c in cases() if c['name'].startswith('03'))
        before=dict(case['state'].raw)
        assemble_constructive(case['state'],AssemblySettings(path_steps=8),ConstructiveSettings(max_shaft_length=11,min_screw_engagement=10),only='bolted')
        for n,s in before.items():self.assertEqual(difference_volume(s,case['state'].raw[n]),0.)
    def test_shaft_cap_and_blind_engagement_are_enforced(self):
        state=fixed_pair(block(20,20,30,(0,0,15)),block(20,20,30,(0,0,-15)))
        split=Split(state.original,state.raw['b'],state.raw['a'],np.eye(3),np.zeros(3),{})
        with self.assertRaisesRegex(GeometryRejected,'exceeds'):
            fasten(split,[(0,0)],2,AssemblySettings(),ConstructiveSettings())
        result=fasten(split,[(0,0)],2,AssemblySettings(),ConstructiveSettings(max_shaft_length=80))
        self.assertGreater(result.parameters['features'][0]['shaft_length'],50)
        shallow=fixed_pair(block(20,20,5,(0,0,2.5)),block(20,20,6,(0,0,-3)))
        split=Split(shallow.original,shallow.raw['b'],shallow.raw['a'],np.eye(3),np.zeros(3),{})
        with self.assertRaisesRegex(GeometryRejected,'engagement'):
            fasten(split,[(0,0)],2,AssemblySettings(),ConstructiveSettings(),'self_tapping_screw')
    def test_literal_history_replay_is_brep_verified(self):
        source=block(20,20,10,(0,0,5))
        program="r=None\nr=extrude(r,(0,0,0),'XY','rect(20,20)',10)\n"
        elements=history_elements(program,source)
        self.assertEqual(len(elements),1)
        self.assertEqual(len(decompose_constructive(source,elements).raw),1)
        with self.assertRaises(GeometryRejected):history_elements(program,block(21,20,10,(0,0,5)))
    def test_reverse_history_preserves_the_whole_cylinder(self):
        from cadgen.constructive_decomposition import Element
        cylinder=cq.Solid.makeCylinder(10,20)
        key=block(14,6,20,(15,0,10))
        state=decompose_constructive(cylinder.fuse(key),[
            Element('key',key,np.array([0.,0.,1.])),Element('cyl',cylinder,np.array([0.,0.,1.]))])
        self.assertEqual(len(state.raw),2)
        self.assertTrue(any(difference_volume(s,cylinder)<1e-5 for s in state.raw.values()))
    def test_service_ribbon_is_not_a_new_tiny_joint(self):
        from cadgen.constructive_joint_design import propose_constructive
        state=fixed_pair(block(30,20,10,(29.9995,0,5)),block(30,20,10,(0,0,-5)))
        with self.assertRaises(GeometryRejected) as caught:
            propose_constructive(state.raw,'a','b',state.checks['constructive_elements'],AssemblySettings(),ConstructiveSettings())
        self.assertTrue(any('service-overlap' in r['reason'] for r in caught.exception.report['rejected']))
    def test_redundant_parallel_prisms_merge_without_fragmentation(self):
        from cadgen.constructive_decomposition import Element
        a=block(20,20,10,(0,0,5));b=block(20,20,10,(0,0,15))
        state=decompose_constructive(a.fuse(b),[Element('a',a,np.array([0.,0.,1.])),Element('b',b,np.array([0.,0.,1.]))])
        self.assertEqual(len(state.raw),1)
        self.assertEqual(len(state.checks['constructive_merges']),1)
    def test_mid_shaft_coaxial_step_is_not_an_annular_sleeve(self):
        from cadgen.constructive_decomposition import Element
        shaft=cq.Solid.makeCylinder(7,60,cq.Vector(0,0,-30))
        middle=cq.Solid.makeCylinder(10,12,cq.Vector(0,0,-6))
        state=decompose_constructive(shaft.fuse(middle),[
            Element('shaft',shaft,np.array([0.,0.,1.])),Element('step',middle,np.array([0.,0.,1.]))])
        self.assertEqual(len(state.raw),3)
        self.assertTrue(any(difference_volume(s,middle)<1e-5 for s in state.raw.values()))
        self.assertEqual(state.checks['constructive_allocations'][0]['selected'],'natural_coaxial_step_ownership')
    def test_mid_prismatic_step_keeps_three_natural_regions(self):
        from cadgen.constructive_decomposition import Element
        shaft=block(10,12,60);step=block(16,18,12)
        state=decompose_constructive(shaft.fuse(step),[
            Element('shaft',shaft,np.array([0.,0.,1.])),Element('step',step,np.array([0.,0.,1.]))])
        self.assertEqual(len(state.raw),3)
        self.assertTrue(any(difference_volume(s,step)<1e-5 for s in state.raw.values()))
        self.assertEqual(state.checks['constructive_allocations'][0]['selected'],'natural_prismatic_step_ownership')
    def test_design_settings_reject_invalid_limits(self):
        for design in (ConstructiveSettings(max_shaft_length=0),ConstructiveSettings(min_screw_engagement=60)):
            with self.assertRaises(ValueError):design.validate()

    def test_failed_section_analysis_does_not_discard_partition(self):
        from unittest.mock import patch
        from cadgen.constructive_decomposition import Element
        shape=block(10,12,20)
        with patch('cadgen.constructive_decomposition.recognize',side_effect=ValueError('nonplanar contour')):
            state=decompose_constructive(shape,[Element('body',shape,np.array([0.,0.,1.]))])
        self.assertTrue(state.checks['geometric_partition_valid'])
        self.assertFalse(state.stops['body']['analysis']['recognition']['simple'])
        self.assertEqual(state.stops['body']['analysis']['recognition']['reason'],'recognition_error')


class ConstructiveRanking(unittest.TestCase):
    def test_unrestricted_search_ranks_distributed_and_long_layouts(self):
        for width,length,layout in ((100,80,'four_pins'),(16,120,'two_long_grooves')):
            with self.subTest(layout=layout):
                state=fixed_pair(block(width,length,20,(0,0,10)),block(width,length,20,(0,0,-10)))
                assemble_constructive(state,AssemblySettings(path_steps=8))
                self.assertTrue(state.assembly['success'])
                self.assertEqual(state.joints[0].parameters['layout'],layout)
                search=state.joints[0].selection['constructive_search']
                self.assertGreater(search['valid_designs'],1)
                self.assertTrue(search['first_success_not_automatically_selected'])


class ConstructiveServiceCaps(unittest.TestCase):
    def test_service_end_caps_are_material_not_separate_components(self):
        from cadgen.constructive_decomposition import Element
        shaft=cq.Solid.makeCylinder(7,20)
        middle=cq.Solid.makeCylinder(10,19.999,cq.Vector(0,0,.0005))
        original=shaft.fuse(middle)
        state=decompose_constructive(original,[Element('shaft',shaft,np.array([0.,0.,1.])),
            Element('step',middle,np.array([0.,0.,1.]))])
        self.assertEqual(len(state.raw),1)
        self.assertLessEqual(difference_volume(original,next(iter(state.raw.values()))),1e-5)
        self.assertEqual(state.checks['constructive_allocations'][0]['steps'][0]['service_end_caps_absorbed'],2)


if __name__=='__main__':unittest.main()
