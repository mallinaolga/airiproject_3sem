r"""Случайные детали со сквозными продольными пазами шести типов.

Запуск из папки cadgen-students 3 (создаёт модели только при запуске):
    .\.venv-win\Scripts\python.exe generirovanie_pazov/generate_grooves.py
    .\.venv-win\Scripts\python.exe generirovanie_pazov/generate_grooves.py --count 10
    .\.venv-win\Scripts\python.exe generirovanie_pazov/generate_grooves.py --profile dovetail --seed 42

Единицы — мм. Паз идёт вдоль Y и открыт сверху и с обоих торцов.
Сечение строится в плоскости XZ. Его верх лежит на z=0, дно — ниже.
Тип профиля по умолчанию равновероятно выбирается для каждой детали.
Скрипт не читает другие детали и не проверяет совместимость.

Общие определения профилей также использует generate_parts.py. Импорт этого
модуля, в том числе из второго скрипта, не создаёт геометрию или файлы.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime
import json
import math
from pathlib import Path
import random
from typing import Callable


PROFILE_TYPES = (
    "rectangular",  # Прямоугольный паз: верхний левый на картинке.
    "v",            # V-образный: верхний средний.
    "trapezoid",    # Широкий вход, узкое дно: верхний правый.
    "dovetail",     # Узкий вход, широкое дно: нижний левый.
    "t",            # Узкая шейка и широкая прямоугольная часть: нижний средний.
    "round",        # Полукруглый: нижний правый.
)


@dataclass(frozen=True)
class Profile:
    kind: str
    opening_width: float
    depth: float
    bottom_width: float | None = None
    neck_depth: float | None = None
    radius: float | None = None

    @property
    def max_width(self) -> float:
        return max(self.opening_width, self.bottom_width or 0.0)

    def validate(self) -> None:
        if self.kind not in PROFILE_TYPES:
            raise ValueError(f"Unknown profile: {self.kind}")
        for name, value in asdict(self).items():
            if name != "kind" and value is not None:
                if not math.isfinite(value) or value <= 0:
                    raise ValueError(f"{name} must be finite and positive")
        if self.kind == "trapezoid":
            if self.bottom_width is None or not self.bottom_width < self.opening_width:
                raise ValueError("A trapezoid must have a narrower bottom")
        if self.kind in ("dovetail", "t"):
            if self.bottom_width is None or not self.bottom_width > self.opening_width:
                raise ValueError("An undercut must have a wider bottom")
        if self.kind == "t":
            if self.neck_depth is None or not 0 < self.neck_depth < self.depth:
                raise ValueError("T-slot neck must end above the bottom")
        if self.kind == "round":
            if (self.radius is None or not math.isclose(self.depth, self.radius)
                    or not math.isclose(self.opening_width, 2*self.radius)):
                raise ValueError("A semicircle needs width = 2*radius and depth = radius")


def sample_profile(rng: random.Random, kind: str = "random") -> Profile:
    """Выбирает форму и размеры без доступа к другому генератору или его файлам."""
    kind = rng.choice(PROFILE_TYPES) if kind == "random" else kind
    width = round(rng.uniform(8.0, 24.0), 2)
    depth = round(rng.uniform(5.0, 18.0), 2)
    options = {}
    if kind == "trapezoid":
        options["bottom_width"] = round(width*rng.uniform(0.35, 0.8), 2)
    elif kind == "dovetail":
        options["bottom_width"] = round(width*rng.uniform(1.25, 1.8), 2)
    elif kind == "t":
        options["bottom_width"] = round(width*rng.uniform(1.5, 2.2), 2)
        options["neck_depth"] = round(depth*rng.uniform(0.3, 0.6), 2)
    elif kind == "round":
        depth = width/2
        options["radius"] = width/2
    profile = Profile(kind, width, depth, **options)
    profile.validate()
    return profile


def profile_prism(profile: Profile, length: float):
    """Объём профиля: X по ширине, Y вдоль детали, Z от -depth до 0.

    Этот объём вычитается из корпуса для паза или добавляется к основанию
    для выступа. Это общий способ построения формы, а не подгонка размеров.
    """
    import cadquery as cq

    profile.validate()
    if not math.isfinite(length) or length <= 0:
        raise ValueError("Profile length must be finite and positive")
    half = profile.opening_width/2
    depth = profile.depth
    plane = cq.Workplane("XZ")
    if profile.kind == "round":
        wire = (plane.moveTo(-half, 0).lineTo(half, 0)
                .threePointArc((0, -depth), (-half, 0)).close())
    else:
        if profile.kind == "rectangular":
            points = [(-half, 0), (half, 0), (half, -depth), (-half, -depth)]
        elif profile.kind == "v":
            points = [(-half, 0), (half, 0), (0, -depth)]
        elif profile.kind in ("trapezoid", "dovetail"):
            bottom = profile.bottom_width/2
            points = [(-half, 0), (half, 0), (bottom, -depth), (-bottom, -depth)]
        else:  # T-shaped undercut
            bottom = profile.bottom_width/2
            neck = profile.neck_depth
            points = [(-half, 0), (half, 0), (half, -neck), (bottom, -neck),
                      (bottom, -depth), (-bottom, -depth), (-bottom, -neck),
                      (-half, -neck)]
        wire = plane.polyline(points).close()
    # The normal of CadQuery's XZ plane points along -Y.
    return wire.extrude(length).translate((0, length/2, 0)).val()


def make_groove(rng: random.Random, kind: str = "random"):
    """Создаёт один корпус с пазом; возвращает CAD-тело и его параметры."""
    import cadquery as cq

    profile = sample_profile(rng, kind)
    left_wall = round(rng.uniform(3.0, 10.0), 2)
    right_wall = round(rng.uniform(3.0, 10.0), 2)
    floor = round(rng.uniform(3.0, 10.0), 2)
    length = round(rng.uniform(30.0, 100.0), 2)
    width = profile.max_width + left_wall + right_wall
    height = profile.depth + floor
    offset_x = (left_wall-right_wall)/2
    body = cq.Workplane("XY").box(width, length, height,
                                   centered=(True, True, False)).val()
    # Cutter overhang guarantees that both ends are open, including undercuts.
    cutter = profile_prism(profile, length+2.0).translate((offset_x, 0, height))
    shape = body.cut(cutter).clean()
    metadata = {
        "role": "groove", "profile": asdict(profile),
        "body": {"width": width, "length": length, "height": height},
        "walls": {"left": left_wall, "right": right_wall, "floor": floor},
        "feature": {"axis": "Y", "length": length,
                    "opening_center": [offset_x, 0, height],
                    "open_ends": "both"},
    }
    return shape, metadata


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--count", type=int, default=1, help="Number of independent models (default: 1)")
    parser.add_argument("--profile", choices=("random", *PROFILE_TYPES), default="random",
                        help="Profile family; random chooses independently for each model")
    parser.add_argument("--seed", type=int, help="Optional seed for reproducibility")
    parser.add_argument("--output", type=Path,
                        help="New output directory; existing directories are never overwritten")
    return parser


def generate_batch(args, stream: str, builder: Callable) -> Path:
    """Экспорт STL/STEP/JSON. Вызывается только явно, не при импорте."""
    import cadquery as cq

    if args.count < 1:
        raise ValueError("--count must be at least 1")
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(2**63)
    # Different streams: even identical --seed values do not produce matched pairs.
    rng = random.Random(f"{stream}:{seed}")
    output = args.output or (Path(__file__).resolve().parent / "generated" /
                            (stream + "_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")))
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    manifest = {"schema_version": 1, "units": "mm", "stream": stream, "seed": seed,
                "requested_count": args.count, "requested_profile": args.profile,
                "compatibility_checked": False, "models": []}

    def save_manifest():
        (output / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    save_manifest()
    for index in range(args.count):
        shape, metadata = builder(rng, args.profile)
        if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0:
            raise RuntimeError(f"Invalid CAD solid at index {index}; seed={seed}")
        name = f"{stream}_{index:04d}_{metadata['profile']['kind']}"
        item_dir = output / name
        item_dir.mkdir()
        cq.exporters.export(shape, str(item_dir / f"{name}.step"))
        cq.exporters.export(shape, str(item_dir / f"{name}.stl"),
                            tolerance=0.05, angularTolerance=0.1)
        metadata.update(units="mm", index=index, seed=seed, stream=stream,
                        compatibility_checked=False)
        (item_dir / f"{name}.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest["models"].append({"name": name, "profile": metadata["profile"]["kind"],
                                   "step": f"{name}/{name}.step",
                                   "stl": f"{name}/{name}.stl",
                                   "parameters": f"{name}/{name}.json"})
        save_manifest()
        print(f"[{index+1}/{args.count}] {name}", flush=True)
    print(f"Seed: {seed}\nOutput: {output}")
    return output


def main():
    parser = build_parser("Generate random solids with longitudinal grooves (no fit checks)")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be at least 1")
    try:
        generate_batch(args, "grooves", make_groove)
    except FileExistsError:
        parser.error("Output directory already exists. Choose a new --output directory.")


if __name__ == "__main__":
    main()
