"""Read saved publication/observer data and write linked review reports."""

from collections import Counter
from itertools import combinations
import json
from pathlib import Path

import cadquery as cq
import numpy as np

from publish_constructive_diagnostics import (TARGET,SOURCE,FAILED,clean,save,box,sha,
    terminology,load_parts,difference_volume,classification)


CATEGORIES={
    'local_valid':'Пара прошла геометрию и дискретный путь',
    'groove_creation_failed':'Не удалось создать паз/выступ',
    'bolt_creation_failed':'Не удалось создать болтовое крепление',
    'cylindrical_fit_creation_failed':'Не удалось создать цилиндрическую посадку',
    'geometric_validation_failed':'Не пройдена проверка геометрии пары',
    'no_pair_insertion_direction':'Нет проверенного направления установки пары',
    'joint_conflict':'Конфликт креплений',
    'no_complete_assembly_order':'Нет проверенного полного порядка',
    'search_limit':'Лимит поиска',
}
STATUS={
    'complete_validated':'Полностью успешная',
    'partial_validated_export_failed':'Частично проверенная: не прошёл STEP',
    'assembly_not_found':'Полная сборка не найдена',
}


def number(v):return '—' if v is None else f'{v:.7g}'
def vector(v):return '('+', '.join(number(x) for x in v)+')'
def cell(s):return str(s).replace('|','/').replace('\n',' ')
def write(path,lines):Path(path).write_text('\n'.join(lines).rstrip('\n')+'\n',encoding='utf-8')


def translated_reason(text):
    known=[
        ('Feature below explicit design floor','Размер элемента ниже проектного предела 0.1 мм; микроскопическое уменьшение не выполнялось.'),
        ('Service-overlap ribbon','Служебная узкая полоса не принята как площадка крепления.'),
        ('service-overlap ribbon','Служебная узкая полоса отклонена до подбора размеров.'),
        ('Cylinder axis misses receiver material','Ось цилиндра не проходит через материал принимающей детали.'),
        ('Socket lacks actual side material','Вокруг заглублённой посадки нет достаточного материала боковых стенок.'),
        ('Fit is supported only by a narrow contact trace','Опора цилиндрического выступа есть только на узкой полосе, не на массиве материала.'),
        ('No sampled assembly path','Геометрия создана, но проверенные направления вставки дали столкновения.'),
        ('Blind bolt lacks required second-part engagement','Для болта в глухом отверстии не хватает входа 10 мм во вторую деталь с сохранением дна.'),
        ('exceeds','Вычисленная длина стержня превышает разрешённый предел.'),
        ('Insufficient actual socket floor','Недостаточно фактического материала за дном посадки.'),
        ('No connected joint graph','Не найден связный граф допустимых креплений; это не доказательство невозможности сборки.'),
        ('Distributed centers collapse','Предложенные распределённые центры совпали после ограничения реальной гранью.'),
        ('Insufficient material anchoring the protrusion','Недостаточно фактического материала для закрепления основания выступа.'),
        ('Insufficient floor/side material around groove','Вырез не оставляет проверяемого запаса материала дна или боковых стенок паза.'),
        ('No accessible flat','Не найдена достаточная доступная плоская опора крепежа.'),
        ('No connected donor','Нет связной области материала донора.'),
        ('Main geometry changed','Геометрические изменения не согласованы с заявленным технологическим вырезом.'),
        ('Assembled components intersect','В собранном положении найдены недопустимые пересечения.'),
    ]
    text=terminology(text)
    return next((ru for key,ru in known if key in text),text)


