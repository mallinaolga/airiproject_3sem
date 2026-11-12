"""Actual smooth through-bolt fits, hardware dependencies and export."""
from dataclasses import replace
from pathlib import Path
import random
import tempfile
import cadquery as cq
import pytest

from Bolty import BoltSpec, build_bolt
from Otverstiya import through_hole_cutter
from cadgen.assembly_geometry import AssemblySettings, GeometryRejected, build_bolted, split_model, validate_connection, sampled_path
from cadgen.assembly_generator import GeneratedAssembly, export_result
from cadgen.joint_design import bolt_group, make_joint, materialize
from cadgen.assembly_planning import validate_partition


@pytest.fixture
def fixture():
    settings = AssemblySettings(path_steps=8)
    original = cq.Workplane("XY").box(60, 50, 30).val()
    return split_model(original, [0, 0, 0], [0, 0, 1], settings), settings


def build(split, settings):
    return build_bolted(split, random.Random(42), settings, centers=[(0, 0)], diameter=4)


@pytest.mark.parametrize("gap", [0., .2, .9])
def test_measured_fit_and_hardware_paths(fixture, gap):
    split, settings = fixture
    settings = replace(settings, clearance=gap)
    result = build(split, settings)
    checks = validate_connection(split, result, settings)
    assert result.parameters["joint_type"] == "bolted"
    fit = checks["bolted_fit_checks"][0]
    assert fit["coaxiality_checked"] and fit["shaft_reaches_through_nut"]
    assert fit["actual_radial_clearance"] == pytest.approx(gap)
    assert fit["head_bearing_area"] > 0 and fit["nut_bearing_area"] > 0
    assert checks["paths"]["bolt_1"]["status"] == checks["paths"]["nut_1"]["status"] == "sampled_clear"
    assert not checks["threaded"]


@pytest.mark.parametrize("gap", [-.1, 1., float("nan"), float("inf")])
def test_direct_builder_checks_clearance(fixture, gap):
    split, settings = fixture
    with pytest.raises(ValueError): build(split, replace(settings, clearance=gap))


@pytest.mark.parametrize("diameter", [0, -1, float("nan")])
def test_direct_builder_checks_diameter(fixture, diameter):
    split, settings = fixture
    with pytest.raises(ValueError): build_bolted(split, random.Random(42), settings, diameter=diameter)


@pytest.mark.parametrize("name,shift", [("bolt_1", (.05, 0, 0)), ("nut_1", (.05, 0, 0)),
                                      ("bolt_1", (0, 0, .5)), ("nut_1", (0, 0, -.5))])
def test_noncolliding_misalignment_or_missing_bearing_rejected(fixture, name, shift):
    split, settings = fixture
    result = build(split, settings)
    result.components = [(n, s.translate(shift) if n == name else s) for n,s in result.components]
    with pytest.raises(GeometryRejected, match="placement mismatch"):
        validate_connection(split, result, settings)


def test_short_bolt_even_with_matching_metadata_is_rejected(fixture):
    split, settings = fixture
    result = build(split, settings)
    spec = replace(BoltSpec(**result.parameters["bolt"]), shaft_length=10)
    result.parameters["bolt"]["shaft_length"] = 10
    result.components[2] = ("bolt_1", build_bolt(spec).translate((0, 0, 15)))
    with pytest.raises(GeometryRejected, match="length"):
        validate_connection(split, result, settings)


def test_oversized_actual_holes_rejected(fixture):
    split, settings = fixture
    result = build(split, settings)
    tool = through_hole_cutter(5, -16, 16)
    result.components[:2] = [(n, s.cut(tool)) for n,s in result.components[:2]]
    result.removed = split.original.intersect(tool)
    with pytest.raises(GeometryRejected, match="bore diameter"):
        validate_connection(split, result, settings)


def test_insufficient_bearing_material(fixture):
    split, settings = fixture
    with pytest.raises(GeometryRejected, match="material column"):
        build_bolted(split, random.Random(42), settings, centers=[(24, 0)], diameter=4)


@pytest.mark.parametrize("mutation", ["missing_nut", "missing_path", "nut_without_bolt", "nut_first"])
def test_incomplete_hardware_or_dependencies(fixture, mutation):
    split, settings = fixture
    result = build(split, settings)
    if mutation == "missing_nut": result.components.pop()
    elif mutation == "missing_path": result.paths.pop()
    elif mutation == "nut_first": result.paths[1:] = list(reversed(result.paths[1:]))
    else: result.paths[-1] = ("nut_1", ["part_1", "part_2"], [(0, 0, -1)])
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


@pytest.mark.parametrize("name,direction,z", [("bolt_1", (0, 0, 1), 22), ("nut_1", (0, 0, -1), -24)])
def test_external_obstacle_blocks_hardware(fixture, name, direction, z):
    split, settings = fixture
    parts = dict(build(split, settings).components)
    obstacle = cq.Workplane("XY").box(30, 30, 2).translate((0, 0, z)).val()
    stationary = [s for n,s in parts.items() if n != name] + [obstacle]
    assert sampled_path(parts[name], stationary, [direction], settings)["status"] == "not_found"


def test_two_bolt_sequence_and_export(fixture):
    split, settings = fixture
    result = bolt_group(split, [(-13, 0), (13, 0)], 42, settings, 2)
    assert result.parameters["joint_type"] == "bolted"
    checks = validate_connection(split, result, settings)
    assert len(checks["bolted_fit_checks"]) == 2
    joint = make_joint(split, result, ("upper", "lower"), "j1", 5, {}, settings)
    raw = {"upper": split.world(split.upper), "lower": split.world(split.lower)}
    _, sequence = validate_partition(split.world(split.original), raw, materialize(raw, [joint], settings), [joint], settings, 128)
    order = {step["component"]: step["step"] for step in sequence}
    for i in (1, 2):
        assert max(order["upper"], order["lower"]) < order[f"j1_bolt_{i}"] < order[f"j1_nut_{i}"]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/"bolted"
        assembly = GeneratedAssembly(split.world(split.original), split, result, checks, 42)
        meta = export_result(assembly, path, settings)
        assert meta["checks"]["step_roundtrip_separate_solids"] == 6
        assert meta["connection"]["joint_type"] == "bolted"
        assert (path/"assembly.stl").stat().st_size > 0


def test_constructive_through_bolt(fixture):
    from cadgen.constructive_fasteners import fasten
    from cadgen.constructive_geometry import ConstructiveSettings
    split, settings = fixture
    result = fasten(split, [(0, 0)], 4, settings, ConstructiveSettings())
    assert result.parameters["joint_type"] == "bolted"
    assert validate_connection(split, result, settings)["bolted_fit_checks"][0]["coaxiality_checked"]
