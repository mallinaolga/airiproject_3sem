# model_09 — Частично проверенная: не прошёл STEP

[Исходник](original.stl) · [Разбиение разнесённо](split_exploded.stl) · [Разбиение в исходных положениях](split_assembled.stl) · [Метаданные](metadata.json)

## Каждая геометрическая деталь ДО креплений

| Деталь | STL | STEP | Простота |
|---|---|---|---|
| part_1 | [STL](part_1.stl) | [STEP](part_1.step) | подтверждена |
| part_2 | [STL](part_2.stl) | [STEP](part_2.step) | НЕ подтверждена |
| part_3 | [STL](part_3.stl) | [STEP](part_3.step) | подтверждена |
| part_4 | [STL](part_4.stl) | [STEP](part_4.step) | подтверждена |
| part_5 | [STL](part_5.stl) | [STEP](part_5.step) | подтверждена |
| part_6 | [STL](part_6.stl) | [STEP](part_6.step) | подтверждена |

## Частично проверенный кандидат ПОСЛЕ креплений — НЕ готовая сборка

[Разобранная модель](partial_assembly/parts_exploded.stl) · [Собранное положение STL](partial_assembly/assembly.stl) · [STEP](partial_assembly/assembly.step) · [Метаданные](partial_assembly/metadata.json)

| Компонент | Тип | STL | STEP |
|---|---|---|---|
| part_1 | геометрическая деталь | [STL](partial_assembly/part_1.stl) | [STEP](partial_assembly/part_1.step) |
| part_2 | геометрическая деталь | [STL](partial_assembly/part_2.stl) | [STEP](partial_assembly/part_2.step) |
| part_3 | геометрическая деталь | [STL](partial_assembly/part_3.stl) | [STEP](partial_assembly/part_3.step) |
| part_4 | геометрическая деталь | [STL](partial_assembly/part_4.stl) | [STEP](partial_assembly/part_4.step) |
| part_5 | геометрическая деталь | [STL](partial_assembly/part_5.stl) | [STEP](partial_assembly/part_5.step) |
| part_6 | геометрическая деталь | [STL](partial_assembly/part_6.stl) | [STEP](partial_assembly/part_6.step) |
| bolt_1 | сквозной болт | [STL](partial_assembly/bolt_1.stl) | [STEP](partial_assembly/bolt_1.step) |
| nut_1 | гайка | [STL](partial_assembly/nut_1.stl) | [STEP](partial_assembly/nut_1.step) |
| bolt_2 | сквозной болт | [STL](partial_assembly/bolt_2.stl) | [STEP](partial_assembly/bolt_2.step) |
| nut_2 | гайка | [STL](partial_assembly/nut_2.stl) | [STEP](partial_assembly/nut_2.step) |

## Каждая соседняя пара

- part_1 ↔ part_3: [разнесённые детали](joint_diagnostics/part_1__part_3/pair_exploded.stl), [размеры и отказы](joint_diagnostics/part_1__part_3/README.md).
- part_1 ↔ part_5: [разнесённые детали](joint_diagnostics/part_1__part_5/pair_exploded.stl), [размеры и отказы](joint_diagnostics/part_1__part_5/README.md).
- part_1 ↔ part_6: [разнесённые детали](joint_diagnostics/part_1__part_6/pair_exploded.stl), [размеры и отказы](joint_diagnostics/part_1__part_6/README.md).
- part_2 ↔ part_3: [разнесённые детали](joint_diagnostics/part_2__part_3/pair_exploded.stl), [размеры и отказы](joint_diagnostics/part_2__part_3/README.md).
- part_2 ↔ part_4: [разнесённые детали](joint_diagnostics/part_2__part_4/pair_exploded.stl), [размеры и отказы](joint_diagnostics/part_2__part_4/README.md).

[Ошибка STEP](STEP_DIAGNOSTIC.json). Геометрические STL выше от неё не зависят.
