
import argparse
import json
from collections import Counter
from pathlib import Path

import cadquery as cq


def find_step_files(folder):
    folder = Path(folder)

    if not folder.is_dir():
        raise FileNotFoundError(f"Папка не найдена: {folder}")

    return sorted(
        path
        for path in folder.rglob("*.step")
        if ".tmp." not in path.name
    )


def load_part(file_path):
    model = cq.importers.importStep(str(file_path))
    shape = model.val()

    if not shape.isValid():
        raise ValueError(f"Некорректная модель: {file_path}")

    return shape


def analyze_part(file_path):
    shape = load_part(file_path)

    surfaces = []
    surface_types = Counter()

    for face_id, face in enumerate(shape.Faces()):
        surface_type = face.geomType()
        surface_types[surface_type] += 1

        center = face.Center()

        surfaces.append({
            "face_id": face_id,
            "type": surface_type,
            "area": face.Area(),
            "center": [
                center.x,
                center.y,
                center.z
            ]
        })

    bbox = shape.BoundingBox()

    return {
        "file": str(file_path),
        "volume": shape.Volume(),
        "dimensions": {
            "x": bbox.xlen,
            "y": bbox.ylen,
            "z": bbox.zlen
        },
        "faces_count": len(surfaces),
        "surface_types": dict(surface_types),
        "surfaces": surfaces
    }


def analyze_all_parts(folder, output_path):
    step_files = find_step_files(folder)

    print(f"Найдено STEP-файлов: {len(step_files)}")

    results = []

    for file_path in step_files:
        try:
            result = analyze_part(file_path)
            results.append(result)

            print(f"\nДеталь: {file_path.name}")
            print(f"Объем: {result['volume']:.3f}")
            print(f"Количество граней: {result['faces_count']}")
            print(f"Типы поверхностей: {result['surface_types']}")

        except Exception as error:
            print(f"Ошибка при анализе {file_path}: {error}")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print(f"\nУспешно проанализировано деталей: {len(results)}")
    print(f"Результаты сохранены: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "folder",
        help="Папка с STEP-файлами"
    )

    parser.add_argument(
        "--output",
        default="assembly_analysis.json",
        help="Путь к JSON-отчету"
    )

    args = parser.parse_args()

    analyze_all_parts(args.folder, args.output)
