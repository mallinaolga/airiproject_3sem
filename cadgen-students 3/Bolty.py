r"""Генератор шести типов болтов/винтов с гладким цилиндрическим стержнем.

Из папки cadgen-students 3:
    .\.venv-win\Scripts\python.exe Bolty.py --count 24
    .\.venv-win\Scripts\python.exe Bolty.py --type all --count 24
    .\.venv-win\Scripts\python.exe Bolty.py --type hex_socket --count 10 --seed 42
    .\.venv-win\Scripts\python.exe Bolty.py --self-test

--type random: count моделей со случайным типом.
--type all: count моделей КАЖДОГО из шести типов.
Каждая модель сохраняется как STEP, STL и JSON с размерами в мм.
Результаты: generirovanie_boltov/batch_... рядом с этим файлом.

Резьбы нет. Диаметр стержня случайный, 4–10 мм; длина случайная, 12–70 мм.
Линейные параметры болтов выбираются с шагом 0.5 мм, включая размеры шлица.
У полусферической головки диаметр целый, чтобы радиус и высота также были
кратны 0.5 мм. Размеры шлица округляются; тип его профиля сохраняется.
Ширина головки минимум на 4 мм больше диаметра стержня.
Otverstiya.py и Gaiki.py выбирают отверстия независимо в том же диапазоне:
совместимость конкретной пары не гарантируется. Диапазон задан ниже один раз.
Плоская головка — цилиндр с плоским верхом, а не потайной конус.
Полукруглая головка — полусфера на невысоком цилиндрическом основании.
Углубления имеют одинаковые типы профилей и случайные размеры: прямой шлиц,
симметричный крест и правильный шестигранник. Это упрощённые CAD-профили,
без привязки к стандартам отвёрток и крепежа.
Импорт файла ничего не генерирует. --self-test строит модели только в памяти.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime
import json
import math
from pathlib import Path
import random
import time


# Общий диапазон стержней и отверстий; импортируется двумя другими генераторами.
DIAMETER_MIN_MM = 4.0
DIAMETER_MAX_MM = 10.0
DIMENSION_STEP_MM = 0.5


def sample_dimension(rng: random.Random, minimum: float, maximum: float,
                     step: float = DIMENSION_STEP_MM) -> float:
    """Равновероятный выбор допустимого значения на сетке, без выхода за границы."""
    lower = math.ceil(minimum / step - 1e-9)
    upper = math.floor(maximum / step + 1e-9)
    if lower > upper:
        raise ValueError(f"No values with step {step} in [{minimum}, {maximum}]")
    return rng.randint(lower, upper) * step


def snap_dimension(value: float) -> float:
    return math.floor(value / DIMENSION_STEP_MM + 0.5) * DIMENSION_STEP_MM


def sample_diameter(rng: random.Random) -> float:
    return sample_dimension(rng, DIAMETER_MIN_MM, DIAMETER_MAX_MM)


def save_manifest_json(path: Path, data: dict) -> None:
    """Retry short Windows sharing locks while keeping the previous index intact."""
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    for attempt in range(10):
        try:
            temporary.replace(path)
            return
        except PermissionError:
            if attempt == 9:
                raise
            time.sleep(0.05*(attempt+1))


TYPES = (
    "slotted_round",  # Полукруглая головка, прямой шлиц «−».
    "slotted_flat",   # Плоская головка, прямой шлиц «−».
    "cross_round",    # Полукруглая головка, крест «+».
    "cross_flat",     # Плоская головка, крест «+».
    "hex_socket",     # Цилиндрическая головка, шестигранное углубление.
    "hex_head",       # Наружная шестигранная головка, без углубления.
)


@dataclass(frozen=True)
class BoltSpec:
    kind: str
    shaft_length: float
    shaft_diameter: float
    head_width: float  # Диаметр круглой головки или размер шестигранника по граням.
    head_height: float  # Номинальная высота головки до вырезания углубления.
    band_height: float  # Цилиндрическое основание полусферы; 0 у плоских головок.
    drive_size: float  # Длина шлица/размах креста либо размер шестигранника по граням.

    @property
    def drive_kind(self) -> str:
        if self.kind.startswith("slotted"):
            return "slot"
        if self.kind.startswith("cross"):
            return "cross"
        return "hexagon" if self.kind == "hex_socket" else "none"

    @property
    def drive_depth(self) -> float:
        return snap_dimension(self.drive_size * (0.65 if self.kind == "hex_socket" else 0.45))

    @property
    def drive_width(self) -> float | None:
        if self.drive_kind == "slot":
            return snap_dimension(self.drive_size / 6)
        if self.drive_kind == "cross":
            return snap_dimension(self.drive_size / 4)
        return None


def sample_spec(rng: random.Random, kind: str) -> BoltSpec:
    if kind not in TYPES:
        raise ValueError(f"Unknown bolt type: {kind}")
    length = sample_dimension(rng, 12.0, 70.0)
    diameter = sample_diameter(rng)
    width = sample_dimension(rng, max(10.0, diameter+4.0), 18.0,
                             step=1.0 if kind.endswith("round") else DIMENSION_STEP_MM)
    if kind == "hex_head":
        return BoltSpec(kind, length, diameter, width, sample_dimension(rng, 4.0, 9.0), 0.0, 0.0)
    if kind == "hex_socket":
        size = sample_dimension(rng, width*0.28, width*0.5)
        height = snap_dimension(size*0.65) + sample_dimension(rng, 1.5, 3.5)
        return BoltSpec(kind, length, diameter, width, height, 0.0, size)
    size = sample_dimension(rng, width*0.45, width*0.75)
    if kind.endswith("round"):
        band = sample_dimension(rng, 1.0, 2.5)
        height = band + width/2
    else:
        band = 0.0
        height = snap_dimension(size*0.45) + sample_dimension(rng, 1.5, 3.5)
    return BoltSpec(kind, length, diameter, width, height, band, size)


def build_bolt(spec: BoltSpec, *, adaptive=False):
    """Стержень занимает z=-length..0, головка начинается на z=0."""
    import cadquery as cq

    if spec.kind not in TYPES:
        raise ValueError(f"Unknown bolt type: {spec.kind}")
    for field, value in asdict(spec).items():
        if field != "kind" and (not math.isfinite(value) or value < 0):
            raise ValueError(f"Invalid dimension: {field}")
    if (spec.shaft_length <= 0 or spec.shaft_diameter <= 0
            or spec.head_width < (1.4*spec.shaft_diameter if adaptive else spec.shaft_diameter+4.0-1e-9) or spec.head_height <= 0):
        raise ValueError("Length and head height must be positive; head must leave a positive bearing shoulder (legacy: at least 4 mm wider)")
    if spec.drive_kind != "none" and (spec.drive_size <= 0 or spec.drive_depth >= spec.head_height):
        raise ValueError("Drive must be nonempty and leave material below its floor")

    shaft = (cq.Workplane("XY").circle(spec.shaft_diameter/2)
             .extrude(spec.shaft_length).translate((0, 0, -spec.shaft_length)).val())
    if spec.kind == "hex_head":
        head = (cq.Workplane("XY").polygon(6, spec.head_width, circumscribed=True)
                .extrude(spec.head_height).val())
    elif spec.kind.endswith("round"):
        radius = spec.head_width/2
        if spec.band_height <= 0 or not math.isclose(spec.head_height, spec.band_height+radius):
            raise ValueError("Round head must be a hemisphere on a cylindrical band")
        band = cq.Workplane("XY").circle(radius).extrude(spec.band_height).val()
        dome = cq.Solid.makeSphere(radius, pnt=(0, 0, spec.band_height),
                                   angleDegrees1=0, angleDegrees2=90)
        head = band.fuse(dome).clean()
    else:
        head = cq.Workplane("XY").circle(spec.head_width/2).extrude(spec.head_height).val()
    whole = shaft.fuse(head).clean()
    if spec.drive_kind != "none":
        floor = spec.head_height-spec.drive_depth
        # Cut starts at the recess floor and extends beyond the top surface.
        plane = cq.Workplane("XY", origin=(0, 0, floor))
        cut_height = spec.drive_depth + 1.0
        if spec.drive_kind == "slot":
            cutter = plane.rect(spec.drive_size, spec.drive_width).extrude(cut_height).val()
        elif spec.drive_kind == "cross":
            horizontal = plane.rect(spec.drive_size, spec.drive_width).extrude(cut_height).val()
            vertical = (cq.Workplane("XY", origin=(0, 0, floor))
                        .rect(spec.drive_width, spec.drive_size).extrude(cut_height).val())
            cutter = horizontal.fuse(vertical).clean()
        else:
            cutter = plane.polygon(6, spec.drive_size, circumscribed=True).extrude(cut_height).val()
        shape = whole.cut(cutter).clean()
        if shape.Volume() >= whole.Volume()-1e-6:
            raise RuntimeError("Drive cut did not remove material")
    else:
        shape = whole
    if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0:
        raise RuntimeError(f"Invalid bolt geometry: {spec}")
    return shape


def metadata(spec: BoltSpec) -> dict:
    return {
        "units": "mm", "type": spec.kind, "dimension_step_mm": DIMENSION_STEP_MM,
        "shaft": {"shape": "cylinder", "diameter": spec.shaft_diameter,
                  "length": spec.shaft_length, "threaded": False},
        "head": {"width": spec.head_width,
                 "width_meaning": "across_flats" if spec.kind == "hex_head" else "diameter",
                 "nominal_height": spec.head_height, "band_height": spec.band_height},
        "drive": {"kind": spec.drive_kind, "size": spec.drive_size,
                  "size_meaning": "across_flats" if spec.kind == "hex_socket" else "span",
                  "arm_width": spec.drive_width, "depth": spec.drive_depth},
        "coordinates": {"shaft_axis": "Z", "head_bottom_z": 0,
                        "shaft_tip_z": -spec.shaft_length},
        "parameters": asdict(spec),
    }


def generate(count: int, kind: str, seed: int | None, output: Path | None) -> Path:
    import cadquery as cq

    if count < 1 or kind not in ("random", "all", *TYPES):
        raise ValueError("Invalid count or type")
    seed = seed if seed is not None else random.SystemRandom().randrange(2**63)
    rng = random.Random(f"bolts:{seed}")
    output = output or (Path(__file__).resolve().parent / "generirovanie_boltov" /
                        ("batch_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")))
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    kinds = [t for t in TYPES for _ in range(count)] if kind == "all" else [kind]*count
    manifest = {"schema_version": 3, "seed": seed, "units": "mm", "type": kind,
                "dimension_step_mm": DIMENSION_STEP_MM,
                "shaft_diameter_range_mm": [DIAMETER_MIN_MM, DIAMETER_MAX_MM],
                "requested_models": len(kinds), "models": []}

    def save_manifest():
        save_manifest_json(output / "manifest.json", manifest)

    save_manifest()
    for index, selected in enumerate(kinds):
        selected = rng.choice(TYPES) if selected == "random" else selected
        spec = sample_spec(rng, selected)
        shape = build_bolt(spec)
        name = f"bolt_{index:04d}_{selected}"
        folder = output / selected / name
        folder.mkdir(parents=True)
        cq.exporters.export(shape, str(folder / f"{name}.step"))
        cq.exporters.export(shape, str(folder / f"{name}.stl"), tolerance=0.03, angularTolerance=0.1)
        details = metadata(spec)
        details.update(seed=seed, index=index)
        (folder / f"{name}.json").write_text(json.dumps(details, ensure_ascii=False, indent=2), encoding="utf-8")
        relative = folder.relative_to(output).as_posix()
        manifest["models"].append({"name": name, "type": selected,
                                   "step": f"{relative}/{name}.step", "stl": f"{relative}/{name}.stl",
                                   "parameters": f"{relative}/{name}.json"})
        save_manifest()
        print(f"[{index+1}/{len(kinds)}] {name}", flush=True)
    print(f"Seed: {seed}\nOutput: {output}")
    return output


def self_test():
    """Контроль геометрии только в памяти: никаких файлов моделей не создаётся."""
    import cadquery as cq

    rng = random.Random(42)
    for kind in TYPES:
        for _ in range(4):
            spec = sample_spec(rng, kind)
            shape = build_bolt(spec)
            # Isolate a 1 mm slice midway along the shaft: its volume and width
            # must match this specimen's diameter for every head type and length.
            slab = (cq.Workplane("XY", origin=(0, 0, -spec.shaft_length/2))
                    .box(40, 40, 1).val())
            section = shape.intersect(slab)
            box = section.BoundingBox()
            assert DIAMETER_MIN_MM <= spec.shaft_diameter <= DIAMETER_MAX_MM
            assert math.isclose(box.xlen, spec.shaft_diameter, abs_tol=1e-6)
            assert math.isclose(box.ylen, spec.shaft_diameter, abs_tol=1e-6)
            assert math.isclose(section.Volume(), math.pi*(spec.shaft_diameter/2)**2, rel_tol=1e-6)
            assert math.isclose(shape.BoundingBox().zmin, -spec.shaft_length, abs_tol=1e-6)
            if spec.drive_kind != "none":
                floor = spec.head_height-spec.drive_depth
                assert not shape.isInside(cq.Vector(0, 0, floor+spec.drive_depth/2), 1e-7)
                assert shape.isInside(cq.Vector(0, 0, floor/2), 1e-7)
            else:
                assert shape.isInside(cq.Vector(0, 0, spec.head_height/2), 1e-7)
        print(f"PASS: {kind}")
    print("24 solids checked in memory; no model files created.")


def main():
    parser = argparse.ArgumentParser(description="Six bolt types; random 4-10 mm smooth shafts, lengths and heads")
    parser.add_argument("--count", type=int, default=1, help="Total models, or models PER TYPE with --type all")
    parser.add_argument("--type", choices=("random", "all", *TYPES), default="random")
    parser.add_argument("--seed", type=int, help="Optional reproducible seed")
    parser.add_argument("--output", type=Path, help="New output directory; existing directories are not overwritten")
    parser.add_argument("--self-test", action="store_true", help="Check geometry in memory without exporting models")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be at least 1")
    if args.self_test:
        self_test()
        return
    try:
        generate(args.count, args.type, args.seed, args.output)
    except FileExistsError:
        parser.error("Output directory already exists. Choose a new --output.")


if __name__ == "__main__":
    main()