def proposed(t):
    items=[]
    for f in t['feature_proposals']:
        items.append(f"{f['profile']['kind']}: {number(f['width_mm'])} × {number(f['depth_mm'])} × "
            f"{number(f['length_mm'])} мм @ {vector(f['center_in_cut_frame_mm'])}")
    if not items:
        for c in t['builder_calls']:
            v=c.get('values',{})
            if c['function']=='fasten':
                items.append(f"Болт Ø{number(v.get('diameter'))}, стержень {number(v.get('length'))} мм; "
                    f"центры {v.get('centers')}; вход во вторую деталь {number(v.get('engagement'))} мм; "
                    f"доступная глубина {number(v.get('receiver_depth'))} мм")
            elif c['function']=='cylindrical_fit':
                items.append(f"Цилиндр R{number(v.get('radius'))}, глубина {number(v.get('depth'))}, "
                    f"зазор {number(v.get('gap'))}, дно/стенка {number(v.get('floor'))} мм; "
                    f"доступно по оси {number(v.get('rd'))} мм")
    gaps=[number(c['values']['clearance_mm']) for c in t['builder_calls']
          if c['function']=='build_groove' and 'clearance_mm' in c.get('values',{})]
    if gaps:items.append('Зазоры: '+', '.join(gaps)+' мм')
    return '; '.join(items) or 'Индивидуальные размеры не выбраны: отказ до построения элемента.'


