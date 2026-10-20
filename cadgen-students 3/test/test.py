"""Generate rings, bars and verified insertion examples (dimensions in mm).

Run from the project folder:
    .\.venv-win\Scripts\python.exe test/test.py
    .\.venv-win\Scripts\python.exe test/test.py --seed 42 --count 10
    .\.venv-win\Scripts\python.exe test/test.py --self-test

Every run creates its own output folder next to this script. Open its STL files
in a mesh viewer. STEP assemblies preserve the two separate components.
"""

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime
import json
import math
from pathlib import Path
import random

import cadquery as cq


VOLUME_TOLERANCE = 1e-6  # mm^3: numerical tolerance, not a manufacturing tolerance


@dataclass(frozen=True)
class Ring:
    hole: float
    radius: float
    height: float


@dataclass(frozen=True)
class Bar:
    width: float
    depth: float
    length: float


def make_ring(spec):
    outer = cq.Workplane("XY").circle(spec.radius).extrude(spec.height)
    cutter = cq.Workplane("XY").rect(spec.hole, spec.hole).extrude(spec.height)
    return outer.cut(cutter).val()


def make_bar(spec):
    return cq.Workplane("XY").rect(spec.width, spec.depth).extrude(spec.length).val()


def fit_pair(ring, bar, ring_shape, bar_shape, min_gap):
    """Check a centered straight insertion through the whole square hole.

    For a rectangle in a square, the smallest square envelope is attained at
    either 0 or 45 degrees. Both orientations are tried. Tilting is not used.
    min_gap is the minimum distance to each of the four hole walls.
    """
    if bar.length < ring.height:
        return {"fits": False, "reason": "too_short_for_through_insertion"}, None

    orientations = []
    for angle in (0, 45):
        radians = math.radians(angle)
        envelope_x = bar.width * math.cos(radians) + bar.depth * math.sin(radians)
        envelope_y = bar.width * math.sin(radians) + bar.depth * math.cos(radians)
        gap = (ring.hole - max(envelope_x, envelope_y)) / 2
        orientations.append((gap, angle))
    gap, angle = max(orientations)
    if gap < min_gap - 1e-9:
        return {"fits": False, "reason": "cross_section_too_large",
                "best_wall_gap_mm": gap}, None

    final_z = (ring.height - bar.length) / 2
    moved = bar_shape.rotate((0, 0, 0), (0, 0, 1), angle).translate((0, 0, final_z))
    overlap = ring_shape.intersect(moved).Volume()

    # Exact swept solid for translation of this constant rectangular prism.
    # It covers EVERY intermediate position, not only a set of sampled frames.
    start_z = -bar.length - 5.0
    swept_height = final_z + bar.length - start_z
    swept = (
        cq.Workplane("XY").rect(bar.width, bar.depth).extrude(swept_height)
        .val().rotate((0, 0, 0), (0, 0, 1), angle).translate((0, 0, start_z))
    )
    swept_overlap = ring_shape.intersect(swept).Volume()
    fits = overlap <= VOLUME_TOLERANCE and swept_overlap <= VOLUME_TOLERANCE
    return {
        "fits": fits,
        "reason": "straight_insertion_clear" if fits else "collision",
        "rotation_z_deg": angle,
        "translation_mm": [0, 0, final_z],
        "minimum_wall_gap_mm": gap,
        "engagement_mm": ring.height,
        "intersection_volume_mm3": overlap,
        "swept_intersection_volume_mm3": swept_overlap,
        "insertion_start_z_mm": start_z,
        "continuous_straight_path_checked": True,
    }, moved if fits else None


