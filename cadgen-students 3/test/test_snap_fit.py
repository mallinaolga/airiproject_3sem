"""Prescribed bending, engagement and two-body snap-fit integration."""
from dataclasses import replace
import cadquery as cq
import pytest

from cadgen.assembly_geometry import AssemblySettings, GeometryRejected, split_model, validate_connection
from cadgen.assembly_validation import overlap_volume
from cadgen.snap_fit import SnapFitSpec, build_snap_fit, check_snap_motion, tongue_shape, pair_sequence


@pytest.fixture
def fixture():
    settings = AssemblySettings(path_steps=4)
    original = cq.Workplane("XY").box(50, 50, 40).val()
    return split_model(original, [0, 0, 0], [0, 0, 1], settings), settings


@pytest.mark.parametrize("gap", [0., .2, .9])
def test_snapping_deformation_retention_and_release(fixture, gap):
    split, settings = fixture
    settings = replace(settings, clearance=gap)
    spec = SnapFitSpec()
    result = build_snap_fit(split, settings, spec)
    report = validate_connection(split, result, settings)["snap_fit_checks"]
    assert [n for n, _ in result.components] == ["part_1", "part_2"]
    assert all(s.isValid() and len(s.Solids()) == 1 for _, s in result.components)
    assert result.parameters["additional_components"] == []
    assert result.parameters["joint_type"] == "snap_fit"
    assert result.parameters["engagement_depth"] == pytest.approx(spec.hook_height-gap)
    assert result.components[0][1].Volume() > split.upper.Volume()
    assert result.components[1][1].Volume() < split.lower.Volume()
    assert result.paths == []
    assert report["status"] == "sampled_deformation_clear"
    assert report["maximum_sampled_deflection"] == pytest.approx(spec.required_deflection(gap))
    assert {p["stage"] for p in report["poses"]} == {"approach", "cam_deflection", "pass_shoulder", "recover", "seat"}
    assert any(p["deflection"] > 0 for p in report["poses"])
    assert report["poses"][-1]["deflection"] == report["poses"][-1]["axial_translation"] == 0
    assert max(p["intersection_volume"] for p in report["poses"]) <= settings.volume_tolerance
    assert report["straight_withdrawal_blocked"]
    assert report["retention_intersection_volume"] > settings.volume_tolerance
    assert report["release"]["poses"] == list(reversed(report["poses"]))
    assert report["release"]["requires_external_actuation"]
    assert not report["physical_elasticity_checked"] and not report["continuous_path_proven"]
    # The assumed displacement leaves the root fixed and moves the tip left.
    bent = tongue_shape(spec, report["maximum_sampled_deflection"])
    assert bent.Volume() == pytest.approx(tongue_shape(spec).Volume())
    assert bent.BoundingBox().xmin < tongue_shape(spec).BoundingBox().xmin


@pytest.mark.parametrize("spec", [SnapFitSpec(length=4), SnapFitSpec(thickness=3),
    SnapFitSpec(relief_depth=.1), SnapFitSpec(max_deflection=.1), SnapFitSpec(hook_height=.1),
    SnapFitSpec(length=19), SnapFitSpec(width=48), SnapFitSpec(ramp_angle_degrees=89)])
def test_rejected_designs(fixture, spec):
    split, settings = fixture
    with pytest.raises(GeometryRejected): build_snap_fit(split, settings, spec)


@pytest.mark.parametrize("spec", [SnapFitSpec(length=10, thickness=.8, width=3, hook_height=1),
                                 SnapFitSpec(ramp_angle_degrees=45, width=5)])
def test_parameterized_cantilevers(fixture, spec):
    split, settings = fixture
    result = build_snap_fit(split, settings, spec)
    checks = validate_connection(split, result, settings)["snap_fit_checks"]
    assert checks["status"] == "sampled_deformation_clear"
    assert checks["maximum_sampled_deflection"] == pytest.approx(spec.required_deflection(settings.clearance))


@pytest.mark.parametrize("gap", [-.1, 1, float("nan")])
def test_bad_clearance(fixture, gap):
    split, settings = fixture
    with pytest.raises(ValueError): build_snap_fit(split, replace(settings, clearance=gap))