def pair_report(folder):
    data=json.loads((folder/'attempts.json').read_text());a,b=data['components']
    attempts=data['attempts'];contact=data['contact']
    model_folder=folder.parent.parent
    saved_plan=[]
    for sub in ('assembly','partial_assembly'):
        if (model_folder/sub/'metadata.json').exists():
            saved_plan=json.loads((model_folder/sub/'metadata.json').read_text())['joints'];break
    def rounded(v):
        if isinstance(v,float):return round(v,7)
        if isinstance(v,list):return [rounded(x) for x in v]
        if isinstance(v,dict):return {k:rounded(x) for k,x in v.items()}
        return v
    def signature(p):
        return rounded({k:p[k] for k in ('type','layout','depth_variant','features','cut_to_world_rotation','cut_origin') if k in p})
    for t in attempts:
        t['builder_role_to_published_part']={'part_1':t['owners'][0],'part_2':t['owners'][1]}
        if t['local_validation_passed']:
            t['matches_saved_global_variant_parameters_1e_7']=any(
                j['components']==t['owners'] and signature(j['parameters'])==signature(t['joint']['parameters']) for j in saved_plan)
    save(folder/'attempts.json',data)
    static=sum(t['static_geometry_passed'] for t in attempts)
    local=sum(t['local_validation_passed'] for t in attempts)
    lines=[f'# {data["model"]}: {a} ↔ {b}','',
        '[Разнесённая пара до креплений](pair_exploded.stl) · [Все попытки JSON](attempts.json)','',
        f"Габариты деталей: {a} {vector(data['part_dimensions_mm'][a])} мм; "
        f"{b} {vector(data['part_dimensions_mm'][b])} мм.",
        f"Площадь подтверждённого контакта: {number(contact['area_mm2'])} мм²; "
        f"минимальное расстояние: {number(contact['minimum_distance_mm'])} мм.",'',
        '| Грань | Тип | Размеры | Площадь, мм² |','|---|---|---|---:|']
    for i,f in enumerate(contact['faces'],1):
        dimensions=('плоская грань '+vector(f['local_dimensions_mm'])+' мм' if 'local_dimensions_mm' in f else
            f"R{number(f['radius_mm'])} мм, осевая длина {number(f['axial_span_mm'])} мм, угол {number(f['angular_span_radians'])} рад"
            if f['type']=='CYLINDER' else 'B-Rep bbox '+vector(f['dimensions_mm'])+' мм')
        lines.append(f"| {i} | {f['type']} | {dimensions} | {number(f['area_mm2'])} |")
    if not contact['faces']:
        lines.extend(['','Подтверждённой общей грани нет. Детали касаются границами/рёбрами либо '
            'B-Rep-проверка не подтвердила площадку. Такой контакт не подменяется бесконечной плоскостью.'])
    profiles=sorted({f['profile']['kind'] for t in attempts for f in t['feature_proposals']})
    methods=sorted({t['label'].split('/')[0] for t in attempts})
    lines.extend(['','## Что проверялось','',
        f"Реально вызванные способы: {', '.join(methods) or 'нет: отказ предварительной геометрической проверки'}.",
        f"Профили с фактически предложенными размерами: {', '.join(profiles) or 'не подбирались'}.",
        f"Выполнено попыток: {len(attempts)}. Статическую проверку геометрии прошли: {static}; "
        f"геометрию и дискретный путь пары: {local}; возвращено представителей: {data['locally_valid_returned_options']}.",
        f"Лимиты: до {data['design_settings']['max_designs_per_pair']} построений, до "
        f"{data['design_settings']['max_options_per_pair']} возвращённых вариантов. "
        f"Вызовов, пропущенных по бюджету роли/пары: {len(data['budget_skipped_calls'])}. "
        'Нулевая разница между числом попыток и общим лимитом не требуется: роли имеют отдельные бюджеты.',
        'Это повторный локальный поиск на сохранённых деталях, без изменения алгоритма, '
        'разбиения или статуса исходной модели. Полный глобальный поиск не повторялся.','',
        '## Предварительные отказы',''])
    for r in data['pre_filter_and_search_rejections']:
        # Attempt-level refusals are listed individually below; this section
        # also contains filters that never called any builder.
        if r['design'] in ('planar_interface','cylinder_axis'):
            lines.append(f"- `{r['design']}`: {translated_reason(r['reason'])} Исходная причина: `{cell(r['reason'])}`.")
    if data.get('error'):lines.append(f"- Итог локального поиска: {translated_reason(data['error']['reason'])}")
    lines.extend(['','## Все выполненные попытки','',
        'Размеры и центры указаны в собственной системе стыка. Матрица `cut_to_world_rotation` '
        'и начало `cut_origin_mm` для каждой попытки находятся в JSON. Локальные имена '
        '`part_1`/`part_2` в исходных сообщениях ошибок означают донора/приёмника, '
        'их реальные номера явно указаны в колонке и `builder_role_to_published_part`.','',
        '| Попытка | Донор → приёмник / способ | Предложенные размеры и положения | Итог | Причина |',
        '|---|---|---|---|---|'])
    for t in attempts:
        result=CATEGORIES.get(t['outcome'],t['outcome'])
        reason=(('Параметры совпали с вариантом сохранённого глобального плана (округление 1e-7); статус всей модели указан отдельно.'
                 if t.get('matches_saved_global_variant_parameters_1e_7') else
                 'Локально допустим; передан среди представителей. Точный глобальный отказ этого варианта не записан.'
                 if t.get('retained_in_returned_options') else
                 'Локально допустим; отсечён лимитом набора представителей до глобального перебора.')
                if t['local_validation_passed'] else translated_reason(t.get('reason','')))
        if t.get('last_path_check',{}).get('failed_trials'):
            trials=t['last_path_check']['failed_trials']
            reason+=' '+ '; '.join(f"направление {f.get('direction')}, ход {number(f.get('distance'))} мм, "
                f"пересечение {number(f.get('intersection_volume'))} мм³" for f in trials)
        lines.append(f"| {t['id']} | {t['owners'][0]} → {t['owners'][1]} / `{t['label']}` | "
                     f"{cell(proposed(t))} | {result} | {cell(reason)} |")
    lines.extend(['','## Отдельные геометрические результаты',''])
    if not data['representative_views']:
        lines.append('Геометрически подтверждённый вариант для экспорта отсутствует. Фиктивная геометрия не создавалась.')
    for rep in data['representative_views']:
        stem=rep['stem'];valid=rep['local_geometry_and_sampled_pair_path_passed']
        state=('геометрия и дискретный путь пары прошли; полная модель оценивается отдельно' if valid else
               'только статическая геометрия прошла; направления установки не прошли')
        lines.append(f"- `{stem}` — {state}: [разнесённо]({stem}_exploded.stl), [в сборочном положении]({stem}_assembled.stl).")
    model_status=json.loads((model_folder/'metadata.json').read_text())['original_assembly_status']
    original_global=json.loads((model_folder/'assembly_report.json').read_text())
    explanation=(f"Исходный граф остался несвязным; недостижимые детали: {original_global.get('unreachable_components',[])}. "
        'Корректная локальная пара не может сама устранить отсутствие соединения у другой составляющей.'
        if original_global.get('unreachable_components') else
        'Полный порядок в памяти найден, но последующая проверка STEP не прошла. Эта модель остаётся частично проверенной.'
        if model_status=='export_failed' else
        'Модель полностью прошла сохранённую проверку. Другие локальные варианты являются альтернативами выбранному плану.'
        if model_status=='success' else data['why_local_options_are_not_complete_model'])
    lines.extend(['','## Участие в полной сборке и причины отказов','',explanation,
        'Для несвязного исходного графа глобальные комбинации, конфликты креплений и полный порядок '
        'не проверялись: причина не приписывается каждому локально корректному пазу. '
        'Конкретные сохранённые глобальные отказы есть в JSON; если в них не записан '
        'профиль варианта, восстановить его связь с конкретной попыткой нельзя.',''])
    relevant=[]
    for rejection in data['original_global_rejections']:
        direct=set(rejection.get('edge',[]))=={a,b}
        combination=any(set(j['components'])=={a,b} for j in rejection.get('joints',[]))
        if direct or combination:
            relevant.append(dict(rejection,attribution='pair' if direct else 'whole_combination_including_pair'))
    data['global_rejections_involving_pair']=relevant
    save(folder/'attempts.json',data)
    if relevant:
        lines.extend(['Сохранённые глобальные отказы, относящиеся к этой паре:',''])
        for r in relevant:lines.append(f"- `{r['attribution']}`: {cell(r['reason'])}. Профиль конкретного варианта в таком отказе не указан.")
    else:lines.append('Индивидуального сохранённого глобального отказа этой пары нет; конфликт или ошибку порядка ей не приписываем.')
    lines.extend(['','Проверки пути дискретные. Силовая фиксация и прочность не доказаны.'])
    write(folder/'README.md',lines)
    return dict(model=data['model'],components=data['components'],area=contact['area_mm2'],
        faces=contact['faces'],attempts=len(attempts),static=static,local=local,
        returned=data['locally_valid_returned_options'],categories=dict(Counter(t['outcome'] for t in attempts)),
        pre_filters=data['pre_filter_and_search_rejections'],skipped=len(data['budget_skipped_calls']),
        path=str((folder/'README.md').relative_to(TARGET)),view=str((folder/'pair_exploded.stl').relative_to(TARGET)))


