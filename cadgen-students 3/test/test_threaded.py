"""Integral symbolic threaded pair: no fastener bodies or physical thread."""
from dataclasses import replace
import math
import random
import cadquery as cq
import pytest

from Otverstiya import through_hole_cutter
from cadgen.assembly_geometry import (AssemblySettings, GeometryRejected, split_model,
    validate_connection, difference_volume, sampled_path)
from cadgen.threaded import build_threaded


@pytest.fixture
def fixture():
    settings = AssemblySettings(path_steps=8)
    original = cq.Workplane("XY").box(60, 50, 30).val()
    return split_model(original, [0, 0, 0], [0, 0, 1], settings), settings


def build(split, settings, **kwargs):
    return build_threaded(split, random.Random(42), settings, centers=[(0, 0)], diameter=4, **kwargs)


@pytest.mark.parametrize("gap", [0., .2, .9])
def test_integral_pair_and_symbolic_metadata(fixture, gap):
    split, settings = fixture
    settings = replace(settings, clearance=gap)
    result = build(split, settings)
    checks = validate_connection(split, result, settings)
    p = result.parameters
    assert p["type"] == p["joint_type"] == "threaded"
    assert p["thread_representation"] == "symbolic" and p["thread_geometry"] is False
    assert p["nominal_pitch"] is None and p["nominal_diameter"] == 4
    assert p["additional_components"] == []
    assert p["participating_components"] == ["part_1", "part_2"]
    assert [n for n, _ in result.components] == ["part_1", "part_2"]
    assert all(len(s.Solids()) == 1 for _, s in result.components)
    donor, receiver = [s for _, s in result.components]
    boss = cq.Solid.makeCylinder(2, 6, cq.Vector(0, 0, -6))
    cavity = cq.Solid.makeCylinder(2+gap, 6+gap, cq.Vector(0, 0, -6-gap))
    assert difference_volume(donor, split.upper.fuse(boss)) < settings.volume_tolerance
    assert difference_volume(receiver, split.lower.cut(cavity)) < settings.volume_tolerance
    assert donor.Volume()-split.upper.Volume() == pytest.approx(math.pi*4*6)
    assert not checks["helical_motion_checked"]
    assert checks["threaded_fit_checks"]["coaxiality_checked"]
    assert checks["paths"]["part_1"]["status"] == "sampled_clear"
    assert not checks["mechanical_retention_checked"]


def test_no_real_threads_or_fastener_builders(fixture, monkeypatch):
    import Bolty
    import Gaiki
    import cadgen.assembly_geometry as geometry
    def forbidden(*args, **kwargs):
        pytest.fail("Threaded must not call a bolt or nut builder")
    monkeypatch.setattr(Bolty, "build_bolt", forbidden)
    monkeypatch.setattr(Gaiki, "build_nut", forbidden)
    monkeypatch.setattr(geometry, "build_bolted", forbidden)
    monkeypatch.setattr(geometry, "build_bolt", forbidden)
    monkeypatch.setattr(geometry, "build_nut", forbidden)
    split, settings = fixture
    a, b = [build(split, settings, pitch=p) for p in (None, 1.25)]
    for result in (a, b):
        validate_connection(split, result, settings)
        assert len(result.components) == 2
        for _, shape in result.components:
            assert set(f.geomType() for f in shape.Faces()) <= {"PLANE", "CYLINDER"}
            assert set(e.geomType() for e in shape.Edges()) <= {"LINE", "CIRCLE"}
    assert a.parameters["nominal_pitch"] is None and b.parameters["nominal_pitch"] == 1.25
    for (_, one), (_, two) in zip(a.components, b.components):
        assert difference_volume(one, two) < settings.volume_tolerance


@pytest.mark.parametrize("gap", [-.1, 1., float("nan")])
def test_bad_clearance(fixture, gap):
    split, settings = fixture
    with pytest.raises(ValueError): build(split, replace(settings, clearance=gap))


@pytest.mark.parametrize("pitch", [0, -1, float("nan")])
def test_bad_nominal_pitch(fixture, pitch):
    split, settings = fixture
    with pytest.raises(ValueError): build(split, settings, pitch=pitch)


@pytest.mark.parametrize("diameter", [0, -1, float("nan")])
def test_bad_diameter(fixture, diameter):
    split, settings = fixture
    with pytest.raises(ValueError):
        build_threaded(split, random.Random(42), settings, diameter=diameter)


