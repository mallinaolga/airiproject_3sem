# Расчёт поворота и перемещения деталей для поиска возможных вариантов их соединения

## Проверка гипотез сборки STEP-деталей: пересечения, контактные поверхности
# и дискретная проверка прямолинейного подвода. Посадка не подтверждается автоматически.

import argparse
import json
import math
from pathlib import Path

import cadquery as cq
import numpy as np
from scipy.spatial.transform import Rotation

from .geometry_analysis import load_part


def resolve_step_path(filename, project_root):
    path = Path(filename)
    if path.is_file():
        return path
    alternative = project_root / path
    if alternative.is_file():
        return alternative
    raise FileNotFoundError(f"Не найден STEP-файл: {filename}")


def transform_part(shape, rotation_matrix, translation):
    rotation = np.asarray(rotation_matrix, dtype=float)
    shift = np.asarray(translation, dtype=float)
    if rotation.shape != (3, 3) or shift.shape != (3,):
        raise ValueError("Ожидаются матрица 3x3 и перенос из трёх чисел")
    if not np.isfinite(rotation).all() or not np.isfinite(shift).all():
        raise ValueError("Поворот и перенос должны быть конечными числами")
    if not np.allclose(rotation.T @ rotation, np.eye(3), atol=1e-4):
        raise ValueError("Матрица поворота не ортогональна")
    if not np.isclose(np.linalg.det(rotation), 1.0, atol=1e-4):
        raise ValueError("Матрица не задаёт собственный поворот")

    rotvec = Rotation.from_matrix(rotation).as_rotvec()
    angle = float(np.linalg.norm(rotvec))
    moved = shape
    if angle > 1e-10:
        axis = tuple((rotvec / angle).tolist())
        moved = moved.rotate((0, 0, 0), axis, math.degrees(angle))
    return moved.translate(tuple(shift.tolist()))


def overlap_volume(a, b):
    return max(0.0, float(a.intersect(b).Volume()))


def planar_contact_area(a, b, distance_tolerance):
    """Сумма площадей совпадающих участков плоских граней (не криволинейных)."""
    faces_a = [f for f in a.Faces() if f.geomType() == "PLANE"]
    faces_b = [f for f in b.Faces() if f.geomType() == "PLANE"]
    total = 0.0
    for fa in faces_a:
        na = fa.normalAt()
        ca = fa.Center()
        for fb in faces_b:
            nb = fb.normalAt()
            cb = fb.Center()
            if na.dot(nb) > -0.9999:
                continue
            if abs((cb - ca).dot(na)) > distance_tolerance:
                continue
            try:
                common = fa.intersect(fb)
                total += max(0.0, float(common.Area()))
            except Exception:
                raise
    return total


def bbox_diagonal(shape):
    bb = shape.BoundingBox()
    return math.sqrt(bb.xlen ** 2 + bb.ylen ** 2 + bb.zlen ** 2)


