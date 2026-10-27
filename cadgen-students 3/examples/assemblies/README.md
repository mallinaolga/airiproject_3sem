# AIRI: результаты автоматической декомпозиции CADGen

Реальные результаты алгоритма; не контрольные синтетические модели. Пути проверены дискретно, резьба и механическое удержание не моделируются.

| Модель | Seed | Частей | Разрезов | Пазов/выступов | Болтов/гаек | Соединения | Остановка | Проверка | Представления |
|---|---:|---:|---:|---:|---|---|---|---|---|
| [1](model_01/metadata.json) | 4759556275248130055 | 4 | 3 | 3/3 | 0/0 | {'groove': 3} | {'no_meaningful_splits': 2, 'no_feasible_connections': 2} | валидна, полный порядок найден | [исходник](model_01/original.stl) · [разрезы](model_01/split_exploded.stl) · [крепления](model_01/parts_exploded.stl) · [сборка](model_01/assembly.stl) |
| [2](model_02/metadata.json) | 2366738684808547986 | 6 | 5 | 5/5 | 0/0 | {'groove': 5} | {'no_meaningful_splits': 2, 'no_feasible_connections': 4} | валидна, полный порядок найден | [исходник](model_02/original.stl) · [разрезы](model_02/split_exploded.stl) · [крепления](model_02/parts_exploded.stl) · [сборка](model_02/assembly.stl) |
| [3](model_03/metadata.json) | 3365915334631980501 | 5 | 4 | 4/4 | 0/0 | {'groove': 4} | {'no_meaningful_splits': 4, 'no_feasible_connections': 1} | валидна, полный порядок найден | [исходник](model_03/original.stl) · [разрезы](model_03/split_exploded.stl) · [крепления](model_03/parts_exploded.stl) · [сборка](model_03/assembly.stl) |
| [4](model_04/metadata.json) | 8697456928445524537 | 5 | 4 | 4/4 | 0/0 | {'groove': 4} | {'no_meaningful_splits': 4, 'no_feasible_connections': 1} | валидна, полный порядок найден | [исходник](model_04/original.stl) · [разрезы](model_04/split_exploded.stl) · [крепления](model_04/parts_exploded.stl) · [сборка](model_04/assembly.stl) |
| [5](model_05/metadata.json) | 6408026581464355185 | 5 | 4 | 4/4 | 0/0 | {'groove': 4} | {'no_meaningful_splits': 3, 'no_feasible_connections': 2} | валидна, полный порядок найден | [исходник](model_05/original.stl) · [разрезы](model_05/split_exploded.stl) · [крепления](model_05/parts_exploded.stl) · [сборка](model_05/assembly.stl) |
| [6](model_06/metadata.json) | 3498244309149206551 | 2 | 1 | 1/1 | 0/0 | {'groove': 1} | {'no_meaningful_splits': 1, 'no_feasible_connections': 1} | валидна, полный порядок найден | [исходник](model_06/original.stl) · [разрезы](model_06/split_exploded.stl) · [крепления](model_06/parts_exploded.stl) · [сборка](model_06/assembly.stl) |
| [7](model_07/metadata.json) | 5018634549418312103 | 4 | 3 | 3/3 | 0/0 | {'groove': 3} | {'no_meaningful_splits': 1, 'no_feasible_connections': 3} | валидна, полный порядок найден | [исходник](model_07/original.stl) · [разрезы](model_07/split_exploded.stl) · [крепления](model_07/parts_exploded.stl) · [сборка](model_07/assembly.stl) |
| [8](model_08/metadata.json) | 3693542949846216359 | 4 | 3 | 3/3 | 0/0 | {'groove': 3} | {'no_meaningful_splits': 2, 'no_feasible_connections': 2} | валидна, полный порядок найден | [исходник](model_08/original.stl) · [разрезы](model_08/split_exploded.stl) · [крепления](model_08/parts_exploded.stl) · [сборка](model_08/assembly.stl) |
| [9](model_09/metadata.json) | 2994180625895095827 | 5 | 4 | 4/4 | 0/0 | {'groove': 4} | {'no_meaningful_splits': 2, 'no_feasible_connections': 3} | валидна, полный порядок найден | [исходник](model_09/original.stl) · [разрезы](model_09/split_exploded.stl) · [крепления](model_09/parts_exploded.stl) · [сборка](model_09/assembly.stl) |
| [10](model_10/metadata.json) | 9178489342659831066 | 4 | 3 | 3/3 | 0/0 | {'groove': 3} | {'no_meaningful_splits': 3, 'no_feasible_connections': 1} | валидна, полный порядок найден | [исходник](model_10/original.stl) · [разрезы](model_10/split_exploded.stl) · [крепления](model_10/parts_exploded.stl) · [сборка](model_10/assembly.stl) |

Seed серии: `42`. Успешных сборок: 10/10; отклонено исходников: 11.

Декомпозиция ограничена исследованным семейством сечений. `technical_limit_reached` означает вычислительную остановку, а не отсутствие целесообразных разрезов.

Число частей — результат геометрии и проверок, целевой диапазон не задавался.

Независимый контроль всех файлов: [validation.json](validation.json). Подробный отчёт: [AUTO_EXPERIMENT.md](../../AUTO_EXPERIMENT.md).
