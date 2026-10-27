"""Run from project root: python -m unittest discover -s test -p 'test_*.py' -v."""

from dataclasses import replace
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import cadquery as cq
import numpy as np

from Gaiki import NutSpec, build_nut
from generirovanie_pazov.generate_grooves import PROFILE_TYPES
from cadgen.assembly_geometry import (
    AssemblySettings, GeometryRejected, build_bolted, build_groove, difference_volume,
    sampled_path, split_model, validate_connection,
)
from cadgen.assembly_generator import create_from_model, export_result, generate_batch, generate_one
from cadgen.assembly_source import generate_source, seeded_generators
from cadgen.assembly_validation import overlap_volume, transform_part


def box():
    return cq.Workplane("XY").box(60, 50, 40).val()


class AssemblyGeometryTests(unittest.TestCase):
    def setUp(self):
        self.settings = AssemblySettings(path_steps=8)
        self.original = box()
        self.split = split_model(self.original, [0, 0, 0], [0, 0, 1], self.settings)

    def test_split_valid_single_solids_and_reconstruction(self):
        for part in (self.split.upper, self.split.lower):
            self.assertTrue(part.isValid())
            self.assertEqual(len(part.Solids()), 1)
            self.assertGreater(part.Volume(), 0)
        self.assertAlmostEqual(self.split.upper.Volume(), self.original.Volume()/2)
        self.assertLess(difference_volume(self.split.original, self.split.upper.fuse(self.split.lower)), 1e-5)
        self.assertLess(overlap_volume(self.split.upper, self.split.lower), 1e-5)

    def test_oblique_split_on_rotated_translated_model(self):
        original = self.original.rotate((0, 0, 0), (1, 2, 3), 39).translate((80, -30, 20))
        split = split_model(original, [80, -30, 20], [0.2, 0.4, 1], self.settings)
        world = split.world(split.upper).fuse(split.world(split.lower))
        self.assertLess(difference_volume(original, world), 1e-5)

    def test_rectangular_shared_geometry_and_measured_clearance(self):
        connection = build_groove(self.split, random.Random(42), self.settings)
        checks = validate_connection(self.split, connection, self.settings)
        self.assertTrue(checks["main_geometry_preserved"])
        self.assertTrue(connection.parameters["profile_containment_checked"])
        self.assertEqual(connection.parameters["profile"]["kind"], "rectangular")
        for gap in connection.parameters["measured_profile_surface_gaps"]:
            self.assertAlmostEqual(gap, 0.2, places=6)
        self.assertLess(max(checks["intersection_volumes"].values()), 1e-5)
        self.assertLess(checks["technological_void_error_volume"], 1e-5)
        self.assertGreater(checks["removed_main_body_volume"], 0)
        self.assertFalse(checks["continuous_path_proven"])
        self.assertFalse(checks["mechanical_retention_checked"])

    def test_zero_clearance_does_not_remove_unaccounted_material(self):
        settings = replace(self.settings, clearance=0)
        connection = build_groove(self.split, random.Random(42), settings)
        checks = validate_connection(self.split, connection, settings)
        self.assertLess(checks["removed_main_body_volume"], 1e-5)
        self.assertLess(checks["added_main_body_volume"], 1e-5)

    def test_all_six_existing_profiles_with_appropriate_paths(self):
        for profile in PROFILE_TYPES:
            with self.subTest(profile=profile):
                connection = build_groove(self.split, random.Random(42), self.settings, profile)
                checks = validate_connection(self.split, connection, self.settings)
                self.assertEqual(connection.parameters["profile"]["kind"], profile)
                self.assertEqual(checks["paths"]["part_1"]["status"], "sampled_clear")
                for gap in connection.parameters["measured_profile_surface_gaps"]:
                    self.assertAlmostEqual(gap, self.settings.clearance, places=6)
                if profile in ("dovetail", "t"):
                    self.assertEqual(connection.parameters["open_ends"], "both")
                    self.assertEqual(connection.parameters["insertion"], "longitudinal_slide")
                    self.assertEqual(abs(checks["paths"]["part_1"]["withdrawal_direction_in_cut_frame"][1]), 1)
                if profile == "round":
                    self.assertEqual(connection.parameters["round_radial_clearance"], 0.2)
                    self.assertEqual(connection.parameters["round_diametral_clearance"], 0.4)

    def test_undercuts_reject_normal_insertion_and_closed_ends(self):
        for profile in ("dovetail", "t"):
            with self.subTest(profile=profile):
                connection = build_groove(self.split, random.Random(42), self.settings, profile)
                donor, receiver = [shape for _, shape in connection.components]
                path = sampled_path(donor, [receiver], [(0, 0, 1)], self.settings)
                self.assertEqual(path["status"], "not_found")
                for y in (-26, 26):
                    cap = cq.Workplane("XY").box(60, 2, 20).translate((0, y, -10)).val()
                    receiver = receiver.fuse(cap)
                path = sampled_path(donor, [receiver], [(0, 1, 0), (0, -1, 0)], self.settings)
                self.assertEqual(path["status"], "not_found")

    def test_actual_material_collision_rejects_joint(self):
        connection = build_groove(self.split, random.Random(42), self.settings)
        name, donor = connection.components[0]
        connection.components[0] = (name, donor.translate((1, 0, 0)))
        with self.assertRaisesRegex(GeometryRejected, "intersect"):
            validate_connection(self.split, connection, self.settings)

    def test_unintended_external_change_is_rejected(self):
        connection = build_groove(self.split, random.Random(42), self.settings)
        name, receiver = connection.components[1]
        # Remove a corner far from the declared technological void.
        bb = receiver.BoundingBox()
        tool = cq.Workplane("XY").box(5, 5, 5).translate((bb.xmax-1, bb.ymax-1, bb.zmin+1)).val()
        connection.components[1] = (name, receiver.cut(tool))
        with self.assertRaisesRegex(GeometryRejected, "declared technological void"):
            validate_connection(self.split, connection, self.settings)

    def test_bolt_holes_nut_and_accessible_bearing_surfaces(self):
        connection = build_bolted(self.split, random.Random(42), self.settings)
        checks = validate_connection(self.split, connection, self.settings)
        p = connection.parameters
        self.assertEqual(len(connection.components), 4)
        self.assertTrue(p["coaxial_holes_checked"])
        self.assertTrue(p["head_cannot_pass_hole"])
        self.assertAlmostEqual(p["hole_diameter"]-p["shaft_diameter"], 0.4)
        self.assertEqual(p["nut"]["hole_diameter"], p["hole_diameter"])
        self.assertGreaterEqual(p["bolt"]["shaft_length"], p["main_body_thickness"]+p["nut"]["height"])
        self.assertGreater(p["head_bearing_area"], 1)
        self.assertGreater(p["nut_bearing_area"], 1)
        self.assertFalse(p["threaded"])
        self.assertFalse(p["thread_retention_modeled"])
        self.assertEqual(set(checks["paths"]), {"part_1", "bolt_1", "nut_1"})
        self.assertLess(max(checks["intersection_volumes"].values()), 1e-5)
        np.testing.assert_allclose(p["hole_removed_volumes"], p["expected_hole_removed_volumes"], atol=1e-5)

    def test_incompatible_hardware_is_rejected(self):
        connection = build_bolted(self.split, random.Random(42), self.settings)
        name, bolt = connection.components[2]
        connection.components[2] = (name, bolt.translate((1, 0, 0)))
        with self.assertRaisesRegex(GeometryRejected, "intersect"):
            validate_connection(self.split, connection, self.settings)
        with self.assertRaises(ValueError):
            build_nut(NutSpec(8, 7, 4))

    def test_empty_sliver_and_multiple_solids_are_rejected(self):
        for origin in ([0, 0, 100], [0, 0, 19.99]):
            with self.subTest(origin=origin), self.assertRaises(GeometryRejected):
                split_model(self.original, origin, [0, 0, 1], self.settings)
        compound = cq.Compound.makeCompound([self.original, self.original.translate((100, 0, 0))])
        with self.assertRaises(GeometryRejected):
            create_from_model(compound, 42)

    def test_clearance_and_settings_boundaries(self):
        for clearance in (-0.1, 1, float("nan"), float("inf")):
            with self.subTest(clearance=clearance), self.assertRaises(ValueError):
                replace(self.settings, clearance=clearance).validate()
        for field in ("min_wall", "volume_tolerance", "feature_attempts", "plane_attempts", "path_steps"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                replace(self.settings, **{field: 0}).validate()


class AssemblyPipelineTests(unittest.TestCase):
    def test_export_failure_is_never_marked_successful(self):
        settings = AssemblySettings(path_steps=8)
        result = create_from_model(box(), 42, settings=settings)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/"failed_export"
            with patch("cadgen.assembly_generator.cq.exporters.export", side_effect=OSError("disk unavailable")):
                with self.assertRaises(OSError):
                    export_result(result, root, settings)
            metadata = json.loads((root/"metadata.json").read_text())
            self.assertFalse(metadata["success"])
            self.assertEqual(metadata["status"], "export_failed")
            self.assertIn("disk unavailable", metadata["export_error"])

    def test_export_reimports_components_and_rigid_placements(self):
        for mode in ("groove", "bolted"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                original = box().rotate((0, 0, 0), (1, 3, 2), 23).translate((40, 70, -15))
                settings = AssemblySettings(path_steps=8)
                result = create_from_model(original, 42, mode, settings=settings)
                root = Path(tmp)/"assembly"
                metadata = export_result(result, root, settings)
                self.assertTrue(metadata["success"])
                self.assertTrue(metadata["checks"]["step_placements_verified"])
                expected_count = 2 if mode == "groove" else 4
                self.assertEqual(len(cq.importers.importStep(str(root/"assembly.step")).solids().vals()), expected_count)
                self.assertEqual(len(cq.importers.importStep(str(root/"exploded.step")).solids().vals()), expected_count)
                self.assertLess(difference_volume(original, cq.importers.importStep(str(root/"original.step")).val()), 1e-5)
                for entry, (_, verified) in zip(metadata["components"], result.connection.components):
                    local = cq.importers.importStep(str(root/entry["step"])).val()
                    world = transform_part(local, entry["rotation_matrix"], entry["translation"])
                    self.assertLess(difference_volume(world, result.split.world(verified)), 1e-5)
                    self.assertGreater((root/entry["stl"]).stat().st_size, 84)
                self.assertTrue((root/"assembly.stl").is_file())
                self.assertEqual(json.loads((root/"metadata.json").read_text())["status"], "success")
                with self.assertRaises(FileExistsError):
                    export_result(result, root, settings)

    def test_seed_reproduces_cadgen_source_cut_joint_and_components(self):
        first = generate_one(42)
        second = generate_one(42)
        self.assertEqual(first.source_program, second.source_program)
        self.assertEqual(first.source_parameters["generator"], "CADFactory")
        self.assertLess(difference_volume(first.original, second.original), 1e-5)
        self.assertEqual(first.split.metadata(), second.split.metadata())
        self.assertEqual(first.connection.parameters, second.connection.parameters)
        self.assertEqual(first.request, second.request)
        for (_, a), (_, b) in zip(first.connection.components, second.connection.components):
            self.assertLess(difference_volume(a, b), 1e-5)

    def test_seed_context_does_not_change_callers_rng_state(self):
        python_state, numpy_state = random.getstate(), np.random.get_state()
        with seeded_generators(42):
            random.random()
            np.random.rand(10)
        self.assertEqual(random.getstate(), python_state)
        restored = np.random.get_state()
        self.assertEqual(restored[0], numpy_state[0])
        np.testing.assert_array_equal(restored[1], numpy_state[1])
        self.assertEqual(restored[2:], numpy_state[2:])

    def test_cadgen_sources_and_split_planes_vary(self):
        sources = [generate_source(seed) for seed in (42, 43, 44)]
        self.assertGreater(len({round(shape.Volume(), 5) for shape, _, _ in sources}), 1)
        planes = [create_from_model(box(), seed).split.metadata() for seed in range(1, 9)]
        self.assertGreater(len({tuple(p["normal"]) for p in planes}), 1)
        self.assertGreater(len({tuple(p["origin"]) for p in planes}), 1)

    def test_full_cadgen_to_assembly_step_both_modes(self):
        for mode in ("groove", "bolted"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)/mode
                manifest = generate_batch(root, connection=mode, seed=42, max_attempts=4)
                self.assertEqual(manifest["successful_count"], 1, manifest)
                self.assertEqual(manifest["status"], "complete")
                folder = root/manifest["assemblies"][0]["folder"]
                metadata = json.loads((folder/"metadata.json").read_text())
                self.assertEqual(metadata["source"]["generator"], "CADFactory")
                self.assertEqual(metadata["request"]["connection"], mode)
                self.assertEqual(metadata["request"]["source"], "cadgen")
                self.assertTrue(metadata["success"])
                self.assertTrue((folder/"original.py").is_file())
                self.assertTrue((folder/"assembly.step").is_file())

    def test_batch_counts_successful_assemblies_after_a_real_geometry_rejection(self):
        tiny = cq.Workplane("XY").box(1, 1, 1).val()
        values = [(tiny, {"generator": "test_tiny"}, None),
                  (box(), {"generator": "test_box"}, None),
                  (box(), {"generator": "test_box"}, None)]
        with tempfile.TemporaryDirectory() as tmp, patch(
                "cadgen.assembly_generator.generate_source", side_effect=values):
            root = Path(tmp)/"batch"
            manifest = generate_batch(root, count=2, connection="groove", seed=42, max_attempts=2)
            self.assertEqual(manifest["successful_count"], 2, manifest)
            self.assertEqual(len(manifest["failures"]), 1)
            self.assertEqual(manifest["failures"][0]["requested_slot"], 1)
            self.assertTrue(manifest["failures"][0]["rejected_candidates"])
            self.assertEqual(len(list(root.glob("assembly_*/assembly.step"))), 2)
            with self.assertRaises(FileExistsError):
                generate_batch(root, seed=42)

    def test_incomplete_cli_reports_failure_and_keeps_reasons(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/"impossible"
            run = subprocess.run([sys.executable, "-m", "cadgen.assembly_generator", "--source", "box",
                                  "--count", "1", "--seed", "42", "--min-wall", "1000",
                                  "--max-attempts", "1", "--plane-attempts", "1",
                                  "--output", str(root)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 1, run.stderr)
            manifest = json.loads((root/"manifest.json").read_text())
            self.assertEqual(manifest["status"], "incomplete")
            self.assertEqual(manifest["successful_count"], 0)
            self.assertEqual(len(manifest["failures"]), 1)
            self.assertIn("0/1", run.stdout)


if __name__ == "__main__":
    unittest.main()
