"""Search a generated STEP dataset directly; export contact/fit assemblies."""

import argparse
from collections import Counter
from dataclasses import asdict
from datetime import datetime
from itertools import combinations, islice
import json
from pathlib import Path
import time

import cadquery as cq

from .connection_search import SearchSettings, describe_part, search_pair
from .geometry_analysis import load_part


def export_connection(a, moved_b, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    assembly = cq.Assembly(name=path.stem)
    assembly.add(a, name="part_a", color=cq.Color(0.2, 0.55, 0.9))
    assembly.add(moved_b, name="part_b", color=cq.Color(1.0, 0.6, 0.15))
    cq.exporters.export(assembly.toCompound(), str(path.with_suffix(".stl")),
                        tolerance=0.05, angularTolerance=0.1)
    assembly.save(str(path.with_suffix(".step")), exportType="STEP")


def run_search(folder, output, settings, max_pairs=None, max_exports=100):
    folder, output = Path(folder).resolve(), Path(output).resolve()
    if not folder.is_dir():
        raise ValueError(f"STEP folder does not exist: {folder}")
    # Results must not become inputs on the next invocation.
    files = sorted(p for p in folder.rglob("*")
                   if p.suffix.lower() in (".step", ".stp") and ".tmp." not in p.name
                   and not any(part.startswith("connections_") or part in ("assemblies", "connections")
                               for part in p.relative_to(folder).parts[:-1])
                   and (p != output and output not in p.parents))
    if not files:
        raise ValueError(f"No STEP files under {folder}")
    output.mkdir(parents=True, exist_ok=False)
    parts, load_errors = [], []
    for i, path in enumerate(files):
        print(f"Reading {i+1}/{len(files)}: {path.name}", flush=True)
        try:
            parts.append(describe_part(str(path), load_part(path), settings))
        except Exception as error:
            load_errors.append(dict(file=str(path), error=f"{type(error).__name__}: {error}"))
    total_pairs = len(parts)*(len(parts)-1)//2
    planned = total_pairs if max_pairs is None else min(total_pairs, max_pairs)
    report = dict(
        schema_version=2, input_folder=str(folder), settings=asdict(settings),
        note="Bounded geometric search. Two support directions, curved recess, or cylindrical "
             "insertion; no material overlap. Approach is sampled, not continuously proven. "
             "A not_found result is not a proof of impossibility. Units follow the imported STEP.",
        parts=[dict(id=i, file=p.name, warnings=p.warnings) for i, p in enumerate(parts)],
        load_errors=load_errors, pairs=[], summary={},
    )
    counts = Counter()
    exports = 0
    start = time.monotonic()

    def save():
        report["summary"] = dict(
            input_files=len(files), parts_analyzed=len(parts), load_errors=len(load_errors),
            total_possible_pairs=total_pairs, pairs_checked=len(report["pairs"]),
            pairs_skipped=total_pairs-len(report["pairs"]), status_counts=dict(counts),
            assemblies_exported=exports, elapsed_seconds=round(time.monotonic()-start, 2),
        )
        temporary = output / "report.tmp"
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(output / "report.json")

    save()
    try:
        for k, ((i, a), (j, b)) in enumerate(
                islice(combinations(enumerate(parts), 2), planned), 1):
            result, moved = search_pair(a, b, settings)
            result.update(part_a=a.name, part_b=b.name, part_a_id=i, part_b_id=j)
            if moved is not None and exports < max_exports:
                target = output / "assemblies" / f"pair_{i:03d}_{j:03d}"
                try:
                    export_connection(a.shape, moved, target)
                    result["assembly_stl"] = target.with_suffix(".stl").relative_to(output).as_posix()
                    result["assembly_step"] = target.with_suffix(".step").relative_to(output).as_posix()
                    exports += 1
                except Exception as error:
                    result["export_error"] = f"{type(error).__name__}: {error}"
            elif moved is not None:
                result["export_skipped"] = "max_exports"
            counts[result["status"]] += 1
            report["pairs"].append(result)
            save()
            print(f"Pair {k}/{planned}: {i} + {j}: {result['status']}; "
                  f"poses={result['tested_poses']}", flush=True)
    except KeyboardInterrupt:
        report["interrupted"] = True
        save()
        print("Interrupted. Completed pair results have been saved.", flush=True)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Report: {output / 'report.json'}")
    if len(parts) == 1:
        print("One part: no distinct pair to check. Generate at least two parts.")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", required=True, help="Dataset or train folder; STEP search is recursive")
    parser.add_argument("--output", help="New results directory; never overwrite an earlier run")
    parser.add_argument("--project-root", default=".", help="Base directory for relative paths")
    parser.add_argument("--max-poses", type=int, default=32, help="Maximum poses per pair")
    parser.add_argument("--max-pairs", type=int, help="Optional limit; default: all distinct pairs")
    parser.add_argument("--max-exports", type=int, default=100, help="Maximum exported assemblies")
    parser.add_argument("--contact-tolerance", type=float, default=0.1)
    parser.add_argument("--volume-tolerance", type=float, default=1e-5)
    parser.add_argument("--min-contact-area", type=float, default=0.1)
    parser.add_argument("--min-engagement", type=float, default=1.0)
    parser.add_argument("--path-steps", type=int, default=12)
    args = parser.parse_args()
    import math
    numbers = (args.contact_tolerance, args.volume_tolerance,
               args.min_contact_area, args.min_engagement)
    if any(not math.isfinite(x) or x <= 0 for x in numbers):
        parser.error("Geometric tolerances, contact area and engagement must be finite and positive")
    if (args.max_poses < 1 or args.path_steps < 2 or args.max_exports < 0
            or (args.max_pairs is not None and args.max_pairs < 0)):
        parser.error("max-poses >= 1, path-steps >= 2, max-pairs/max-exports >= 0")
    root = Path(args.project_root).resolve()
    folder = root / args.folder
    output = root / args.output if args.output else (
        folder / ("connections_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")))
    settings = SearchSettings(contact_tolerance=args.contact_tolerance,
                              volume_tolerance=args.volume_tolerance,
                              min_contact_area=args.min_contact_area,
                              min_engagement=args.min_engagement,
                              max_poses=args.max_poses, path_steps=args.path_steps)
    try:
        run_search(folder, output, settings, args.max_pairs, args.max_exports)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
