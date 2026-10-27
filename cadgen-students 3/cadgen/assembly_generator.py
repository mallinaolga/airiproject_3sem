"""Generate a single CADGen solid, split it, and export verified assemblies.

python -m cadgen.assembly_generator --count 10 --connection random --seed 42
Units are mm. Straight insertion paths are sampled, never continuously proven.
"""

import argparse
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
import json
import random
import time

import cadquery as cq
import numpy as np
from OCP.gp import gp_Trsf

from generirovanie_pazov.generate_grooves import PROFILE_TYPES

from .assembly_geometry import (
    AssemblySettings, Connection, GeometryRejected, Split, build_bolted, build_groove,
    candidate_planes, require_solid, split_model, validate_connection,
)
from .assembly_source import generate_source
from .assembly_validation import transform_part


class GenerationFailed(GeometryRejected):
    def __init__(self, message, rejections):
        super().__init__(message)
        self.rejections = rejections


@dataclass
class GeneratedAssembly:
    original: cq.Shape
    split: Split
    connection: Connection
    checks: dict
    seed: int
    source_parameters: dict = field(default_factory=dict)
    source_program: str | None = None
    rejections: list = field(default_factory=list)
    request: dict = field(default_factory=dict)


def create_from_model(original, seed, connection="groove", profile="rectangular", settings=None):
    """Try bounded cuts/features on ONE supplied source, never independent pairs."""
    settings = settings or AssemblySettings()
    settings.validate()
    if connection not in ("groove", "bolted", "random") or profile not in (*PROFILE_TYPES, "random"):
        raise ValueError("Unknown connection or profile")
    original = require_solid(original, "original")
    rng = random.Random(f"assembly:{seed}")
    selected = rng.choice(("groove", "bolted")) if connection == "random" else connection
    rejections = []
    for index, (origin, normal) in enumerate(candidate_planes(original, rng, settings, selected)):
        stage = "split"
        try:
            split = split_model(original, origin, normal, settings)
            stage = "connection"
            result = (build_groove(split, rng, settings, profile) if selected == "groove"
                      else build_bolted(split, rng, settings))
            stage = "validation"
            checks = validate_connection(split, result, settings)
            return GeneratedAssembly(original, split, result, checks, seed,
                                     source_parameters=dict(generator="provided_solid", volume=original.Volume()),
                                     rejections=rejections,
                                     request=dict(connection=connection, profile=profile, source="provided"))
        except Exception as error:
            # OCC can raise several exception classes for bad booleans. They
            # remain recorded failures; no failed candidate becomes successful.
            rejections.append(dict(plane_attempt=index+1, stage=stage,
                                   origin=origin.tolist(), normal=normal.tolist(),
                                   error_type=type(error).__name__, reason=str(error)))
    raise GenerationFailed(f"No validated {selected} assembly within {settings.plane_attempts} cuts", rejections)


def generate_one(seed, connection="groove", profile="rectangular", source="cadgen", config=None, settings=None):
    original, parameters, program = generate_source(seed, source, config)
    result = create_from_model(original, seed, connection, profile, settings)
    result.source_parameters = parameters
    result.source_program = program
    result.request.update(source=source, cad_config=str(config) if config else None)
    return result


def json_default(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"Unsupported JSON value: {type(value).__name__}")


def save_json(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=json_default,
                                    allow_nan=False), encoding="utf-8")
    temporary.replace(path)


def location(rotation, translation):
    transform = gp_Trsf()
    transform.SetValues(*(float(v) for row, shift in zip(rotation, translation) for v in (*row, shift)))
    return cq.Location(transform)


