r"""Случайные детали с продольными выступами шести типов.

Запуск из папки cadgen-students 3 (создаёт модели только при запуске):
    .\.venv-win\Scripts\python.exe generirovanie_pazov/generate_parts.py
    .\.venv-win\Scripts\python.exe generirovanie_pazov/generate_parts.py --count 10
    .\.venv-win\Scripts\python.exe generirovanie_pazov/generate_parts.py --profile dovetail --seed 42

Выступ выступает вниз из основания: плоскость крепления z=0, основание выше,
выступ ниже. Продольная ось — Y. Единицы — мм.

Используются те же семейства профилей, что и у пазов, но тип, размеры и длина
выбираются независимо. Гарантии вхождения нет: сравнение будет отдельным этапом.
Файлы ранее созданных пазов не читаются. Даже одинаковые --seed у двух скриптов
не подгоняют детали друг к другу, так как используются разные случайные потоки.

Общие определения форм и экспорт импортируются из соседнего generate_grooves.py.
Держите оба файла в одной папке. Сам импорт ничего не генерирует.
"""

from __future__ import annotations

from dataclasses import asdict
import random

if __package__:
    from .generate_grooves import build_parser, generate_batch, profile_prism, sample_profile
else:
    from generate_grooves import build_parser, generate_batch, profile_prism, sample_profile


def make_part(rng: random.Random, kind: str = "random"):
    """Создаёт основание с выступом; размеры не зависят от существующих пазов."""
    import cadquery as cq

    profile = sample_profile(rng, kind)
    left_margin = round(rng.uniform(2.0, 10.0), 2)
    right_margin = round(rng.uniform(2.0, 10.0), 2)
    base_width = profile.max_width + left_margin + right_margin
    base_length = round(rng.uniform(30.0, 100.0), 2)
    base_thickness = round(rng.uniform(3.0, 10.0), 2)
    protrusion_length = round(base_length*rng.uniform(0.65, 1.0), 2)
    offset_x = (left_margin-right_margin)/2
    base = cq.Workplane("XY").box(base_width, base_length, base_thickness,
                                   centered=(True, True, False)).val()
    tongue = profile_prism(profile, protrusion_length).translate((offset_x, 0, 0))
    shape = base.fuse(tongue).clean()
    metadata = {
        "role": "protrusion", "profile": asdict(profile),
        "body": {"width": base_width, "length": base_length, "height": base_thickness},
        "feature": {"axis": "Y", "length": protrusion_length,
                    "attachment_center": [offset_x, 0, 0],
                    "direction_from_base": "-Z"},
    }
    return shape, metadata


def main():
    parser = build_parser("Generate random solids with protrusions (no fit checks)")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be at least 1")
    try:
        generate_batch(args, "parts", make_part)
    except FileExistsError:
        parser.error("Output directory already exists. Choose a new --output directory.")


if __name__ == "__main__":
    main()
