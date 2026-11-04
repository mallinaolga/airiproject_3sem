# 100 моделей — новый алгоритм

Используются ранее сохранённые 100 различных исходников: 10 прежних и 90 новых с фиксированными seed. Повторная генерация и повторный запуск не выполняются.
Эксперимент остановлен по запросу пользователя после модели №74. Продолжение — с №75; результаты №1–74 повторно не рассчитываются.
Декомпозиция, крепления, параметры поиска и проверки не изменены. Успех означает прохождение проверки сборки и экспорта.
Старый прогон остановлен по запросу пользователя; его результаты сохранены отдельно в `old/` и не входят в эту статистику.

| Показатель | Значение |
|---|---:|
| Всего исходников | 100 |
| Завершено | 74 |
| Успешно разделено | 70 |
| Полностью собрано | 41 |
| Отказы среди завершённых (без timeout) | 30 |
| Timeout | 3 |
| Ожидают завершения | 26 |
| Итоговый процент успешных сборок | Ещё не рассчитан |
| Многодетальные: собрано / завершено | 41 / 70 |

[JSON](results.json) · [CSV](results.csv) · [Исходники и seed](sources/manifest.json)

Все STL и STEP находятся в `new/model_NN/geometry/`, `new/model_NN/assembly/` и `sources/model_NN/`. Не прошедшие экспорт кандидаты остаются в `failed_export/`; их нельзя считать успешными сборками.
Для каждой модели ниже есть страница со всеми уже записанными STL, STEP и диагностическими JSON, включая неуспешные модели. Страницы обновляются по мере обработки.

