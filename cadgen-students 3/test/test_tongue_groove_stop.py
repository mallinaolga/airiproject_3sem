"""Real terminal stop, longitudinal accessibility and shared assembly exports."""
from dataclasses import replace
from pathlib import Path
import random
import tempfile
import cadquery as cq
import pytest

from cadgen.assembly_geometry import AssemblySettings, GeometryRejected, split_model, validate_connection, sampled_path
from cadgen.tongue_groove_stop import build_tongue_groove_stop
from cadgen.assembly_generator import create_from_model, export_result


@pytest.fixture
def fixture():
    settings = AssemblySettings(path_steps=8)
    source = cq.Workplane("XY").box(60, 50, 40).val()
    return split_model(source, [0, 0, 0], [0, 0, 1], settings), settings


def build(split, settings):
    return build_tongue_groove_stop(split, random.Random(42), settings, centers=[(0, 0)])


@pytest.mark.parametrize("gap", [0., .2, .9])
def test_real_stop_and_accessible_insertion(fixture, gap):
    split, settings = fixture
    settings = replace(settings, clearance=gap)
    result = build(split, settings)
    checks = validate_connection(split, result, settings)
    p = result.parameters
    assert p["joint_type"] == "tongue_groove_stop"
    assert p["profile"]["kind"] == "rectangular"
    assert not p["self_retaining"]
    assert checks["stop_contact_area"] == pytest.approx(p["profile"]["opening_width"]*p["profile"]["depth"])
    assert all(v > settings.volume_tolerance for v in checks["forward_probe_intersection_volumes"])
    assert max(checks["intersection_volumes"].values()) <= settings.volume_tolerance
    assert checks["paths"]["part_1"]["withdrawal_direction_in_cut_frame"] == [0., -1., 0.]
    donor, receiver = [s for _, s in result.components]
    assert sampled_path(donor, [receiver], [(0, 1, 0)], settings)["status"] == "not_found"
    assert sampled_path(donor, [receiver], [(0, 0, 1)], settings)["status"] == "sampled_clear"


@pytest.mark.parametrize("gap", [-.1, 1., float("nan"), float("inf")])
def test_bad_clearance(fixture, gap):
    split, settings = fixture
    with pytest.raises(ValueError): build(split, replace(settings, clearance=gap))


@pytest.mark.parametrize("mode", ["absent", "too_far", "too_near"])
def test_missing_or_misplaced_stop(fixture, mode):
    split, settings = fixture
    result = build(split, settings)
    p = result.parameters
    # Remove the end wall or move its bearing face away from the final tongue.
    y = p["stop_y"]
    receiver = result.components[1][1]
    if mode == "too_near":
        tool = cq.Workplane("XY").box(20, 1, 10).translate((0, y-.5, -5)).val()
        receiver = receiver.fuse(tool)
    else:
        length = 60 if mode == "absent" else 1
        tool = cq.Workplane("XY").box(60, length, 40).translate((0, y+length/2, -20)).val()
        receiver = receiver.cut(tool)
    result.components[1] = ("part_2", receiver)
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


def test_wrong_stop_metadata(fixture):
    split, settings = fixture
    result = build(split, settings)
    result.parameters["stop_y"] += 1
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


def test_collision_on_entry(fixture):
    split, settings = fixture
    result = build(split, settings)
    donor, receiver = [s for _, s in result.components]
    cap = cq.Workplane("XY").box(60, 2, 20).translate((0, -26, -10)).val()
    assert sampled_path(donor, [receiver.fuse(cap)], [(0, -1, 0)], settings)["status"] == "not_found"
    result.components[1] = ("part_2", receiver.fuse(cap))
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


@pytest.mark.parametrize("center", [(29, 0), (0, 22)])
def test_thin_walls(fixture, center):
    split, settings = fixture
    with pytest.raises(GeometryRejected):
        build_tongue_groove_stop(split, random.Random(42), settings, centers=[center])


def test_wall_missing_along_entrance_channel(fixture):
    split, settings = fixture
    # The original closed pocket remains feasible, but the opened entrance does not.
    void = cq.Workplane("XY").box(2, 3, 2).translate((0, -20, -3)).val()
    split = replace(split, lower=split.lower.cut(void), original=split.original.cut(void))
    with pytest.raises(GeometryRejected, match="thickness along channel"):
        build(split, settings)


def test_seed_and_step_stl(fixture):
    split, settings = fixture
    a = create_from_model(split.original, 42, connection="tongue_groove_stop", settings=settings)
    b = create_from_model(split.original, 42, connection="tongue_groove_stop", settings=settings)
    assert a.connection.parameters == b.connection.parameters
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/"stop"
        meta = export_result(a, path, settings)
        assert meta["connection"]["joint_type"] == "tongue_groove_stop"
        assert meta["checks"]["step_roundtrip_separate_solids"] == 2
        assert (path/"assembly.stl").stat().st_size > 0


def test_fixed_partition_integration(fixture):
    from cadgen.decomposition import Partition, DecompositionSettings
    from cadgen.decomposition_assembly import assemble_partition
    from cadgen.auto_assembly import export_auto
    split, settings = fixture
    state = Partition(split.original, {"upper": split.upper, "lower": split.lower})
    config = DecompositionSettings()
    assemble_partition(state, 42, settings, config, connection="tongue_groove_stop")
    assert state.assembly["success"], state.assembly
    assert state.joints[0].parameters["joint_type"] == "tongue_groove_stop"
    assert len(state.sequence) == 2
    with tempfile.TemporaryDirectory() as tmp:
        meta = export_auto(state, 42, {}, None, Path(tmp)/"stop", settings, config, {})
        assert meta["success"]
        assert meta["counts"]["grooves"] == meta["counts"]["protrusions"] == 1
        assert meta["joints"][0]["parameters"]["joint_type"] == "tongue_groove_stop"
        assert meta["joints"][0]["parameters"]["stop_checks"]["forward_stop_checked"]