def step_diagnostics():
    rows=[]
    for n in (6,9):
        model=TARGET/f'model_{n:02d}';p=model/'partial_assembly'
        m=json.loads((p/'metadata.json').read_text());expected=load_parts(p,m['components'])
        read=cq.importers.importStep(str(p/'assembly.step'));remaining=list(read.solids().vals());metrics=[]
        for name,shape in sorted(expected.items(),key=lambda item:-item[1].Volume()):
            center=np.array(shape.Center().toTuple());diag=shape.BoundingBox().DiagonalLength
            def cost(s):
                return np.linalg.norm(np.array(s.Center().toTuple())-center)/max(diag,1)+abs(s.Volume()-shape.Volume())/max(shape.Volume(),1)
            match=min(remaining,key=cost);remaining.remove(match)
            metrics.append(dict(component=name,role=next(c['role'] for c in m['components'] if c['name']==name),
                individual_volume_mm3=shape.Volume(),assembly_volume_mm3=match.Volume(),
                centroid_distance_mm=float(np.linalg.norm(np.array(match.Center().toTuple())-center)),
                symmetric_difference_mm3=difference_volume(shape,match),both_valid=shape.isValid() and match.isValid(),
                individual=box(shape),assembly=box(match),individual_face_count=len(shape.Faces()),assembly_face_count=len(match.Faces())))
        error=difference_volume(read.val(),cq.Compound.makeCompound(list(expected.values())))
        result=dict(model=model.name,status='partial_validated_export_failed',
            original_export_error=m.get('export_error'),original_comparison_tolerance_mm3=m['settings']['volume_tolerance'],
            reloaded_individual_vs_assembly_compound_difference_mm3=error,
            saved_assembly_solids=len(read.solids().vals()),individual_solids=len(expected),components=metrics,
            in_memory_checks=m['checks'],original_source='saved failed_export; no repair or new joint generation',
            explanation='Export rejected the symmetric B-Rep set difference between in-memory components and the reloaded assembly. This audit compares available individual STEP files to the assembly. Matching masses/centroids alone do not establish geometric equality. The failure is retained; decomposed STL files are separate and unchanged.')
        save(model/'STEP_DIAGNOSTIC.json',result);rows.append(result)
    lines=['# Ошибки проверки STEP: №6 и №9','',
        'Это отказы проверки экспорта после найденного в памяти порядка сборки. '
        'Они не означают отказ геометрической декомпозиции. STL всех геометрических '
        'составляющих доступны независимо от этих STEP. Никакие STEP не исправлялись.','']
    for r in rows:
        name=r['model'];lines.extend([f'## {name}','',
            f"Ошибка экспортёра: `{r['original_export_error']}`. Допуск сравнения: "
            f"{number(r['original_comparison_tolerance_mm3'])} мм³.",
            f"Сохранено отдельных тел: {r['individual_solids']}; прочитано из сборки: {r['saved_assembly_solids']}. "
            f"Текущее сравнение составных STEP даёт {number(r['reloaded_individual_vs_assembly_compound_difference_mm3'])} мм³.",
            f'[Численные данные]({name}/STEP_DIAGNOSTIC.json) · [Геометрическое разбиение STL]({name}/split_exploded.stl)','',
            '| Компонент | Объём отдельно / в STEP-сборке, мм³ | Сдвиг центра, мм | Симметрическая разность, мм³ | Оба Solid валидны |',
            '|---|---:|---:|---:|---|'])
        for c in r['components']:
            lines.append(f"| [{c['component']}]({name}/partial_assembly/{c['component']}.stl) | "
                f"{number(c['individual_volume_mm3'])} / {number(c['assembly_volume_mm3'])} | "
                f"{number(c['centroid_distance_mm'])} | {number(c['symmetric_difference_mm3'])} | {'да' if c['both_valid'] else 'нет'} |")
        lines.extend(['',
            'Проверка сравнивает геометрические множества через Boolean-разность, а не только число тел, '
            'объёмы или центры. Даже совпадение последних не позволяет автоматически объявить '
            'экспорт корректным. В сохранённых файлах возможна несогласованность операций сравнения '
            'OpenCascade на почти совпадающих границах; этим отчётом не доказано ни отсутствие '
            'геометрической ошибки, ни физическое повреждение STEP. Полная успешность не присвоена.',''])
    write(TARGET/'STEP_FAILURES.md',lines)