def sample_insertion_paths(a, moved_b, volume_tolerance, steps, clearance_factor):
    """Пробуем прямолинейное сближение по ±X, ±Y, ±Z.

    Это только дискретная эвристика: между отсчётами столкновение возможно.
    """
    travel = (bbox_diagonal(a) + bbox_diagonal(moved_b)) * clearance_factor
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0),
                  (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    outcomes = []
    for direction in directions:
        start = moved_b.translate(tuple(travel * x for x in direction))
        # Начальная позиция должна быть отдельно от A.
        if overlap_volume(a, start) > volume_tolerance:
            outcomes.append({"direction": list(direction), "status": "start_collides"})
            continue
        if a.distance(start) <= 1e-8:
            outcomes.append({"direction": list(direction), "status": "start_not_separated"})
            continue
        blocked_at = None
        for step in range(1, steps):
            fraction = (steps - step) / steps
            intermediate = moved_b.translate(tuple(travel * fraction * x for x in direction))
            if overlap_volume(a, intermediate) > volume_tolerance:
                blocked_at = step
                break
        outcomes.append({
            "direction": list(direction),
            "status": "sampled_clear" if blocked_at is None else "collision_on_path",
            "first_collision_step": blocked_at,
        })
    return outcomes


def check_pose(a, b, pose, volume_tolerance, contact_tolerance,
               min_contact_area, path_steps, path_clearance_factor):
    moved_b = transform_part(b, pose["rotation_matrix"], pose["translation"])
    volume = overlap_volume(a, moved_b)
    relative = volume / max(min(float(a.Volume()), float(moved_b.Volume())), 1e-12)
    distance = 0.0 if volume > volume_tolerance else max(0.0, float(a.distance(moved_b)))
    result = {
        "feature_a_index": pose.get("feature_a_index"),
        "feature_b_index": pose.get("feature_b_index"),
        "rotation_matrix": pose["rotation_matrix"],
        "translation": pose["translation"],
        "intersection_volume": round(volume, 9),
        "relative_overlap": round(relative, 9),
        "minimum_distance": round(distance, 9),
        "planar_contact_area": None,
        "path_trials": [],
        "path_sampled_clear": False,
        "assembly_path_checked": False,
        "tolerances_checked": False,
        "connection_confirmed": False,
    }
    if volume > volume_tolerance:
        result["status"] = "collision"
    elif distance > contact_tolerance:
        result["status"] = "separated"
    else:
        area = planar_contact_area(a, moved_b, contact_tolerance)
        result["planar_contact_area"] = round(area, 9)
        if area < min_contact_area:
            result["status"] = "point_or_edge_contact_or_curved_contact"
        else:
            result["status"] = "surface_contact_candidate"
        trials = sample_insertion_paths(a, moved_b, volume_tolerance,
                                        path_steps, path_clearance_factor)
        result["path_trials"] = trials
        result["path_sampled_clear"] = any(
            item["status"] == "sampled_clear" for item in trials
        )
        # Даже успешная дискретная проверка НЕ доказывает непрерывную траекторию.
        # Даже площадной контакт НЕ доказывает, что выступ соответствует пазу.
    return result


def validate_assemblies(alignments_path, output_path, project_root,
                        volume_tolerance=1e-5, contact_tolerance=1e-3,
                        min_contact_area=1e-4, path_steps=12,
                        path_clearance_factor=1.1):
    with open(alignments_path, "r", encoding="utf-8") as stream:
        alignments = json.load(stream)
    if not isinstance(alignments, list):
        raise ValueError("Файл совмещений должен содержать JSON-массив")

    cache = {}
    results = []
    counters = {"checked": 0, "collision": 0, "surface_contact_candidate": 0,
                "point_or_edge_contact_or_curved_contact": 0, "separated": 0,
                "sampled_clear": 0, "errors": 0}
    for pair in alignments:
        part_a_path = pair["part_a"]
        part_b_path = pair["part_b"]
        candidates = pair.get("alignment_candidates", [])
        entry = {
            "part_a": part_a_path,
            "part_b": part_b_path,
            "status": "no_pose_candidates" if not candidates else "evaluated",
            "validation_candidates": [],
        }
        if candidates:
            try:
                for filename in (part_a_path, part_b_path):
                    if filename not in cache:
                        path = resolve_step_path(filename, project_root)
                        cache[filename] = load_part(path)
                a, b = cache[part_a_path], cache[part_b_path]
            except Exception as exc:
                entry["status"] = "error_loading_part"
                entry["error"] = str(exc)
                counters["errors"] += len(candidates)
                results.append(entry)
                continue

            for index, pose in enumerate(candidates):
                try:
                    outcome = check_pose(a, b, pose, volume_tolerance,
                                         contact_tolerance, min_contact_area,
                                         path_steps, path_clearance_factor)
                    counters["checked"] += 1
                    counters[outcome["status"]] += 1
                    if outcome["path_sampled_clear"]:
                        counters["sampled_clear"] += 1
                except Exception as exc:
                    counters["errors"] += 1
                    outcome = {"status": "error", "error": str(exc)}
                outcome["pose_index"] = index
                entry["validation_candidates"].append(outcome)
        results.append(entry)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as stream:
        json.dump(results, stream, indent=2, ensure_ascii=False)

    print(f"Пар в файле: {len(alignments)}")
    print(f"Проверено гипотез: {counters['checked']}")
    print(f"С объёмным пересечением: {counters['collision']}")
    print(f"С площадным плоским контактом: {counters['surface_contact_candidate']}")
    print("С контактом без достаточной площади плоских граней: "
          f"{counters['point_or_edge_contact_or_curved_contact']}")
    print(f"Без контакта: {counters['separated']}")
    print(f"С хотя бы одним дискретно свободным путём: {counters['sampled_clear']}")
    print(f"Ошибок: {counters['errors']}")
    print(f"Результаты: {output_path}")
    print("ВНИМАНИЕ: посадочные допуски, криволинейные контакты и непрерывная "
          "траектория сборки не подтверждены. Подтверждённых соединений: 0.")
    return results


def main():
    parser = argparse.ArgumentParser(description="Геометрическая проверка гипотез сборки")
    parser.add_argument("--alignments", default="assembly_alignment.json")
    parser.add_argument("--output", default="assembly_validation.json")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--volume-tolerance", type=float, default=1e-5)
    parser.add_argument("--contact-tolerance", type=float, default=1e-3)
    parser.add_argument("--min-contact-area", type=float, default=1e-4)
    parser.add_argument("--path-steps", type=int, default=12)
    parser.add_argument("--path-clearance-factor", type=float, default=1.1)
    args = parser.parse_args()
    if any(value < 0 for value in (args.volume_tolerance, args.contact_tolerance,
                                   args.min_contact_area)):
        parser.error("Допуски должны быть неотрицательными")
    if args.path_steps < 2 or args.path_clearance_factor < 1.0:
        parser.error("path-steps >= 2 и path-clearance-factor >= 1.0")
    validate_assemblies(args.alignments, args.output, Path(args.project_root),
                        args.volume_tolerance, args.contact_tolerance,
                        args.min_contact_area, args.path_steps,
                        args.path_clearance_factor)


if __name__ == "__main__":
    main()
