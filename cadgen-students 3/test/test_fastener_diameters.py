"""Run from the project folder: python -m unittest discover -s test -p test_fastener_diameters.py -v"""

import math
import random
import unittest
from dataclasses import asdict

import cadquery as cq

import Bolty
import Gaiki
import Otverstiya


class EndpointRandom(random.Random):
    """Exercise exact dimension boundaries rather than hoping random samples reach them."""

    def __init__(self, upper):
        super().__init__(0)
        self.upper = upper

    def uniform(self, a, b):
        return b if self.upper else a

    def randint(self, a, b):
        return b if self.upper else a


class FastenerDiameterTests(unittest.TestCase):
    def check_hole(self, shape, diameter, height):
        # A smaller shaft must pass; a larger one must intersect the wall.
        for difference, fits in ((-0.2, True), (0.2, False)):
            shaft = (cq.Workplane("XY", origin=(0, 0, -1))
                     .circle((diameter+difference)/2).extrude(height+2).val())
            volume = shape.intersect(shaft).Volume()
            if fits:
                self.assertLess(volume, 1e-6)
            else:
                self.assertGreater(volume, 1e-6)

    def test_all_bolt_types_at_both_diameter_limits(self):
        for upper in (False, True):
            for kind in Bolty.TYPES:
                with self.subTest(upper=upper, kind=kind):
                    spec = Bolty.sample_spec(EndpointRandom(upper), kind)
                    expected = Bolty.DIAMETER_MAX_MM if upper else Bolty.DIAMETER_MIN_MM
                    self.assertEqual(spec.shaft_diameter, expected)
                    self.assertGreaterEqual(spec.head_width, spec.shaft_diameter+4)
                    shape = Bolty.build_bolt(spec)
                    slab = cq.Workplane("XY", origin=(0, 0, -spec.shaft_length/2)).box(40, 40, 1).val()
                    section = shape.intersect(slab)
                    self.assertAlmostEqual(section.BoundingBox().xlen, expected, places=6)
                    self.assertAlmostEqual(section.Volume(), math.pi*(expected/2)**2, places=6)
                    self.assertEqual(Bolty.metadata(spec)["shaft"]["diameter"], expected)

    def test_plate_and_nut_holes_at_both_limits(self):
        for upper in (False, True):
            expected = Bolty.DIAMETER_MAX_MM if upper else Bolty.DIAMETER_MIN_MM
            for kind in Otverstiya.SHAPES:
                with self.subTest(upper=upper, kind=kind):
                    spec = Otverstiya.sample_spec(EndpointRandom(upper), kind)
                    self.assertEqual(spec.hole_diameter, expected)
                    self.check_hole(Otverstiya.build_plate(spec), expected, spec.thickness)
                    details = Otverstiya.metadata(spec)
                    self.assertFalse(details["compatibility_checked"])
                    self.assertNotIn("diametral_clearance", details)
            nut, details = Gaiki.make_nut(EndpointRandom(upper))
            self.assertEqual(details["hole"]["diameter"], expected)
            self.check_hole(nut, expected, details["height"])
            self.assertFalse(details["compatibility_checked"])
            self.assertNotIn("reference_shaft_diameter", details)

    def test_diameters_vary_and_produce_both_fit_outcomes(self):
        bolts_rng, plates_rng, nuts_rng = (random.Random(f"{name}:42")
                                          for name in ("bolts", "plates", "nuts"))
        bolts = [Bolty.sample_spec(bolts_rng, "hex_head").shaft_diameter for _ in range(20)]
        plates = [Otverstiya.sample_spec(plates_rng).hole_diameter for _ in range(20)]
        nuts = [Gaiki.make_nut(nuts_rng)[1]["hole"]["diameter"] for _ in range(20)]
        for diameters in (bolts, plates, nuts):
            self.assertGreater(len(set(diameters)), 5)
            self.assertTrue(all(Bolty.DIAMETER_MIN_MM <= d <= Bolty.DIAMETER_MAX_MM for d in diameters))
            self.assertTrue(all(d*2 == round(d*2) for d in diameters))
        for holes in (plates, nuts):
            self.assertTrue(any(shaft < hole for shaft in bolts for hole in holes))
            self.assertTrue(any(shaft > hole for shaft in bolts for hole in holes))
            self.assertNotEqual(bolts, holes)

    def test_all_fastener_dimensions_use_half_mm_grid(self):
        rng = random.Random(107)
        for kind in Bolty.TYPES:
            for _ in range(100):
                spec = Bolty.sample_spec(rng, kind)
                dimensions = [v for k, v in asdict(spec).items() if k != "kind"]
                dimensions += [spec.drive_depth, spec.drive_width or 0]
                self.assertTrue(all(x*2 == round(x*2) for x in dimensions), spec)
                self.assertGreaterEqual(spec.head_width-spec.shaft_diameter, 4)
        for _ in range(20):
            _, nut = Gaiki.make_nut(rng)
            values = [nut['across_flats'], nut['height'], nut['outer_chamfer'], nut['hole']['diameter']]
            self.assertTrue(all(x*2 == round(x*2) for x in values), nut)


if __name__ == "__main__":
    unittest.main()