@pytest.mark.parametrize("mutation", ["missing_part", "extra_hardware", "final_position", "shoulder", "metadata", "rigid_path"])
def test_rejects_changed_pair(fixture, mutation):
    split, settings = fixture
    result = build_snap_fit(split, settings)
    if mutation == "missing_part": result.components.pop()
    elif mutation == "extra_hardware":
        result.components.append(("pin_1", cq.Solid.makeCylinder(1, 2)))
    elif mutation == "final_position":
        n, s = result.components[0]
        result.components[0] = n, s.translate((.1, 0, 0))
    elif mutation == "shoulder":
        n, s = result.components[1]
        result.components[1] = n, s.translate((0, 0, -.1))
    elif mutation == "metadata": result.parameters["required_deflection"] = 0
    else: result.paths = [("part_1", ["part_2"], [(0, 0, 1)])]
    with pytest.raises(GeometryRejected): validate_connection(split, result, settings)


def test_actual_relief_obstruction_collides_only_when_bent(fixture):
    split, settings = fixture
    result = build_snap_fit(split, settings)
    donor, receiver = [s for _, s in result.components]
    # Bridge attached to the left slot wall, clear of the relaxed tongue.
    obstruction = cq.Solid.makeBox(2.4, 2, .5, cq.Vector(-3, -1, -6.25))
    blocked = receiver.fuse(obstruction)
    assert overlap_volume(donor, blocked) <= settings.volume_tolerance
    with pytest.raises(GeometryRejected, match="collision"):
        check_snap_motion(donor, blocked, result.parameters, settings)


def test_missing_retaining_shoulder_has_no_engagement(fixture):
    split, settings = fixture
    result = build_snap_fit(split, settings)
    donor, receiver = [s for _, s in result.components]
    spec = SnapFitSpec()
    tool = cq.Solid.makeBox(30, spec.width+2*settings.clearance, spec.length,
                           cq.Vector(spec.thickness/2+settings.clearance,
                                     -spec.width/2-settings.clearance, -spec.length))
    receiver = receiver.cut(tool)
    with pytest.raises(GeometryRejected, match="no geometric axial engagement"):
        check_snap_motion(donor, receiver, result.parameters, settings)


def test_approach_obstacle(fixture):
    split, settings = fixture
    result = build_snap_fit(split, settings)
    donor, receiver = [s for _, s in result.components]
    obstruction = cq.Workplane("XY").box(30, 30, 2).translate((0, 0, 25)).val()
    with pytest.raises(GeometryRejected, match="approach collision"):
        check_snap_motion(donor, receiver.fuse(obstruction), result.parameters, settings)


def test_mixed_sequence_is_unverified(fixture):
    _, settings = fixture
    with pytest.raises(GeometryRejected, match="isolated two-body"):
        pair_sequence({}, {}, [object(), object()], settings)


def test_seed_step_stl_and_roundtrip(fixture, tmp_path):
    from cadgen.assembly_generator import create_from_model, export_result
    split, settings = fixture
    a = create_from_model(split.original, 42, connection="snap_fit", settings=settings)
    b = create_from_model(split.original, 42, connection="snap_fit", settings=settings)
    assert a.connection.parameters == b.connection.parameters
    meta = export_result(a, tmp_path/"snap", settings)
    assert len(meta["components"]) == 2
    assert meta["checks"]["step_roundtrip_separate_solids"] == 2
    assert (tmp_path/"snap"/"assembly.stl").stat().st_size > 0


def test_rotated_pair_sequence_and_export(fixture, tmp_path):
    from cadgen.decomposition import Partition, DecompositionSettings
    from cadgen.decomposition_assembly import assemble_partition
    from cadgen.auto_assembly import export_auto
    split, settings = fixture
    transform = lambda s: s.rotate((0, 0, 0), (0, 1, 0), 90).translate((30, 20, 10))
    state = Partition(transform(split.original), {"upper": transform(split.upper), "lower": transform(split.lower)})
    config = DecompositionSettings()
    assemble_partition(state, 42, settings, config, connection="snap_fit")
    assert state.assembly["success"], state.assembly
    assert len(state.sequence) == 2 and state.joints[0].hardware == []
    assert state.sequence[1]["action"] == "prescribed_cantilever_deflection"
    assert abs(state.sequence[1]["insertion_direction"][0]) == pytest.approx(1.)
    assert any(p["deflection"] > 0 for p in state.sequence[1]["poses_in_cut_frame"])
    meta = export_auto(state, 42, {}, None, tmp_path/"pair", settings, config, {})
    assert len(meta["components"]) == 2
    assert meta["joints"][0]["parameters"]["joint_type"] == "snap_fit"
