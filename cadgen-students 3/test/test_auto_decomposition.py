"""Geometry, joint graph, complete assembly order and four-view regression tests."""

from dataclasses import asdict, replace
from itertools import combinations
import json
from pathlib import Path
import tempfile
import unittest

import cadquery as cq
import numpy as np
import trimesh

from cadgen.assembly_geometry import AssemblySettings, GeometryRejected, difference_volume, split_model
from cadgen.assembly_validation import overlap_volume, transform_part
from cadgen.decomposition import Budget, DecompositionSettings, decompose, rank_cuts
from cadgen.joint_design import materialize, propose_joints
from cadgen.assembly_planning import assembly_graph, find_sequence, validate_partition, union
from cadgen.auto_assembly import export_auto, export_examples, generate_auto_batch
from generirovanie_pazov.generate_grooves import PROFILE_TYPES


def block(dimensions, center=(0,0,0)):
    return cq.Workplane("XY").box(*dimensions).translate(center).val()


def neck(width=12):
    return block((25,30,30),(-25,0,0)).fuse(
        block((25,30,30),(25,0,0)),block((40,width,width))).clean()


def chain():
    return block((25,30,30),(-40,0,0)).fuse(block((25,30,30)),
        block((25,30,30),(40,0,0)),block((80,12,12))).clean()


def steps():
    return block((80,70,20),(0,0,-10)).fuse(block((50,40,25),(5,0,12.5)),
        block((25,24,20),(8,2,35))).clean()


class DecompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.geometry=AssemblySettings(path_steps=8)
        cls.settings=DecompositionSettings()
        cls.state=decompose(steps(),42,cls.geometry,cls.settings)

    def test_narrow_bridge_is_detected_by_sections(self):
        candidates,analysis=rank_cuts(neck(),self.geometry,self.settings,Budget(5000))
        self.assertTrue(candidates,analysis)
        self.assertTrue(any(c.metrics["neck_contrast"]>.3 or c.metrics["area_transition"]>.3 for c in candidates))
        self.assertGreater(candidates[0].score,self.settings.min_score)

    def test_step_boundary_and_real_simplicity_gain(self):
        candidates,_=rank_cuts(steps(),self.geometry,self.settings,Budget(5000))
        self.assertTrue(candidates)
        self.assertTrue(any(abs(c.split.rotation[:,2][2])>.99 and
                            min(abs(c.split.origin[2]-z) for z in (0,25))<1e-6
                            for c in candidates))
        self.assertTrue(any(c.metrics["simplicity_gain"]>=self.settings.min_simplicity_gain for c in candidates))

    def test_no_fixed_component_target_and_no_pointless_box_cut(self):
        self.assertFalse(any("parts" in name for name in asdict(self.settings)))
        simple=decompose(block((60,50,40)),42,self.geometry,self.settings)
        self.assertEqual(len(simple.raw),1)
        self.assertEqual(simple.stops["p"]["reason"],"no_meaningful_splits")
        self.assertGreaterEqual(len(self.state.raw),3)

    def test_recursive_partition_reconstructs_source_before_fasteners(self):
        state=self.state
        self.assertEqual(len(state.cuts),len(state.raw)-1)
        self.assertLess(difference_volume(state.original,union(state.raw.values())),1e-5)
        for s in state.raw.values():
            self.assertTrue(s.isValid());self.assertEqual(len(s.Solids()),1)
            self.assertGreaterEqual(s.Volume(),self.settings.min_component_volume)
        for a,b in combinations(state.raw.values(),2):self.assertLess(overlap_volume(a,b),1e-5)

    def test_rotated_and_translated_geometry(self):
        original=neck().rotate((0,0,0),(1,2,3),37).translate((80,-40,20))
        state=decompose(original,42,self.geometry,self.settings)
        self.assertGreaterEqual(len(state.raw),2)
        self.assertLess(difference_volume(original,union(state.raw.values())),1e-5)
        self.assertTrue(state.checks["geometric_partition_valid"])
        self.assertFalse(state.assembly["success"])
        self.assertFalse(state.sequence)

    def test_technical_limits_are_separate_from_geometric_stops(self):
        for options in ({"max_operations":1},{"max_candidates":1},{"max_depth":1}):
            with self.subTest(options=options):
                state=decompose(chain(),42,self.geometry,replace(self.settings,**options))
                self.assertTrue(state.checks.get("geometry_limits") or
                                "technical_limit_reached" in [v["reason"] for v in state.stops.values()])
                self.assertFalse(state.checks["decomposition_complete_within_search"])

    def test_small_neck_has_no_feasible_fastener(self):
        state=decompose(neck(6),42,self.geometry,replace(self.settings,min_component_size=4))
        self.assertEqual(len(state.raw),3)
        self.assertTrue(state.checks["all_leaves_constant_section"])
        self.assertFalse(state.assembly["success"])
        self.assertTrue(state.assembly["trials"])
        self.assertNotIn("no_feasible_connections",[s["reason"] for s in state.stops.values()])

    def test_graph_is_connected_and_edges_have_actual_contact(self):
        graph=assembly_graph(self.state.raw,self.state.joints,self.geometry)
        self.assertTrue(graph["connected"])
        self.assertEqual(len(graph["selected_edges"]),len(self.state.raw)-1)
        self.assertTrue(all(c["area"]>0 for c in graph["contacts"]))
        self.assertGreaterEqual(max(sum(n in j.owners for j in self.state.joints) for n in self.state.raw),2)

    def test_multiple_joints_do_not_conflict(self):
        for a,b in combinations(self.state.joints,2):self.assertLess(overlap_volume(a.zone,b.zone),1e-5)
        parts=materialize(self.state.raw,self.state.joints,self.geometry)
        for a,b in combinations(parts.values(),2):self.assertLess(overlap_volume(a,b),1e-5)

    def test_complete_sequence_uses_all_previously_installed_components(self):
        parts=materialize(self.state.raw,self.state.joints,self.geometry)
        installed=set()
        for step in self.state.sequence:
            self.assertEqual(set(step["stationary_components"]),installed)
            self.assertNotIn(step["component"],installed)
            if installed:
                self.assertGreater(step["checked_positions"],self.geometry.path_steps)
                self.assertFalse(step["continuous_path_proven"])
                for d in (0,step["distances"][len(step["distances"])//2],max(step["distances"])):
                    direction=-np.array(step["insertion_direction"])
                    moving=parts[step["component"]].translate(tuple(direction*d))
                    for fixed in installed:self.assertLess(overlap_volume(moving,parts[fixed]),1e-5)
            installed.add(step["component"])
        self.assertEqual(installed,set(parts))

    def test_blocked_closed_cavity_is_not_called_assemblable(self):
        shell=block((30,30,30)).cut(block((12,12,12)))
        inner=block((10,10,10))
        with self.assertRaisesRegex(GeometryRejected,"sequence"):
            find_sequence({"shell":shell,"inner":inner},{"shell":shell,"inner":inner},[],self.geometry,64)

    def test_seed_repeats_partition_and_connections(self):
        first=decompose(steps(),42,self.geometry,self.settings)
        second=decompose(steps(),42,self.geometry,self.settings)
        self.assertEqual(first.cuts,second.cuts)
        self.assertEqual([j.metadata() for j in first.joints],[j.metadata() for j in second.joints])
        self.assertEqual(first.sequence,second.sequence)


class AutomaticJointTests(unittest.TestCase):
    def setUp(self):self.geometry=AssemblySettings(path_steps=8)

    def options(self,dimensions,**kwargs):
        original=block(dimensions)
        split=split_model(original,[0,0,0],[0,0,1],self.geometry)
        return original,split,propose_joints(split,("a","b"),"j1",42,self.geometry,**kwargs)

    def test_wide_face_prefers_bolts_and_number_depends_on_geometry(self):
        _,_,wide=self.options((100,100,40))
        _,_,small=self.options((30,30,40))
        self.assertEqual(wide[0].parameters["type"],"bolted")
        self.assertGreater(wide[0].parameters["bolt_count"],small[0].parameters["bolt_count"])

    def test_narrow_interface_prefers_a_feasible_groove(self):
        _,_,options=self.options((50,14,40))
        self.assertEqual(options[0].parameters["type"],"groove")
        self.assertFalse(options[0].parameters.get("threaded",False))

    def test_long_guide_uses_combined_only_with_separate_bolt_space(self):
        original,split,options=self.options((180,60,40))
        self.assertEqual(options[0].parameters["type"],"combined")
        self.assertIn(options[0].parameters["groove"]["profile"]["kind"],("dovetail","t"))
        self.assertGreater(options[0].parameters["bolt_count"],0)
        raw={"a":split.world(split.upper),"b":split.world(split.lower)}
        parts=materialize(raw,[options[0]],self.geometry)
        checks,sequence=validate_partition(original,raw,parts,[options[0]],self.geometry,128)
        self.assertEqual({s["component"] for s in sequence},set(parts))
        self.assertTrue(checks["assembly_sequence_checked"])

    def test_all_existing_profiles_are_reused_and_verified(self):
        for profile in PROFILE_TYPES:
            with self.subTest(profile=profile):
                _,_,options=self.options((60,50,40),connection="groove",profile=profile)
                self.assertEqual(options[0].parameters["profile"]["kind"],profile)
                for gap in options[0].parameters["measured_profile_surface_gaps"]:
                    self.assertAlmostEqual(gap,.2,places=6)

    def test_bolts_installed_after_bodies_nuts_after_bolts(self):
        original,split,options=self.options((100,100,40))
        joint=options[0]
        raw={"a":split.world(split.upper),"b":split.world(split.lower)}
        parts=materialize(raw,[joint],self.geometry)
        checks,sequence=validate_partition(original,raw,parts,[joint],self.geometry,128)
        positions={s["component"]:s["step"] for s in sequence}
        for name in parts:
            if "_bolt_" in name:
                self.assertGreater(positions[name],max(positions["a"],positions["b"]))
                self.assertGreater(positions[name.replace("_bolt_","_nut_")],positions[name])
        self.assertLess(max(checks["final_intersection_volumes"].values()),1e-5)


class AutoExportTests(unittest.TestCase):
    def test_four_views_separate_step_and_raw_components(self):
        geometry=AssemblySettings(path_steps=8)
        settings=DecompositionSettings()
        state=decompose(steps(),42,geometry,settings)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"run"
            target=root/"result"
            meta=export_auto(state,42,{"generator":"control_fixture"},None,target,geometry,settings,
                             {"decomposition":"auto","connection":"auto"})
            self.assertTrue(meta["success"])
            self.assertEqual(len(meta["raw_components"]),len(state.raw))
            self.assertEqual(len(cq.importers.importStep(str(target/"assembly.step")).solids().vals()),len(meta["components"]))
            raw=[]
            for c in meta["raw_components"]:
                shape=cq.importers.importStep(str(target/c["step"])).val()
                raw.append(transform_part(shape,c["rotation_matrix"],c["translation"]))
            self.assertLess(difference_volume(state.original,union(raw)),1e-5)
            for file in ("original.stl","split_exploded.stl","parts_exploded.stl","assembly.stl"):
                mesh=trimesh.load(str(target/file),force="mesh")
                self.assertGreater(len(mesh.faces),0);self.assertLess((target/file).stat().st_size,10_000_000)
            manifest=dict(seed=42,requested_count=1,successful_count=1,failures=[],assemblies=[dict(folder="result")])
            export_examples(root,manifest,Path(tmp)/"examples")
            readme=(Path(tmp)/"examples"/"README.md").read_text()
            self.assertIn("model_01/split_exploded.stl",readme)
            self.assertIn("model_01/parts_exploded.stl",readme)
            with self.assertRaises(FileExistsError):export_auto(state,42,{},None,target,geometry,settings,{})

    def test_real_cadgen_geometry_survives_failed_assembly(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch("cadgen.joint_design.propose_joints",side_effect=GeometryRejected("no fixture fastener")):
                manifest=generate_auto_batch(root/"run",count=1,seed=42,max_attempts=2,
                                            geometry=AssemblySettings(path_steps=8),examples=root/"examples")
            self.assertEqual(manifest["successful_count"],0)
            retained=[f for f in manifest["failures"] if f.get("geometry_folder")]
            self.assertTrue(retained,manifest)
            target=root/"run"/retained[0]["geometry_folder"]
            data=json.loads((target/"metadata.json").read_text())
            self.assertEqual(data["source"]["generator"],"CADFactory")
            self.assertTrue(data["geometry_success"])
            self.assertFalse(data["assembly_success"])
            self.assertGreaterEqual(data["main_component_count"],2)
            self.assertEqual(len(list(target.glob("part_*.stl"))),data["main_component_count"])
            self.assertFalse((root/"examples"/"model_01").exists())

    def test_technical_settings_validation(self):
        for settings in (DecompositionSettings(max_depth=0),DecompositionSettings(min_score=float("nan"))):
            with self.assertRaises(ValueError):settings.validate()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):generate_auto_batch(Path(tmp)/"bad",profile="random")


if __name__=="__main__":unittest.main()
