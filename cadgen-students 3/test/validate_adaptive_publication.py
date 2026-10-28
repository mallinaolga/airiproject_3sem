"""Check copied CAD assets, links and dimensions without generating geometry."""

import argparse
import hashlib
import json
from pathlib import Path
import re

import cadquery as cq
import numpy as np
import trimesh


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(folder,protected_snapshot=None,algorithm_snapshot=None):
    folder=Path(folder).resolve();project=folder.parents[1];repo=project.parent
    manifest=json.loads((folder/"publication_manifest.json").read_text())
    audit=json.loads((folder/"joint_dimensions.json").read_text())
    assert audit["joints_count"]==76 and audit["small_joints_count"]==10
    rows=audit["joints"]
    sizes=[r["minimum_nominal_cavity_dimension_mm"] for r in rows]
    assert sizes==sorted(sizes)
    assert len(manifest["models"])==10
    copied_count=stl_count=step_count=parts=0
    for model in manifest["models"]:
        target=folder/model["model"]
        meta=json.loads((target/"metadata.json").read_text())
        dimensions=json.loads((target/"joint_dimensions.json").read_text())
        assert len(dimensions["joints"])==len(meta["joints"])==model["joints"]
        assert len(meta["components"])==model["parts"]
        assert all(c["role"]=="main" for c in meta["components"])
        assert meta["success"] and meta["assembly_report"]["success"]
        assert (target/"original.stl").is_file() and (target/"exploded.stl").is_file()
        for name,item in model["files"].items():
            path=target/name;assert sha(path)==item["sha256"],path
            source=Path(manifest["source"])/model["model"]/"assembly"/item["source"]
            if source.is_file():assert sha(source)==sha(path),path
            copied_count+=1
            if path.suffix==".stl":
                mesh=trimesh.load(str(path),force="mesh")
                assert 84<path.stat().st_size<10_000_000
                assert len(mesh.faces)>0 and np.isfinite(mesh.vertices).all() and mesh.volume>0,path
                stl_count+=1
            elif path.suffix==".step":step_count+=1
        assembly=cq.importers.importStep(str(target/"assembly.step")).solids().vals()
        assert len(assembly)==model["parts"] and all(s.isValid() for s in assembly)
        parts+=len(assembly)
        def references(value):
            if isinstance(value,list):
                for v in value:references(v)
            elif isinstance(value,dict):
                for key,v in value.items():
                    if key in ("file","options_file") and isinstance(v,str):
                        path=(target/v).resolve();assert path.is_relative_to(target) and path.is_file(),path
                        if key=="file" and "sha256" in value:assert sha(path)==value["sha256"]
                    else:references(v)
        references(meta)
        for alternatives in (target/"alternatives").glob("*.json"):
            references(json.loads(alternatives.read_text()))
        for c in meta["components"]+meta["raw_components"]:
            assert (target/c["step"]).is_file()
            if "stl" in c:assert (target/c["stl"]).is_file()
        print(f"PASS {model['model']}: {model['parts']} processed parts, {model['joints']} joints",flush=True)
    assert parts==86 and stl_count==116 and step_count==192
    links=0
    for markdown in [*folder.rglob("*.md"),project/"JOINT_DIMENSIONS.md"]:
        for target in re.findall(r'\]\(([^)]+)\)',markdown.read_text()):
            assert not target.startswith(("http:","https:")),"Examples should use relative links"
            path=(markdown.parent/target.split("#")[0]).resolve()
            assert path.is_file(),(markdown,target)
            links+=1
    protected=0
    for snapshot in (protected_snapshot,algorithm_snapshot):
        if snapshot:
            hashes=json.loads(Path(snapshot).read_text())
            for relative,digest in hashes.items():assert sha(repo/relative)==digest,relative
            protected+=len(hashes)
    types={p.suffix.lower() for p in folder.rglob("*") if p.is_file()}
    assert types<={".md",".json",".step",".stl"},types
    result=dict(status="passed",models=10,parts=parts,joints=76,small_joints=10,
                copied_cad_files=copied_count,stl_files=stl_count,step_files=step_count,
                relative_links_checked=links,protected_files_checked=protected,
                geometry_generation_performed=False,mesh_regeneration_performed=False)
    (folder/"publication_validation.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result),flush=True)
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder",default="examples/adaptive_joints")
    parser.add_argument("--protected-snapshot")
    parser.add_argument("--algorithm-snapshot")
    args=parser.parse_args()
    validate(args.folder,args.protected_snapshot,args.algorithm_snapshot)