@pytest.mark.parametrize("depth", [.5, 14.])
def test_insufficient_engagement_or_floor(fixture, depth):
    split, settings = fixture
    with pytest.raises(GeometryRejected): build(split, settings, engagement_length=depth)


@pytest.mark.parametrize("mutation", ["axis", "hole", "short", "missing_part", "extra_body",
                                     "collision", "engagement", "diameter", "real_thread", "helical_claim"])
def test_invalid_fit_or_metadata(fixture, mutation):
    split, settings = fixture
    result = build(split, settings)
    if mutation == "axis":
        name, shape = result.components[0]
        result.components[0] = name, shape.translate((.05, 0, 0))
    elif mutation == "hole":
        tool = through_hole_cutter(5, -6.2, 0)
        result.components[1] = "part_2", split.lower.cut(tool)
    elif mutation == "short":
        tool = through_hole_cutter(4, -6, -2)
        result.components[0] = "part_1", result.components[0][1].cut(tool)
    elif mutation == "missing_part": result.components.pop()
    elif mutation == "extra_body":
        result.components.append(("bolt_1", cq.Solid.makeCylinder(1, 2, cq.Vector(0, 0, 40))))
    elif mutation == "collision":
        n, s = result.components[0]
        result.components[0] = n, s.translate((0, 0, -1))
    elif mutation == "engagement": result.parameters["engagement_length"] = .5
    elif mutation == "diameter": result.parameters["nominal_diameter"] = 6
    elif mutation == "real_thread": result.parameters["thread_geometry"] = True
    else: result.parameters["helical_motion_checked"] = True
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


@pytest.mark.parametrize("side", ["socket", "anchor"])
def test_insufficient_material(fixture, side):
    split, settings = fixture
    xy = (28, 0)
    if side == "anchor":
        split = replace(split, upper=split.upper.cut(through_hole_cutter(2, 0, 3)))
        xy = (0, 0)
    with pytest.raises(GeometryRejected, match="material"):
        build_threaded(split, random.Random(42), settings, centers=[xy], diameter=4)


def test_blocked_proxy_insertion(fixture):
    split, settings = fixture
    parts = dict(build(split, settings).components)
    obstacle = cq.Workplane("XY").box(30, 30, 2).translate((0, 0, 22)).val()
    assert sampled_path(parts["part_1"], [parts["part_2"], obstacle],
                        [(0, 0, 1)], settings)["status"] != "sampled_clear"


def test_generator_step_stl_and_roundtrip(fixture, tmp_path):
    from cadgen.assembly_generator import create_from_model, export_result
    split, settings = fixture
    result = create_from_model(split.original, 42, connection="threaded", settings=settings)
    again = create_from_model(split.original, 42, connection="threaded", settings=settings)
    assert result.connection.parameters == again.connection.parameters
    target = tmp_path/"threaded"
    meta = export_result(result, target, settings)
    assert meta["connection"]["joint_type"] == "threaded"
    assert meta["checks"]["step_roundtrip_separate_solids"] == 2
    assert len(meta["components"]) == 2
    assert (target/"assembly.stl").stat().st_size > 0


def test_partition_sequence_and_export(fixture, tmp_path):
    from cadgen.decomposition import Partition, DecompositionSettings
    from cadgen.decomposition_assembly import assemble_partition
    from cadgen.auto_assembly import export_auto
    split, settings = fixture
    state = Partition(split.original, {"upper": split.upper, "lower": split.lower})
    config = DecompositionSettings()
    assemble_partition(state, 42, settings, config, connection="threaded")
    assert state.assembly["success"], state.assembly
    assert not state.checks["assembly_sequence_checked"]
    assert state.checks["smooth_proxy_sequence_checked"]
    assert not state.checks["helical_motion_checked"]
    joint = state.joints[0]
    assert set(joint.parameters["participating_components"]) == set(joint.owners)
    assert joint.hardware == []
    assert len(state.sequence) == 2
    assert state.sequence[1]["action"] == "smooth_proxy_linear_insertion"
    assert not state.sequence[1]["helical_motion_checked"]
    meta = export_auto(state, 42, {}, None, tmp_path/"pair", settings, config, {})
    assert meta["success"] and meta["joints"][0]["parameters"]["joint_type"] == "threaded"
    assert len(meta["components"]) == 2
    assert meta["counts"]["bolts"] == meta["counts"]["nuts"] == meta["counts"]["pins"] == 0
