"""Separate pin geometry, invalid fits, assembly integration and STEP roundtrip."""
from dataclasses import replace
from pathlib import Path
import random
import tempfile

import cadquery as cq
import numpy as np
import pytest

from cadgen.assembly_geometry import AssemblySettings, GeometryRejected, split_model, validate_connection
from cadgen.pin_joint import build_pin
from cadgen.joint_design import propose_joints, materialize
from cadgen.assembly_planning import validate_partition
from cadgen.assembly_generator import create_from_model, export_result


@pytest.fixture
def setup_pin():
    settings = AssemblySettings(path_steps=8)
    original = cq.Workplane("XY").box(40, 40, 20).val()
    split = split_model(original, [0, 0, 0], [0, 0, 1], settings)
    return split, settings


def build(split, settings, **kwargs):
    return build_pin(split, random.Random(42), settings, center=(0, 0), **kwargs)


def test_separate_pin_and_measured_holes(setup_pin):
    split, settings = setup_pin
    result = build(split, settings)
    checks = validate_connection(split, result, settings)
    assert checks["coaxial_holes_checked"]
    assert checks["paths"]["pin_1"]["status"] == "sampled_clear"
    assert not result.parameters["integral_protrusion"]
    assert not result.parameters["self_retaining"]
    for name, shape in result.components[:2]:
        cylinders = [f for f in shape.Faces() if f.geomType() == "CYLINDER"]
        assert len(cylinders) == 1
        assert cylinders[0].Area() == pytest.approx(2*np.pi*2.2*10)
    assert result.components[2][1].Volume() == pytest.approx(np.pi * 4 * 20)
    assert max(checks["intersection_volumes"].values()) < settings.volume_tolerance


@pytest.mark.parametrize("diameter", [0, -1, float("nan"), float("inf")])
def test_invalid_diameter(setup_pin, diameter):
    split, settings = setup_pin
    with pytest.raises(ValueError):
        build(split, settings, diameter=diameter)


@pytest.mark.parametrize("gap", [-.1, 1., float("nan")])
def test_invalid_clearance(setup_pin, gap):
    split, settings = setup_pin
    with pytest.raises(ValueError):
        build(split, replace(settings, clearance=gap))


def test_thin_wall_and_internal_void(setup_pin):
    split, settings = setup_pin
    with pytest.raises(GeometryRejected, match="material"):
        build_pin(split, random.Random(42), settings, center=(18, 0))
    void = cq.Solid.makeCylinder(1, 2, cq.Vector(0, 0, -6))
    damaged = replace(split, lower=split.lower.cut(void))
    with pytest.raises(GeometryRejected, match="material"):
        build(damaged, settings)


@pytest.mark.parametrize("component,change", [
    ("pin_1", "offset"), ("pin_1", "short"), ("pin_1", "wide"),
    ("part_2", "offset"), ("pin_1", "missing"), ("pin_1", "extra")])
def test_bad_actual_geometry_is_rejected(setup_pin, component, change):
    split, settings = setup_pin
    result = build(split, settings)
    parts = dict(result.components)
    if change == "offset": parts[component] = parts[component].translate((1, 0, 0))
    elif change == "short": parts[component] = cq.Solid.makeCylinder(2, 5)
    elif change == "wide": parts[component] = cq.Solid.makeCylinder(3, 20, cq.Vector(0, 0, -10))
    elif change == "missing": del parts[component]
    else: parts["pin_2"] = parts[component]
    result.components = list(parts.items())
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


def test_invalid_insertion_direction(setup_pin):
    split, settings = setup_pin
    result = build(split, settings)
    result.paths[-1] = ("pin_1", ["part_1", "part_2"], [(1, 0, 0)])
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


@pytest.mark.parametrize("parameter,value", [("hole_diameter", 3), ("pin_length", 2), ("clearance", 1),
                                            ("hole_diameter", float("nan"))])
def test_inconsistent_dimensions(setup_pin, parameter, value):
    split, settings = setup_pin
    result = build(split, settings)
    result.parameters[parameter] = value
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


@pytest.mark.parametrize("gap", [0., .9])
def test_valid_clearance_boundaries(setup_pin, gap):
    split, settings = setup_pin
    settings = replace(settings, clearance=gap)
    validate_connection(split, build(split, settings), settings)


def test_external_obstacle_blocks_pin_insertion(setup_pin):
    from cadgen.assembly_geometry import sampled_path
    split, settings = setup_pin
    parts = dict(build(split, settings).components)
    cap = cq.Workplane("XY").box(40, 40, 2).translate((0, 0, 12)).val()
    path = sampled_path(parts["pin_1"], [parts["part_1"], parts["part_2"], cap], [(0, 0, 1)], settings)
    assert path["status"] == "not_found"


def test_partition_pin_export(setup_pin):
    from cadgen.decomposition import Partition, DecompositionSettings
    from cadgen.decomposition_assembly import assemble_partition
    from cadgen.auto_assembly import export_auto
    split, geometry = setup_pin
    settings = DecompositionSettings()
    state = Partition(split.original, {"upper": split.upper, "lower": split.lower})
    assemble_partition(state, 42, geometry, settings, connection="pinned")
    assert state.assembly["success"], state.assembly
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)/"partition"
        meta = export_auto(state, 42, {}, None, target, geometry, settings, {"connection": "pinned"})
        assert meta["counts"]["pins"] == 1
        assert meta["counts"]["nuts"] == 0
        assert [c["role"] for c in meta["components"]].count("pin") == 1
        solids = cq.importers.importStep(str(target/"assembly.step")).solids().vals()
        assert len(solids) == 3 and all(s.isValid() for s in solids)


def test_joint_sequence_and_rotated_axis(setup_pin):
    split, settings = setup_pin
    original = split.original.rotate((0, 0, 0), (0, 1, 0), 90)
    split = split_model(original, [0, 0, 0], [1, 0, 0], settings)
    joint = propose_joints(split, ("upper", "lower"), "j1", 42, settings, connection="pinned")[0]
    raw = {"upper": split.world(split.upper), "lower": split.world(split.lower)}
    parts = materialize(raw, [joint], settings)
    checks, sequence = validate_partition(original, raw, parts, [joint], settings, 128)
    assert checks["assembly_sequence_checked"]
    assert sequence[-1]["component"] == "j1_pin_1"
    assert joint.parameters["hardware_directions_world"]["j1_pin_1"] == [[1., 0., 0.]]


def test_seed_and_step_stl_export(setup_pin):
    split, settings = setup_pin
    first = create_from_model(split.original, 42, connection="pinned", settings=settings)
    second = create_from_model(split.original, 42, connection="pinned", settings=settings)
    assert first.connection.parameters == second.connection.parameters
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)/"pin"
        meta = export_result(first, target, settings)
        assert meta["checks"]["step_roundtrip_separate_solids"] == 3
        assert meta["components"][2]["provenance"] == "cadgen.pin_joint.build_pin"
        for suffix in ("step", "stl"):
            assert (target/f"pin_1.{suffix}").stat().st_size > 0
