
# Создание демонстрационной STEP-сборки из двух совмещённых деталей.

import argparse
import json
from pathlib import Path

import cadquery as cq

from .geometry_analysis import load_part
from .assembly_validation import resolve_step_path, transform_part


def find_demo_candidate(results):
    """Находит вариант с контактом и без значимого пересечения."""
    candidates = []

    for pair in results:
        for pose in pair.get("validation_candidates", []):
            if pose.get("status") == "error":
                continue

            if "rotation_matrix" not in pose or "translation" not in pose:
                continue

            overlap = pose.get("intersection_volume")
            distance = pose.get("minimum_distance")

            if overlap is None or distance is None:
                continue

            if overlap > 1e-5 or distance > 1e-3:
                continue

            contact_area = float(pose.get("planar_contact_area") or 0)

            # Нужен хотя бы предварительно зарегистрированный контакт.
            if (
                "contact" not in pose.get("status", "")
                and contact_area <= 0
            ):
                continue

            candidates.append((contact_area, pair, pose))

    if not candidates:
        return None

    # Предпочитаем вариант с большей площадью контакта.
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1], candidates[0][2]


def export_demo(validation_path, output_path, project_root):
    with open(validation_path, "r", encoding="utf-8") as file:
        results = json.load(file)

    selected = find_demo_candidate(results)

    if selected is None:
        print("Не найдено подходящих вариантов для демонстрации.")
        return

    pair, pose = selected

    path_a = resolve_step_path(pair["part_a"], project_root)
    path_b = resolve_step_path(pair["part_b"], project_root)

    part_a = load_part(path_a)
    part_b = load_part(path_b)

    # Оставляем первую деталь неподвижной.
    # Вторую поворачиваем и перемещаем по результатам этапа 6.
    moved_b = transform_part(
        part_b,
        pose["rotation_matrix"],
        pose["translation"],
    )

    # Добавляем обе детали в одну сборку как отдельные компоненты.
    assembly = cq.Assembly(name="demo_assembly")
    assembly.add(part_a, name="part_a")
    assembly.add(moved_b, name="part_b")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    assembly.save(str(output_path), exportType="STEP")
    # Экспорт сборки в STL для просмотра
    stl_path = output_path.with_suffix(".stl")

    combined = cq.Compound.makeCompound([part_a, moved_b])
    cq.exporters.export(combined, str(stl_path))

    print(f"STL-файл для просмотра: {stl_path}")

    # Дополнительно сохраняем информацию о выбранной паре.
    info_path = output_path.with_suffix(".json")

    info = {
        "part_a": pair["part_a"],
        "part_b": pair["part_b"],
        "pose_index": pose.get("pose_index"),
        "rotation_matrix": pose["rotation_matrix"],
        "translation": pose["translation"],
        "intersection_volume": pose["intersection_volume"],
        "minimum_distance": pose["minimum_distance"],
        "planar_contact_area": pose.get("planar_contact_area"),
        "status": "demonstration_only",
        "note": "Геометрическая демонстрация, не подтверждённая механическая посадка",
    }

    with open(info_path, "w", encoding="utf-8") as file:
        json.dump(info, file, indent=4, ensure_ascii=False)

    print("\nДемонстрационная сборка создана!")
    print(f"Первая деталь: {path_a}")
    print(f"Вторая деталь: {path_b}")
    print(f"STEP-файл: {output_path}")
    print(f"Описание сборки: {info_path}")
    print("Важно: механическая совместимость деталей не подтверждена.")


def main():
    parser = argparse.ArgumentParser(
        description="Экспорт демонстрационной CAD-сборки"
    )

    parser.add_argument(
        "--validation",
        default="assembly_validation.json",
        help="JSON с результатами проверки совмещений",
    )

    parser.add_argument(
        "--output",
        default="assemblies/demo_assembly.step",
        help="Путь к итоговому STEP-файлу",
    )

    parser.add_argument(
        "--project-root",
        default=".",
        help="Корневая папка проекта",
    )

    args = parser.parse_args()

    export_demo(
        Path(args.validation),
        Path(args.output),
        Path(args.project_root),
    )


if __name__ == "__main__":
    main()
