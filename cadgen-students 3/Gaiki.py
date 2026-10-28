r"""Шестигранные гайки без резьбы под гладкие стержни из Bolty.py.

Запуск из папки cadgen-students 3:
    .\.venv-win\Scripts\python.exe Gaiki.py --count 100

Случайные размер под ключ, высота и наружная фаска. Сквозное отверстие
независимо выбирается в диапазоне 4–10 мм, общем со стержнями болтов.
Линейные размеры кратны 0.5 мм; наружная фаска составляет 0.5 мм.
Не каждая гайка подходит к каждому болту. Модели без резьбы:
резьбовое крепление не моделируется.
Новый запуск сохраняет STEP/STL/JSON и all_nuts.stl в отдельную папку
generirovanie_gaek/batch_... . Импорт ничего не генерирует.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import json
import math
from pathlib import Path
import random

from Bolty import (DIAMETER_MIN_MM, DIAMETER_MAX_MM, DIMENSION_STEP_MM,
                   sample_diameter, sample_dimension, save_manifest_json)


@dataclass(frozen=True)
class NutSpec:
    hole_diameter: float
    across_flats: float
    height: float
    chamfer: float = 0.5


def build_nut(spec: NutSpec, *, adaptive=False):
    """Build explicitly dimensioned compatible hardware; no thread is modeled."""
    import cadquery as cq

    hole, across_flats, height, chamfer = (spec.hole_diameter, spec.across_flats,
                                          spec.height, spec.chamfer)
    if (not all(math.isfinite(x) and x > 0 for x in (hole, across_flats, height))
            or not math.isfinite(chamfer) or chamfer < 0
            or across_flats <= hole or 2*chamfer >= min(height, across_flats-hole)):
        raise ValueError("Invalid nut dimensions or insufficient wall for chamfer")
    body = (cq.Workplane("XY").polygon(6, across_flats, circumscribed=True)
            .extrude(height))
    if chamfer:
        body = body.faces(">Z or <Z").edges().chamfer(chamfer)
    body = body.val()
    cutter = (cq.Workplane("XY", origin=(0, 0, -1)).circle(hole/2)
              .extrude(height+2).val())
    nut = body.cut(cutter).clean()
    if not nut.isValid() or len(nut.Solids()) != 1 or nut.Volume() <= 0:
        raise RuntimeError("Invalid nut solid")
    removed = body.Volume()-nut.Volume()
    if not math.isclose(removed, math.pi*(hole/2)**2*height, rel_tol=1e-6):
        raise RuntimeError("Hole is not fully through the nut")
    shaft = (cq.Workplane("XY", origin=(0, 0, -1)).circle((hole*.9 if adaptive else hole-0.1)/2)
             .extrude(height+2).val())
    if nut.intersect(shaft).Volume() > 1e-6:
        raise RuntimeError("Through-hole probe intersects the nut")
    return nut


def make_nut(rng: random.Random):
    hole = sample_diameter(rng)
    across_flats = sample_dimension(rng, hole+3.0, hole+8.0)
    height = sample_dimension(rng, 3.0, 8.0)
    chamfer = sample_dimension(rng, 0.25, min(0.65, height*0.2, (across_flats-hole)*0.2))
    nut = build_nut(NutSpec(hole, across_flats, height, chamfer))
    details = {
        "units": "mm", "role": "nut", "outer_shape": "hexagonal",
        "dimension_step_mm": DIMENSION_STEP_MM,
        "across_flats": across_flats, "height": height, "outer_chamfer": chamfer,
        "hole": {"type": "cylindrical_through", "diameter": hole, "depth": height,
                 "axis_direction": [0, 0, 1], "entry_center": [0, 0, 0],
                 "exit_center": [0, 0, height], "threaded": False},
        "hole_diameter_range_mm": [DIAMETER_MIN_MM, DIAMETER_MAX_MM],
        "compatibility_checked": False,
    }
    return nut, details


def generate(count=100, seed=None, output=None):
    import cadquery as cq

    if count < 1:
        raise ValueError("Count must be positive")
    seed = seed if seed is not None else random.SystemRandom().randrange(2**63)
    rng = random.Random(f"nuts:{seed}")
    output = Path(output) if output else (Path(__file__).resolve().parent /
        "generirovanie_gaek" / ("batch_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f")))
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    manifest = {"schema_version": 3, "units": "mm", "seed": seed,
                "dimension_step_mm": DIMENSION_STEP_MM,
                "requested_count": count, "threaded": False,
                "hole_diameter_range_mm": [DIAMETER_MIN_MM, DIAMETER_MAX_MM], "models": []}

    def save_manifest():
        save_manifest_json(output / "manifest.json", manifest)

    save_manifest()
    gallery = []
    columns = math.ceil(math.sqrt(count))
    spacing = (DIAMETER_MAX_MM+8.0)/math.cos(math.pi/6)+8
    for index in range(count):
        nut, details = make_nut(rng)
        name = f"nut_{index:04d}"
        folder = output / "nuts" / name
        folder.mkdir(parents=True)
        cq.exporters.export(nut, str(folder / f"{name}.step"))
        cq.exporters.export(nut, str(folder / f"{name}.stl"), tolerance=0.03, angularTolerance=0.1)
        details.update(seed=seed, index=index)
        (folder / f"{name}.json").write_text(json.dumps(details, ensure_ascii=False, indent=2), encoding="utf-8")
        relative = folder.relative_to(output).as_posix()
        manifest["models"].append({"name": name, "step": f"{relative}/{name}.step",
                                   "stl": f"{relative}/{name}.stl",
                                   "parameters": f"{relative}/{name}.json"})
        save_manifest()
        gallery.append(nut.translate(((index % columns)*spacing, (index // columns)*spacing, 0)))
        if (index+1) % 10 == 0 or index+1 == count:
            print(f"Generated {index+1}/{count}", flush=True)
    cq.exporters.export(cq.Compound.makeCompound(gallery), str(output / "all_nuts.stl"),
                        tolerance=0.03, angularTolerance=0.1)
    print(f"Output: {output}\nSeed: {seed}")
    return output


def main():
    parser = argparse.ArgumentParser(description="Random hexagonal nuts without threads for Bolty.py")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", type=Path, help="New output directory; existing data is never overwritten")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be at least 1")
    try:
        generate(args.count, args.seed, args.output)
    except FileExistsError:
        parser.error("Output directory already exists; choose a new --output.")


if __name__ == "__main__":
    main()
