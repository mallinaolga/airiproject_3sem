"""Two-phase bayonet motion, retention witnesses and export regressions."""
from dataclasses import replace
from pathlib import Path
import tempfile
import cadquery as cq
import pytest

from cadgen.assembly_geometry import AssemblySettings, GeometryRejected, split_model, validate_connection
from cadgen.bayonet import BayonetSpec, build_bayonet, check_bayonet_motion
from cadgen.assembly_generator import create_from_model, export_result


@pytest.fixture
def fixture():
    settings = AssemblySettings(path_steps=12)
    original = cq.Workplane("XY").box(50, 50, 40).val()
    return split_model(original, [0, 0, 0], [0, 0, 1], settings), settings


@pytest.mark.parametrize("gap", [0., .2, .9])
def test_axial_then_rotation_and_reverse(fixture, gap):
    split, settings = fixture
    settings = replace(settings, clearance=gap)
    result = build_bayonet(split, settings)
    checks = validate_connection(split, result, settings)
    motion = checks["paths"]["part_1"]
    assert result.parameters["joint_type"] == "bayonet"
    assert result.parameters["lug_count"] == 2
    assert not result.parameters["self_locking"]
    assert result.paths == []
    assert motion["status"] == "sampled_clear"
    assert motion["locked_axial_withdrawal_blocked"]
    assert motion["axial_lock_intersection_volume"] > settings.volume_tolerance
    assert motion["rotation_stage"]["angles_degrees_from_entry"] == pytest.approx(list(range(0, 61, 5)))
    assert "sampled_clear" in motion["reverse_rotation_and_withdrawal"]
    assert not motion["continuous_path_proven"]


@pytest.mark.parametrize("gap", [-.1, 1, float("nan")])
def test_bad_clearance(fixture, gap):
    split, settings = fixture
    with pytest.raises(ValueError): build_bayonet(split, replace(settings, clearance=gap))


@pytest.mark.parametrize("spec", [BayonetSpec(depth=3), BayonetSpec(depth=19), BayonetSpec(radius=23),
                                 BayonetSpec(turn_angle=5), BayonetSpec(turn_angle=170)])
def test_bad_wall_depth_or_angle(fixture, spec):
    split, settings = fixture
    with pytest.raises(GeometryRejected): build_bayonet(split, settings, spec)


@pytest.mark.parametrize("kind", ["axis_offset", "wrong_lug_angle", "wrong_depth"])
def test_incompatible_actual_placement(fixture, kind):
    split, settings = fixture
    result = build_bayonet(split, settings)
    donor = result.components[0][1]
    if kind == "axis_offset": donor = donor.translate((.05, 0, 0))
    elif kind == "wrong_lug_angle": donor = donor.rotate((0, 0, 0), (0, 0, 1), -30)
    else: donor = donor.translate((0, 0, .1))
    result.components[0] = ("part_1", donor)
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


def test_bad_kinematic_depth_metadata(fixture):
    split, settings = fixture
    result = build_bayonet(split, settings)
    result.parameters["insertion_depth"] += 1
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


@pytest.mark.parametrize("stage", ["entry", "turn", "final"])
def test_obstructed_motion(fixture, stage):
    split, settings = fixture
    result = build_bayonet(split, settings)
    donor, receiver = [s for _,s in result.components]
    # A compact obstacle intersects a lug at the specified phase.
    angle, z = {"entry": (0, -4), "turn": (30, -8), "final": (60, -8)}[stage]
    obstacle = cq.Workplane("XY").box(1, 1, 1).translate((7, 0, z)).val().rotate((0, 0, 0), (0, 0, 1), angle)
    with pytest.raises(GeometryRejected, match="collides"):
        check_bayonet_motion(donor, receiver.fuse(obstacle), result.parameters, settings)


def test_no_linear_path_substitution(fixture):
    split, settings = fixture
    result = build_bayonet(split, settings)
    result.paths = [("part_1", ["part_2"], [(0, 0, 1)])]
    with pytest.raises(GeometryRejected, match="linear-only"):
        validate_connection(split, result, settings)


def test_multi_joint_sequence_is_explicitly_unverified(fixture):
    from cadgen.bayonet import pair_sequence
    _, settings = fixture
    with pytest.raises(GeometryRejected, match="only an isolated two-body pair"):
        pair_sequence({}, {}, [object(), object()], settings)


def test_step_stl_and_seed(fixture):
    split, settings = fixture
    a = create_from_model(split.original, 42, connection="bayonet", settings=settings)
    b = create_from_model(split.original, 42, connection="bayonet", settings=settings)
    assert a.connection.parameters == b.connection.parameters
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)/"bayonet"
        meta = export_result(a, target, settings)
        assert meta["checks"]["step_roundtrip_separate_solids"] == 2
        assert meta["connection"]["joint_type"] == "bayonet"
        assert (target/"assembly.stl").stat().st_size > 0


def test_rotated_pair_partition_and_export(fixture):
    from cadgen.decomposition import Partition, DecompositionSettings
    from cadgen.decomposition_assembly import assemble_partition
    from cadgen.auto_assembly import export_auto
    split, settings = fixture
    turn = lambda s: s.rotate((0, 0, 0), (0, 1, 0), 90).translate((30, 20, 10))
    state = Partition(turn(split.original), {"upper": turn(split.upper), "lower": turn(split.lower)})
    config = DecompositionSettings()
    assemble_partition(state, 42, settings, config, connection="bayonet")
    assert state.assembly["success"], state.assembly
    assert state.sequence[1]["action"] == "axial_then_rotation"
    assert abs(state.sequence[1]["axis"][0]) == pytest.approx(1.)
    assert len(state.sequence[1]["stages"]) == 2
    with tempfile.TemporaryDirectory() as tmp:
        meta = export_auto(state, 42, {}, None, Path(tmp)/"pair", settings, config, {})
        assert meta["success"]
        assert meta["joints"][0]["parameters"]["joint_type"] == "bayonet"
