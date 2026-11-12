"""Assembly profile policy, separate from the general CAD primitive library."""

from generirovanie_pazov.generate_grooves import PROFILE_TYPES, sample_profile


ASSEMBLY_PROFILE_TYPES = tuple(p for p in PROFILE_TYPES if p not in ("round", "v"))


def sample_assembly_profile(rng, kind="random"):
    """Sample only assembly-approved profiles without changing legacy sampling."""
    if kind == "random":
        kind = rng.choice(ASSEMBLY_PROFILE_TYPES)
    if kind not in ASSEMBLY_PROFILE_TYPES:
        raise ValueError(f"Profile {kind!r} is not permitted for AIRI assemblies")
    return sample_profile(rng, kind)
