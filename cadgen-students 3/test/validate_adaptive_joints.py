"""Independently verify saved adaptive assemblies; never execute source CADGen."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import cadquery as cq

from cadgen.assembly_geometry import difference_volume
from cadgen.assembly_validation import transform_part
from validate_auto_examples import verify_model


def validate(root, source=None, expected_count=10):
    root=Path(root).resolve()
    report=json.loads((root/"report.json").read_text())
    assert report["status"]=="complete" and report["source_checksums_unchanged"]
    assert len(report["models"])==expected_count
    source=Path(source or report["source"]).resolve()
    rows=[]
    for row in report["models"]:
        folder=root/row["model"];original_folder=source/row["model"]/"geometry"
        original_meta=json.loads((original_folder/"metadata.json").read_text())
        assert row["components"]==original_meta["main_component_count"] and row["partition_unchanged"]
        if row["assembly_success"]:
            # Source identity is checked against the existing STEP. Executing
            # original.py would regenerate CAD and is deliberately disabled.
            result,original=verify_model(folder/"assembly",check_program=False)
            assert difference_volume(original,cq.importers.importStep(str(original_folder/"original.step")).val())<=1e-5
            meta=json.loads((folder/"assembly"/"metadata.json").read_text())
            parts={c["name"]:c for c in meta["raw_components"]}
            for c in original_meta["raw_components"]:
                exported=parts[meta["component_id_map"][c["name"]]]
                a=transform_part(cq.importers.importStep(str(original_folder/c["step"])).val(),
                                 c["rotation_matrix"],c["translation"])
                b=transform_part(cq.importers.importStep(str(folder/"assembly"/exported["step"])).val(),
                                 exported["rotation_matrix"],exported["translation"])
                assert difference_volume(a,b)<=1e-5,(row["model"],c["name"])
            rows.append(dict(result,model=row["model"],all_checks_passed=True))
        else:
            assert not (folder/"assembly").exists(),"Failed assembly has a ready export"
            rows.append(dict(model=row["model"],failed_assembly_has_no_ready_export=True))
        print(f"PASS {row['model']}: assembly={row['assembly_success']}",flush=True)
    actual_hashes={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in source.rglob("*") if p.is_file()}
    assert actual_hashes==report["source_checksums"],"Original decomposition results changed"
    project=Path(__file__).resolve().parents[1]
    subprocess.run(["git","diff","--quiet","HEAD","--","examples/assemblies",
                    "examples/two_stage_decomposition"],cwd=project,check=True)
    for relative in re.findall(r'\]\(([^)]+)\)',(root/"README.md").read_text()):
        assert not relative.startswith(("http:","https:","/"))
        assert (root/relative).is_file(),relative
    result=dict(status="passed",models_verified=len(rows),models=rows,source_files_unchanged=True,
                published_examples_unchanged=True,source_generation_performed=False,
                decomposition_performed=False,continuous_path_proven=False)
    (root/"validation.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"ALL PASSED: {len(rows)} models; original results and published examples preserved.")
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder",default="generations/assemblies/adaptive_joints_final")
    parser.add_argument("--source",help="Override the original decomposition directory recorded in report.json")
    parser.add_argument("--expected-count",type=int,default=10)
    args=parser.parse_args()
    validate(args.folder,args.source,args.expected_count)
