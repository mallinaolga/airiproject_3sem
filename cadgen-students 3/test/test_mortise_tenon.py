"""Rectangular groove reuse as a blind mortise and integral tenon."""
from dataclasses import replace
from pathlib import Path
import random
import tempfile

import cadquery as cq
import pytest

from generirovanie_pazov.generate_grooves import Profile
from cadgen.assembly_geometry import (AssemblySettings, GeometryRejected, build_groove,
                                     split_model, validate_connection, sampled_path)
from cadgen.assembly_generator import GeneratedAssembly, export_result


@pytest.fixture
def fixture():
    settings = AssemblySettings(path_steps=8)
    original = cq.Workplane("XY").box(60, 50, 40).val()
    return split_model(original, [0, 0, 0], [0, 0, 1], settings), settings


def joint(split, settings, *, depth=5, center=(0, 0)):
    return build_groove(split, random.Random(42), settings, "rectangular", centers=[center],
                        exact_profile=Profile("rectangular", 10, depth),
                        footprint=dict(width=10, depth=depth, length=12, anchor_depth=2))


@pytest.mark.parametrize("clearance", [0., .2, .9])
def test_blind_socket_geometry_and_insertion(fixture, clearance):
    split, settings = fixture
    settings = replace(settings, clearance=clearance)
    result = joint(split, settings)
    p = result.parameters
    assert p["type"] == "groove" and p["profile"]["kind"] == "rectangular"
    assert p["joint_type"] == "mortise_tenon" and p["socket"] == "blind"
    assert p["tenon_depth"] == pytest.approx(5)
    assert p["socket_depth"] == pytest.approx(5+clearance)
    assert p["bottom_clearance"] == pytest.approx(clearance)
    donor, receiver = [shape for _, shape in result.components]
    assert len(donor.Solids()) == len(receiver.Solids()) == 1
    assert donor.isInside(cq.Vector(0, 0, -2))
    assert not receiver.isInside(cq.Vector(0, 0, -2))
    # Actual floor and four end/side walls remain material, not a through slot.
    for point in [(0, 0, -8), (8, 0, -2), (-8, 0, -2), (0, 9, -2), (0, -9, -2)]:
        assert receiver.isInside(cq.Vector(*point))
    checks = validate_connection(split, result, settings)
    assert checks["paths"]["part_1"]["status"] == "sampled_clear"
    assert checks["paths"]["part_1"]["withdrawal_direction_in_cut_frame"] == [0., 0., 1.]
    assert not p["self_retaining"]
    assert not checks["continuous_path_proven"]
    assert max(checks["intersection_volumes"].values()) <= settings.volume_tolerance


@pytest.mark.parametrize("clearance", [-.1, 1., float("nan"), float("inf")])
def test_direct_builder_rejects_invalid_clearance(fixture, clearance):
    split, settings = fixture
    with pytest.raises(ValueError): joint(split, replace(settings, clearance=clearance))


@pytest.mark.parametrize("depth,center", [(19, (0, 0)), (5, (29, 0)), (5, (0, 24))])
def test_insufficient_floor_or_side_walls(fixture, depth, center):
    split, settings = fixture
    with pytest.raises(GeometryRejected, match="floor/side material"):
        joint(split, settings, depth=depth, center=center)


def test_displaced_tenon_collides(fixture):
    split, settings = fixture
    result = joint(split, settings)
    name, donor = result.components[0]
    result.components[0] = (name, donor.translate((1, 0, 0)))
    with pytest.raises(GeometryRejected, match="intersect"):
        validate_connection(split, result, settings)


def test_lateral_insertion_is_blocked(fixture):
    split, settings = fixture
    donor, receiver = [shape for _, shape in joint(split, settings).components]
    assert sampled_path(donor, [receiver], [(1, 0, 0)], settings)["status"] == "not_found"


def test_metadata_survives_export(fixture):
    split, settings = fixture
    connection = joint(split, settings)
    result = GeneratedAssembly(split.original, split, connection,
                               validate_connection(split, connection, settings), 42)
    with tempfile.TemporaryDirectory() as tmp:
        meta = export_result(result, Path(tmp)/"mortise", settings)
        assert meta["connection"]["joint_type"] == "mortise_tenon"
        assert meta["checks"]["step_roundtrip_separate_solids"] == 2