| Модель | Статус | Деталей | Собрана |
|---|---|---:|---|
| [model_01](catalog/model_01.md) | success | 8 | да |
| [model_02](catalog/model_02.md) | failed | 7 | нет |
| [model_03](catalog/model_03.md) | success | 7 | да |
| [model_04](catalog/model_04.md) | success | 9 | да |
| [model_05](catalog/model_05.md) | failed | 6 | нет |
| [model_06](catalog/model_06.md) | success | 7 | да |
| [model_07](catalog/model_07.md) | failed | 5 | нет |
| [model_08](catalog/model_08.md) | success | 6 | да |
| [model_09](catalog/model_09.md) | export_failed | 6 | нет |
| [model_10](catalog/model_10.md) | success | 8 | да |
| [model_11](catalog/model_11.md) | decomposition_failed | 1 | нет |
| [model_12](catalog/model_12.md) | success | 7 | да |
| [model_13](catalog/model_13.md) | failed | 6 | нет |
| [model_14](catalog/model_14.md) | success | 6 | да |
| [model_15](catalog/model_15.md) | failed | 4 | нет |
| [model_16](catalog/model_16.md) | success | 7 | да |
| [model_17](catalog/model_17.md) | success | 7 | да |
| [model_18](catalog/model_18.md) | success | 8 | да |
| [model_19](catalog/model_19.md) | success | 6 | да |
| [model_20](catalog/model_20.md) | decomposition_failed | 1 | нет |
| [model_21](catalog/model_21.md) | success | 5 | да |
| [model_22](catalog/model_22.md) | success | 6 | да |
| [model_23](catalog/model_23.md) | failed | 7 | нет |
| [model_24](catalog/model_24.md) | success | 9 | да |
| [model_25](catalog/model_25.md) | success | 5 | да |
| [model_26](catalog/model_26.md) | timeout | 8 | нет |
| [model_27](catalog/model_27.md) | success | 6 | да |
| [model_28](catalog/model_28.md) | failed | 6 | нет |
| [model_29](catalog/model_29.md) | success | 8 | да |
| [model_30](catalog/model_30.md) | failed | 6 | нет |
| [model_31](catalog/model_31.md) | success | 6 | да |
| [model_32](catalog/model_32.md) | failed | 5 | нет |
| [model_33](catalog/model_33.md) | success | 7 | да |
| [model_34](catalog/model_34.md) | success | 10 | да |
| [model_35](catalog/model_35.md) | success | 5 | да |
| [model_36](catalog/model_36.md) | failed | 6 | нет |
| [model_37](catalog/model_37.md) | failed | 7 | нет |
| [model_38](catalog/model_38.md) | success | 5 | да |
| [model_39](catalog/model_39.md) | decomposition_failed | 1 | нет |
| [model_40](catalog/model_40.md) | success | 6 | да |
| [model_41](catalog/model_41.md) | success | 6 | да |
| [model_42](catalog/model_42.md) | failed | 7 | нет |
| [model_43](catalog/model_43.md) | success | 6 | да |
| [model_44](catalog/model_44.md) | failed | 8 | нет |
| [model_45](catalog/model_45.md) | success | 5 | да |
| [model_46](catalog/model_46.md) | failed | 6 | нет |
| [model_47](catalog/model_47.md) | failed | 5 | нет |
| [model_48](catalog/model_48.md) | success | 7 | да |
| [model_49](catalog/model_49.md) | failed | 5 | нет |
| [model_50](catalog/model_50.md) | success | 8 | да |
| [model_51](catalog/model_51.md) | success | 5 | да |
| [model_52](catalog/model_52.md) | success | 6 | да |
| [model_53](catalog/model_53.md) | success | 5 | да |
| [model_54](catalog/model_54.md) | success | 4 | да |
| [model_55](catalog/model_55.md) | timeout | 6 | нет |
| [model_56](catalog/model_56.md) | success | 6 | да |
| [model_57](catalog/model_57.md) | failed | 4 | нет |
| [model_58](catalog/model_58.md) | success | 7 | да |
| [model_59](catalog/model_59.md) | failed | 7 | нет |
| [model_60](catalog/model_60.md) | failed | 6 | нет |
| [model_61](catalog/model_61.md) | success | 6 | да |
| [model_62](catalog/model_62.md) | success | 6 | да |
| [model_63](catalog/model_63.md) | failed | 8 | нет |
| [model_64](catalog/model_64.md) | failed | 8 | нет |
| [model_65](catalog/model_65.md) | success | 5 | да |
| [model_66](catalog/model_66.md) | technical_limit_reached | 6 | нет |
| [model_67](catalog/model_67.md) | failed | 7 | нет |
| [model_68](catalog/model_68.md) | failed | 5 | нет |
| [model_69](catalog/model_69.md) | timeout | 6 | нет |
| [model_70](catalog/model_70.md) | failed | 8 | нет |
| [model_71](catalog/model_71.md) | success | 7 | да |
| [model_72](catalog/model_72.md) | success | 7 | да |
| [model_73](catalog/model_73.md) | decomposition_failed | 1 | нет |
| [model_74](catalog/model_74.md) | success | 8 | да |
| [model_75](catalog/model_75.md) | not_processed | — | ожидается |
| [model_76](catalog/model_76.md) | not_processed | — | ожидается |
| [model_77](catalog/model_77.md) | not_processed | — | ожидается |
| [model_78](catalog/model_78.md) | not_processed | — | ожидается |
| [model_79](catalog/model_79.md) | not_processed | — | ожидается |
| [model_80](catalog/model_80.md) | not_processed | — | ожидается |
| [model_81](catalog/model_81.md) | not_processed | — | ожидается |
| [model_82](catalog/model_82.md) | not_processed | — | ожидается |
| [model_83](catalog/model_83.md) | not_processed | — | ожидается |
| [model_84](catalog/model_84.md) | not_processed | — | ожидается |
| [model_85](catalog/model_85.md) | not_processed | — | ожидается |
| [model_86](catalog/model_86.md) | not_processed | — | ожидается |
| [model_87](catalog/model_87.md) | not_processed | — | ожидается |
| [model_88](catalog/model_88.md) | not_processed | — | ожидается |
| [model_89](catalog/model_89.md) | not_processed | — | ожидается |
| [model_90](catalog/model_90.md) | not_processed | — | ожидается |
| [model_91](catalog/model_91.md) | not_processed | — | ожидается |
| [model_92](catalog/model_92.md) | not_processed | — | ожидается |
| [model_93](catalog/model_93.md) | not_processed | — | ожидается |
| [model_94](catalog/model_94.md) | not_processed | — | ожидается |
| [model_95](catalog/model_95.md) | not_processed | — | ожидается |
| [model_96](catalog/model_96.md) | not_processed | — | ожидается |
| [model_97](catalog/model_97.md) | not_processed | — | ожидается |
| [model_98](catalog/model_98.md) | not_processed | — | ожидается |
| [model_99](catalog/model_99.md) | not_processed | — | ожидается |
| [model_100](catalog/model_100.md) | not_processed | — | ожидается |

Успех среди обработанных: 41/74 (55.41%). Timeout учитывается отдельно от обычных отказов.

Не обработаны: model_75, model_76, model_77, model_78, model_79, model_80, model_81, model_82, model_83, model_84, model_85, model_86, model_87, model_88, model_89, model_90, model_91, model_92, model_93, model_94, model_95, model_96, model_97, model_98, model_99, model_100.

Продолжение: `python -m cadgen.benchmark_supervisor` из корня Python-проекта. Сохранённые terminal-результаты, включая timeout, пропускаются; лимит каждой новой модели — 900 секунд. Исходники не генерируются заново.

Незавершённая попытка №75 сохранена в `interrupted/model_75/`; она не входит в статистику и не мешает продолжить с №75.

## Причины неуспеха

| Статус | Причина | Моделей |
|---|---|---:|
| failed | No connected joint graph on the fixed geometric constituents | 24 |
| export_failed | GeometryRejected: STEP roundtrip geometry or placements changed | 1 |
| decomposition_failed | GeometryRejected: h2: expected one valid positive-volume solid | 1 |
| decomposition_failed | ValueError: Null TopoDS_Shape object | 2 |
| timeout | Timeout during assembly path verification: OpenCascade Boolean intersection in sampled_path/overlap_volume | 1 |
| timeout | Per-model wall-clock deadline exceeded (900 seconds) | 2 |
| technical_limit_reached | No validated complete assembly of the fixed constituents within the search | 1 |
| decomposition_failed | GeometryRejected: h1: expected one valid positive-volume solid | 1 |
