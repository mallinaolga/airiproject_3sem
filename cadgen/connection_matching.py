# Сопоставление потенциальных цилиндрических соединений по геометрии и зазорам.
# Результаты — кандидаты, а не подтверждённые соединения.

import argparse
import json
import math
from pathlib import Path


def _finite_positive(value):
    try:
        value = float(value)
        return value if math.isfinite(value) and value > 0 else None
    except (TypeError, ValueError):
        return None


def match_cylinder_pair(face_a, face_b, min_clearance, max_clearance,
                        min_coverage=0.95):
    """Сравнение локальных цилиндрических граней без привязки к осям XYZ.

    Для посадки необходимо установить, что каждая грань является полной
    доступной поверхностью, что тела можно расположить и собрать. Здесь
    проверяются только тип, диаметр, оценка полноты и зазор.
    """
    roles = {face_a.get("role"), face_b.get("role")}
    if roles != {"inner_cylinder", "outer_cylinder"}:
        return None
    hole = face_a if face_a["role"] == "inner_cylinder" else face_b
    pin = face_b if hole is face_a else face_a
    hole_radius = _finite_positive(hole.get("radius"))
    pin_radius = _finite_positive(pin.get("radius"))
    if hole_radius is None or pin_radius is None:
        return None

    # По оценке покрытия отсеиваем явные фрагменты окружности.
    # Значение >1 возможно на сложной грани: не считать его доказательством полноты.
    for face in (hole, pin):
        coverage = face.get("circumferential_coverage_estimate")
        if coverage is None or not math.isfinite(float(coverage)):
            return None
        if not (min_coverage <= float(coverage) <= 1.05):
            return None

    diametral_clearance = 2.0 * (hole_radius - pin_radius)
    if not (min_clearance <= diametral_clearance <= max_clearance):
        return None

    length_hole = _finite_positive(hole.get("axial_length"))
    length_pin = _finite_positive(pin.get("axial_length"))
    if length_hole is None or length_pin is None:
        return None

    return {
        "feature_a_face_id": face_a.get("face_id"),
        "feature_b_face_id": face_b.get("face_id"),
        "hole_in_part": "a" if hole is face_a else "b",
        "pin_in_part": "a" if pin is face_a else "b",
        "hole_diameter": 2.0 * hole_radius,
        "pin_diameter": 2.0 * pin_radius,
        "diametral_clearance": round(diametral_clearance, 9),
        "hole_axial_length": length_hole,
        "pin_axial_length": length_pin,
        "potential_axial_engagement": min(length_hole, length_pin),
        "status": "cylindrical_geometry_candidate_only",
    }


def match_parts(data, min_clearance=0.0, max_clearance=0.2,
                min_coverage=0.95):
    """Сравнивает все пары успешно проанализированных деталей."""
    if min_clearance < 0 or max_clearance < min_clearance:
        raise ValueError("Неверный диапазон диаметрального зазора")
    if not 0 < min_coverage <= 1:
        raise ValueError("min_coverage должен быть от 0 (исключительно) до 1")

    pairs = []
    for i, part_a in enumerate(data):
        for part_b in data[i + 1:]:
            cylinders_a = part_a.get("features", {}).get("cylindrical", [])
            cylinders_b = part_b.get("features", {}).get("cylindrical", [])
            matches = []
            for a in cylinders_a:
                for b in cylinders_b:
                    candidate = match_cylinder_pair(
                        a, b, min_clearance, max_clearance, min_coverage
                    )
                    if candidate is not None:
                        matches.append(candidate)
            matches.sort(key=lambda m: (m["diametral_clearance"],
                                        -m["potential_axial_engagement"]))
            pairs.append({
                "part_a": part_a["file"],
                "part_b": part_b["file"],
                "cylindrical_candidates": matches,
                "status": ("cylindrical_candidates_only" if matches
                           else "no_cylindrical_candidates"),
            })
    return pairs


def main():
    parser = argparse.ArgumentParser(description="Поиск цилиндрических пар штифт–отверстие")
    parser.add_argument("--features", default="connection_features.json")
    parser.add_argument("--output", default="connection_matching.json")
    parser.add_argument("--min-clearance", type=float, default=0.0,
                        help="Минимальный диаметральный зазор (в единицах STEP)")
    parser.add_argument("--max-clearance", type=float, default=0.2,
                        help="Максимальный диаметральный зазор (в единицах STEP)")
    parser.add_argument("--min-coverage", type=float, default=0.95,
                        help="Минимальная доля полного цилиндра, оценочно")
    args = parser.parse_args()
    with open(args.features, encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, list):
        parser.error("Ожидается JSON-массив деталей")
    try:
        result = match_parts(data, args.min_clearance, args.max_clearance,
                             args.min_coverage)
    except ValueError as exc:
        parser.error(str(exc))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Пар проверено: {len(result)}")
    print(f"Пар с цилиндрическими кандидатами: {sum(bool(p['cylindrical_candidates']) for p in result)}")
    print(f"Всего кандидатов: {sum(len(p['cylindrical_candidates']) for p in result)}")
    print(f"Результаты: {out}")
    print("Внимание: посадка, пространственное совмещение и сборочный путь не проверены.")


if __name__ == "__main__":
    main()
