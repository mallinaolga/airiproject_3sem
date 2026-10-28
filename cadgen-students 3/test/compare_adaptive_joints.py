"""Attempt joints on the saved 86 components; never run CADGen or decomposition."""

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time

import cadquery as cq

from cadgen.assembly_geometry import AssemblySettings, difference_volume
from cadgen.assembly_validation import transform_part
from cadgen.auto_assembly import export_auto, renamed
from cadgen.decomposition import DecompositionSettings, Partition
from cadgen.decomposition_assembly import assemble_partition
from cadgen.joint_design import materialize


def save(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")


def hashes(folder):
    return {str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob("*") if p.is_file()}


def load_partition(folder):
    meta=json.loads((folder/"metadata.json").read_text())
    raw={c["name"]:transform_part(cq.importers.importStep(str(folder/c["step"])).val(),
                                      c["rotation_matrix"],c["translation"])
         for c in meta["raw_components"]}
    original=cq.importers.importStep(str(folder/"original.step")).val()
    # Do not reclassify, merge, split or otherwise alter the saved constituents.
    names=meta["component_id_map"]
    state=Partition(original,raw,stops=meta["stopping_conditions"],cuts=meta["cuts"],
                    checks=renamed(meta["checks"],names))
    return state,meta


def run(source,output,models):
    source,output=Path(source).resolve(),Path(output).resolve()
    if output==source or source in output.parents:
        raise ValueError("Output must be outside the immutable source results")
    output.mkdir(parents=True,exist_ok=False)
    snapshot=hashes(source)
    report=dict(status="running",source=str(source),cadgen_run=False,decomposition_run=False,
                fixed_partition=True,models=[])
    save(output/"report.json",report)
    for index in models:
        name=f"model_{index:02d}";started=time.monotonic()
        folder=output/name;folder.mkdir()
        state,meta=load_partition(source/name/"geometry")
        geometry=AssemblySettings();settings=DecompositionSettings(**meta["decomposition_settings"])
        signatures={n:s.Volume() for n,s in state.raw.items()}
        row=dict(model=name,components=len(state.raw),assembly_success=False)
        print(f"START {name}: {len(state.raw)} unchanged components",flush=True)

        def edge_callback(a,b,options,entry=None):
            if entry is not None:
                save(folder/f"{a}__{b}_report.json",entry)
                print(f"  {a}/{b}: {entry['status']}, options={entry.get('options',0)}",flush=True)
                return
            # A representative locally validated joint, not a claim that the
            # whole model is assemblable. Unmodified neighbours are not added.
            target=folder/"pair_candidates"/f"{a}__{b}";target.mkdir(parents=True)
            selected=options[0]
            raw={a:state.raw[a],b:state.raw[b]}
            parts=materialize(raw,[selected],geometry)
            assembly=cq.Assembly(name="locally_validated_pair")
            for n,s in parts.items():
                assembly.add(s,name=n)
            assembly.save(str(target/"pair.step"),exportType="STEP")
            cq.exporters.export(assembly.toCompound(),str(target/"pair.stl"),tolerance=.03,angularTolerance=.1)
            save(target/"metadata.json",dict(local_pair_validation=True,full_model_assembly_validated=False,
                 selected=selected.metadata(),alternatives=[o.metadata() for o in options],
                 note="Local candidates only; consult the model assembly_report.json for global results."))

        try:
            assemble_partition(state,meta.get("seed",42),geometry,settings,edge_callback=edge_callback)
            row.update(assembly_status=state.assembly["status"],assembly_success=state.assembly["success"],
                       reason=state.assembly.get("reason"))
        except Exception as error:
            state.assembly.update(status="error",success=False,reason=f"{type(error).__name__}: {error}")
            row.update(assembly_status="error",reason=state.assembly["reason"])
        save(folder/"assembly_report.json",state.assembly)
        trials=state.assembly.get("trials",[])
        row["contact_pairs"]=len(trials)
        row["groove_pairs"]=sum("groove" in e.get("joint_types",[]) for e in trials)
        row["bolted_pairs"]=sum("bolted" in e.get("joint_types",[]) for e in trials)
        row["selected_joint_types"]=dict(Counter(j.parameters["type"] for j in state.joints))
        row["selected_joints"]=len(state.joints)
        row["rejected_pairs"]=sum(e["status"]=="rejected" for e in trials)
        if state.assembly["success"]:
            try:
                export_auto(state,42,meta["source"],(source/name/"geometry"/"original.py").read_text(),
                            folder/"assembly",geometry,settings,dict(source="two_stage_final",adaptive_joints=True))
                row["assembly_folder"]="assembly"
            except Exception as error:
                row.update(assembly_success=False,assembly_status="export_failed",export_error=str(error))
        assert signatures=={n:s.Volume() for n,s in state.raw.items()}
        row.update(partition_unchanged=True,elapsed_seconds=round(time.monotonic()-started,3))
        save(folder/"metadata.json",row)
        report["models"].append(row);save(output/"report.json",report)
        print(json.dumps(row,ensure_ascii=False),flush=True)
    report.update(status="complete",source_checksums_unchanged=hashes(source)==snapshot,source_checksums=snapshot)
    save(output/"report.json",report)
    assert report["source_checksums_unchanged"]
    write_readme(report,output)
    return report


def write_readme(report,output):
    lines=["# Адаптивные соединения сохранённых компонентов", "",
        "CADGen и декомпозиция не запускались. Пары в `pair_candidates/` проверены локально; "
        "они не означают успех сборки всей модели. `assembly/` экспортируется только после полной проверки.", "",
        "| Модель | Компонентов | Контактных пар | Пар с пазом | Пар с болтами | Полностью собрано |",
        "|---|---:|---:|---:|---:|---|"]
    for row in sorted(report["models"],key=lambda r:r["model"]):
        name=row["model"]
        lines.append(f"| [{name}]({name}/assembly_report.json) | {row['components']} | {row['contact_pairs']} | "
                     f"{row['groove_pairs']} | {row['bolted_pairs']} | {'да' if row['assembly_success'] else 'нет'} |")
    lines.extend(["", "Число пазовых пар — локально проверенные альтернативы. В готовой сборке выбирается "
        "дерево соединений на всех компонентах; остальные пары не устанавливаются одновременно.", "",
        "## Готовые файлы", ""])
    for row in sorted(report["models"],key=lambda r:r["model"]):
        if row["assembly_success"]:
            name=row["model"]
            lines.append(f"- {name}: [сборка STL]({name}/assembly/assembly.stl), "
                f"[STEP]({name}/assembly/assembly.step), "
                f"[детали с креплениями]({name}/assembly/parts_exploded.stl); "
                f"установлено {row['selected_joints']} креплений.")
    lines.extend(["", "Подробные отказы, бюджеты, варианты профилей и зазоры — в JSON каждой контактной пары. "
        "Конечное число положений на пути не доказывает непрерывную бесстолкновительную вставку; "
        "прочность, изготовимость и механическое удержание не проверялись.", ""])
    (output/"README.md").write_text("\n".join(lines),encoding="utf-8")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",default="generations/assemblies/two_stage_final")
    parser.add_argument("--output",default="generations/assemblies/adaptive_joints")
    parser.add_argument("--models",nargs="+",type=int,default=[3,1,2,4,5,6,7,8,9,10])
    args=parser.parse_args()
    run(args.source,args.output,args.models)
