"""Ten CADGen sources through the existing automatic generation pipeline."""
import argparse
import json
from pathlib import Path
from collections import Counter

from cadgen.assembly_connections import JOINT_TYPES
from cadgen.assembly_geometry import AssemblySettings
from cadgen.auto_assembly import generate_auto_batch
from cadgen.assembly_generator import save_json


def finalize_existing(output):
    """Preserve failed sources from the first run and write a compact report.

    Regeneration uses the same recorded seed; it is not a replacement attempt.
    Future runs already save these sources before decomposition.
    """
    import cadquery as cq
    from cadgen.assembly_source import generate_source
    summary = json.loads((output/"summary.json").read_text(encoding="utf-8"))
    table = ["# All bracings: ten CADGen inputs", "",
             "Global installation order/trajectories were not checked.", "",
             "| Model | Seed | Raw parts | Joints | Selected types | Result |",
             "|---|---|---|---|---|---|"]
    for row in summary["models"]:
        folder = output/f"model_{row['model']:02d}"
        for failure in row["failures"]:
            if (failure.get("source_parameters") and not failure.get("source_folder")
                    and not failure.get("geometry_folder")):
                target = folder/"source_recovered_from_recorded_seed"
                if not target.exists():
                    target.mkdir()
                    try:
                        shape, parameters, program = generate_source(row["seed"], complexity="decomposition")
                        save_json(target/"parameters.json", parameters)
                        (target/"original.py").write_text(program,encoding="utf-8")
                        details = dict(regenerated_from_same_seed=True, source_valid=shape.isValid(),
                                       solid_count=len(shape.Solids()), volume=shape.Volume())
                        save_json(target/"source_check.json", details)
                        cq.exporters.export(shape,str(target/"original.step"))
                        cq.exporters.export(shape,str(target/"original.stl"))
                    except Exception as error:
                        save_json(target/"recovery_error.json",dict(reason=str(error)))
                failure["diagnostic_source_folder"] = target.name
        if row["assemblies"]:
            entry = row["assemblies"][0]
            raw, joints = entry["main_components"], entry["joint_count"]
            types = ", ".join(f"{k}: {v}" for k,v in entry["connection_types"].items())
            status = "geometry_verified; STEP/STL exported"
        else:
            failure = row["failures"][0]
            raw = "—"
            if failure.get("geometry_folder"):
                metadata = json.loads((folder/failure["geometry_folder"]/"metadata.json").read_text(encoding="utf-8"))
                raw = metadata["main_component_count"]
            joints, types = 0, "—"
            status = failure["stage"]+": "+failure["reason"]
            if failure.get("diagnostic_source_folder"):
                diagnostic = folder/failure["diagnostic_source_folder"]/"source_check.json"
                if diagnostic.exists():
                    row["source_geometry"] = json.loads(diagnostic.read_text(encoding="utf-8"))
                    info = row["source_geometry"]
                    status += f"; source_valid={info['source_valid']}, solids={info['solid_count']}"
            if failure.get("assembly",{}).get("status") == "technical_limit_reached":
                status += f"; technical_limit_reached, search_states={failure['assembly']['search_states']}"
        row.update(raw_parts=raw,joint_count=joints,result=status)
        table.append(f"| {row['model']} | {row['seed']} | {raw} | {joints} | {types} | {status} |")
    table.extend(["", "Selected joint coverage: "+str(summary.get("joint_coverage")),
                  "Missing types in the ten selected results: "+str(summary.get("missing_types")),
                  "", "All rejected source attempts and candidate designs remain in JSON reports."])
    save_json(output/"summary.json",summary)
    (output/"REPORT.md").write_text("\n".join(table)+"\n",encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--finalize-existing", action="store_true")
    args = parser.parse_args()
    if args.finalize_existing:
        finalize_existing(args.output)
        return
    args.output.mkdir(parents=True, exist_ok=False)
    seeds = (42, 17, 73, 101, 123, 202, 314, 515, 616, 717)
    rows = []
    for index, seed in enumerate(seeds):
        preferred = (JOINT_TYPES[index],) if index < 8 else (("bayonet","snap_fit","threaded")
                     if index == 8 else ("pinned","bolted","dovetail"))
        manifest = generate_auto_batch(args.output/f"model_{index+1:02d}", count=1, seed=seed,
            connection="all", max_attempts=1, geometry=AssemblySettings(path_steps=4),
            check_sequence=False, preferred_types=preferred)
        row = dict(model=index+1, seed=seed, preferred_types=preferred,
                   success=manifest["successful_count"] == 1, assemblies=manifest["assemblies"],
                   failures=manifest["failures"])
        rows.append(row)
        save_json(args.output/"summary.json", dict(models=rows, all_ten_completed=len(rows)==10))
    coverage = Counter()
    for row in rows:
        for assembly in row["assemblies"]: coverage.update(assembly["connection_types"])
    save_json(args.output/"summary.json",dict(models=rows,all_ten_completed=True,
        successful_count=sum(r["success"] for r in rows),joint_coverage=dict(coverage),
        missing_types=sorted(set(JOINT_TYPES)-set(coverage)),assembly_sequence_checked=False))


if __name__ == "__main__":
    main()
