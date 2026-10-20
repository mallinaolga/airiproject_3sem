# определение поворота и перемещения одной детали относительно другой
# запуск python -m cadgen.assembly_alignment
import argparse
import json
import math
from pathlib import Path

import numpy as np


AXES = {"X": np.array([1., 0., 0.]), "Y": np.array([0., 1., 0.]), "Z": np.array([0., 0., 1.])}


def unit(vector):
    vector = np.asarray(vector, dtype=float)
    length = np.linalg.norm(vector)
    if length <= 1e-10:
        raise ValueError("Вырожденный вектор направления")
    return vector / length


def frame(u, axis):
    """Правый ортонормированный базис: вдоль стороны, поперёк неё, ось профиля."""
    w = unit(axis)
    u = np.asarray(u, dtype=float) - np.dot(u, w) * w
    u = unit(u)
    v = unit(np.cross(w, u))
    return np.column_stack((u, v, w))


def feature_geometry(part, index):
    """Восстанавливает два луча угла по упорядоченному контуру, а не по JSON-корреляциям."""
    candidates = part["features"].get("profile_candidates", [])
    if not isinstance(index, int) or index < 0 or index >= len(candidates):
        raise ValueError(f"Кандидат с индексом {index} отсутствует")
    feature = candidates[index]
    axis = feature.get("axis")
    if axis not in AXES:
        raise ValueError("Неизвестная ось сечения")
    wire_id = feature.get("wire_id")
    vertex_id = feature.get("vertex_index")
    contours = part["features"]["cross_sections"][axis].get("contours", [])
    contour = next((c for c in contours if c.get("wire_id") == wire_id), None)
    if contour is None:
        raise ValueError("Контур кандидата не найден")
    edges = contour.get("edges_ordered", [])
    n = len(edges)
    if not isinstance(vertex_id, int) or not 0 <= vertex_id < n:
        raise ValueError("Некорректный индекс вершины")
    before, after = edges[(vertex_id - 1) % n], edges[vertex_id]
    if before["geometry"] != "LINE" or after["geometry"] != "LINE":
        raise ValueError("Совмещение по дуге пока не поддерживается")
    center = np.asarray(feature["position"], dtype=float)
    # Оба луча направлены ОТ вершины вдоль примыкающих рёбер.
    ray_before = unit(np.asarray(before["start"], dtype=float) - center)
    ray_after = unit(np.asarray(after["end"], dtype=float) - center)
    if np.linalg.norm(np.cross(ray_before, ray_after)) <= 1e-7:
        raise ValueError("Вырожденный угол")
    return {
        "position": center,
        "axis": AXES[axis],
        "rays": [ray_before, ray_after],
        "axis_name": axis,
        "role": feature["role"],
    }


def calculate_poses(geom_a, geom_b, limit=4):
    """Матрица преобразует точки детали B в координаты неподвижной A: pA = R @ pB + t."""
    if geom_a["role"] == geom_b["role"]:
        return []
    poses = []
    seen = set()
    # Не предполагаем одинаковое положение деталей или совпадение их осей.
    for ray_a_idx in (0, 1):
        for ray_b_idx in (0, 1):
            for axis_sign in (-1, 1):
                basis_a = frame(geom_a["rays"][ray_a_idx], geom_a["axis"])
                basis_b = frame(geom_b["rays"][ray_b_idx], axis_sign * geom_b["axis"])
                rotation = basis_a @ basis_b.T
                translation = geom_a["position"] - rotation @ geom_b["position"]
                # Сохраняем оценку согласования ВТОРОЙ стороны угла.
                other_a = geom_a["rays"][1 - ray_a_idx]
                other_b = geom_b["rays"][1 - ray_b_idx]
                cosine = float(np.clip(np.dot(other_a, rotation @ other_b), -1., 1.))
                other_ray_error = math.degrees(math.acos(cosine))
                key = tuple(np.round(rotation.flatten(), 8)) + tuple(np.round(translation, 6))
                if key in seen:
                    continue
                seen.add(key)
                poses.append({
                    "rotation_matrix": np.round(rotation, 12).tolist(),
                    "translation": np.round(translation, 9).tolist(),
                    "matched_ray_a": ray_a_idx,
                    "matched_ray_b": ray_b_idx,
                    "profile_axis_b_sign": axis_sign,
                    "second_ray_error_deg": round(other_ray_error, 6),
                    "determinant": round(float(np.linalg.det(rotation)), 9),
                    "status": "pose_hypothesis_unvalidated",
                })
    poses.sort(key=lambda p: p["second_ray_error_deg"])
    return poses[:limit]


