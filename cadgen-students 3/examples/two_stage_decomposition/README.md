# AIRI: геометрическая декомпозиция 10 моделей

Готовые результаты последнего анализа: **86 компонентов, 75 подтверждены как простые, 11 не распознаны**. Новые модели не генерировались; STL скопированы побайтово из `generations/assemblies/two_stage_final/`.

Нажмите на ссылку STL, чтобы открыть просмотр на GitHub. Номер модели открывает `metadata.json` с классификацией, причинами остановки, геометрическими преобразованиями и отдельным результатом поиска креплений.

- `original.stl` — исходная цельная модель.
- `split_exploded.stl` — все геометрические компоненты в разнесённом положении.
- `split_assembled.stl` — те же компоненты в исходных положениях, без креплений.
- `part_i.stl` — отдельный компонент в локальных координатах; его исходное и разнесённое положения записаны в метаданных.

Полная сборка с креплениями в выполненном поиске не найдена ни для одной из десяти моделей. `split_assembled.stl` показывает только геометрическое восстановление исходника и не означает успешную механическую сборку.

| Модель / метаданные | Компонентов | Простых | Не распознано | Исходник | Разобранный вид | Исходные положения | Отдельные компоненты |
|---|---:|---:|---:|---|---|---|---|
| [1](model_01/metadata.json) | 9 | 8 | 1 | [STL](model_01/original.stl) | [STL](model_01/split_exploded.stl) | [STL](model_01/split_assembled.stl) | [1](model_01/part_1.stl) · [2](model_01/part_2.stl) · [3](model_01/part_3.stl) · [4](model_01/part_4.stl) · [5](model_01/part_5.stl) · [6](model_01/part_6.stl) · [7](model_01/part_7.stl) · [8](model_01/part_8.stl) · [9](model_01/part_9.stl) |
| [2](model_02/metadata.json) | 11 | 8 | 3 | [STL](model_02/original.stl) | [STL](model_02/split_exploded.stl) | [STL](model_02/split_assembled.stl) | [1](model_02/part_1.stl) · [2](model_02/part_2.stl) · [3](model_02/part_3.stl) · [4](model_02/part_4.stl) · [5](model_02/part_5.stl) · [6](model_02/part_6.stl) · [7](model_02/part_7.stl) · [8](model_02/part_8.stl) · [9](model_02/part_9.stl) · [10](model_02/part_10.stl) · [11](model_02/part_11.stl) |
| [3](model_03/metadata.json) | 6 | 6 | 0 | [STL](model_03/original.stl) | [STL](model_03/split_exploded.stl) | [STL](model_03/split_assembled.stl) | [1](model_03/part_1.stl) · [2](model_03/part_2.stl) · [3](model_03/part_3.stl) · [4](model_03/part_4.stl) · [5](model_03/part_5.stl) · [6](model_03/part_6.stl) |
| [4](model_04/metadata.json) | 8 | 7 | 1 | [STL](model_04/original.stl) | [STL](model_04/split_exploded.stl) | [STL](model_04/split_assembled.stl) | [1](model_04/part_1.stl) · [2](model_04/part_2.stl) · [3](model_04/part_3.stl) · [4](model_04/part_4.stl) · [5](model_04/part_5.stl) · [6](model_04/part_6.stl) · [7](model_04/part_7.stl) · [8](model_04/part_8.stl) |
| [5](model_05/metadata.json) | 7 | 6 | 1 | [STL](model_05/original.stl) | [STL](model_05/split_exploded.stl) | [STL](model_05/split_assembled.stl) | [1](model_05/part_1.stl) · [2](model_05/part_2.stl) · [3](model_05/part_3.stl) · [4](model_05/part_4.stl) · [5](model_05/part_5.stl) · [6](model_05/part_6.stl) · [7](model_05/part_7.stl) |
| [6](model_06/metadata.json) | 9 | 8 | 1 | [STL](model_06/original.stl) | [STL](model_06/split_exploded.stl) | [STL](model_06/split_assembled.stl) | [1](model_06/part_1.stl) · [2](model_06/part_2.stl) · [3](model_06/part_3.stl) · [4](model_06/part_4.stl) · [5](model_06/part_5.stl) · [6](model_06/part_6.stl) · [7](model_06/part_7.stl) · [8](model_06/part_8.stl) · [9](model_06/part_9.stl) |
| [7](model_07/metadata.json) | 6 | 5 | 1 | [STL](model_07/original.stl) | [STL](model_07/split_exploded.stl) | [STL](model_07/split_assembled.stl) | [1](model_07/part_1.stl) · [2](model_07/part_2.stl) · [3](model_07/part_3.stl) · [4](model_07/part_4.stl) · [5](model_07/part_5.stl) · [6](model_07/part_6.stl) |
| [8](model_08/metadata.json) | 7 | 6 | 1 | [STL](model_08/original.stl) | [STL](model_08/split_exploded.stl) | [STL](model_08/split_assembled.stl) | [1](model_08/part_1.stl) · [2](model_08/part_2.stl) · [3](model_08/part_3.stl) · [4](model_08/part_4.stl) · [5](model_08/part_5.stl) · [6](model_08/part_6.stl) · [7](model_08/part_7.stl) |
| [9](model_09/metadata.json) | 7 | 6 | 1 | [STL](model_09/original.stl) | [STL](model_09/split_exploded.stl) | [STL](model_09/split_assembled.stl) | [1](model_09/part_1.stl) · [2](model_09/part_2.stl) · [3](model_09/part_3.stl) · [4](model_09/part_4.stl) · [5](model_09/part_5.stl) · [6](model_09/part_6.stl) · [7](model_09/part_7.stl) |
| [10](model_10/metadata.json) | 16 | 15 | 1 | [STL](model_10/original.stl) | [STL](model_10/split_exploded.stl) | [STL](model_10/split_assembled.stl) | [1](model_10/part_1.stl) · [2](model_10/part_2.stl) · [3](model_10/part_3.stl) · [4](model_10/part_4.stl) · [5](model_10/part_5.stl) · [6](model_10/part_6.stl) · [7](model_10/part_7.stl) · [8](model_10/part_8.stl) · [9](model_10/part_9.stl) · [10](model_10/part_10.stl) · [11](model_10/part_11.stl) · [12](model_10/part_12.stl) · [13](model_10/part_13.stl) · [14](model_10/part_14.stl) · [15](model_10/part_15.stl) · [16](model_10/part_16.stl) |

У модели №4 исчерпан бюджет поиска разрезов; заключительная проверка подтвердила простоту 7 из 8 частей. Нераспознанные компоненты сохранены полностью. Ограничения поиска и причины отказа сборки приведены в метаданных.

[Описание алгоритма и подробный разбор моделей №1, №2 и №7](../../TWO_STAGE_DECOMPOSITION.md) · [Предыдущие примеры сборок](../assemblies/README.md).
