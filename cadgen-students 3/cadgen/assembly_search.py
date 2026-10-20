
# Этап 8. Автоматический поиск возможных соединений между CAD-деталями.
# Объединяет анализ геометрии, поиск кандидатов, совмещение и проверку сборки.

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"Ожидается JSON-массив: {path}")

    return data


def run_stage(module_name, arguments, project_root):
    command = [
        sys.executable,
        "-m",
        module_name,
        *arguments,
    ]

    print(f"\nЗапуск: {' '.join(command)}", flush=True)

    subprocess.run(
        command,
        cwd=project_root,
        check=True,
    )


def count_candidates_with_clear_path(candidates):
    count = 0

    for candidate in candidates:
        if candidate.get("path_sampled_clear") is True:
            count += 1
            continue

        trials = candidate.get("path_trials", [])

        if isinstance(trials, list) and any(
            isinstance(trial, dict)
            and trial.get("path_sampled_clear") is True
            for trial in trials
        ):
            count += 1

    return count


def build_report(features, matching, alignments, validations):
    matching_by_pair = {
        (entry["part_a"], entry["part_b"]): entry
        for entry in matching
    }

    alignment_by_pair = {
        (entry["part_a"], entry["part_b"]): entry
        for entry in alignments
    }

    results = []
    status_totals = Counter()

    for pair in validations:
        part_a = pair["part_a"]
        part_b = pair["part_b"]

        pair_key = (part_a, part_b)

        matching_info = matching_by_pair.get(pair_key, {})
        alignment_info = alignment_by_pair.get(pair_key, {})

        candidates = pair.get("validation_candidates", [])
        pose_statuses = Counter(
            candidate.get("status", "unknown")
            for candidate in candidates
        )

        clear_paths = count_candidates_with_clear_path(candidates)

        # Подтверждение возможно только при явной проверке
        # посадки и непрерывного пути сборки.
        confirmed = [
            candidate
            for candidate in candidates
            if candidate.get("status") == "confirmed_connection"
            and candidate.get("tolerances_checked") is True
            and candidate.get("assembly_path_checked") is True
            and candidate.get("continuous_path_checked") is True
        ]

        has_contact = any(
            candidate.get("status") in (
                "contact_candidate",
                "planar_contact_candidate",
            )
            or (
                candidate.get("intersection_volume") == 0
                and candidate.get("planar_contact_area", 0) > 0
            )
            for candidate in candidates
        )

        if confirmed:
            result_status = "confirmed_connection"

        elif has_contact:
            result_status = "requires_connector_validation"

        elif candidates and all(
            candidate.get("status") == "collision"
            for candidate in candidates
        ):
            result_status = "all_tested_poses_collide"

        elif not candidates:
            result_status = "no_pose_candidates"

        else:
            result_status = "not_confirmed"

        status_totals[result_status] += 1

        results.append({
            "part_a": part_a,
            "part_b": part_b,
            "status": result_status,
            "cylindrical_matching": matching_info,
            "alignment_candidates_count": len(
                alignment_info.get("alignment_candidates", [])
            ),
            "validated_poses_count": len(candidates),
            "pose_status_counts": dict(pose_statuses),
            "sampled_clear_paths_count": clear_paths,
            "confirmed_poses_count": len(confirmed),
        })

    summary = {
        "parts_analyzed": len(features),
        "pairs_checked": len(results),
        "pairs_with_alignment": sum(
            item["alignment_candidates_count"] > 0
            for item in results
        ),
        "poses_checked": sum(
            item["validated_poses_count"]
            for item in results
        ),
        "preliminary_pairs": status_totals[
            "requires_connector_validation"
        ],
        "confirmed_pairs": status_totals[
            "confirmed_connection"
        ],
        "pair_status_counts": dict(status_totals),
    }

    return {
        "summary": summary,
        "confirmation_note": (
            "Контакт и дискретно свободный путь не доказывают "
            "совместимость соединительных элементов. "
            "Требуется проверка посадки и непрерывной траектории."
        ),
        "pairs": results,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Этап 8: автоматический поиск соединений CAD-деталей"
    )

    parser.add_argument(
        "--folder",
        default="generations/demo/train/0",
        help="Папка со STEP-файлами",
    )

    parser.add_argument(
        "--project-root",
        default=".",
        help="Корневая папка проекта",
    )

    parser.add_argument(
        "--output",
        default="assembly_search.json",
        help="Итоговый JSON-отчёт",
    )

    parser.add_argument(
        "--reuse-files",
        action="store_true",
        help="Использовать существующие JSON без повторного анализа",
    )

    args = parser.parse_args()

    root = Path(args.project_root).resolve()

    files = {
        "features": root / "connection_features.json",
        "matching": root / "connection_matching.json",
        "alignment": root / "assembly_alignment.json",
        "validation": root / "assembly_validation.json",
    }

    if not args.reuse_files:
        folder = Path(args.folder)

        if not folder.is_absolute():
            folder = root / folder

        if not folder.is_dir():
            parser.error(f"Папка с STEP-файлами не найдена: {folder}")

        # Этапы 3–5: распознавание и сопоставление.
        run_stage(
            "cadgen.connection_features",
            [
                str(folder),
                "--output",
                str(files["features"]),
            ],
            root,
        )

        run_stage(
            "cadgen.connection_matching",
            [
                "--features",
                str(files["features"]),
                "--output",
                str(files["matching"]),
            ],
            root,
        )

        # Этап 6: построение гипотез совмещения.
        run_stage(
            "cadgen.assembly_alignment",
            [],
            root,
        )

        # Этап 7: проверка геометрии и пути сборки.
        run_stage(
            "cadgen.assembly_validation",
            [],
            root,
        )

    for filename in files.values():
        if not filename.is_file():
            parser.error(f"Не найден файл: {filename}")

    report = build_report(
        load_json(files["features"]),
        load_json(files["matching"]),
        load_json(files["alignment"]),
        load_json(files["validation"]),
    )

    output_path = Path(args.output)

    if not output_path.is_absolute():
        output_path = root / output_path

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
        )

    summary = report["summary"]

    print("\n========== ЭТАП 8 ==========")
    print(f"Проанализировано деталей: {summary['parts_analyzed']}")
    print(f"Проверено пар: {summary['pairs_checked']}")
    print(f"Пар с совмещениями: {summary['pairs_with_alignment']}")
    print(f"Проверено положений: {summary['poses_checked']}")
    print(f"Предварительных пар: {summary['preliminary_pairs']}")
    print(f"Подтверждённых пар: {summary['confirmed_pairs']}")
    print(f"Результаты сохранены: {output_path}")

    print(
        "\nВнимание: пока не проверены все требования "
        "к посадке соединительных элементов."
    )


if __name__ == "__main__":
    main()
