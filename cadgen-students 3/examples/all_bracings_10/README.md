# All-bracings: 10 моделей

Эксперимент all_bracings_integration_20261113_01 (дата из имени запуска: 2026-11-13).
Скопированы существующие результаты: 10 моделей, 6 успешных геометрических восстановлений, 4 отказа.
Глобальный порядок установки и непрерывные траектории не проверялись.

Папки model_01–model_10 сохраняют исходную внутреннюю структуру, имена и метаданные. Исходные сводные отчёты находятся в reports/. manifest.json содержит пути относительно этой папки.

Для готовой сборки открывайте assembly.step или assembly.stl по ссылкам ниже. exploded.step и parts_exploded.stl содержат разнесённые виды. geometry/ содержит результат декомпозиции; все имеющиеся диагностические материалы отказных моделей также скопированы.

| Модель | Seed | Статус из исходного отчёта | Готовая сборка |
|---|---:|---|---|
| model_01 | 42 | decomposition: original: expected one valid positive-volume solid; source_valid=True, solids=2 | Нет: см. диагностику модели |
| model_02 | 17 | decomposition: original: expected one valid positive-volume solid; source_valid=True, solids=2 | Нет: см. диагностику модели |
| model_03 | 73 | decomposition: original: expected one valid positive-volume solid; source_valid=True, solids=2 | Нет: см. диагностику модели |
| model_04 | 101 | geometry_verified; STEP/STL exported | [STEP](model_04/assembly_0001_slot_0001_attempt_01/assembly/assembly.step) / [STL](model_04/assembly_0001_slot_0001_attempt_01/assembly/assembly.stl) |
| model_05 | 123 | geometry_verified; STEP/STL exported | [STEP](model_05/assembly_0001_slot_0001_attempt_01/assembly/assembly.step) / [STL](model_05/assembly_0001_slot_0001_attempt_01/assembly/assembly.stl) |
| model_06 | 202 | geometry_verified; STEP/STL exported | [STEP](model_06/assembly_0001_slot_0001_attempt_01/assembly/assembly.step) / [STL](model_06/assembly_0001_slot_0001_attempt_01/assembly/assembly.stl) |
| model_07 | 314 | geometry_verified; STEP/STL exported | [STEP](model_07/assembly_0001_slot_0001_attempt_01/assembly/assembly.step) / [STL](model_07/assembly_0001_slot_0001_attempt_01/assembly/assembly.stl) |
| model_08 | 515 | geometry_verified; STEP/STL exported | [STEP](model_08/assembly_0001_slot_0001_attempt_01/assembly/assembly.step) / [STL](model_08/assembly_0001_slot_0001_attempt_01/assembly/assembly.stl) |
| model_09 | 616 | assembly: No validated complete assembly of the fixed constituents within the search; technical_limit_reached, search_states=256 | Нет: см. диагностику модели |
| model_10 | 717 | geometry_verified; STEP/STL exported | [STEP](model_10/assembly_0001_slot_0001_attempt_01/assembly/assembly.step) / [STL](model_10/assembly_0001_slot_0001_attempt_01/assembly/assembly.stl) |