def export_shape(shape, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(shape, str(target.with_suffix(".stl")), tolerance=0.05,
                        angularTolerance=0.1)
    cq.exporters.export(shape, str(target.with_suffix(".step")))


def export_assembly(first, second, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    assembly = cq.Assembly(name=target.name)
    assembly.add(first, name="ring", color=cq.Color(0.2, 0.55, 0.9))
    assembly.add(second, name="insert", color=cq.Color(1.0, 0.6, 0.15))
    assembly.save(str(target.with_suffix(".step")), exportType="STEP")
    # Keep the two solids separate. STL does not preserve component colors.
    compound = cq.Compound.makeCompound([first, second])
    cq.exporters.export(compound, str(target.with_suffix(".stl")), tolerance=0.05,
                        angularTolerance=0.1)


def create_round_demo(folder):
    ring = cq.Workplane("XY").circle(20).circle(10).extrude(10).val()
    pin = cq.Workplane("XY").circle(9.9).extrude(30).val()
    export_shape(ring, folder / "ring")
    export_shape(pin, folder / "cylinder")
    export_assembly(ring, pin.translate((0, 0, -10)), folder / "assembly")


def self_test():
    ring = Ring(hole=20, radius=22, height=10)
    shape = make_ring(ring)
    cases = [
        ("clearance", Bar(19, 18, 30), 0.1, True),
        ("oversized", Bar(25, 25, 30), 0.1, False),
        ("too_short", Bar(10, 10, 5), 0.1, False),
        ("diagonal_fit", Bar(23, 3, 30), 0.1, True),
        ("zero_clearance", Bar(20, 20, 30), 0.0, True),
        ("required_gap", Bar(20, 20, 30), 0.1, False),
    ]
    for name, bar, gap, expected in cases:
        result, moved = fit_pair(ring, bar, shape, make_bar(bar), gap)
        assert result["fits"] == expected, (name, result)
        if expected:
            assert moved.isValid(), name
            assert result["continuous_straight_path_checked"], name
        if name == "diagonal_fit":
            assert result["rotation_z_deg"] == 45, result
        print(f"PASS: {name}")
    # A shifted bar overlaps the wall even though its dimensions fit.
    displaced = make_bar(Bar(19, 18, 30)).translate((3, 0, -10))
    assert shape.intersect(displaced).Volume() > VOLUME_TOLERANCE
    print("PASS: displaced_collision")


def generate(count, seed, min_gap):
    rng = random.Random(seed)
    output = Path(__file__).resolve().parent / (
        "output_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    )
    output.mkdir(parents=True)
    create_round_demo(output / "round_demo")
    rings, bars = [], []
    gallery = []
    columns = math.ceil(math.sqrt(count))
    spacing = 90
    for i in range(count):
        hole = round(rng.uniform(12, 26), 2)
        ring = Ring(hole, round(hole / math.sqrt(2) + rng.uniform(6, 12), 2),
                    round(rng.uniform(6, 12), 2))
        bar = Bar(round(rng.uniform(8, 30), 2), round(rng.uniform(8, 30), 2),
                  round(rng.uniform(18, 36), 2))
        ring_shape, bar_shape = make_ring(ring), make_bar(bar)
        for name, shape in (("ring", ring_shape), ("bar", bar_shape)):
            if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0:
                raise RuntimeError(f"Invalid generated {name} {i}")
            export_shape(shape, output / "parts" / f"{name}_{i:03d}")
        rings.append((ring, ring_shape))
        bars.append((bar, bar_shape))
        position = ((i % columns) * spacing, (i // columns) * spacing, 0)
        gallery.append(ring_shape.translate(position))
        gallery.append(bar_shape.translate((position[0] + 45, position[1], 0)))
    export_shape(cq.Compound.makeCompound(gallery), output / "all_parts")

    pairs, accepted = [], 0
    for i, (ring, ring_shape) in enumerate(rings):
        for j, (bar, bar_shape) in enumerate(bars):
            result, moved = fit_pair(ring, bar, ring_shape, bar_shape, min_gap)
            result.update(ring_id=i, bar_id=j)
            if result["fits"]:
                name = f"ring_{i:03d}__bar_{j:03d}"
                export_assembly(ring_shape, moved, output / "assemblies" / name)
                result["assembly_stl"] = f"assemblies/{name}.stl"
                accepted += 1
                print(f"FIT ring {i} + bar {j}: gap={result['minimum_wall_gap_mm']:.3f} mm")
            pairs.append(result)
    report = {
        "units": "mm", "seed": seed, "minimum_wall_gap_mm": min_gap,
        "scope": "Centered square through-hole and rectangular prism; straight axial insertion. "
                 "Geometric fit only; no friction, retention or manufacturing tolerances.",
        "rings": [dict(id=i, **asdict(item[0])) for i, item in enumerate(rings)],
        "bars": [dict(id=i, **asdict(item[0])) for i, item in enumerate(bars)],
        "pairs_checked": len(pairs), "assemblies_created": accepted, "pairs": pairs,
    }
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nChecked {len(pairs)} pairs; created {accepted} assemblies.")
    print(f"Output: {output}")
    print("Open all_parts.stl, round_demo/assembly.stl or assemblies/*.stl in your viewer.")
    if not accepted:
        print("No random pairs fit. Try another --seed or a larger --count.")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--count", type=int, default=8, help="Number of rings AND bars (default: 8)")
    parser.add_argument("--seed", type=int, default=None, help="Optional reproducible random seed")
    parser.add_argument("--min-gap", type=float, default=0.1, help="Minimum gap to each wall, mm")
    parser.add_argument("--self-test", action="store_true", help="Run checks without exporting files")
    args = parser.parse_args()
    if args.count < 1 or not math.isfinite(args.min_gap) or args.min_gap < 0:
        parser.error("--count must be positive; --min-gap must be finite and nonnegative")
    if args.self_test:
        self_test()
    else:
        seed = args.seed if args.seed is not None else random.SystemRandom().randrange(2**32)
        print(f"Seed: {seed}")
        generate(args.count, seed, args.min_gap)


if __name__ == "__main__":
    main()
