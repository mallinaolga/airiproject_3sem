"""Summarize saved constructive results; no source or fastener generation."""

import argparse
from collections import Counter
import json
from pathlib import Path

import cadquery as cq

from .assembly_generator import save_json
from .assembly_validation import overlap_volume
from .validate_constructive_results import load_parts


def feature_sizes(parameters):
    sizes=[]
    for f in parameters.get('features',[parameters]):
        if f['type']=='groove':sizes.extend([f['profile']['opening_width'],f['profile']['depth'],f['central_engagement_length']])
        elif f['type']=='cylindrical_fit':sizes.extend([2*f['pin_radius'],f['depth']])
    return sizes


def write_comparison(folder,source):
    folder=Path(folder);source=Path(source)
    report=json.loads((folder/'report.json').read_text())
    rows=[];lines=['# Сравнение с опубликованными адаптивными сборками','',
        'Исходники те же. Геометрия сохранена до креплений. Нулевое число установленных '
        'креплений при отказе означает отсутствие готовой сборки, а не отсутствие локальных кандидатов.','',
        '| Модель | Было деталей | Стало | Простых подтверждено | Пазовых элементов | Болтов | Саморезов | Полностью собрана |',
        '|---|---:|---:|---:|---:|---:|---:|---|']
    for row in sorted(report['models'],key=lambda r:r['model']):
        name=row['model'];old=json.loads((source/name/'metadata.json').read_text())
        target=folder/name;gm=json.loads((target/'geometry/metadata.json').read_text())
        success=row['assembly_success'];local=[]
        for path in sorted(target.glob('interface_*.json')):
            entry=json.loads(path.read_text())
            local.append(dict(components=entry['components'],status=entry['status'],options=entry.get('options',0),
                              reason=entry.get('reason'),search=entry.get('constructive_search') or entry.get('adaptive_search')))
        old_sizes=[s for j in old['joints'] for s in feature_sizes(j['parameters'])]
        old_micro=sum(any(v<.01 for v in feature_sizes(j['parameters'])) for j in old['joints'])
        old_types=dict(Counter(j['parameters']['type'] for j in old['joints']))
        comparison=dict(model=name,previous_components=old['main_component_count'],
            components=gm['main_component_count'],raw_simple_components=sum(
                s.get('analysis',{}).get('recognition',{}).get('simple',False) for s in gm['stopping_conditions'].values()),
            previous_connection_types=old_types,previous_counts=old['counts'],
            previous_minimum_feature_mm=min(old_sizes) if old_sizes else None,previous_microscopic_joints=old_micro,
            installed_counts={k:row.get(k,0) if success else 0 for k in ('groove_elements','bolts','screws','cylindrical_fits')},
            assembly_success=success,assembly_status=row['assembly_status'],assembly_reason=row.get('assembly_reason'),
            elapsed_seconds=row.get('elapsed_seconds'),local_interfaces=local,
            geometric_reconstruction_error=gm['checks']['raw_reconstruction_error_volume'])
        rows.append(comparison);counts=comparison['installed_counts'];simple=comparison['raw_simple_components']
        lines.append(f"| [{name}]({name}/geometry/split_exploded.stl) | {old['main_component_count']} | "
            f"{gm['main_component_count']} | {simple} | {counts['groove_elements']} | {counts['bolts']} | "
            f"{counts['screws']} | {'да' if success else 'нет'} |")
    lines.extend(['','## Остановка и сравнение креплений',''])
    for row in rows:
        name=row['model'];success=row['assembly_success']
        gm=json.loads((folder/name/'geometry/metadata.json').read_text())
        stops=Counter(s['reason'] for s in gm['stopping_conditions'].values())
        lines.extend([f"### {name}",'',
            f"До изменения: {row['previous_connection_types']}; размеры пазов от "
            f"{row['previous_minimum_feature_mm']:.8g} мм; микроскопических соединений (<0.01 мм): {row['previous_microscopic_joints']}.",
            f"После изменения: {row['components']} конструктивных элементов; остановки {dict(stops)}. "
            f"Постоянное внешнее сечение подтверждено у {row['raw_simple_components']}; "
            f"не подтверждено у {row['components']-row['raw_simple_components']}. "
            'Последние сохранены как элементы истории с реальной геометрией присоединения; простыми не объявлены.',
            f"Сборка: `{row['assembly_status']}`. {row.get('assembly_reason') or 'Полный проверенный порядок сохранён.'}",
            f"Время этапа сборки и экспорта из геометрической контрольной точки: {row['elapsed_seconds']} с. "
            'Сопоставимое время старого запуска не измерялось.',
            f"[Диагностика сборки]({name}/assembly_report.json) · [Разбиение]({name}/decomposition_report.json)",''])
        for edge in row['local_interfaces']:
            lines.append(f"- `{edge['components']}`: {edge['status']}, вариантов {edge['options']}. {edge.get('reason') or ''}")
        lines.append('')
        if name in ('model_09','model_10'):
            old=json.loads((source/name/'metadata.json').read_text())
            old_parts=load_parts(source/name,old['raw_components']);new_parts=load_parts(folder/name/'geometry',gm['raw_components'])
            matrix={a:{b:overlap_volume(left,right) for b,right in new_parts.items()} for a,left in old_parts.items()}
            save_json(folder/name/'old_to_new_material.json',dict(units='mm^3',overlap_volumes=matrix))
            lines.extend(['Распределение материала старых деталей между новыми (объёмы больше 1e-5 мм³):','',
                '| Старая деталь | Новые детали: общий материал, мм³ |','|---|---|'])
            for part,volumes in matrix.items():
                text=', '.join(f'{n}: {v:.5g}' for n,v in volumes.items() if v>1e-5)
                lines.append(f'| {part} | {text} |')
            lines.extend(['','Новые составляющие и исходные направления выдавливания:',''])
            for component in gm['raw_components']:
                n=component['name'];d=gm['checks']['constructive_elements'][n];s=new_parts[n];b=s.BoundingBox()
                lines.append(f"- [{n}]({name}/geometry/{n}.stl): {d['family']}, ось {d['axis']}, "
                    f"габариты {b.xlen:.6g} × {b.ylen:.6g} × {b.zlen:.6g} мм; "
                    f"подрезан присоединением: {'да' if d['trimmed_by_attachment'] else 'нет'}.")
            lines.append('')
    lines.extend(['## Численные и вычислительные ограничения','',
        'В таблице считаются только крепления полностью экспортированных сборок. '
        'Кандидат, не прошедший STEP round-trip или общий порядок, не является готовым результатом. '
        'Подробные размеры всех кандидатов находятся в `interface_*.json`. '
        'Нижний проектный предел — 0.1 мм; по границе 0.01 мм новые пазы не уменьшаются. '
        'Старые успешные результаты содержат 10 микроскопических пазов.','',
        'Поиск ограничен 72 конструкциями на пару, 12 сохранёнными представителями и 128 состояниями. '
        'Неудача не доказывает невозможность собрать модель. Траектории дискретные; '
        'прочность и непрерывная бесстолкновительность не доказаны.',''])
    (folder/'COMPARISON.md').write_text('\n'.join(lines),encoding='utf-8')
    save_json(folder/'comparison.json',dict(models=rows))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    parser.add_argument('--source',type=Path,default=Path('examples/adaptive_joints'))
    args=parser.parse_args();write_comparison(args.folder,args.source)


if __name__=='__main__':main()
