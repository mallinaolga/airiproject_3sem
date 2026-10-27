"""Geometric leaves must survive failed or differently configured assembly."""

from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import cadquery as cq

from cadgen.assembly_geometry import AssemblySettings, GeometryRejected, difference_volume
from cadgen.decomposition import DecompositionSettings, Partition, decompose, decompose_geometry, rank_cuts, Budget, finalize_geometry
from cadgen.decomposition_assembly import assemble_partition
from cadgen.decomposition_export import export_geometry
from cadgen.auto_assembly import export_auto


def steps():
    return cq.Workplane("XY").circle(25).extrude(25).union(
        cq.Workplane("XY",origin=(0,0,25)).circle(18).extrude(25)).val()


class StageSeparationTests(unittest.TestCase):
    def test_first_stage_never_calls_joint_builders(self):
        with patch("cadgen.joint_design.propose_joints",side_effect=AssertionError("called too soon")):
            result=decompose_geometry(steps())
        self.assertEqual(len(result.raw),2)
        self.assertEqual(result.assembly["status"],"not_attempted")
        self.assertFalse(result.joints)
        self.assertTrue(result.checks["all_leaves_constant_section"])

    def test_cut_limit_does_not_prevent_final_leaf_classification(self):
        result=decompose_geometry(steps(),replace(DecompositionSettings(),max_depth=1))
        self.assertEqual(len(result.raw),2)
        self.assertTrue(result.checks["all_leaves_constant_section"])
        self.assertFalse(result.checks["decomposition_complete_within_search"])
        self.assertTrue(all(s.get("final_recognition_checked") for s in result.stops.values()))

    def test_geometric_cuts_do_not_depend_on_assembly_wall_or_clearance(self):
        shape=steps();settings=DecompositionSettings()
        a=rank_cuts(shape,AssemblySettings(),settings,Budget(5000))
        b=rank_cuts(shape,AssemblySettings(min_wall=50,clearance=.8),settings,Budget(5000))
        self.assertEqual([c.metadata() for c in a[0]],[c.metadata() for c in b[0]])
        self.assertEqual(a[1],b[1])

    def test_failed_assembly_preserves_all_fixed_geometric_constituents(self):
        result=decompose_geometry(steps());before=dict(result.raw);cuts=list(result.cuts);stops=dict(result.stops)
        with patch("cadgen.joint_design.propose_joints",side_effect=GeometryRejected("no fastener fits")):
            assemble_partition(result,42,AssemblySettings(),DecompositionSettings())
        self.assertEqual(result.assembly["status"],"failed")
        self.assertFalse(result.assembly["success"])
        self.assertEqual(result.cuts,cuts);self.assertEqual(result.stops,stops)
        self.assertEqual(set(result.raw),set(before))
        for name,shape in before.items():self.assertEqual(difference_volume(shape,result.raw[name]),0)
        self.assertFalse(result.joints);self.assertFalse(result.sequence)

    def test_thin_geometric_step_is_not_filtered_by_fastener_dimensions(self):
        shape=cq.Workplane("XY").circle(25).extrude(20).union(
            cq.Workplane("XY",origin=(0,0,20)).circle(18).extrude(3)).val()
        result=decompose_geometry(shape)
        self.assertEqual(len(result.raw),2,result.stops)
        self.assertTrue(result.checks["all_leaves_constant_section"])

    def test_geometric_exports_survive_and_ready_export_rejects_failure(self):
        state=decompose_geometry(steps());settings=DecompositionSettings()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            meta=export_geometry(state,root/"geometry",settings)
            self.assertTrue(meta["geometry_success"])
            self.assertFalse(meta["assembly_success"])
            self.assertEqual(len(list((root/"geometry").glob("part_*.stl"))),2)
            self.assertTrue((root/"geometry"/"split_exploded.stl").exists())
            with patch("cadgen.joint_design.propose_joints",side_effect=GeometryRejected("no fastener")):
                assemble_partition(state,42,AssemblySettings(),settings)
            with self.assertRaisesRegex(GeometryRejected,"all fixed geometric constituents"):
                export_auto(state,42,{},None,root/"assembly",AssemblySettings(),settings,{})
            self.assertFalse((root/"assembly").exists())
            self.assertEqual(len(list((root/"geometry").glob("part_*.stl"))),2)

    def test_successful_stage_two_uses_exactly_the_stage_one_parts(self):
        state=decompose_geometry(steps());before=dict(state.raw)
        assemble_partition(state,42,AssemblySettings(path_steps=8),DecompositionSettings())
        self.assertTrue(state.assembly["success"],state.assembly)
        self.assertEqual(set(before),set(state.raw))
        self.assertTrue(state.checks["assembly_sequence_checked"])
        self.assertEqual({n for j in state.joints for n in j.owners},set(before))
        for n,s in before.items():self.assertEqual(difference_volume(s,state.raw[n]),0)

    def test_collateral_fragments_of_one_prism_are_rejoined_geometrically(self):
        core=cq.Workplane("XY").box(80,50,20).val()
        a=cq.Workplane("XY").box(40,50,20).translate((-20,0,0)).val()
        b=cq.Workplane("XY").box(40,50,20).translate((20,0,0)).val()
        bump=cq.Solid.makeCylinder(6,15,cq.Vector(20,0,10))
        source=core.fuse(bump).clean()
        raw=dict(a=a,b=b,c=bump)
        from cadgen.section_analysis import recognize
        stops={n:dict(reason="no_meaningful_splits",analysis=dict(recognition=recognize(s,Budget(5000))[0]))
               for n,s in raw.items()}
        state=Partition(source,raw,stops=stops)
        with patch("cadgen.joint_design.propose_joints",side_effect=AssertionError("not geometry")):
            finalize_geometry(state,DecompositionSettings())
        self.assertEqual(len(state.raw),2)
        self.assertEqual(len(state.checks["geometry_merges"]),1)
        self.assertTrue(any(difference_volume(core,s)==0 for s in state.raw.values()))
        self.assertEqual(state.checks["raw_reconstruction_error_volume"],0)


if __name__=="__main__":unittest.main()
