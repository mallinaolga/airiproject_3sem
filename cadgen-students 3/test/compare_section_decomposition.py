"""Compare two independent stages on existing STEP sources, without generation."""

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time

import cadquery as cq

from cadgen.assembly_geometry import AssemblySettings
from cadgen.assembly_source import decomposition_history
from cadgen.assembly_validation import transform_part
from cadgen.auto_assembly import export_auto, renamed
from cadgen.decomposition import Budget, DecompositionSettings, Partition, decompose_geometry, finalize_geometry
from cadgen.decomposition_assembly import assemble_partition
from cadgen.decomposition_export import export_geometry
from cadgen.section_analysis import recognize


def save(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")


def checksums(folder):
    return {str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob("*")) if p.is_file()}


def audit_existing(target):
    target=Path(target).resolve()
    rows=[]
    for folder in sorted(target.glob("model_*")):
        geometry_folder=folder/"geometry" if (folder/"geometry").exists() else folder
        meta=json.loads((geometry_folder/"metadata.json").read_text())
        settings=DecompositionSettings(**meta["decomposition_settings"])
        for c in meta["raw_components"]:
            shape=cq.importers.importStep(str(geometry_folder/c["step"])).val()
            shape=transform_part(shape,c["rotation_matrix"],c["translation"])
            recognition=recognize(shape,Budget(settings.max_operations))[0]
            stored=meta["stopping_conditions"][c["name"]]
            same=recognition["simple"]==stored.get("analysis",{}).get("recognition",{}).get("simple",False)
            rows.append(dict(model=folder.name,component=c["name"],recognition=recognition,
                             stored_stop=stored["reason"],stored_classification_matches=same))
    result=dict(status="passed" if all(r["stored_classification_matches"] for r in rows) else "failed",
                components=rows,all_stored_simple_classifications_match=all(r["stored_classification_matches"] for r in rows))
    save(target/"recognition_audit.json",result)
    return result


def model_detail(folder,old,previous,state,geometric):
    names=geometric["component_id_map"]
    lines=[f"# {folder.name}: геометрия и сборка", "",
           f"Прежде было {previous} частей. Геометрия теперь содержит {len(state.raw)} компонентов.","",
           "## Элементы исходной модели", "",
           "Операции исходного CADGen (подсказки, проверяемые конечным B-Rep):", "", "```python"]
    lines.extend(line for line in (folder/"geometry"/"original.py").read_text().splitlines() if line.startswith("r="))
    lines.extend(["```", "", "## Выполненные естественные разрезы", "",
                  "| Узел | Начало плоскости | Нормаль | Дочерние компоненты |", "|---|---|---|---|"])
    for cut in state.cuts:
        p=cut["selected"]["plane"]
        lines.append(f"| {cut['node']} | {p['origin']} | {p['normal']} | {cut['children']} |")
    lines.extend(["", "## Предложенные и отклонённые разрезы", "",
                  "Журнал сохранённых плоскостей, их источников и причин решения: [geometric_analysis.json](geometric_analysis.json).", ""])
    for node,analysis in state.checks["geometric_analyses"].items():
        counter=Counter(p.get("reason",p.get("status","not_checked")) for p in analysis.get("proposed_planes",[]))
        if counter:lines.append(f"- `{node}`: {dict(counter)}.")
    lines.extend(["", "Допустимые альтернативы не отменяются из-за креплений: выбирается лучший геометрический разрез, затем его дети исследуются заново.", "",
                  "## Конечные геометрические компоненты", "",
                  "| Компонент | Простой | Причина остановки | Поверхности B-Rep |", "|---|---|---|---|"])
    for n,shape in sorted(state.raw.items()):
        stop=state.stops[n]
        simple=stop.get("analysis",{}).get("recognition",{}).get("simple",False)
        lines.append(f"| [{names[n]}](geometry/{names[n]}.stl) | {'да' if simple else 'нет'} | {stop['reason']} | {dict(Counter(f.geomType() for f in shape.Faces()))} |")
    lines.extend(["", "## Геометрическое объединение случайных фрагментов", "",
                  "Союз соседей принимается только при подтверждении одного постоянного сечения и сохранении всего материала.", ""])
    for merge in state.checks.get("geometry_merges",[]):
        lines.append(f"- {merge['components']} → {merge['result']}: {merge['reason']}.")
    lines.extend(["", "При лимите разрезов остаточные компоненты дополнительно классифицируются в отдельном ограниченном бюджете. "
                  "Часть может иметь подтверждённое сечение и одновременно запись о ранее достигнутом лимите поиска.", "",
                  "## Отдельный этап сборки", "",
                  f"Статус: `{state.assembly['status']}`. {state.assembly.get('reason','Все геометрические компоненты участвуют в проверенной сборке.')}", "",
                  "[Полный отчёт креплений](assembly_report.json). Неудача сборки не меняет геометрические компоненты.", ""])
    (folder/"ANALYSIS.md").write_text("\n".join(lines),encoding="utf-8")


