"""Small, thin, asymmetric and obstructed joint regression fixtures."""

from dataclasses import replace
import random
import unittest
from unittest.mock import patch

import cadquery as cq
import numpy as np

from cadgen.adaptive_joints import (JointSearchRejected, adaptive_clearance, contact_centers,
                                   local_settings, material_depth)
from cadgen.assembly_geometry import (AssemblySettings, GeometryRejected, Split, build_groove,
                                     build_bolted, contact_patch, validate_connection)
from cadgen.assembly_validation import transform_part, overlap_volume
from cadgen.joint_design import materialize, propose_joints
from cadgen.assembly_planning import validate_partition
from generirovanie_pazov.generate_grooves import PROFILE_TYPES


def box(x,y,z,center=(0,0,0)):
    return cq.Workplane("XY").box(x,y,z).translate(center).val()


def fixture(x=2.,y=3.,lower=.8,upper=.5):
    a=box(x,y,lower,(0,0,-lower/2));b=box(x,y,upper,(0,0,upper/2))
    return Split(a.fuse(b).clean(),a,b,np.eye(3),np.zeros(3),{})


class AdaptiveJointTests(unittest.TestCase):
    def setUp(self):
        self.geometry=AssemblySettings(path_steps=8)

    def test_submillimeter_features_and_all_shared_profiles(self):
        split=fixture()
        for kind in PROFILE_TYPES:
            with self.subTest(kind=kind):
                options=propose_joints(split,("upper","lower"),"j1",42,self.geometry,
                                       connection="groove",profile=kind)
                joint=options[0]
                self.assertEqual(joint.parameters["profile"]["kind"],kind)
                self.assertLess(joint.parameters["profile"]["depth"],1)
                self.assertLess(joint.parameters["clearance"],.05)
                self.assertGreater(joint.parameters["local_material_margin"],0)
                raw=dict(upper=split.upper,lower=split.lower)
                parts=materialize(raw,[joint],self.geometry)
                checks,sequence=validate_partition(split.original,raw,parts,[joint],self.geometry,128)
                self.assertTrue(checks["assembly_sequence_checked"])
                self.assertEqual(len(sequence),2)

    def test_large_min_wall_is_not_a_minimum_feature_dimension(self):
        split=fixture()
        a=propose_joints(split,("u","l"),"j",42,self.geometry,connection="groove")[0]
        b=propose_joints(split,("u","l"),"j",42,replace(self.geometry,min_wall=30),connection="groove")[0]
        self.assertEqual(a.parameters["profile"],b.parameters["profile"])
        self.assertEqual(a.parameters["clearance"],b.parameters["clearance"])

    def test_tiny_component_is_not_compared_with_pair_volume(self):
        lower=box(60,60,20,(0,0,-10));upper=box(1.2,2,.25,(0,0,.125))
        split=Split(lower.fuse(upper),lower,upper,np.eye(3),np.zeros(3),{})
        options=propose_joints(split,("u","l"),"j",42,self.geometry,connection="groove")
        self.assertTrue(options)
        self.assertLess(upper.Volume()/split.original.Volume(),.001)

    def test_round_profile_on_tiny_cylinder(self):
        lower=cq.Solid.makeCylinder(.6,.5,cq.Vector(0,0,-.5))
        upper=cq.Solid.makeCylinder(.6,.4)
        split=Split(lower.fuse(upper),lower,upper,np.eye(3),np.zeros(3),{})
        options=propose_joints(split,("u","l"),"j",42,self.geometry,connection="groove")
        self.assertIn("round",[o.parameters["profile"]["kind"] for o in options])

    def test_failed_large_feature_is_shrunk_before_rejection(self):
        from cadgen.adaptive_joints import build_groove as actual
        tried=[]
        def limited_depth(*args,**kwargs):
            tried.append(kwargs["footprint"]["depth"])
            if kwargs["footprint"]["depth"]>.1:
                raise GeometryRejected("synthetic local obstruction")
            return actual(*args,**kwargs)
        with patch("cadgen.adaptive_joints.build_groove",side_effect=limited_depth):
            options=propose_joints(fixture(),("u","l"),"j",42,self.geometry,connection="groove")
        self.assertTrue(any(d>.1 for d in tried))
        self.assertTrue(any(d<=.1 for d in tried))
        self.assertLess(options[0].selection["scale_factor"],1)

    def test_long_thin_parts_have_small_valid_joints(self):
        split=fixture(.25,12,.15,.15)
        options=propose_joints(split,("u","l"),"j",42,self.geometry,connection="groove")
        self.assertLess(options[0].parameters["profile"]["depth"],.15)
        self.assertGreater(options[0].parameters["transferred_volume"],0)

    def test_clearance_scales_and_zero_is_preserved(self):
        self.assertAlmostEqual(adaptive_clearance(.2,1),.04)
        self.assertEqual(adaptive_clearance(.2,20),.2)
        self.assertEqual(adaptive_clearance(0,1),0)
        for value in (-.1,1,float("nan")):
            with self.assertRaises(ValueError):adaptive_clearance(value,1)

    def test_profiles_continue_after_preferred_profile_fails(self):
        from cadgen.adaptive_joints import build_groove as actual
        attempted=[]
        def reject_first(*args,**kwargs):
            kind=args[3];attempted.append(kind)
            if kind=="rectangular":raise GeometryRejected("synthetic preferred-profile obstruction")
            return actual(*args,**kwargs)
        with patch("cadgen.adaptive_joints.build_groove",side_effect=reject_first):
            options=propose_joints(fixture(),("u","l"),"j",42,self.geometry,connection="groove")
        self.assertEqual(set(attempted),set(PROFILE_TYPES))
        self.assertTrue(options)
        self.assertNotIn("rectangular",[j.parameters["profile"]["kind"] for j in options])

    def test_face_samples_avoid_holes_and_cover_off_center_material(self):
        lower=box(8,8,1,(0,0,-.5)).cut(cq.Solid.makeCylinder(2,3,cq.Vector(0,0,-1.5)))
        upper=lower.translate((0,0,1))
        patch_shape=contact_patch(lower,upper)
        face=max(patch_shape.Faces(),key=lambda f:f.Area())
        centers=contact_centers(face,12)
        self.assertTrue(centers)
        for center,radius in centers:
            self.assertGreater(np.linalg.norm(center),2)
            self.assertGreater(radius,0)
        split=Split(lower.fuse(upper),lower,upper,np.eye(3),np.zeros(3),{})
        joint=propose_joints(split,("u","l"),"j",42,self.geometry,connection="groove")[0]
        parts=materialize(dict(u=upper,l=lower),[joint],self.geometry)
        hole=cq.Solid.makeCylinder(2,2,cq.Vector(0,0,-1))
        for s in parts.values():self.assertLess(overlap_volume(s,hole),1e-8)

    def test_contact_normals_reliably_point_out_of_first_solid(self):
        split=fixture()
        for a,b in ((split.lower,split.upper),(split.upper,split.lower)):
            f=contact_patch(a,b).Faces()[0];p=f.Center();n=f.normalAt()
            self.assertFalse(a.isInside(p+n*.0001))
            self.assertTrue(a.isInside(p-n*.0001))

    def test_ray_depth_stops_at_internal_void_not_far_bbox(self):
        s=box(4,4,3,(0,0,-1.5)).cut(box(2,2,1,(0,0,-1.5)))
        self.assertAlmostEqual(material_depth(s,(0,0),(0,0,-1)),1.,places=6)

    def test_oversized_cavity_and_disconnected_receiver_rejected(self):
        split=fixture()
        settings=local_settings(self.geometry,.2,(split.lower,split.upper))
        with self.assertRaises(GeometryRejected):
            build_groove(split,random.Random(42),settings,"rectangular",centers=[(.95,0)],
                         footprint=dict(width=2.,depth=.7,length=2.,anchor_depth=.2),adaptive=True)

    def test_proportional_small_bolt_is_valid_and_insertable(self):
        split=fixture(3,3,1,1)
        settings=local_settings(self.geometry,.4,(split.lower,split.upper))
        connection=build_bolted(split,random.Random(42),settings,centers=[(0,0)],adaptive=True,diameter=.4)
        checks=validate_connection(split,connection,settings)
        self.assertTrue(checks["main_geometry_preserved"])
        self.assertEqual(connection.parameters["shaft_diameter"],.4)
        self.assertGreater(connection.parameters["head_bearing_area"],0)

    def test_auto_prioritizes_grooves_and_attempts_bolts_after_failure(self):
        split=fixture(3,3,1,1)
        options=propose_joints(split,("u","l"),"j",42,self.geometry)
        self.assertTrue(all(j.parameters["type"]=="groove" for j in options))
        with patch("cadgen.adaptive_joints.build_groove",side_effect=GeometryRejected("no groove")):
            options=propose_joints(split,("u","l"),"j",42,self.geometry)
        self.assertTrue(all(j.parameters["type"]=="bolted" for j in options))


if __name__=="__main__":unittest.main()
