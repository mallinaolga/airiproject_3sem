"""Existing decomposition -> joint search -> multi-part geometry -> export."""
from dataclasses import replace
import cadquery as cq
import pytest

from cadgen.assembly_geometry import AssemblySettings, GeometryRejected, difference_volume, split_model
from cadgen.assembly_connections import JOINT_TYPES, propose_all_connections
from cadgen.decomposition import DecompositionSettings, decompose_geometry
from cadgen.decomposition_assembly import assemble_partition
from cadgen.assembly_planning import validate_partition
from cadgen.joint_design import materialize


def source():
    # A single stepped source is decomposed by the real BREP algorithm.
    parts = [cq.Workplane("XY").box(w, w-4, 30).translate((0, 0, 15+30*i)).val()
             for i, w in enumerate((70, 60, 50, 40))]
    return parts[0].fuse(*parts[1:]).clean()


@pytest.fixture(scope="module")
def restored():
    geometry = AssemblySettings(path_steps=4)
    settings = DecompositionSettings()
    state = decompose_geometry(source(), settings)
    before = dict(state.raw)
    assemble_partition(state, 42, geometry, settings, "all", check_sequence=False,
                       preferred_types=("bayonet", "snap_fit", "threaded"))
    return state, before, geometry, settings


def test_mixed_multi_body_does_not_invoke_sequence(restored, monkeypatch):
    import cadgen.assembly_planning as planning
    state, before, geometry, settings = restored
    assert len(state.raw) >= 4
    assert state.assembly["success"], state.assembly
    assert {"bayonet", "snap_fit"} <= {j.parameters["joint_type"] for j in state.joints}
    assert len(state.joints) >= 3
    assert state.sequence == [] and not state.checks["assembly_sequence_checked"]
    assert state.checks["graph"]["connected"]
    for name in before:
        assert difference_volume(before[name], state.raw[name]) < geometry.volume_tolerance
    monkeypatch.setattr(planning, "find_sequence", lambda *a: pytest.fail("Planner must not run"))
    checks, sequence = validate_partition(state.original, state.raw, materialize(state.raw,state.joints,geometry),
                                         state.joints, geometry, 256, check_sequence=False)
    assert checks["geometry_verified"] and sequence == []


def test_eight_types_are_real_feasible_options():
    geometry = AssemblySettings(path_steps=4)
    split = split_model(cq.Workplane("XY").box(60,60,50).val(), [0,0,0], [0,0,1], geometry)
    options = propose_all_connections(split, ("a","b"), "j", 42, geometry)
    assert set(JOINT_TYPES) == {j.parameters["joint_type"] for j in options}
    for j in options:
        assert j.parameters["local_geometry_checks"]["valid_single_solid_components"]
        assert j.parameters.get("profile",{}).get("kind") not in ("round","v")
        if j.parameters["joint_type"] == "bolted": assert len(j.hardware) >= 2
        elif j.parameters["joint_type"] == "pinned": assert len(j.hardware) == 1
        else: assert not j.hardware


def test_export_geometry_status_and_roundtrip(restored, tmp_path):
    from cadgen.auto_assembly import export_auto
    state, _, geometry, settings = restored
    meta = export_auto(state,42,{},None,tmp_path/"assembly",geometry,settings,{})
    assert meta["success"] and meta["assembly_status"] == "geometry_verified"
    assert meta["assembly_sequence_status"] == "not_requested"
    assert not meta["assembly_sequence"]
    assert meta["checks"]["step_roundtrip_separate_solids"] == len(state.raw)


def test_final_collision_still_rejected(restored):
    state, _, geometry, settings = restored
    parts = materialize(state.raw,state.joints,geometry)
    names=list(parts)
    parts[names[0]] = parts[names[1]]
    with pytest.raises(GeometryRejected):
        validate_partition(state.original,state.raw,parts,state.joints,geometry,256,check_sequence=False)


def test_disconnected_graph_still_rejected(restored):
    state, _, geometry, _ = restored
    joints = state.joints[:-1]
    with pytest.raises(GeometryRejected, match="disconnected"):
        validate_partition(state.original,state.raw,materialize(state.raw,joints,geometry),
                           joints,geometry,256,check_sequence=False)


def test_rejected_source_is_saved_before_decomposition(tmp_path, monkeypatch):
    import cadgen.auto_assembly as pipeline
    a = cq.Workplane("XY").box(10,10,10).val()
    compound = cq.Compound.makeCompound([a,a.translate((30,0,0))])
    monkeypatch.setattr(pipeline,"generate_source",lambda *a,**k:(compound,{"generator":"test"},None))
    manifest = pipeline.generate_auto_batch(tmp_path/"run",count=1,max_attempts=1,seed=42,connection="all")
    assert manifest["successful_count"] == 0
    failure = manifest["failures"][0]
    assert failure["stage"] == "decomposition"
    assert failure["source_geometry"]["solid_count"] == 2
    folder = tmp_path/"run"/failure["source_folder"]
    assert (folder/"original.step").exists() and (folder/"original.stl").exists()
    assert len(cq.importers.importStep(str(folder/"original.step")).solids().vals()) == 2


def test_no_feasible_design_keeps_reasons():
    geometry = AssemblySettings(path_steps=4)
    split = split_model(cq.Workplane("XY").box(60,60,50).val(), [0,0,0], [0,0,1], geometry)
    with pytest.raises(ValueError, match="Unknown preferred"):
        propose_all_connections(split,("a","b"),"j",42,geometry,preferred_types=("round",))