def run(source,target,previous=None,reuse_geometry=None):
    source,target=Path(source).resolve(),Path(target).resolve()
    if target==source or source in target.parents:raise ValueError("Output must be outside original examples")
    before=checksums(source);target.mkdir(parents=True,exist_ok=False)
    previous=Path(previous) if previous else None
    report=dict(stage_separation=True,status="running",source_generation_performed=False,
                source=str(source),models=[],settings=asdict(DecompositionSettings()))
    save(target/"report.json",report)
    for original_folder in sorted(source.glob("model_*")):
        started=time.monotonic();old=json.loads((original_folder/"metadata.json").read_text())
        old_count=old["main_component_count"]
        if previous and (previous/original_folder.name/"metadata.json").exists():
            old_count=json.loads((previous/original_folder.name/"metadata.json").read_text())["main_component_count"]
        row=dict(model=original_folder.name,previous_components=old_count,base_components=old["main_component_count"])
        folder=target/original_folder.name;folder.mkdir()
        try:
            original=cq.importers.importStep(str(original_folder/"original.step")).val()
            settings=DecompositionSettings();geometry=AssemblySettings(**old["settings"])
            history=decomposition_history(old["source"])
            if reuse_geometry:
                cached=Path(reuse_geometry)/original_folder.name/"geometry"
                meta=json.loads((cached/"metadata.json").read_text())
                if meta["decomposition_settings"]!=asdict(settings):
                    raise ValueError("Cached geometric settings differ from current settings")
                inverse={v:k for k,v in meta["component_id_map"].items()}
                raw={}
                for c in meta["raw_components"]:
                    shape=cq.importers.importStep(str(cached/c["step"])).val()
                    raw[inverse[c["name"]]]=transform_part(shape,c["rotation_matrix"],c["translation"])
                state=Partition(original,raw,stops=renamed(meta["stopping_conditions"],inverse),
                                cuts=meta["cuts"],checks=renamed(meta["checks"],inverse))
                state=finalize_geometry(state,settings,history)
            else:
                state=decompose_geometry(original,settings,history=history)
            geometric=export_geometry(state,folder/"geometry",settings,old["source"],(original_folder/"original.py").read_text())
            save(folder/"geometric_analysis.json",dict(cuts=state.cuts,merges=state.checks.get("geometry_merges",[]),stops=state.stops,
                                                       analyses=state.checks["geometric_analyses"]))
            save(folder/"metadata.json",dict(status="geometry_exported",success=False,geometry_success=True,
                 main_component_count=len(state.raw),assembly_status="not_attempted"))
            print(f"GEOMETRY {folder.name}: {len(state.raw)} constituents saved",flush=True)
            try:assemble_partition(state,old["seed"],geometry,settings)
            except Exception as error:
                state.assembly=dict(status="failed",success=False,partition_modified=False,reason=f"{type(error).__name__}: {error}")
            save(folder/"assembly_report.json",state.assembly)
            ready=None
            if state.assembly["success"]:
                ready=export_auto(state,old["seed"],old["source"],(original_folder/"original.py").read_text(),
                                  folder/"assembly",geometry,settings,dict(decomposition="auto",source="existing_STEP"))
            simple=sum(s.get("analysis",{}).get("recognition",{}).get("simple",False) for s in state.stops.values())
            row.update(status="analyzed",geometry_success=True,components=len(state.raw),simple=simple,
                unrecognized=len(state.raw)-simple,assembly_success=bool(ready),assembly_status=state.assembly["status"],
                assembly_reason=state.assembly.get("reason"),stopping_reasons=dict(Counter(s["reason"] for s in state.stops.values())),
                cuts=len(state.cuts),geometric_merges=len(state.checks.get("geometry_merges",[])),geometry_checks=geometric["checks"]["geometric_partition_valid"])
            model_detail(folder,old,old_count,state,geometric)
            save(folder/"metadata.json",dict(row,success=bool(ready),main_component_count=len(state.raw),
                                            geometry_folder="geometry",assembly_folder="assembly" if ready else None))
        except Exception as error:row.update(status="error",reason=f"{type(error).__name__}: {error}")
        row["elapsed_seconds"]=round(time.monotonic()-started,3)
        report["models"].append(row);save(target/"report.json",report)
        print(json.dumps(row,ensure_ascii=False),flush=True)
    report.update(status="complete",original_examples_unchanged=before==checksums(source),source_checksums=before)
    save(target/"report.json",report)
    assert report["original_examples_unchanged"]
    lines=["# Геометрия отдельно от сборки", "",
           "Прежние исходники STEP; CADGen не запускался. Геометрические STL сохранены независимо от результата сборки.", "",
           "| Модель | Было частей | Геометрических составляющих | Простых | Не распознано | Удалось собрать |", "|---|---:|---:|---:|---:|---|"]
    for row in report["models"]:
        if row["status"]=="analyzed":
            lines.append(f"| [{row['model']}]({row['model']}/ANALYSIS.md) | {row['previous_components']} | {row['components']} | {row['simple']} | {row['unrecognized']} | {'да' if row['assembly_success'] else 'нет'} |")
        else:lines.append(f"| {row['model']} | {row['previous_components']} | ошибка | | | {row['reason']} |")
    lines.extend(["", "В каждом каталоге `geometry/` лежат отдельные STEP/STL частей, исходник и разнесённый вид `split_exploded.stl`.",
                  "Каталог `assembly/` появляется только при проверенной сборке всех тех же частей. Причины отказов — `assembly_report.json`.", ""])
    (target/"README.md").write_text("\n".join(lines),encoding="utf-8")
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",default="examples/assemblies")
    parser.add_argument("--output",default="generations/assemblies/two_stage_comparison")
    parser.add_argument("--previous",default="generations/assemblies/section_comparison")
    parser.add_argument("--audit-existing",action="store_true")
    parser.add_argument("--reuse-geometry",help="Optional saved geometric partition; reclassify and merge without recutting")
    args=parser.parse_args()
    if args.audit_existing:
        report=audit_existing(args.output);raise SystemExit(report["status"]!="passed")
    report=run(args.source,args.output,args.previous,args.reuse_geometry)
    raise SystemExit(any(r["status"]!="analyzed" for r in report["models"]))