def main():
    # Apply publication vocabulary to initial copied metadata as well as replay data.
    for f in TARGET.rglob('*.json'):save(f,json.loads(f.read_text()))
    pairs=[];rows=json.loads((TARGET/'models.json').read_text())['models']
    for row in rows:
        name=row['model'];folder=TARGET/name
        gm=json.loads((SOURCE/name/'geometry/metadata.json').read_text())
        old=json.loads((SOURCE/name/'metadata.json').read_text())
        m=json.loads((folder/'metadata.json').read_text())
        m.update(assembly_success=old['assembly_success'],assembly_status=old['assembly_status'],
            installed_joint_counts={k:v if old['assembly_success'] else 0 for k,v in old.get('validated_candidate_counts',{}).items()},
            candidate_joint_counts=old.get('validated_candidate_counts',{}))
        m.pop('counts',None);save(folder/'metadata.json',m)
        index=json.loads((folder/'joint_diagnostics/index.json').read_text())
        for pair in index['pairs']:pairs.append(pair_report(folder/pair['folder']))
    save(TARGET/'pair_summary.json',dict(pairs=pairs))
    step_diagnostics()
    decomposition=['# Классификация всех 69 геометрических составляющих','',
        'Классификация скопирована из сохранённого анализа, повторного разбиения нет. '
        '«Не подтверждена» не означает «простая»: такой компонент остаётся логичным '
        'элементом истории с реальными подрезками присоединений.','',
        '| Модель / деталь | Простота | Геометрическая семья | Размеры X × Y × Z, мм | Причина распознавания / остановки |',
        '|---|---|---|---|---|']
    for row in rows:
        name=row['model'];m=json.loads((TARGET/name/'metadata.json').read_text())
        for c in m['geometric_components']:
            r=c['recognition'];stop=c['stopping_condition']
            reason=r.get('reason','unknown')+'; '+stop['reason']
            if r.get('errors'):reason+='; ошибки анализа: '+'; '.join(r['errors'])
            decomposition.append(f"| [{name}/{c['name']}]({name}/{c['stl']}) | "
                f"{'подтверждена' if c['simple'] else 'НЕ подтверждена'} | {c['constructive_element']['family']} | "
                f"{vector(c['dimensions_mm'])} | {cell(reason)} |")
    decomposition.extend(['','## Цилиндр и ключик, модели №9 и №10','',
        '№9: [ключик part_4](model_09/part_4.stl) сохранён целиком; цилиндрические составляющие '
        '[part_1](model_09/part_1.stl), [part_2](model_09/part_2.stl), [part_3](model_09/part_3.stl) '
        'соответствуют двум участкам вала и среднему увеличенному радиусу. У подрезанной зоны '
        'присоединения простота не подменяется успешностью крепления. Всего 6 деталей, простота подтверждена у 5.','',
        '№10: нижний и верхний участки исходной призмы — [part_1](model_10/part_1.stl) и '
        '[part_2](model_10/part_2.stl), увеличенная средняя призма — [part_3](model_10/part_3.stl). '
        'Боковые цилиндры и отдельный призматический выступ сохранены как собственные элементы, '
        'а не разрезаны продолжениями глобальных плоскостей. Всего 8 деталей, простота подтверждена у 5.','',
        'Полные направления выдавливания, исходные операции, признаки подрезок и ошибки анализа '
        'сохранены в `metadata.json` каждой модели. Исходники и все геометрические STL скопированы побайтно.'])
    write(TARGET/'DECOMPOSITION.md',decomposition)
    problem=['# Причины отказов по соседним парам','',
        'Здесь нет нового глобального решения и нет исправлений алгоритма. Все соседние пары '
        'повторно проверены существующим ограниченным локальным поиском на сохранённых компонентах. '
        'Включены также касания границ без подтверждённой общей площадки.','',
        'Категории раздельны: не построен паз; не построен болт; не прошла статическая геометрия; '
        'нет проверенного направления пары; конфликт креплений; нет полного порядка; лимит. '
        'Первые четыре определяются по стадии фактического отказа, остальные — только по сохранённой глобальной диагностике.','',
        'Локально допустимые соединения не означают готовую сборку. Для №1, №2, №5, №7 '
        'глобальная проверка остановилась до перебора комбинаций из-за отсутствующего ребра '
        'к отдельной составляющей. Поэтому корректные пазы на других парах не объявлены конфликтующими '
        'или недоступными без проверки.','']
    problem.extend(['## Конкретные разрывы графа у №1, №2, №5 и №7','',
        '- **№1, part_5 ↔ part_6:** две цилиндрические контактные грани R25 мм, '
        'осевая протяжённость 23 мм, суммарная площадь 68.82927 мм². Планарных площадок нет, '
        'поэтому шесть плоских профилей здесь не вызывались. Осевая посадка не проходит '
        'через материал приёмника. Две попытки нормальной цилиндрической бобышки отклонены: '
        'нет бокового материала вокруг гнезда либо массивной опоры выступа. '
        '[Пара, размеры посадок и отказы](model_01/joint_diagnostics/part_5__part_6/README.md).',
        '- **№2, part_1 ↔ part_5:** площадь 0.4188884 мм². Есть цилиндрические следы '
        'длиной 0.0005 мм и плоская площадка примерно 2 × 0.2097594 мм. Площадка отклонена '
        'общим предварительным порогом 0.3 мм, до подбора пазов и обычных болтов. '
        'Попытка цилиндрической посадки с поперечным болтом дошла до расчёта стержня '
        '**64.21 мм**, что больше разрешённых 50 мм. '
        '[Полная запись](model_02/joint_diagnostics/part_1__part_5/README.md).',
        '- **№5, part_1 ↔ part_4:** площадь 1778.329 мм²; 70 попыток, '
        '**18 статически допустимых конструкций**, но ни одна не прошла проверку направления пары. '
        'У остальных вариантов не хватало материала опоры/стенок или срабатывал минимальный размер. '
        '[Геометрия без успешного пути и все размеры](model_05/joint_diagnostics/part_1__part_4/README.md). '
        '**part_4 ↔ part_6:** площадь 40.12461 мм²; 68 попыток, **50 статически допустимых**, '
        'ни одной с успешным путём. Например, при ходе 3.903577 мм пересечение составляет '
        '0.1460394 мм³. Это отказ установки, а не отсутствие построенного паза. '
        '[Посмотреть эту пару](model_05/joint_diagnostics/part_4__part_6/README.md).',
        '- **№7, part_1 ↔ part_4:** площадь 1.280132 мм²; грани примерно '
        '7.224458 × 0.1788826 мм и две площадки 0.1916941 × 0.0005 мм. '
        'Все отсекаются до вызова построителей порогом 0.3 мм. Ось цилиндра также '
        'не попадает в материал приёмника. '
        '[Пара и предварительные отказы](model_07/joint_diagnostics/part_1__part_4/README.md).','',
        '**О названии фильтра:** сообщение исходного кода `service-overlap ribbon` применяется '
        'к любой площадке с минимальным габаритом меньше `max(20 × 0.0005, 3 × 0.1) = 0.3 мм`. '
        'Поэтому площадки шириной 0.1789 и 0.2098 мм тоже получают эту метку: '
        'она сама по себе не доказывает, что вся площадка — служебное перекрытие CADGen. '
        'Это установленное ограничение текущего фильтра; здесь оно не исправлялось.',''])
    for row in rows:
        name=row['model'];m=json.loads((TARGET/name/'metadata.json').read_text());old=json.loads((TARGET/name/'assembly_report.json').read_text())
        problem.extend([f'## {name} — {STATUS[row["status"]]}','',
            f"Недостижимые в исходном графе детали: {old.get('unreachable_components',[])}. "
            f"Сохранённых глобальных отказов: {len(old.get('global_rejections',[]))}.",'',
            '| Соседняя пара | Площадь, мм² | Попыток | Статически допустимых | С путём пары | Представителей | Диагностика |',
            '|---|---:|---:|---:|---:|---:|---|'])
        for p in pairs:
            if p['model']!=name:continue
            a,b=p['components'];problem.append(f"| [{a} ↔ {b}]({p['view']}) | {number(p['area'])} | "
                f"{p['attempts']} | {p['static']} | {p['local']} | {p['returned']} | [Размеры, позиции и все отказы]({p['path']}) |")
        problem.append('')
    problem.extend(['## Что означает лимит','',
        'Глобальные бюджеты прежнего запуска: до 128 состояний и до 12 представителей на ребро. '
        'В локальном повторе — до 72 вызовов построителей с отдельными бюджетами ролей. '
        'Если поверхность отклонена предварительно, размеры пазов не выдумываются. '
        'Если вызов пропущен из-за бюджета, он перечислен в `budget_skipped_calls` и не выдан за испытанный. '
        'Отсутствие результата не является доказательством невозможности.','',
        '[Ошибки проверки STEP №6 и №9](STEP_FAILURES.md) · [Все 69 составляющих](DECOMPOSITION.md)'])
    write(TARGET/'PROBLEM_JOINTS.md',problem)
    root=['# Все 10 моделей: конструктивное разбиение и диагностика креплений','',
        'Сохранены **все 69 геометрических составляющих**, включая неуспешные модели. '
        'До креплений: 51 составляющая распознана простой, у 18 простота не подтверждена. '
        'Новые исходные CADGen-модели не создавались, алгоритмы и разбиение не менялись.','',
        '- **Полностью успешные:** №3, №4, №8, №10 — сохранён и проверен полный экспорт сборки.',
        '- **Частично проверенные:** №6 и №9 — порядок в памяти найден, проверка STEP не прошла; это не готовые сборки.',
        '- **Полная сборка не найдена:** №1, №2, №5, №7 — локально корректные пары доступны отдельно, но граф соединений несвязен.','',
        '[Проблемные соединения: все пары, размеры и причины](PROBLEM_JOINTS.md) · '
        '[Классификация 69 деталей](DECOMPOSITION.md) · [Ошибки STEP](STEP_FAILURES.md)','',
        '| Модель | Составляющих | Статус | Исходник | Разнесённое разбиение | Разбиение в исходных положениях | Детали и результаты |',
        '|---|---:|---|---|---|---|---|']
    for row in rows:
        name=row['model'];root.append(f"| {name} | {row['components']} | {STATUS[row['status']]} | "
            f"[original.stl]({name}/original.stl) | [split_exploded.stl]({name}/split_exploded.stl) | "
            f"[split_assembled.stl]({name}/split_assembled.stl) | [Все детали]({name}/README.md) |")
        m=json.loads((TARGET/name/'metadata.json').read_text());lines=[f'# {name} — {STATUS[row["status"]]}','',
            '[Исходник](original.stl) · [Разбиение разнесённо](split_exploded.stl) · '
            '[Разбиение в исходных положениях](split_assembled.stl) · [Метаданные](metadata.json)','',
            '## Каждая геометрическая деталь ДО креплений','',
            '| Деталь | STL | STEP | Простота |','|---|---|---|---|']
        for c in m['geometric_components']:
            lines.append(f"| {c['name']} | [STL]({c['stl']}) | [STEP]({c['step']}) | {'подтверждена' if c['simple'] else 'НЕ подтверждена'} |")
        processed=TARGET/name/('assembly' if row['status']=='complete_validated' else 'partial_assembly')
        if processed.exists():
            sub=processed.name;pm=json.loads((processed/'metadata.json').read_text())
            lines.extend(['','## '+('Готовая сборка ПОСЛЕ креплений' if sub=='assembly' else
                'Частично проверенный кандидат ПОСЛЕ креплений — НЕ готовая сборка'),'',
                f'[Разобранная модель]({sub}/parts_exploded.stl) · [Собранное положение STL]({sub}/assembly.stl) · '
                f'[STEP]({sub}/assembly.step) · [Метаданные]({sub}/metadata.json)','',
                '| Компонент | Тип | STL | STEP |','|---|---|---|---|'])
            for c in pm['components']:
                role={'main':'геометрическая деталь','bolt':'сквозной болт','nut':'гайка','blind_bolt':'болт в глухом отверстии'}.get(c['role'],c['role'])
                lines.append(f"| {c['name']} | {role} | [STL]({sub}/{c['stl']}) | [STEP]({sub}/{c['step']}) |")
        lines.extend(['','## Каждая соседняя пара',''])
        for p in pairs:
            if p['model']!=name:continue
            path=p['path'].split(name+'/',1)[1];view=p['view'].split(name+'/',1)[1]
            lines.append(f"- {' ↔ '.join(p['components'])}: [разнесённые детали]({view}), [размеры и отказы]({path}).")
        if row['status']=='partial_validated_export_failed':lines.append('\n[Ошибка STEP](STEP_DIAGNOSTIC.json). Геометрические STL выше от неё не зависят.')
        write(TARGET/name/'README.md',lines)
    root.extend(['','STL отдельных деталей центрированы для просмотра; исходные положения и преобразования '
        'сохранены в метаданных. `split_assembled.stl` содержит все геометрические части без креплений. '
        'Кандидаты пар разделяют статическую геометрию и проверку направления вставки. '
        'Геометрически построенный паз с неудачным путём явно помечен `static_only`.','',
        'В терминологии публикации используются сквозные болты с гайкой и болты в глухих отверстиях. '
        'Имена полей публикации нормализованы; внутренние алгоритмы и идентификаторы исходного кода не изменены. '
        'Резьба и прочность не моделировались. Траектории дискретные.','',
        'SHA-256 копированных файлов и исходного кода находятся в [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json).'])
    root.extend(['','[Проверка опубликованных файлов](PUBLICATION_VALIDATION.json) · '
        '[Ранее пройденные 105 тестов неизменённых алгоритмов](baseline_test_summary.json).'])
    write(TARGET/'README.md',root)
    print('REPORTS',len(rows),'models',len(pairs),'neighbour pairs',sum(p['attempts'] for p in pairs),'observed attempts')


if __name__=='__main__':main()
