"""Existing dovetail geometry: retention after clearance and integration."""
from dataclasses import replace
from pathlib import Path
import random
import tempfile
import cadquery as cq
import pytest

from generirovanie_pazov.generate_grooves import Profile
from cadgen.assembly_geometry import (AssemblySettings, GeometryRejected, build_groove,
                                     split_model, validate_connection, sampled_path)
from cadgen.assembly_generator import create_from_model, export_result


@pytest.fixture
def fixture():
    settings = AssemblySettings(path_steps=8)
    source = cq.Workplane("XY").box(60, 50, 40).val()
    return split_model(source, [0, 0, 0], [0, 0, 1], settings), settings


def build(split, settings, profile=None, center=(0, 0)):
    return build_groove(split, random.Random(42), settings, "dovetail", centers=[center],
                        exact_profile=profile or Profile("dovetail", 10, 5, bottom_width=16),
                        footprint=dict(width=16, depth=5, length=12, anchor_depth=2))


@pytest.mark.parametrize("gap", [0., .2, .9])
def test_actual_undercut_and_normal_retention(fixture, gap):
    split, settings = fixture
    settings = replace(settings, clearance=gap)
    result = build(split, settings)
    donor, receiver = [s for _, s in result.components]
    tongue = donor.cut(split.upper)
    # Measure actual cross-section edges, not just the nominal profile.
    top = [v.Center().x for v in tongue.Vertices() if abs(v.Center().z) < 1e-6]
    bottom = [v.Center().x for v in tongue.Vertices() if abs(v.Center().z+5) < 1e-6]
    assert max(bottom)-min(bottom) == pytest.approx(16)
    assert max(top)-min(top) == pytest.approx(10)
    checks = validate_connection(split, result, settings)
    assert checks["normal_withdrawal_blocked"]
    assert checks["witness_intersection_volume"] > settings.volume_tolerance
    assert result.parameters["joint_type"] == "dovetail"
    assert result.parameters["type"] == "groove"
    assert not result.parameters["longitudinal_stop"]
    for direction in [(0, 1, 0), (0, -1, 0)]:
        assert sampled_path(donor, [receiver], [direction], settings)["status"] == "sampled_clear"
    for measured in result.parameters["measured_profile_surface_gaps"]:
        assert measured == pytest.approx(gap)


def test_clearance_must_not_erase_undercut(fixture):
    split, settings = fixture
    weak = Profile("dovetail", 10, 5, bottom_width=10.1)
    with pytest.raises(GeometryRejected, match="normal retention"):
        build(split, settings, weak)


@pytest.mark.parametrize("gap", [-.1, 1., float("nan")])
def test_invalid_clearance(fixture, gap):
    split, settings = fixture
    with pytest.raises(ValueError): build(split, replace(settings, clearance=gap))


def test_thin_floor_or_wall(fixture):
    split, settings = fixture
    with pytest.raises(GeometryRejected, match="floor/side"):
        build(split, settings, center=(28, 0))
    with pytest.raises(GeometryRejected, match="floor/side"):
        build(split, settings, Profile("dovetail", 10, 19, bottom_width=16))


def test_one_closed_end_leaves_only_other_entrance(fixture):
    split, settings = fixture
    donor, receiver = [s for _, s in build(split, settings).components]
    bb = receiver.BoundingBox()
    receiver = receiver.fuse(cq.Workplane("XY").box(bb.xlen, 2, bb.zlen)
                             .translate(((bb.xmin+bb.xmax)/2, bb.ymax+1, (bb.zmin+bb.zmax)/2)).val())
    assert sampled_path(donor, [receiver], [(0, 1, 0)], settings)["status"] == "not_found"
    assert sampled_path(donor, [receiver], [(0, -1, 0)], settings)["status"] == "sampled_clear"


def test_both_closed_ends_block_insertion_without_final_overlap(fixture):
    from cadgen.assembly_validation import overlap_volume
    split, settings = fixture
    donor, receiver = [s for _, s in build(split, settings).components]
    bb = receiver.BoundingBox()
    for y in (bb.ymin-1, bb.ymax+1):
        cap = cq.Workplane("XY").box(bb.xlen, 2, bb.zlen).translate(
            ((bb.xmin+bb.xmax)/2, y, (bb.zmin+bb.zmax)/2)).val()
        receiver = receiver.fuse(cap)
    assert receiver.isValid()
    assert overlap_volume(donor, receiver) <= settings.volume_tolerance
    assert sampled_path(donor, [receiver], [(0, -1, 0), (0, 1, 0)], settings)["status"] == "not_found"


def test_export_retains_joint_type_and_checks(fixture):
    split, settings = fixture
    result = create_from_model(split.original, 42, profile="dovetail", settings=settings)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/"dovetail"
        meta = export_result(result, path, settings)
        assert meta["connection"]["joint_type"] == "dovetail"
        assert meta["checks"]["normal_withdrawal_blocked"]
        assert meta["checks"]["step_roundtrip_separate_solids"] == 2
        assert (path/"assembly.stl").stat().st_size > 0


def test_constructive_builder_reuses_dovetail(fixture):
    from cadgen.constructive_joint_design import _grooves
    from cadgen.constructive_geometry import ConstructiveSettings
    from cadgen.assembly_geometry import contact_patch
    split, settings = fixture
    face = contact_patch(split.lower, split.upper).Faces()[0]
    result = _grooves(split, face, "one_long_groove", "dovetail", settings, ConstructiveSettings())
    assert result.parameters["features"][0]["joint_type"] == "dovetail"
    assert result.parameters["features"][0]["retention_checks"]["normal_withdrawal_blocked"]
    validate_connection(split, result, settings)
