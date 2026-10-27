r"""Случайные детали со сквозными круглыми отверстиями под болты из Bolty.py.

Запуск из папки cadgen-students 3:
    .\.venv-win\Scripts\python.exe Otverstiya.py --count 24
    .\.venv-win\Scripts\python.exe Otverstiya.py --count 24 --shape rectangular
    .\.venv-win\Scripts\python.exe Otverstiya.py --self-test

Отверстие случайное, 4–10 мм с шагом 0.5 мм, независимо от конкретных болтов.
Общий диапазон импортируется из Bolty.py. Для сравнения будут как подходящие,
так и неподходящие пары. Толщина 3–10 мм. Зазор можно вычислить только после
выбора конкретного болта: диаметр отверстия минус диаметр его стержня.

Формы корпуса: прямоугольная пластина, круглая пластина, шестигранная пластина.
Отверстие одно, по центру, вдоль Z; обе стороны открыты. Корпус занимает
z=0..thickness. Ни резьбы, ни углубления под головку нет.

Новый запуск создаёт generirovanie_otverstiy/batch_... со STEP/STL/JSON,
manifest.json и общей STL-раскладкой all_parts.stl. Существующие папки
не перезаписываются. Импорт ничего не генерирует.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime
import json
import math
from pathlib import Path
import random

from Bolty import (DIAMETER_MIN_MM, DIAMETER_MAX_MM, DIMENSION_STEP_MM,
                   sample_diameter, save_manifest_json)


SHAPES = ("rectangular", "round", "hexagonal")


@dataclass(frozen=True)
class PlateSpec:
    shape: str
    width: float  # rectangle width, disk diameter, or hexagon across flats
    length: float  # used for rectangular plates only; otherwise equal to width
    thickness: float
    hole_diameter: float


def sample_spec(rng: random.Random, shape: str = "random") -> PlateSpec:
    shape = rng.choice(SHAPES) if shape == "random" else shape
    if shape not in SHAPES:
        raise ValueError(f"Unknown body shape: {shape}")
    # Keep enough material for the largest hole in the common diameter range.
    width = round(rng.uniform(max(24.0, DIAMETER_MAX_MM+14.0),
                              max(52.0, DIAMETER_MAX_MM+35.0)), 2)
    length = (round(rng.uniform(max(24.0, DIAMETER_MAX_MM+14.0),
                                max(65.0, DIAMETER_MAX_MM+40.0)), 2)
              if shape == "rectangular" else width)
    thickness = round(rng.uniform(3.0, 10.0), 2)
    hole = sample_diameter(rng)
    return PlateSpec(shape, width, length, thickness, hole)


def through_hole_cutter(diameter: float, z_min: float, z_max: float,
                        center: tuple[float, float] = (0.0, 0.0)):
    """Shared axial tool for plates and two halves of one assembly (millimeters)."""
    import cadquery as cq

    if (not all(math.isfinite(x) for x in (diameter, z_min, z_max, *center))
            or diameter <= 0 or z_max <= z_min):
        raise ValueError("Invalid through-hole dimensions")
    return (cq.Workplane("XY", origin=(*center, z_min)).circle(diameter/2)
            .extrude(z_max-z_min).val())


def build_plate(spec: PlateSpec):
    import cadquery as cq

    if spec.shape not in SHAPES:
        raise ValueError(f"Unknown shape: {spec.shape}")
    for name, value in asdict(spec).items():
        if name != "shape" and (not math.isfinite(value) or value <= 0):
            raise ValueError(f"Invalid dimension: {name}")
    if spec.hole_diameter >= min(spec.width, spec.length):
        raise ValueError("Hole must leave material around its entire perimeter")
    plane = cq.Workplane("XY")
    if spec.shape == "rectangular":
        body = plane.rect(spec.width, spec.length).extrude(spec.thickness).val()
    elif spec.shape == "round":
        body = plane.circle(spec.width/2).extrude(spec.thickness).val()
    else:
        body = plane.polygon(6, spec.width, circumscribed=True).extrude(spec.thickness).val()
    cutter = through_hole_cutter(spec.hole_diameter, -1, spec.thickness+1)
    result = body.cut(cutter).clean()
    if not result.isValid() or len(result.Solids()) != 1 or result.Volume() <= 0:
        raise RuntimeError(f"Invalid plate: {spec}")
    # Verify that the full through-cylinder, rather than a blind pocket, was removed.
    removed = body.Volume()-result.Volume()
    expected = math.pi*(spec.hole_diameter/2)**2*spec.thickness
    if not math.isclose(removed, expected, rel_tol=1e-6, abs_tol=1e-6):
        raise RuntimeError("Through-hole volume check failed")
    return result


def metadata(spec: PlateSpec) -> dict:
    return {
        "units": "mm", "role": "through_hole_part", "parameters": asdict(spec),
        "hole": {"type": "cylindrical_through", "diameter": spec.hole_diameter,
                 "depth": spec.thickness, "axis_direction": [0, 0, 1],
                 "entry_center": [0, 0, 0], "exit_center": [0, 0, spec.thickness],
                 "open_ends": "both", "threaded": False},
        "hole_diameter_range_mm": [DIAMETER_MIN_MM, DIAMETER_MAX_MM],
        "hole_diameter_step_mm": DIMENSION_STEP_MM,
        "compatibility_checked": False,
    }


def generate(count=24, shape="random", seed=None, output=None):
    import cadquery as cq

    if count < 1:
        raise ValueError("Count must be positive")
    seed = seed if seed is not None else random.SystemRandom().randrange(2**63)
    rng = random.Random(f"plates:{seed}")
    output = Path(output) if output else (Path(__file__).resolve().parent /
        "generirovanie_otverstiy" / ("batch_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f")))
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    manifest = {"schema_version": 3, "units": "mm", "seed": seed,
                "hole_diameter_step_mm": DIMENSION_STEP_MM,
                "requested_count": count, "requested_shape": shape,
                "hole_diameter_range_mm": [DIAMETER_MIN_MM, DIAMETER_MAX_MM], "models": []}

    def save_manifest():
        save_manifest_json(output / "manifest.json", manifest)

    save_manifest()
    gallery = []
    columns = math.ceil(math.sqrt(count))
    # Spacing accommodates the full circumscribed hexagon diameter and rectangles.
    spacing = max(85.0, 2*(DIAMETER_MAX_MM+40))
    for index in range(count):
        spec = sample_spec(rng, shape)
        model = build_plate(spec)
        name = f"part_{index:04d}_{spec.shape}"
        folder = output / "parts" / name
        folder.mkdir(parents=True)
        cq.exporters.export(model, str(folder / f"{name}.step"))
        cq.exporters.export(model, str(folder / f"{name}.stl"), tolerance=0.03, angularTolerance=0.1)
        details = metadata(spec)
        details.update(seed=seed, index=index)
        (folder / f"{name}.json").write_text(json.dumps(details, ensure_ascii=False, indent=2), encoding="utf-8")
        relative = folder.relative_to(output).as_posix()
        manifest["models"].append({"name": name, "shape": spec.shape,
                                   "step": f"{relative}/{name}.step", "stl": f"{relative}/{name}.stl",
                                   "parameters": f"{relative}/{name}.json"})
        save_manifest()
        gallery.append(model.translate(((index % columns)*spacing, (index // columns)*spacing, 0)))
        print(f"[{index+1}/{count}] {name}: hole {spec.hole_diameter:.2f} mm", flush=True)
    cq.exporters.export(cq.Compound.makeCompound(gallery), str(output / "all_parts.stl"),
                        tolerance=0.03, angularTolerance=0.1)
    print(f"Output: {output}\nSeed: {seed}")
    return output


def self_test():
    """Check through-holes and all six bolt heads in memory, without exports."""
    import cadquery as cq
    from Bolty import TYPES, build_bolt, sample_spec as sample_bolt

    rng = random.Random(42)
    for kind in SHAPES:
        for _ in range(2):
            spec = sample_spec(rng, kind)
            plate = build_plate(spec)
            assert DIAMETER_MIN_MM <= spec.hole_diameter <= DIAMETER_MAX_MM
            probe = (cq.Workplane("XY", origin=(0, 0, -1)).circle((spec.hole_diameter-0.1)/2)
                     .extrude(spec.thickness+2).val())
            assert plate.intersect(probe).Volume() < 1e-6
            for z in (0.001, spec.thickness/2, spec.thickness-0.001):
                assert not plate.isInside(cq.Vector(0, 0, z), 1e-7)
            for bolt_type in TYPES:
                bolt_spec = sample_bolt(rng, bolt_type)
                bolt = build_bolt(bolt_spec).translate((0, 0, spec.thickness))
                assert bolt_spec.shaft_length > spec.thickness
                overlap = plate.intersect(bolt).Volume()
                if bolt_spec.shaft_diameter <= spec.hole_diameter:
                    assert overlap < 1e-5, bolt_type
                else:
                    assert overlap > 1e-5, bolt_type
        print(f"PASS: {kind}, through-hole and independent bolt diameters")
    print("Checks passed; no test models exported.")


def main():
    parser = argparse.ArgumentParser(description="Random plates with circular through-holes for Bolty.py")
    parser.add_argument("--count", type=int, default=24)
    parser.add_argument("--shape", choices=("random", *SHAPES), default="random")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", type=Path, help="New output directory")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be at least 1")
    if args.self_test:
        self_test()
        return
    try:
        generate(args.count, args.shape, args.seed, args.output)
    except FileExistsError:
        parser.error("Output directory already exists; choose a new --output.")


if __name__ == "__main__":
    main()
