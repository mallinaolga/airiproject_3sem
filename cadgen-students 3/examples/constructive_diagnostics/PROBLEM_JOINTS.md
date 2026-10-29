# Причины отказов по соседним парам

Здесь нет нового глобального решения и нет исправлений алгоритма. Все соседние пары повторно проверены существующим ограниченным локальным поиском на сохранённых компонентах. Включены также касания границ без подтверждённой общей площадки.

Категории раздельны: не построен паз; не построен болт; не прошла статическая геометрия; нет проверенного направления пары; конфликт креплений; нет полного порядка; лимит. Первые четыре определяются по стадии фактического отказа, остальные — только по сохранённой глобальной диагностике.

Локально допустимые соединения не означают готовую сборку. Для №1, №2, №5, №7 глобальная проверка остановилась до перебора комбинаций из-за отсутствующего ребра к отдельной составляющей. Поэтому корректные пазы на других парах не объявлены конфликтующими или недоступными без проверки.

## Конкретные разрывы графа у №1, №2, №5 и №7

- **№1, part_5 ↔ part_6:** две цилиндрические контактные грани R25 мм, осевая протяжённость 23 мм, суммарная площадь 68.82927 мм². Планарных площадок нет, поэтому шесть плоских профилей здесь не вызывались. Осевая посадка не проходит через материал приёмника. Две попытки нормальной цилиндрической бобышки отклонены: нет бокового материала вокруг гнезда либо массивной опоры выступа. [Пара, размеры посадок и отказы](model_01/joint_diagnostics/part_5__part_6/README.md).
- **№2, part_1 ↔ part_5:** площадь 0.4188884 мм². Есть цилиндрические следы длиной 0.0005 мм и плоская площадка примерно 2 × 0.2097594 мм. Площадка отклонена общим предварительным порогом 0.3 мм, до подбора пазов и обычных болтов. Попытка цилиндрической посадки с поперечным болтом дошла до расчёта стержня **64.21 мм**, что больше разрешённых 50 мм. [Полная запись](model_02/joint_diagnostics/part_1__part_5/README.md).
- **№5, part_1 ↔ part_4:** площадь 1778.329 мм²; 70 попыток, **18 статически допустимых конструкций**, но ни одна не прошла проверку направления пары. У остальных вариантов не хватало материала опоры/стенок или срабатывал минимальный размер. [Геометрия без успешного пути и все размеры](model_05/joint_diagnostics/part_1__part_4/README.md). **part_4 ↔ part_6:** площадь 40.12461 мм²; 68 попыток, **50 статически допустимых**, ни одной с успешным путём. Например, при ходе 3.903577 мм пересечение составляет 0.1460394 мм³. Это отказ установки, а не отсутствие построенного паза. [Посмотреть эту пару](model_05/joint_diagnostics/part_4__part_6/README.md).
- **№7, part_1 ↔ part_4:** площадь 1.280132 мм²; грани примерно 7.224458 × 0.1788826 мм и две площадки 0.1916941 × 0.0005 мм. Все отсекаются до вызова построителей порогом 0.3 мм. Ось цилиндра также не попадает в материал приёмника. [Пара и предварительные отказы](model_07/joint_diagnostics/part_1__part_4/README.md).

**О названии фильтра:** сообщение исходного кода `service-overlap ribbon` применяется к любой площадке с минимальным габаритом меньше `max(20 × 0.0005, 3 × 0.1) = 0.3 мм`. Поэтому площадки шириной 0.1789 и 0.2098 мм тоже получают эту метку: она сама по себе не доказывает, что вся площадка — служебное перекрытие CADGen. Это установленное ограничение текущего фильтра; здесь оно не исправлялось.

## model_01 — Полная сборка не найдена

