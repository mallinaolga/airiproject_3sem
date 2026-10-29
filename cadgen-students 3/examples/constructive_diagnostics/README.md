# Все 10 моделей: конструктивное разбиение и диагностика креплений

Сохранены **все 69 геометрических составляющих**, включая неуспешные модели. До креплений: 51 составляющая распознана простой, у 18 простота не подтверждена. Новые исходные CADGen-модели не создавались, алгоритмы и разбиение не менялись.

- **Полностью успешные:** №3, №4, №8, №10 — сохранён и проверен полный экспорт сборки.
- **Частично проверенные:** №6 и №9 — порядок в памяти найден, проверка STEP не прошла; это не готовые сборки.
- **Полная сборка не найдена:** №1, №2, №5, №7 — локально корректные пары доступны отдельно, но граф соединений несвязен.

[Проблемные соединения: все пары, размеры и причины](PROBLEM_JOINTS.md) · [Классификация 69 деталей](DECOMPOSITION.md) · [Ошибки STEP](STEP_FAILURES.md)

| Модель | Составляющих | Статус | Исходник | Разнесённое разбиение | Разбиение в исходных положениях | Детали и результаты |
|---|---:|---|---|---|---|---|
| model_01 | 8 | Полная сборка не найдена | [original.stl](model_01/original.stl) | [split_exploded.stl](model_01/split_exploded.stl) | [split_assembled.stl](model_01/split_assembled.stl) | [Все детали](model_01/README.md) |
| model_02 | 7 | Полная сборка не найдена | [original.stl](model_02/original.stl) | [split_exploded.stl](model_02/split_exploded.stl) | [split_assembled.stl](model_02/split_assembled.stl) | [Все детали](model_02/README.md) |
| model_03 | 7 | Полностью успешная | [original.stl](model_03/original.stl) | [split_exploded.stl](model_03/split_exploded.stl) | [split_assembled.stl](model_03/split_assembled.stl) | [Все детали](model_03/README.md) |
| model_04 | 9 | Полностью успешная | [original.stl](model_04/original.stl) | [split_exploded.stl](model_04/split_exploded.stl) | [split_assembled.stl](model_04/split_assembled.stl) | [Все детали](model_04/README.md) |
| model_05 | 6 | Полная сборка не найдена | [original.stl](model_05/original.stl) | [split_exploded.stl](model_05/split_exploded.stl) | [split_assembled.stl](model_05/split_assembled.stl) | [Все детали](model_05/README.md) |
| model_06 | 7 | Частично проверенная: не прошёл STEP | [original.stl](model_06/original.stl) | [split_exploded.stl](model_06/split_exploded.stl) | [split_assembled.stl](model_06/split_assembled.stl) | [Все детали](model_06/README.md) |
| model_07 | 5 | Полная сборка не найдена | [original.stl](model_07/original.stl) | [split_exploded.stl](model_07/split_exploded.stl) | [split_assembled.stl](model_07/split_assembled.stl) | [Все детали](model_07/README.md) |
| model_08 | 6 | Полностью успешная | [original.stl](model_08/original.stl) | [split_exploded.stl](model_08/split_exploded.stl) | [split_assembled.stl](model_08/split_assembled.stl) | [Все детали](model_08/README.md) |
| model_09 | 6 | Частично проверенная: не прошёл STEP | [original.stl](model_09/original.stl) | [split_exploded.stl](model_09/split_exploded.stl) | [split_assembled.stl](model_09/split_assembled.stl) | [Все детали](model_09/README.md) |
| model_10 | 8 | Полностью успешная | [original.stl](model_10/original.stl) | [split_exploded.stl](model_10/split_exploded.stl) | [split_assembled.stl](model_10/split_assembled.stl) | [Все детали](model_10/README.md) |

STL отдельных деталей центрированы для просмотра; исходные положения и преобразования сохранены в метаданных. `split_assembled.stl` содержит все геометрические части без креплений. Кандидаты пар разделяют статическую геометрию и проверку направления вставки. Геометрически построенный паз с неудачным путём явно помечен `static_only`.

В терминологии публикации используются сквозные болты с гайкой и болты в глухих отверстиях. Имена полей публикации нормализованы; внутренние алгоритмы и идентификаторы исходного кода не изменены. Резьба и прочность не моделировались. Траектории дискретные.

SHA-256 копированных файлов и исходного кода находятся в [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json).

[Проверка опубликованных файлов](PUBLICATION_VALIDATION.json) · [Ранее пройденные 105 тестов неизменённых алгоритмов](baseline_test_summary.json).
