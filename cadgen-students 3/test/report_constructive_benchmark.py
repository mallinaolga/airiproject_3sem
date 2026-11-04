"""Live catalogue of the existing new-algorithm run; never runs CAD work."""
import csv
import io
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'generations/assemblies/benchmark_100'

def write(path,text):
    temp=path.with_name(path.name+'.tmp')
    temp.write_text(text,encoding='utf-8');temp.replace(path)

def summarize():
    manifest=json.loads((ROOT/'sources/manifest.json').read_text())
    report=json.loads((ROOT/'new/report.json').read_text())
    completed={r['model']:r for r in report['models']}
    catalogue=ROOT/'catalog';catalogue.mkdir(exist_ok=True)
    rows=[];counts=Counter();multi=Counter()
    for source in manifest:
        name=source['model'];folder=ROOT/'new'/name;row=completed.get(name)
        state=(row.get('assembly_status','failed') if row else 'running' if folder.exists() and report.get('status')=='running' else 'not_processed')
        success=row.get('assembly_success',False) if row else None
        reason=(row.get('assembly_reason') or row.get('reason') or '') if row else ''
        rows.append(dict(model=name,status=state,completed=row is not None,components=row.get('components') if row else None,
            decomposition_success=row.get('decomposition_success',False) if row else None,
            assembly_success=success,reason=reason,catalog=f'catalog/{name}.md'))
        if row:
            counts['completed']+=1;counts['success']+=bool(success)
            counts['decomposed']+=bool(row.get('decomposition_success'))
            counts['timeouts']+=state=='timeout'
            counts['failed']+=not bool(success) and state!='timeout'
            counts['step_errors']+=not bool(success) and 'step' in reason.lower()
            counts['models_with_lateral_contacts']+=bool(row.get('lateral_cylinder_prism_contacts'))
            counts['installed_lateral_connections']+=row.get('successful_lateral_groove_connections',0)
            if row.get('decomposition_success') and row.get('components',0)>=2:
                multi['total']+=1;multi['success']+=bool(success)
        lines=[f'# {name}','',f'Статус: **{state}**.',reason,'',
            f'[Исходник STL](../sources/{name}/original.stl) · [Исходник STEP](../sources/{name}/original.step) · [История CADGen](../sources/{name}/history.py)','',
            '## Геометрия и результаты','']
        for sub,label in [('geometry','Декомпозиция'),('assembly','Сборка с креплениями'),('failed_export','Кандидат, не прошедший экспорт — не успешная сборка')]:
            directory=folder/sub
            if directory.exists():
                lines.extend([f'### {label}',''])
                for p in sorted(directory.iterdir()):
                    if p.suffix.lower() in ('.stl','.step','.json'):
                        lines.append(f'- [{p.name}](../new/{name}/{sub}/{p.name})')
                lines.append('')
        lines.extend(['## Диагностика',''])
        for p in sorted(folder.glob('*.json')):
            lines.append(f'- [{p.name}](../new/{name}/{p.name})')
        for p in sorted((folder/'timeout_diagnostics').glob('*')):
            if p.is_file() and p.suffix!='.log' and p.name!='report_before_timeout.json':lines.append(f'- [{p.name}](../new/{name}/timeout_diagnostics/{p.name})')
        interrupted=ROOT/'interrupted'/name/'worker_run'/name
        if interrupted.exists():
            lines.extend(['', '## Сохранённая незавершённая попытка',''])
            for p in sorted(interrupted.rglob('*')):
                if p.is_file() and p.suffix in ('.stl','.step','.json'):
                    lines.append(f'- [{p.relative_to(interrupted)}](../{p.relative_to(ROOT)})')
        if row is None:lines.extend(['','Обработка ещё не завершена. Отсутствующие результаты не считаются отказом.'])
        write(catalogue/f'{name}.md','\n'.join(lines)+'\n')
    total=len(manifest);done=counts['completed']==total and report.get('status')=='complete'
    summary=dict(status='complete' if done else report.get('status','running'),algorithm='new',total_sources=total,
        **counts,pending=total-counts['completed'],success_percent=100*counts['success']/total if done else None,
        success_percent_of_processed=100*counts['success']/counts['completed'] if counts['completed'] else None,
        multipart=dict(multi),multipart_success_percent=100*multi['success']/multi['total'] if done and multi['total'] else None)
    write(ROOT/'results.json',json.dumps(dict(summary=summary,models=rows),indent=2,ensure_ascii=False))
    buffer=io.StringIO();writer=csv.DictWriter(buffer,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    write(ROOT/'results.csv',buffer.getvalue())
    lines=['# 100 моделей — новый алгоритм','',
        'Используются ранее сохранённые 100 различных исходников: 10 прежних и 90 новых с фиксированными seed. Повторная генерация и повторный запуск не выполняются.',
        ('Эксперимент остановлен по запросу пользователя после модели №74. Продолжение — с №75; результаты №1–74 повторно не рассчитываются.' if report.get('status')=='stopped_by_user' else 'Обработка новым алгоритмом продолжается.'),
        'Декомпозиция, крепления, параметры поиска и проверки не изменены. Успех означает прохождение проверки сборки и экспорта.',
        'Старый прогон остановлен по запросу пользователя; его результаты сохранены отдельно в `old/` и не входят в эту статистику.',
        '', '| Показатель | Значение |','|---|---:|',f'| Всего исходников | {total} |',
        f'| Завершено | {counts["completed"]} |',f'| Успешно разделено | {counts["decomposed"]} |',
        f'| Полностью собрано | {counts["success"]} |',f'| Отказы среди завершённых (без timeout) | {counts["failed"]} |',f'| Timeout | {counts["timeouts"]} |',
        f'| Ожидают завершения | {total-counts["completed"]} |',
        f'| Итоговый процент успешных сборок | {str(round(summary["success_percent"],2))+"%" if done else "Ещё не рассчитан"} |',
        f'| Многодетальные: собрано / завершено | {multi["success"]} / {multi["total"]} |','',
        '[JSON](results.json) · [CSV](results.csv) · [Исходники и seed](sources/manifest.json)','',
        'Все STL и STEP находятся в `new/model_NN/geometry/`, `new/model_NN/assembly/` и `sources/model_NN/`. Не прошедшие экспорт кандидаты остаются в `failed_export/`; их нельзя считать успешными сборками.',
        'Для каждой модели ниже есть страница со всеми уже записанными STL, STEP и диагностическими JSON, включая неуспешные модели. Страницы обновляются по мере обработки.',
        '', '| Модель | Статус | Деталей | Собрана |','|---|---|---:|---|']
    for row in rows:
        result='да' if row['assembly_success'] else 'нет' if row['completed'] else 'ожидается'
        lines.append(f'| [{row["model"]}]({row["catalog"]}) | {row["status"]} | {row["components"] if row["components"] is not None else "—"} | {result} |')
    lines.extend(['',f'Успех среди обработанных: {counts["success"]}/{counts["completed"]} ({100*counts["success"]/counts["completed"]:.2f}%). Timeout учитывается отдельно от обычных отказов.', '', 'Не обработаны: '+', '.join(row['model'] for row in rows if not row['completed'])+'.', '', 'Продолжение: `python -m cadgen.benchmark_supervisor` из корня Python-проекта. Сохранённые terminal-результаты, включая timeout, пропускаются; лимит каждой новой модели — 900 секунд. Исходники не генерируются заново.', '', 'Незавершённая попытка №75 сохранена в `interrupted/model_75/`; она не входит в статистику и не мешает продолжить с №75.'])
    failures=Counter((row['status'],row['reason']) for row in rows if row['completed'] and not row['assembly_success'])
    lines.extend(['','## Причины неуспеха','', '| Статус | Причина | Моделей |','|---|---|---:|'])
    for (state,reason),count in failures.items():lines.append(f'| {state} | {reason} | {count} |')
    write(ROOT/'README.md','\n'.join(lines)+'\n')
    write(ROOT/'generated_files.json',json.dumps(sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.suffix!='.tmp'),indent=2))
    return done

if __name__=='__main__':
    # Also terminates the existing runpy-based report monitor once this run is complete.
    if summarize():raise SystemExit(0)
