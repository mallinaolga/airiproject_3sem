"""Assembly policy must not remove profiles from standalone CAD generators."""

import random
import unittest

from cadgen.assembly_profiles import ASSEMBLY_PROFILE_TYPES, sample_assembly_profile
from generirovanie_pazov.generate_grooves import PROFILE_TYPES, sample_profile


class AssemblyProfilePolicyTests(unittest.TestCase):
    def test_allowed_set_preserves_t(self):
        self.assertEqual(set(ASSEMBLY_PROFILE_TYPES),
                         {"rectangular", "trapezoid", "dovetail", "t"})

    def test_random_selection_and_seed_reproducibility(self):
        def samples(seed):
            rng = random.Random(seed)
            return [sample_assembly_profile(rng) for _ in range(200)]
        first = samples(42)
        self.assertEqual(first, samples(42))
        self.assertEqual({p.kind for p in first}, set(ASSEMBLY_PROFILE_TYPES))

    def test_forbidden_explicit_profiles(self):
        for kind in ("round", "v", "unknown"):
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                sample_assembly_profile(random.Random(42), kind)

    def test_legacy_primitives_remain_available(self):
        for kind in ("round", "v"):
            self.assertIn(kind, PROFILE_TYPES)
            profile = sample_profile(random.Random(42), kind)
            profile.validate()
            self.assertEqual(profile.kind, kind)

    def test_builders_reject_forbidden_before_geometry(self):
        from cadgen.assembly_geometry import AssemblySettings, build_groove
        from cadgen.assembly_generator import create_from_model
        for kind in ("round", "v"):
            with self.subTest(kind=kind):
                with self.assertRaises(ValueError):
                    build_groove(None, random.Random(42), AssemblySettings(), kind)
                with self.assertRaises(ValueError):
                    create_from_model(None, 42, profile=kind)