def export_result(result, target, settings):
    """Export local component files + explicit rigid placements in the assembly."""
    target = Path(target)
    target.mkdir(parents=True, exist_ok=False)
    metadata = dict(schema_version=1, status="exporting", success=False, units="mm", seed=result.seed,
                    source=result.source_parameters, request=result.request, settings=asdict(settings),
                    split=result.split.metadata(), connection=result.connection.parameters,
                    checks=result.checks, rejected_candidates=result.rejections, components=[],
                    note="Finite path samples do not prove continuous clearance. "
                         "No thread, friction, load capacity or mechanical retention is modeled.")
    save_json(target/"metadata.json", metadata)
    try:
        cq.exporters.export(result.original, str(target/"original.step"))
        cq.exporters.export(result.original, str(target/"original.stl"), tolerance=0.05, angularTolerance=0.1)
        if result.source_program:
            (target/"original.py").write_text(result.source_program, encoding="utf-8")
        assembled = cq.Assembly(name=target.name)
        exploded = cq.Assembly(name=target.name+"_exploded")
        distance = result.original.BoundingBox().DiagonalLength*1.2
        colors = [(0.2, 0.55, 0.9), (1.0, 0.6, 0.15), (0.55, 0.58, 0.6), (0.7, 0.72, 0.75)]
        for index, (name, shape) in enumerate(result.connection.components):
            center = np.array(shape.Center().toTuple())
            local = shape.translate(tuple(-center))
            rotation = result.split.rotation
            translation = rotation@center + result.split.origin
            # Exploded positions are display placements; only the assembly
            # sequence recorded in checks.paths was collision sampled.
            axis = np.array([0., 1., 0.]) if result.connection.parameters.get("insertion") == "longitudinal_slide" else np.array([0., 0., 1.])
            offset = axis*distance*((1, -1, 3, -3)[index])
            exploded_translation = translation + rotation@offset
            cq.exporters.export(local, str(target/f"{name}.step"))
            cq.exporters.export(local, str(target/f"{name}.stl"), tolerance=0.05, angularTolerance=0.1)
            color = cq.Color(*colors[index])
            assembled.add(local, name=name, loc=location(rotation, translation), color=color)
            exploded.add(local, name=name, loc=location(rotation, exploded_translation), color=color)
            metadata["components"].append(dict(
                name=name, step=f"{name}.step", stl=f"{name}.stl",
                provenance=("split_original_with_joint_modifications" if name.startswith("part_")
                            else "Bolty.build_bolt" if name.startswith("bolt_") else "Gaiki.build_nut"),
                coordinates="component local; apply placement to reconstruct assembly",
                rotation_matrix=rotation.tolist(), translation=translation.tolist(),
                exploded_rotation_matrix=rotation.tolist(), exploded_translation=exploded_translation.tolist(),
                volume=local.Volume()))
        assembled.save(str(target/"assembly.step"), exportType="STEP")
        cq.exporters.export(assembled.toCompound(), str(target/"assembly.stl"),
                            tolerance=0.05, angularTolerance=0.1)
        exploded.save(str(target/"exploded.step"), exportType="STEP")
        cq.exporters.export(exploded.toCompound(), str(target/"exploded.stl"),
                            tolerance=0.05, angularTolerance=0.1)
        # Test the actual STEP that will be delivered, not just the in-memory
        # shapes. The assembly must retain every separate component.
        solids = cq.importers.importStep(str(target/"assembly.step")).solids().vals()
        expected = sorted(s.Volume() for _, s in result.connection.components)
        actual = sorted(s.Volume() for s in solids)
        if (len(solids) != len(expected) or not all(s.isValid() for s in solids)
                or not np.allclose(expected, actual, rtol=1e-8, atol=settings.volume_tolerance)):
            raise GeometryRejected("STEP roundtrip lost or changed assembly components")
        # Locations, including rotations, must agree with the verified geometry.
        expected_world = cq.Compound.makeCompound([result.split.world(s) for _, s in result.connection.components])
        actual_world = cq.Compound.makeCompound(solids)
        if (abs(expected_world.intersect(actual_world).Volume()-sum(expected)) > settings.volume_tolerance):
            raise GeometryRejected("STEP placements differ from the validated assembly")
        metadata["checks"]["step_roundtrip_separate_solids"] = len(solids)
        metadata["checks"]["step_placements_verified"] = True
        metadata.update(status="success", success=True)
        save_json(target/"metadata.json", metadata)
        return metadata
    except Exception as error:
        metadata.update(status="export_failed", success=False, export_error=f"{type(error).__name__}: {error}")
        save_json(target/"metadata.json", metadata)
        raise