def align_all(features_path, pairs_path, output_path, max_poses=4):
    with open(features_path, encoding="utf-8") as handle:
        parts = json.load(handle)
    with open(pairs_path, encoding="utf-8") as handle:
        pairs = json.load(handle)
    if not isinstance(parts, list) or not isinstance(pairs, list):
        raise ValueError("Ожидались JSON-массивы деталей и пар")
    index = {part["file"]: part for part in parts}
    results = []
    hypotheses_count = 0
    pair_count = 0
    for pair in pairs:
        name_a, name_b = pair["part_a"], pair["part_b"]
        result = {
            "part_a": name_a, "part_b": name_b,
            "status": "no_pose_candidates", "alignment_candidates": [],
        }
        if name_a not in index or name_b not in index:
            result["status"] = "missing_part_features"
            results.append(result)
            continue
        for candidate in pair.get("best_candidates", []):
            try:
                ia, ib = candidate["feature_a_index"], candidate["feature_b_index"]
                ga = feature_geometry(index[name_a], ia)
                gb = feature_geometry(index[name_b], ib)
                for pose in calculate_poses(ga, gb, limit=max_poses):
                    result["alignment_candidates"].append({
                        "feature_a_index": ia,
                        "feature_b_index": ib,
                        "angular_error_deg": candidate.get("angular_error_deg"),
                        "side_lengths_relative_error": candidate.get("side_lengths_relative_error"),
                        **pose,
                    })
            except (ValueError, KeyError, IndexError, TypeError, np.linalg.LinAlgError) as error:
                result.setdefault("skipped_candidates", []).append(str(error))
        result["alignment_candidates"].sort(key=lambda p: (
            p["second_ray_error_deg"],
            p["side_lengths_relative_error"] if p["side_lengths_relative_error"] is not None else float("inf"),
        ))
        # Ограничиваем размер выходного файла, сохраняя лучшие гипотезы.
        result["alignment_candidates"] = result["alignment_candidates"][:max_poses]
        if result["alignment_candidates"]:
            result["status"] = "alignment_hypotheses_only"
            hypotheses_count += len(result["alignment_candidates"])
            pair_count += 1
        results.append(result)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, ensure_ascii=False, indent=2)
    print(f"Проверено пар: {len(results)}")
    print(f"Пар с вариантами совмещения: {pair_count}")
    print(f"Сохранено гипотез совмещения: {hypotheses_count}")
    print(f"Результаты: {output_path}")
    print("Внимание: столкновения, допуски и возможность сборки ещё не проверены.")
    return results


def main():
    parser = argparse.ArgumentParser(description="Этап 6: предварительное 3D-совмещение двух CAD-деталей")
    parser.add_argument("--features", default="connection_features.json")
    parser.add_argument("--pairs", default="connection_features_pairs.json")
    parser.add_argument("--output", default="assembly_alignment.json")
    parser.add_argument("--max-poses", type=int, default=4)
    args = parser.parse_args()
    if args.max_poses < 1:
        parser.error("--max-poses должно быть положительным")
    align_all(args.features, args.pairs, args.output, args.max_poses)


if __name__ == "__main__":
    main()
