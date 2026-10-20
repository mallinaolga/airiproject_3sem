"""Run: python -m unittest discover -s test -p test_connections.py -v"""

from pathlib import Path
import tempfile
import unittest

import cadquery as cq
import numpy as np

from cadgen.assembly_search import run_search
from cadgen.connection_search import SearchSettings, describe_part, evaluate_pose, search_pair
from connection_examples import corner_and_cube, oval_and_recess


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.settings = SearchSettings(max_poses=48, path_steps=8)

    def search(self, shape_a, shape_b):
        a = describe_part("a", shape_a, self.settings)
        b = describe_part("b", shape_b, self.settings)
        result, moved = search_pair(a, b, self.settings)
        self.assertFalse(result["errors"], result)
        return a, b, result, moved

    def test_corner_cube(self):
        corner, cube = corner_and_cube()
        _, _, result, moved = self.search(corner, cube.translate((150, -80, 40)))
        self.assertEqual(result["status"], "connection_found", result)
        self.assertEqual(result["connection"]["reason"], "multi_surface_contact")
        self.assertLessEqual(corner.intersect(moved).Volume(), self.settings.volume_tolerance)
        self.assertFalse(result["connection"]["approach"]["continuous_path_checked"])

    def test_rotated_corner_and_reversed_order(self):
        corner, cube = corner_and_cube()
        corner = corner.rotate((0, 0, 0), (1, 2, 3), 37).translate((30, 40, 50))
        _, _, result, _ = self.search(cube, corner)
        self.assertEqual(result["status"], "connection_found", result)

    def test_oval_in_shallow_recess(self):
        recess, oval = oval_and_recess()
        a, b, result, moved = self.search(recess, oval.translate((90, 10, 30)))
        self.assertEqual(result["status"], "connection_found",
                         (result, a.warnings, b.warnings, [c["fit"] for c in a.curves]))
        self.assertEqual(result["connection"]["reason"], "curved_recess")
        self.assertLessEqual(recess.intersect(moved).Volume(), self.settings.volume_tolerance)

    def test_round_hole_clearance(self):
        ring = cq.Workplane("XY").circle(20).circle(10).extrude(10).val()
        pin = cq.Workplane("XY").circle(8).extrude(25).val()
        _, _, result, _ = self.search(ring, pin)
        self.assertEqual(result["status"], "connection_found", result)
        self.assertEqual(result["connection"]["reason"], "cylindrical_insertion")
        self.assertAlmostEqual(result["connection"]["radial_gap"], 2)

    def test_square_hole(self):
        ring = cq.Workplane("XY").circle(20).rect(20, 20).extrude(10).val()
        bar = cq.Workplane("XY").box(18, 17, 30).val()
        _, _, result, _ = self.search(ring, bar)
        self.assertEqual(result["status"], "connection_found", result)

    def test_round_hole_reversed_and_rotated(self):
        ring = cq.Workplane("XY").circle(20).circle(10).extrude(10).val()
        pin = cq.Workplane("XY").circle(8).extrude(25).val()
        ring = ring.rotate((0, 0, 0), (1, 2, 3), 31).translate((70, 90, 40))
        _, _, result, _ = self.search(pin, ring)
        self.assertEqual(result["status"], "connection_found", result)

    def test_oversized_pin(self):
        ring = cq.Workplane("XY").circle(20).circle(10).extrude(10).val()
        pin = cq.Workplane("XY").circle(12).extrude(25).val()
        _, _, result, _ = self.search(ring, pin)
        self.assertEqual(result["status"], "not_found", result)

    def test_single_plane_point_and_collision_rejected(self):
        box = cq.Workplane("XY").box(10, 10, 10).val()
        a = describe_part("a", box, self.settings)
        for translation, reason in (
                ([10, 0, 0], "insufficient_contact_or_engagement"),
                ([10, 10, 10], "insufficient_contact_or_engagement"),
                ([5, 0, 0], "collision"),
                ([100, 0, 0], "insufficient_contact_or_engagement")):
            with self.subTest(translation=translation):
                pose = dict(rotation_matrix=np.eye(3).tolist(), translation=translation,
                            kind="multi_surface_contact", receiver="a", evidence={})
                result, _ = evaluate_pose(a, a, pose, self.settings)
                self.assertFalse(result["accepted"])
                self.assertEqual(result["reason"], reason)

    def test_dataset_one_and_two_parts_and_exports(self):
        # Only a temporary child of test is created and cleaned up.
        with tempfile.TemporaryDirectory(prefix="connection_check_", dir=Path(__file__).parent) as tmp:
            root = Path(tmp).resolve()
            self.assertEqual(root.parent, Path(__file__).resolve().parent)
            source = root / "parts"
            source.mkdir()
            corner, cube = corner_and_cube()
            cq.exporters.export(corner, str(source / "corner.step"))
            one = run_search(source, source / "connections_one", self.settings)
            self.assertEqual(one["summary"]["parts_analyzed"], 1)
            self.assertEqual(one["summary"]["pairs_checked"], 0)
            cq.exporters.export(cube, str(source / "cube.stp"), exportType="STEP")
            two = run_search(source, source / "connections_two", self.settings)
            self.assertEqual(two["summary"]["pairs_checked"], 1)
            self.assertEqual(two["summary"]["assemblies_exported"], 1)
            step = source / "connections_two" / two["pairs"][0]["assembly_step"]
            self.assertEqual(len(cq.importers.importStep(str(step)).solids().vals()), 2)
            with self.assertRaises(FileExistsError):
                run_search(source, source / "connections_two", self.settings)


if __name__ == "__main__":
    unittest.main()
