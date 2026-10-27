"""Independently inspect delivered files, not in-memory generator results.

python test/validate_auto_examples.py --folder examples/assemblies
Run only on trusted local examples: original.py is replayed to verify provenance.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import re

import cadquery as cq
import numpy as np
import trimesh

from cadgen.assembly_geometry import contact_patch, difference_volume, require_solid, offset_prism
from cadgen.assembly_validation import overlap_volume, transform_part
from cadgen.assembly_planning import union
from cadgen.assembly_generator import save_json
from generirovanie_pazov.generate_grooves import Profile,profile_prism
from Otverstiya import through_hole_cutter
from Bolty import BoltSpec,build_bolt
from Gaiki import NutSpec,build_nut


def declared_voids(metadata,raw):
    result=[];expected=dict(raw)
    for joint in metadata["joints"]:
        p=joint["parameters"];r=np.array(p["cut_to_world_rotation"]);t=np.array(p["cut_origin"])
        upper,lower=[transform_part(raw[n],r.T,-r.T@t) for n in joint["components"]]
        if p["type"] in ("groove","combined"):
            g=p if p["type"]=="groove" else p["groove"]
            pin=profile_prism(Profile(**g["profile"]),g["tool_length"]).translate(tuple(g["center_in_cut_frame"]))
            cavity=offset_prism(pin,g["clearance"])
            void=lower.intersect(cavity).cut(pin)
            if void.Solids():result.append(transform_part(void,r,t))
            donor,receiver=joint["components"]
            expected[donor]=expected[donor].fuse(transform_part(lower.intersect(pin),r,t))
            expected[receiver]=expected[receiver].cut(transform_part(cavity,r,t))
        if p["type"] in ("bolted","combined"):
            for index,bolt in enumerate(p["bolts"]):
                tool=through_hole_cutter(bolt["hole_diameter"],lower.BoundingBox().zmin-1,
                                         upper.BoundingBox().zmax+1,tuple(bolt["center_in_cut_frame"][:2]))
                void=lower.fuse(upper).intersect(tool)
                if void.Solids():result.append(transform_part(void,r,t))
                for owner in joint["components"]:expected[owner]=expected[owner].cut(transform_part(tool,r,t))
                x,y=bolt["center_in_cut_frame"][:2]
                built_bolt=build_bolt(BoltSpec(**bolt["bolt"])).translate((x,y,upper.BoundingBox().zmax))
                built_nut=build_nut(NutSpec(**bolt["nut"])).translate((x,y,lower.BoundingBox().zmin-bolt["nut"]["height"]))
                expected[joint["hardware"][2*index]]=transform_part(built_bolt,r,t)
                expected[joint["hardware"][2*index+1]]=transform_part(built_nut,r,t)
    return (union(result) if result else cq.Compound.makeCompound([])),expected


def verify_model(folder):
    metadata=json.loads((folder/"metadata.json").read_text())
    assert metadata["success"] and metadata["status"]=="success",folder
    assert metadata["source"]["generator"]=="CADFactory",folder
    tolerance=metadata["settings"]["volume_tolerance"]
    original=require_solid(cq.importers.importStep(str(folder/"original.step")).val(),"original")
    namespace={}
    exec(compile((folder/"original.py").read_text(),str(folder/"original.py"),"exec"),namespace)
    assert difference_volume(original,namespace["r"].val())<=tolerance, "CADGen program differs from original STEP"
    parts={};raw={};mass_integration_differences=[]
    for entries,destination in ((metadata["components"],parts),(metadata["raw_components"],raw)):
        for component in entries:
            local=require_solid(cq.importers.importStep(str(folder/component["step"])).val(),component["name"])
            destination[component["name"]]=transform_part(local,component["rotation_matrix"],component["translation"])
            mass_integration_differences.append(dict(file=component["step"],
                absolute_difference=abs(local.Volume()-component["volume"])))
    main={c["name"] for c in metadata["components"] if c["role"]=="main"}
    assert main==set(raw)
    assert len(main)==metadata["main_component_count"]>=2
    assert len(metadata["cuts"])==metadata["cut_count"]
    assert 1+sum(len(c["children"])-1 for c in metadata["cuts"])-len(metadata["checks"].get("geometry_merges",[]))==len(main)
    assert difference_volume(original,union(raw.values()))<=tolerance,"Raw parts do not reconstruct source"
    for a,b in combinations(raw,2):assert overlap_volume(raw[a],raw[b])<=tolerance,(a,b)
    for a,b in combinations(parts,2):assert overlap_volume(parts[a],parts[b])<=tolerance,(a,b)
    # Keep the delivered touching solids separate. OCC fuse can bridge a
    # narrow clearance after STEP reimport even when every individual body
    # is valid and exactly matches its recipe. Subtracting each body tests
    # the actual assembly set without introducing that intermediate union.
    actual_void=original
    for name in sorted(main):
        assert parts[name].cut(original).Volume()<=tolerance
        actual_void=actual_void.cut(parts[name])
    # Compare actual geometric sets, not the subtraction of two independently
    # integrated large-volume values (OCC quadrature can differ numerically).
    expected_void,expected_parts=declared_voids(metadata,raw)
    assert set(expected_parts)==set(parts)
    for name,expected in expected_parts.items():
        assert difference_volume(expected,parts[name])<=tolerance,("Component recipe mismatch",name)
    void_error=difference_volume(actual_void,expected_void)
    assert void_error<=tolerance, ("Technological void geometry mismatch",void_error)
    loaded=cq.importers.importStep(str(folder/"assembly.step"))
    assert len(loaded.solids().vals())==len(parts)
    assert difference_volume(loaded.val(),cq.Compound.makeCompound(list(parts.values())))<=tolerance
    for file,entries,dictionary in (("exploded.step",metadata["components"],parts),
                                     ("split_exploded.step",metadata["raw_components"],raw)):
        expected=[]
        for component in entries:
            shift=np.array(component["exploded_translation"])-np.array(component["translation"])
            expected.append(dictionary[component["name"]].translate(tuple(shift)))
        view=cq.importers.importStep(str(folder/file))
        assert len(view.solids().vals())==len(entries),file
        assert difference_volume(view.val(),cq.Compound.makeCompound(expected))<=tolerance,file
        for a,b in combinations(expected,2):assert overlap_volume(a,b)<=tolerance,file
    graph=metadata["graph"]
    assert graph["connected"] and set(graph["vertices"])==main
    reached={next(iter(main))}
    for _ in main:
        for joint in metadata["joints"]:
            a,b=joint["components"]
            assert contact_patch(raw[a],raw[b]).Area()>1e-6,(a,b)
            if reached.intersection((a,b)):reached.update((a,b))
    assert reached==main
    installed=set()
    for step in metadata["assembly_sequence"]:
        name=step["component"]
        assert name not in installed
        assert set(step["stationary_components"])==installed
        if installed:
            assert not step["continuous_path_proven"]
            assert step["checked_positions"]==len(step["distances"])
            # Additional checks on the exported B-reps at start, mid-path,
            # close to contact and final. Generation checks all saved samples.
            distances=step["distances"]
            for d in {0,max(distances),distances[len(distances)//2],sorted(distances)[1]}:
                shift=-np.array(step["insertion_direction"])*d
                moving=parts[name].translate(tuple(shift))
                fixed=cq.Compound.makeCompound([parts[n] for n in installed])
                assert overlap_volume(moving,fixed)<=tolerance,(name,d)
        installed.add(name)
    assert installed==set(parts)
    assert set(metadata["stopping_conditions"])==main
    technical=bool(metadata["checks"].get("geometry_limits")) or any(
        v["reason"]=="technical_limit_reached" for v in metadata["stopping_conditions"].values())
    assert metadata["checks"]["decomposition_complete_within_search"]== (not technical)
    assert not metadata["checks"]["continuous_path_proven"]
    assert not metadata["checks"]["threaded"]
    meshes={}
    for path in folder.glob("*.stl"):
        mesh=trimesh.load(str(path),force="mesh")
        assert 84<path.stat().st_size<=10_000_000,path
        assert len(mesh.faces)>0 and np.isfinite(mesh.vertices).all() and mesh.volume>0,path
        assert len(mesh.faces)==metadata["stl_exports"][path.name]["triangles"],path
        meshes[path.name]=dict(bytes=path.stat().st_size,triangles=len(mesh.faces))
    assert {"original.stl","split_exploded.stl","parts_exploded.stl","assembly.stl"}<=set(meshes)
    assert len(list(folder.glob("part_*.stl")))==len(main)
    return dict(model=folder.name,seed=metadata["seed"],**metadata["counts"],
                connection_types=dict(Counter(j["parameters"]["type"] for j in metadata["joints"])),
                stop_reasons=dict(Counter(v["reason"] for v in metadata["stopping_conditions"].values())),
                technological_void_error_volume=void_error,mass_integration_differences=mass_integration_differences,
                all_checks_passed=True,stl_files=meshes),original


def verify_geometry(folder):
    from cadgen.decomposition import validate_raw_partition
    metadata=json.loads((folder/"metadata.json").read_text())
    assert metadata["stage"]=="geometry" and metadata["geometry_success"]
    assert not metadata["assembly_success"]
    original=require_solid(cq.importers.importStep(str(folder/"original.step")).val(),"original")
    raw={}
    for component in metadata["raw_components"]:
        local=require_solid(cq.importers.importStep(str(folder/component["step"])).val(),component["name"])
        raw[component["name"]]=transform_part(local,component["rotation_matrix"],component["translation"])
    assert len(raw)==metadata["main_component_count"]
    assert 1+sum(len(c["children"])-1 for c in metadata["cuts"])-len(metadata["checks"].get("geometry_merges",[]))==len(raw)
    checks=validate_raw_partition(original,raw)
    for filename,exploded in (("geometric_partition.step",False),("split_exploded.step",True)):
        shapes=[]
        for c in metadata["raw_components"]:
            shift=np.array(c["exploded_translation"])-np.array(c["translation"]) if exploded else np.zeros(3)
            shapes.append(raw[c["name"]].translate(tuple(shift)))
        view=cq.importers.importStep(str(folder/filename))
        assert len(view.solids().vals())==len(raw)
        assert all(s.isValid() for s in view.solids().vals())
        assert difference_volume(view.val(),cq.Compound.makeCompound(shapes))<=1e-5
        if exploded:
            for a,b in combinations(shapes,2):assert overlap_volume(a,b)<=1e-5
    for path in folder.glob("*.stl"):
        mesh=trimesh.load(str(path),force="mesh")
        assert len(mesh.faces)>0 and np.isfinite(mesh.vertices).all() and mesh.volume>0,path
        assert len(mesh.faces)==metadata["stl_exports"][path.name]["triangles"],path
    assert len(list(folder.glob("part_*.stl")))==len(raw)
    assert set(metadata["stopping_conditions"])==set(raw)
    simple=sum(v.get("analysis",{}).get("recognition",{}).get("simple",False)
               for v in metadata["stopping_conditions"].values())
    return dict(model=folder.parent.name,geometric_components=len(raw),simple=simple,
                unrecognized=len(raw)-simple,all_geometry_checks_passed=True,**checks),original,raw


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder",type=Path,default=Path("examples/assemblies"))
    parser.add_argument("--expected-count",type=int,default=10,help="Number of demonstration models, not parts")
    args=parser.parse_args()
    root=args.folder.resolve()
    models=sorted(p for p in root.glob("model_*") if p.is_dir())
    assert len(models)==args.expected_count
    report=[];originals=[]
    for folder in models:
        if (folder/"geometry").is_dir():
            row,original,raw=verify_geometry(folder/"geometry")
            comparison=json.loads((root/"report.json").read_text())
            reference=Path(comparison["source"])/folder.name/"original.step"
            assert difference_volume(original,cq.importers.importStep(str(reference)).val())<=1e-5
            row["matches_previous_original_step"]=True
            top=json.loads((folder/"metadata.json").read_text())
            attempt=json.loads((folder/"assembly_report.json").read_text())
            assert top["assembly_success"]==attempt["success"]==top["success"]
            assert not attempt["partition_modified"]
            if attempt["success"]:
                ready,_=verify_model(folder/"assembly")
                meta=json.loads((folder/"assembly"/"metadata.json").read_text())
                assert len(meta["raw_components"])==len(raw)
                for c in meta["raw_components"]:
                    shape=cq.importers.importStep(str(folder/"assembly"/c["step"])).val()
                    shape=transform_part(shape,c["rotation_matrix"],c["translation"])
                    assert difference_volume(raw[c["name"]],shape)<=1e-5
                row["assembly_validation"]=ready
            else:
                assert not (folder/"assembly").exists(),"Failed assembly has ready-model exports"
            row["assembly_success"]=attempt["success"]
            print(f"PASS {folder.name}: geometry {len(raw)}; assembly {attempt['status']}",flush=True)
        else:
            row,original=verify_model(folder)
            print(f"PASS {folder.name}: {row['main_components']} main parts; {row['connection_types']}",flush=True)
        assert not any(abs(s.Volume()-original.Volume())<1e-5 and difference_volume(s,original)<1e-5 for s in originals)
        originals.append(original);report.append(row)
    for target in re.findall(r'\]\(([^)]+)\)',(root/"README.md").read_text()):
        assert not target.startswith(("http:","https:","/"))
        assert (root/target).is_file(),target
    result=dict(status="passed",models_verified=len(report),source="existing CADFactory STEP; geometry verified separately from assembly",
                continuous_path_proven=False,models=report)
    save_json(root/"validation.json",result)
    print(f"Verified {len(report)} distinct CADGen sources and all delivered STEP/STL views.")


if __name__=="__main__":main()
