"""Regression controls for exterior-section recognition, not face counts."""

import unittest

import cadquery as cq
import numpy as np

from cadgen.assembly_geometry import AssemblySettings, difference_volume
from cadgen.assembly_validation import overlap_volume
from cadgen.decomposition import Budget, DecompositionSettings, decompose, decompose_geometry, rank_cuts, union
from cadgen.assembly_source import decomposition_history


def box(x, y, h, z=0, x0=0):
    return cq.Workplane("XY").box(x, y, h, centered=(True, True, False)).translate((x0, 0, z)).val()


def cylinders(radii=(25, 18), heights=None):
    heights = heights or [25]*len(radii)
    z, parts = 0, []
    for r, h in zip(radii, heights):
        parts.append(cq.Workplane("XY").circle(r).extrude(h).translate((0, 0, z)).val())
        z += h
    return union(parts).clean()


def key():
    return cq.Workplane("XY").circle(24).extrude(32).union(
        cq.Workplane("XY").center(30, 0).rect(60, 14).extrude(32)).val().clean()


def l_prism():
    return cq.Workplane("XY").polyline([(0,0),(60,0),(60,18),(20,18),(20,52),(0,52)]).close().extrude(35).val()


class SectionDecompositionTests(unittest.TestCase):
    geometry = AssemblySettings(path_steps=8)
    settings = DecompositionSettings()

    def assert_simple(self, shape):
        candidates, analysis = rank_cuts(shape, self.geometry, self.settings, Budget(5000))
        self.assertEqual(candidates, [], analysis)
        self.assertEqual(analysis["reason"], "constant_outer_section", analysis)
        state = decompose(shape, 42, self.geometry, self.settings)
        self.assertEqual(len(state.raw), 1, state.stops)
        self.assertLess(difference_volume(shape, union(state.raw.values())), 1e-5)

    def assert_partition(self, shape, count, normal, levels):
        state = decompose(shape, 42, self.geometry, self.settings)
        self.assertEqual(len(state.raw), count, state.stops)
        self.assertLess(difference_volume(shape, union(state.raw.values())), 1e-5)
        for cut in state.cuts:
            plane = cut["selected"]["plane"]
            self.assertGreater(abs(np.dot(plane["normal"], normal)), .99999)
            self.assertLess(min(abs(np.dot(plane["origin"], normal)-z) for z in levels), 1e-5)
        for i, a in enumerate(state.raw.values()):
            for b in list(state.raw.values())[i+1:]:
                self.assertLess(overlap_volume(a, b), 1e-5)
        self.assertTrue(state.checks["assembly_sequence_checked"])
        return state

    def test_key_and_l_are_single_extrusions(self):
        for shape in (key(), l_prism()):
            with self.subTest(faces=len(shape.Faces())): self.assert_simple(shape)

    def test_cylinder_and_half_cylinder_are_single_extrusions(self):
        for shape in (cylinders((25,)), cylinders((25,)).intersect(box(60,30,25,x0=0).translate((0,15,0)))):
            self.assert_simple(shape)

    def test_many_sided_long_prism_keeps_its_extrusion_axis(self):
        shape = cq.Workplane("XY").polygon(40,60).extrude(1000).val()
        self.assert_simple(shape.rotate((0,0,0),(1,2,3),37).translate((80,-40,20)))

    def test_two_coaxial_steps(self):
        self.assert_partition(cylinders(), 2, (0,0,1), [25])

    def test_three_coaxial_steps(self):
        self.assert_partition(cylinders((30,24,18)), 3, (0,0,1), [25,50])

    def test_rectangular_steps(self):
        self.assert_partition(box(80,70,25).fuse(box(56,46,25,25),box(30,28,25,50)).clean(),
                              3, (0,0,1), [25,50])

    def test_holes_are_preserved_and_do_not_cause_splits(self):
        shape = box(80,70,40)
        for x in (-22,0,22):
            shape = shape.cut(cq.Workplane("XY").center(x,0).circle(5).extrude(40).val())
        self.assert_simple(shape)
        transverse = cq.Solid.makeCylinder(6, 80, cq.Vector(-40,0,20), cq.Vector(1,0,0))
        self.assert_simple(shape.cut(transverse))
        self.assert_simple(cylinders((25,)).cut(cq.Solid.makeCylinder(6,25)))
        blind = box(80,70,40).cut(cq.Solid.makeCylinder(6,20,cq.Vector(0,0,20)))
        self.assert_simple(blind)

    def test_rotated_translated_prism_and_steps(self):
        self.assert_simple(key().rotate((0,0,0),(1,2,3),37).translate((80,-40,20)))
        shape = cylinders((30,24,18)).rotate((0,0,0),(1,2,3),37).translate((80,-40,20))
        state = decompose(shape,42,self.geometry,self.settings)
        self.assertEqual(len(state.raw),3,state.stops)
        self.assertLess(difference_volume(shape,union(state.raw.values())),1e-5)

    def test_rectangular_transverse_and_blind_holes(self):
        transverse = cq.Workplane("YZ").rect(12,14).extrude(80).translate((-40,0,20)).val()
        self.assert_simple(box(80,70,40).cut(transverse))
        blind = cq.Workplane("XY",origin=(0,0,20)).rect(12,14).extrude(20).val()
        self.assert_simple(box(80,70,40).cut(blind))

    def test_history_suggests_planes_but_does_not_force_them(self):
        history = decomposition_history(dict(cad=dict(planes=[dict(axis=2,origin=0)],cs=[
            dict(plane=0,op=dict(type="TwoExtrudes",first=dict(extent=25),
                 second=dict(extent=25),second_normal_offset=25)),
            dict(plane=0,op=dict(type="Unrecognized"))])))
        self.assertEqual(len(history["operations"]),2)
        self.assertEqual(len(history["unsupported"]),1)
        candidates, analysis = rank_cuts(cylinders((25,),[50]),self.geometry,self.settings,
                                         Budget(5000),history)
        self.assertFalse(candidates,analysis)
        self.assertTrue(analysis["recognition"]["simple"])

    def test_external_notch_is_not_filled_as_a_hole(self):
        shape = box(80,70,40).cut(cq.Solid.makeCylinder(12,20,cq.Vector(37,0,20)))
        candidates, analysis = rank_cuts(shape,self.geometry,self.settings,Budget(5000))
        self.assertFalse(analysis["recognition"]["simple"])
        self.assertFalse(analysis["recognition"]["ignored_bores"])
        self.assertTrue(candidates,analysis)

    def test_different_extrusion_directions(self):
        main = box(80,60,25)
        arm = cq.Solid.makeCylinder(15,45,cq.Vector(0,0,25),cq.Vector(1,0,0))
        shape = main.fuse(arm).clean()
        state = decompose_geometry(shape,self.settings)
        self.assertGreaterEqual(len(state.raw),2,state.stops)
        self.assertLess(difference_volume(shape,union(state.raw.values())),1e-5)
        self.assertTrue(state.checks["geometric_partition_valid"])
        self.assertEqual(state.assembly["status"],"not_attempted")

    def test_same_area_different_outer_contours_are_not_constant(self):
        shape = box(60,40,25).fuse(box(48,50,25,25,x0=14)).clean()
        candidates, analysis = rank_cuts(shape,self.geometry,self.settings,Budget(5000))
        self.assertNotEqual(analysis.get("reason"),"constant_outer_section")
        self.assertTrue(candidates,analysis)
        self.assertTrue(any(c.metrics["contour_transition"]>.1 for c in candidates))

    def test_taper_is_unresolved_instead_of_declared_simple(self):
        shape = cq.Solid.makeCone(25,15,50)
        state = decompose(shape,42,self.geometry,self.settings)
        self.assertEqual(len(state.raw),1)
        self.assertEqual(state.stops["p"]["reason"],"unresolved_geometry")


if __name__ == "__main__": unittest.main()