def generate_batch(output, count=1, connection="random", seed=None, profile="rectangular",
                   source="cadgen", config=None, max_attempts=8, settings=None):
    settings = settings or AssemblySettings()
    settings.validate()
    if count < 1 or max_attempts < 1:
        raise ValueError("count and max_attempts must be positive")
    if connection not in ("random", "groove", "bolted") or profile not in ("random", *PROFILE_TYPES):
        raise ValueError("Unknown connection or profile")
    if source not in ("box", "cadgen") or (config and source != "cadgen"):
        raise ValueError("A CAD config requires source=cadgen")
    seed = random.SystemRandom().randrange(2**63) if seed is None else seed
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    manifest = dict(schema_version=1, seed=seed, requested_count=count, successful_count=0,
                    connection=connection, profile=profile, source=source, config=str(config) if config else None,
                    settings=asdict(settings), max_attempts_per_assembly=max_attempts,
                    assemblies=[], failures=[], status="running")
    save_json(output/"manifest.json", manifest)
    start = time.monotonic()
    # Each requested assembly owns its seed stream; a failed slot does not
    # change the seeds of subsequent requested assemblies.
    for slot in range(count):
        stream = random.Random(f"batch:{seed}:{slot}")
        for attempt in range(max_attempts):
            item_seed = seed if slot == 0 and attempt == 0 else stream.randrange(2**63)
            target = None
            try:
                result = generate_one(item_seed, connection, profile, source, config, settings)
                target = output/f"assembly_{len(manifest['assemblies'])+1:04d}_attempt_{attempt+1:02d}_slot_{slot+1:04d}"
                metadata = export_result(result, target, settings)
                manifest["assemblies"].append(dict(folder=target.name, seed=item_seed,
                    connection=metadata["connection"]["type"], profile=metadata["connection"].get("profile"),
                    requested_slot=slot+1, attempt=attempt+1))
                manifest["successful_count"] = len(manifest["assemblies"])
                print(f"[{manifest['successful_count']}/{count}] {target.name}: {metadata['connection']['type']}", flush=True)
                save_json(output/"manifest.json", manifest)
                break
            except Exception as error:
                failure = dict(requested_slot=slot+1, attempt=attempt+1, seed=item_seed,
                               error_type=type(error).__name__, reason=str(error),
                               rejected_candidates=getattr(error, "rejections", []))
                if target is not None:
                    failure["partial_output"] = target.name
                manifest["failures"].append(failure)
                save_json(output/"manifest.json", manifest)
                print(f"Slot {slot+1}, attempt {attempt+1} rejected: {type(error).__name__}: {error}", flush=True)
        else:
            print(f"Slot {slot+1}: exhausted {max_attempts} attempts", flush=True)
    manifest.update(status="complete" if manifest["successful_count"] == count else "incomplete",
                    elapsed_seconds=round(time.monotonic()-start, 3),
                    failure_counts=dict(Counter(f["error_type"] for f in manifest["failures"])))
    save_json(output/"manifest.json", manifest)
    print(f"Successful assemblies: {manifest['successful_count']}/{count}; seed={seed}; output={output}")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=1, help="Requested SUCCESSFUL assemblies")
    parser.add_argument("--decomposition", choices=("two", "auto"), default="two")
    parser.add_argument("--connection", choices=("groove", "bolted", "random", "auto", "combined"))
    parser.add_argument("--profile", choices=("random", "auto", *PROFILE_TYPES))
    parser.add_argument("--source", choices=("cadgen", "box"), default="cadgen")
    parser.add_argument("--cad-config", type=Path, help="Optional existing Python config exposing cad_factory")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", type=Path, help="New directory; existing results are never overwritten")
    parser.add_argument("--max-attempts", type=int, default=8, help="Source attempts per requested assembly")
    parser.add_argument("--plane-attempts", type=int, default=9)
    parser.add_argument("--feature-attempts", type=int, default=8)
    parser.add_argument("--clearance", type=float, default=0.2, help="Normal groove / radial hole clearance, 0 <= c < 1 mm")
    parser.add_argument("--min-wall", type=float, default=2.0)
    parser.add_argument("--volume-tolerance", type=float, default=1e-5)
    parser.add_argument("--path-steps", type=int, default=16)
    parser.add_argument("--min-component-size", type=float, default=6.0)
    parser.add_argument("--min-component-volume", type=float, default=300.0)
    parser.add_argument("--min-split-score", type=float, default=0.8)
    parser.add_argument("--min-simplicity-gain", type=float, default=0.08)
    parser.add_argument("--neck-weight", type=float, default=2.0)
    parser.add_argument("--transition-weight", type=float, default=2.0)
    parser.add_argument("--simplicity-weight", type=float, default=3.0)
    parser.add_argument("--imbalance-weight", type=float, default=0.35)
    parser.add_argument("--max-cut-candidates", type=int, default=160)
    parser.add_argument("--max-recursion-depth", type=int, default=12)
    parser.add_argument("--cad-operation-budget", type=int, default=5000)
    parser.add_argument("--max-connection-trials", type=int, default=12)
    parser.add_argument("--max-sequence-states", type=int, default=256)
    parser.add_argument("--examples", type=Path, help="Auto mode: curate at most ten actual results in a NEW directory")
    args = parser.parse_args()
    settings = AssemblySettings(clearance=args.clearance, min_wall=args.min_wall,
                                volume_tolerance=args.volume_tolerance, plane_attempts=args.plane_attempts,
                                feature_attempts=args.feature_attempts, path_steps=args.path_steps)
    try:
        settings.validate()
        args.connection=args.connection or ("auto" if args.decomposition=="auto" else "random")
        args.profile=args.profile or ("auto" if args.decomposition=="auto" else "rectangular")
        if args.count < 1 or args.max_attempts < 1:
            raise ValueError("count and max-attempts must be positive")
        if args.cad_config and (not args.cad_config.is_file() or args.source != "cadgen"):
            raise ValueError("cad-config must be an existing file and requires source=cadgen")
        output = args.output or Path("generations/assemblies")/(
            "run_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        if args.decomposition=="auto":
            from .auto_assembly import generate_auto_batch
            from .decomposition import DecompositionSettings
            automatic=DecompositionSettings(
                min_component_size=args.min_component_size,min_component_volume=args.min_component_volume,
                min_score=args.min_split_score,min_simplicity_gain=args.min_simplicity_gain,
                neck_weight=args.neck_weight,transition_weight=args.transition_weight,
                simplicity_weight=args.simplicity_weight,imbalance_weight=args.imbalance_weight,
                max_candidates=args.max_cut_candidates,max_depth=args.max_recursion_depth,
                max_operations=args.cad_operation_budget,max_connection_trials=args.max_connection_trials,
                max_sequence_states=args.max_sequence_states)
            manifest=generate_auto_batch(output,args.count,args.connection,args.seed,args.profile,
                args.source,args.cad_config,args.max_attempts,settings,automatic,args.examples)
        else:
            if args.examples or args.connection in ("auto","combined") or args.profile=="auto":
                raise ValueError("auto/combined profiles and examples require --decomposition auto")
            manifest = generate_batch(output, args.count, args.connection, args.seed, args.profile,
                                      args.source, args.cad_config, args.max_attempts, settings)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
    return 0 if manifest["successful_count"] == args.count else 1


if __name__ == "__main__":
    raise SystemExit(main())