Недостижимые в исходном графе детали: ['part_6']. Сохранённых глобальных отказов: 0.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_01/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 340 | 68 | 55 | 55 | 12 | [Размеры, позиции и все отказы](model_01/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_4](model_01/joint_diagnostics/part_1__part_4/pair_exploded.stl) | 340 | 68 | 55 | 55 | 12 | [Размеры, позиции и все отказы](model_01/joint_diagnostics/part_1__part_4/README.md) |
| [part_2 ↔ part_3](model_01/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 340 | 68 | 64 | 64 | 12 | [Размеры, позиции и все отказы](model_01/joint_diagnostics/part_2__part_3/README.md) |
| [part_4 ↔ part_5](model_01/joint_diagnostics/part_4__part_5/pair_exploded.stl) | 1189.72 | 70 | 20 | 16 | 12 | [Размеры, позиции и все отказы](model_01/joint_diagnostics/part_4__part_5/README.md) |
| [part_4 ↔ part_7](model_01/joint_diagnostics/part_4__part_7/pair_exploded.stl) | 7168.45 | 70 | 34 | 30 | 12 | [Размеры, позиции и все отказы](model_01/joint_diagnostics/part_4__part_7/README.md) |
| [part_5 ↔ part_6](model_01/joint_diagnostics/part_5__part_6/pair_exploded.stl) | 68.82927 | 2 | 0 | 0 | 0 | [Размеры, позиции и все отказы](model_01/joint_diagnostics/part_5__part_6/README.md) |
| [part_7 ↔ part_8](model_01/joint_diagnostics/part_7__part_8/pair_exploded.stl) | 10936.07 | 68 | 43 | 35 | 12 | [Размеры, позиции и все отказы](model_01/joint_diagnostics/part_7__part_8/README.md) |

## model_02 — Полная сборка не найдена

Недостижимые в исходном графе детали: ['part_5']. Сохранённых глобальных отказов: 0.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_02/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 380.1327 | 68 | 35 | 35 | 12 | [Размеры, позиции и все отказы](model_02/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_4](model_02/joint_diagnostics/part_1__part_4/pair_exploded.stl) | 333.5884 | 70 | 1 | 1 | 1 | [Размеры, позиции и все отказы](model_02/joint_diagnostics/part_1__part_4/README.md) |
| [part_1 ↔ part_5](model_02/joint_diagnostics/part_1__part_5/pair_exploded.stl) | 0.4188884 | 1 | 0 | 0 | 0 | [Размеры, позиции и все отказы](model_02/joint_diagnostics/part_1__part_5/README.md) |
| [part_1 ↔ part_7](model_02/joint_diagnostics/part_1__part_7/pair_exploded.stl) | 697.7052 | 66 | 20 | 13 | 12 | [Размеры, позиции и все отказы](model_02/joint_diagnostics/part_1__part_7/README.md) |
| [part_2 ↔ part_3](model_02/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 380.1327 | 68 | 35 | 35 | 12 | [Размеры, позиции и все отказы](model_02/joint_diagnostics/part_2__part_3/README.md) |
| [part_4 ↔ part_6](model_02/joint_diagnostics/part_4__part_6/pair_exploded.stl) | 40 | 68 | 53 | 53 | 12 | [Размеры, позиции и все отказы](model_02/joint_diagnostics/part_4__part_6/README.md) |
| [part_4 ↔ part_7](model_02/joint_diagnostics/part_4__part_7/pair_exploded.stl) | 3345.68 | 70 | 49 | 49 | 12 | [Размеры, позиции и все отказы](model_02/joint_diagnostics/part_4__part_7/README.md) |
| [part_6 ↔ part_7](model_02/joint_diagnostics/part_6__part_7/pair_exploded.stl) | 1551.986 | 68 | 52 | 12 | 12 | [Размеры, позиции и все отказы](model_02/joint_diagnostics/part_6__part_7/README.md) |

## model_03 — Полностью успешная

Недостижимые в исходном графе детали: []. Сохранённых глобальных отказов: 0.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_03/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 494 | 68 | 51 | 51 | 12 | [Размеры, позиции и все отказы](model_03/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_4](model_03/joint_diagnostics/part_1__part_4/pair_exploded.stl) | 897.981 | 68 | 60 | 60 | 12 | [Размеры, позиции и все отказы](model_03/joint_diagnostics/part_1__part_4/README.md) |
| [part_1 ↔ part_6](model_03/joint_diagnostics/part_1__part_6/pair_exploded.stl) | 1243.972 | 68 | 48 | 8 | 8 | [Размеры, позиции и все отказы](model_03/joint_diagnostics/part_1__part_6/README.md) |
| [part_2 ↔ part_3](model_03/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 494 | 68 | 51 | 51 | 12 | [Размеры, позиции и все отказы](model_03/joint_diagnostics/part_2__part_3/README.md) |
| [part_2 ↔ part_5](model_03/joint_diagnostics/part_2__part_5/pair_exploded.stl) | 24.01 | 68 | 57 | 49 | 12 | [Размеры, позиции и все отказы](model_03/joint_diagnostics/part_2__part_5/README.md) |
| [part_4 ↔ part_7](model_03/joint_diagnostics/part_4__part_7/pair_exploded.stl) | 248.2294 | 68 | 57 | 57 | 12 | [Размеры, позиции и все отказы](model_03/joint_diagnostics/part_4__part_7/README.md) |

## model_04 — Полностью успешная

Недостижимые в исходном графе детали: []. Сохранённых глобальных отказов: 0.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_04/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 312 | 68 | 51 | 51 | 12 | [Размеры, позиции и все отказы](model_04/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_9](model_04/joint_diagnostics/part_1__part_9/pair_exploded.stl) | 287.7795 | 68 | 54 | 54 | 12 | [Размеры, позиции и все отказы](model_04/joint_diagnostics/part_1__part_9/README.md) |
| [part_2 ↔ part_3](model_04/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 312 | 68 | 51 | 51 | 12 | [Размеры, позиции и все отказы](model_04/joint_diagnostics/part_2__part_3/README.md) |
| [part_2 ↔ part_4](model_04/joint_diagnostics/part_2__part_4/pair_exploded.stl) | 12.008 | 68 | 64 | 52 | 12 | [Размеры, позиции и все отказы](model_04/joint_diagnostics/part_2__part_4/README.md) |
| [part_2 ↔ part_7](model_04/joint_diagnostics/part_2__part_7/pair_exploded.stl) | 1.569796 | 56 | 16 | 16 | 12 | [Размеры, позиции и все отказы](model_04/joint_diagnostics/part_2__part_7/README.md) |
| [part_3 ↔ part_5](model_04/joint_diagnostics/part_3__part_5/pair_exploded.stl) | 884.153 | 70 | 45 | 37 | 12 | [Размеры, позиции и все отказы](model_04/joint_diagnostics/part_3__part_5/README.md) |
| [part_3 ↔ part_6](model_04/joint_diagnostics/part_3__part_6/pair_exploded.stl) | 3.144734 | 70 | 39 | 33 | 12 | [Размеры, позиции и все отказы](model_04/joint_diagnostics/part_3__part_6/README.md) |
| [part_3 ↔ part_7](model_04/joint_diagnostics/part_3__part_7/pair_exploded.stl) | 21.99915 | 70 | 16 | 0 | 0 | [Размеры, позиции и все отказы](model_04/joint_diagnostics/part_3__part_7/README.md) |
| [part_3 ↔ part_8](model_04/joint_diagnostics/part_3__part_8/pair_exploded.stl) | 252.1284 | 68 | 23 | 19 | 12 | [Размеры, позиции и все отказы](model_04/joint_diagnostics/part_3__part_8/README.md) |

## model_05 — Полная сборка не найдена

Недостижимые в исходном графе детали: ['part_4']. Сохранённых глобальных отказов: 0.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_05/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 858 | 68 | 51 | 51 | 12 | [Размеры, позиции и все отказы](model_05/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_4](model_05/joint_diagnostics/part_1__part_4/pair_exploded.stl) | 1778.329 | 70 | 18 | 0 | 0 | [Размеры, позиции и все отказы](model_05/joint_diagnostics/part_1__part_4/README.md) |
| [part_1 ↔ part_6](model_05/joint_diagnostics/part_1__part_6/pair_exploded.stl) | 831.0355 | 68 | 55 | 55 | 12 | [Размеры, позиции и все отказы](model_05/joint_diagnostics/part_1__part_6/README.md) |
| [part_2 ↔ part_3](model_05/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 858 | 68 | 57 | 57 | 12 | [Размеры, позиции и все отказы](model_05/joint_diagnostics/part_2__part_3/README.md) |
| [part_3 ↔ part_5](model_05/joint_diagnostics/part_3__part_5/pair_exploded.stl) | 4 | 68 | 60 | 60 | 12 | [Размеры, позиции и все отказы](model_05/joint_diagnostics/part_3__part_5/README.md) |
| [part_4 ↔ part_6](model_05/joint_diagnostics/part_4__part_6/pair_exploded.stl) | 40.12461 | 68 | 50 | 0 | 0 | [Размеры, позиции и все отказы](model_05/joint_diagnostics/part_4__part_6/README.md) |

## model_06 — Частично проверенная: не прошёл STEP

Недостижимые в исходном графе детали: []. Сохранённых глобальных отказов: 0.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_06/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 1840 | 68 | 54 | 54 | 12 | [Размеры, позиции и все отказы](model_06/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_7](model_06/joint_diagnostics/part_1__part_7/pair_exploded.stl) | 4.004 | 68 | 54 | 46 | 12 | [Размеры, позиции и все отказы](model_06/joint_diagnostics/part_1__part_7/README.md) |
| [part_2 ↔ part_3](model_06/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 1840 | 68 | 51 | 51 | 12 | [Размеры, позиции и все отказы](model_06/joint_diagnostics/part_2__part_3/README.md) |
| [part_2 ↔ part_6](model_06/joint_diagnostics/part_2__part_6/pair_exploded.stl) | 2344.279 | 70 | 49 | 49 | 12 | [Размеры, позиции и все отказы](model_06/joint_diagnostics/part_2__part_6/README.md) |
| [part_3 ↔ part_4](model_06/joint_diagnostics/part_3__part_4/pair_exploded.stl) | 13.78802 | 68 | 3 | 3 | 3 | [Размеры, позиции и все отказы](model_06/joint_diagnostics/part_3__part_4/README.md) |
| [part_3 ↔ part_5](model_06/joint_diagnostics/part_3__part_5/pair_exploded.stl) | 3.144734 | 70 | 46 | 38 | 12 | [Размеры, позиции и все отказы](model_06/joint_diagnostics/part_3__part_5/README.md) |

## model_07 — Полная сборка не найдена

Недостижимые в исходном графе детали: ['part_4']. Сохранённых глобальных отказов: 0.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_07/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 201.0619 | 68 | 43 | 43 | 12 | [Размеры, позиции и все отказы](model_07/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_4](model_07/joint_diagnostics/part_1__part_4/pair_exploded.stl) | 1.280132 | 0 | 0 | 0 | 0 | [Размеры, позиции и все отказы](model_07/joint_diagnostics/part_1__part_4/README.md) |
| [part_1 ↔ part_5](model_07/joint_diagnostics/part_1__part_5/pair_exploded.stl) | 2.504469 | 2 | 1 | 1 | 1 | [Размеры, позиции и все отказы](model_07/joint_diagnostics/part_1__part_5/README.md) |
| [part_2 ↔ part_3](model_07/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 201.0619 | 68 | 39 | 39 | 12 | [Размеры, позиции и все отказы](model_07/joint_diagnostics/part_2__part_3/README.md) |
| [part_2 ↔ part_5](model_07/joint_diagnostics/part_2__part_5/pair_exploded.stl) | 8.586605 | 2 | 1 | 1 | 1 | [Размеры, позиции и все отказы](model_07/joint_diagnostics/part_2__part_5/README.md) |
| [part_3 ↔ part_5](model_07/joint_diagnostics/part_3__part_5/pair_exploded.stl) | 71.1078 | 70 | 29 | 1 | 1 | [Размеры, позиции и все отказы](model_07/joint_diagnostics/part_3__part_5/README.md) |

## model_08 — Полностью успешная

Недостижимые в исходном графе детали: []. Сохранённых глобальных отказов: 8.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_08/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 254.469 | 68 | 47 | 47 | 12 | [Размеры, позиции и все отказы](model_08/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_4](model_08/joint_diagnostics/part_1__part_4/pair_exploded.stl) | 311.0177 | 70 | 43 | 35 | 12 | [Размеры, позиции и все отказы](model_08/joint_diagnostics/part_1__part_4/README.md) |
| [part_2 ↔ part_3](model_08/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 254.469 | 68 | 36 | 36 | 12 | [Размеры, позиции и все отказы](model_08/joint_diagnostics/part_2__part_3/README.md) |
| [part_3 ↔ part_4](model_08/joint_diagnostics/part_3__part_4/pair_exploded.stl) | 361.3271 | 70 | 1 | 1 | 1 | [Размеры, позиции и все отказы](model_08/joint_diagnostics/part_3__part_4/README.md) |
| [part_4 ↔ part_5](model_08/joint_diagnostics/part_4__part_5/pair_exploded.stl) | 8120.065 | 68 | 42 | 41 | 12 | [Размеры, позиции и все отказы](model_08/joint_diagnostics/part_4__part_5/README.md) |
| [part_4 ↔ part_6](model_08/joint_diagnostics/part_4__part_6/pair_exploded.stl) | 2798.588 | 70 | 41 | 33 | 12 | [Размеры, позиции и все отказы](model_08/joint_diagnostics/part_4__part_6/README.md) |
| [part_5 ↔ part_6](model_08/joint_diagnostics/part_5__part_6/pair_exploded.stl) | 90.16292 | 66 | 22 | 14 | 12 | [Размеры, позиции и все отказы](model_08/joint_diagnostics/part_5__part_6/README.md) |

## model_09 — Частично проверенная: не прошёл STEP

Недостижимые в исходном графе детали: []. Сохранённых глобальных отказов: 4.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_09/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 907.9203 | 68 | 36 | 36 | 12 | [Размеры, позиции и все отказы](model_09/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_5](model_09/joint_diagnostics/part_1__part_5/pair_exploded.stl) | 78.55552 | 68 | 31 | 26 | 12 | [Размеры, позиции и все отказы](model_09/joint_diagnostics/part_1__part_5/README.md) |
| [part_1 ↔ part_6](model_09/joint_diagnostics/part_1__part_6/pair_exploded.stl) | 0.5202251 | 1 | 1 | 1 | 1 | [Размеры, позиции и все отказы](model_09/joint_diagnostics/part_1__part_6/README.md) |
| [part_2 ↔ part_3](model_09/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 907.9203 | 68 | 44 | 44 | 12 | [Размеры, позиции и все отказы](model_09/joint_diagnostics/part_2__part_3/README.md) |
| [part_2 ↔ part_4](model_09/joint_diagnostics/part_2__part_4/pair_exploded.stl) | 676.0348 | 70 | 48 | 10 | 10 | [Размеры, позиции и все отказы](model_09/joint_diagnostics/part_2__part_4/README.md) |

## model_10 — Полностью успешная

Недостижимые в исходном графе детали: []. Сохранённых глобальных отказов: 2.

| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |
|---|---:|---:|---:|---:|---:|---|
| [part_1 ↔ part_3](model_10/joint_diagnostics/part_1__part_3/pair_exploded.stl) | 408 | 68 | 48 | 48 | 12 | [Размеры, позиции и все отказы](model_10/joint_diagnostics/part_1__part_3/README.md) |
| [part_1 ↔ part_5](model_10/joint_diagnostics/part_1__part_5/pair_exploded.stl) | 653.0494 | 70 | 54 | 46 | 12 | [Размеры, позиции и все отказы](model_10/joint_diagnostics/part_1__part_5/README.md) |
| [part_1 ↔ part_6](model_10/joint_diagnostics/part_1__part_6/pair_exploded.stl) | 201.0871 | 70 | 40 | 35 | 12 | [Размеры, позиции и все отказы](model_10/joint_diagnostics/part_1__part_6/README.md) |
| [part_1 ↔ part_7](model_10/joint_diagnostics/part_1__part_7/pair_exploded.stl) | 387.7311 | 64 | 20 | 20 | 12 | [Размеры, позиции и все отказы](model_10/joint_diagnostics/part_1__part_7/README.md) |
| [part_1 ↔ part_8](model_10/joint_diagnostics/part_1__part_8/pair_exploded.stl) | 408 | 68 | 49 | 49 | 12 | [Размеры, позиции и все отказы](model_10/joint_diagnostics/part_1__part_8/README.md) |
| [part_2 ↔ part_3](model_10/joint_diagnostics/part_2__part_3/pair_exploded.stl) | 408 | 68 | 51 | 51 | 12 | [Размеры, позиции и все отказы](model_10/joint_diagnostics/part_2__part_3/README.md) |
| [part_2 ↔ part_4](model_10/joint_diagnostics/part_2__part_4/pair_exploded.stl) | 49.2117 | 70 | 39 | 33 | 12 | [Размеры, позиции и все отказы](model_10/joint_diagnostics/part_2__part_4/README.md) |
| [part_3 ↔ part_7](model_10/joint_diagnostics/part_3__part_7/pair_exploded.stl) | 4.334917 | 68 | 49 | 49 | 12 | [Размеры, позиции и все отказы](model_10/joint_diagnostics/part_3__part_7/README.md) |

## Что означает лимит

Глобальные бюджеты прежнего запуска: до 128 состояний и до 12 представителей на ребро. В локальном повторе — до 72 вызовов построителей с отдельными бюджетами ролей. Если поверхность отклонена предварительно, размеры пазов не выдумываются. Если вызов пропущен из-за бюджета, он перечислен в `budget_skipped_calls` и не выдан за испытанный. Отсутствие результата не является доказательством невозможности.

[Ошибки проверки STEP №6 и №9](STEP_FAILURES.md) · [Все 69 составляющих](DECOMPOSITION.md)
