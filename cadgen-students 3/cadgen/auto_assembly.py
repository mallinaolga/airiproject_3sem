"""Automatic decomposition workflow, four views, curated GitHub examples."""

from collections import Counter
from dataclasses import asdict
from pathlib import Path
import json
import math
import random
import shutil
import time

import cadquery as cq
import numpy as np
import trimesh

from .assembly_geometry import AssemblySettings, GeometryRejected, difference_volume
from .assembly_source import generate_source, decomposition_history
from .decomposition import DecompositionSettings, decompose_geometry
from .decomposition_assembly import assemble_partition
from .decomposition_export import export_geometry
from .joint_design import materialize


def renamed(value, names):
    if isinstance(value,str):return names.get(value,value)
    if isinstance(value,list):return [renamed(v,names) for v in value]
    if isinstance(value,tuple):return [renamed(v,names) for v in value]
    if isinstance(value,dict):
        return {"/".join(names.get(p,p) for p in k.split("/")):renamed(v,names) for k,v in value.items()}
    return value


def layout(shapes,margin):
    """Separate bounding rectangles by translation only; no mesh/model scaling."""
    names=list(shapes)
    columns=max(1,math.ceil(math.sqrt(len(names))))
    boxes={n:s.BoundingBox() for n,s in shapes.items()}
    widths=[max((boxes[n].xlen for i,n in enumerate(names) if i%columns==col),default=0)+margin
            for col in range(columns)]
    heights=[max((boxes[n].ylen for n in names[row*columns:(row+1)*columns]),default=0)+margin
             for row in range(math.ceil(len(names)/columns))]
    translations={}
    for i,n in enumerate(names):
        b=boxes[n];col=i%columns;row=i//columns
        center=np.array([(b.xmin+b.xmax)/2,(b.ymin+b.ymax)/2,(b.zmin+b.zmax)/2])
        target=np.array([sum(widths[:col])+widths[col]/2,sum(heights[:row])+heights[row]/2,0])
        translations[n]=target-center
    for i,a in enumerate(names):
        for b in names[i+1:]:
            aa,bb=shapes[a].translate(tuple(translations[a])).BoundingBox(),shapes[b].translate(tuple(translations[b])).BoundingBox()
            if not (aa.xmax < bb.xmin or bb.xmax < aa.xmin or aa.ymax < bb.ymin or bb.ymax < aa.ymin):
                raise GeometryRejected("Exploded layout overlaps")
    return translations


def export_auto(state,seed,parameters,program,target,geometry,settings,request):
    from .assembly_generator import save_json,location
    if not state.assembly.get("success"):
        raise GeometryRejected("Ready assembly export requires success on all fixed geometric constituents")
    target=Path(target);target.mkdir(parents=True,exist_ok=False)
    raw_names={name:f"part_{i}" for i,name in enumerate(sorted(state.raw),1)}
    hardware_names={};b=0;n=0;screw_count=0
    for joint in state.joints:
        for name,_ in joint.hardware:
            if "_bolt_" in name:b+=1;hardware_names[name]=f"bolt_{b}"
            elif "_screw_" in name:screw_count+=1;hardware_names[name]=f"screw_{screw_count}"
            else:n+=1;hardware_names[name]=f"nut_{n}"
    names=dict(raw_names,**hardware_names)
    parts=materialize(state.raw,state.joints,geometry)
    ordered=[*sorted(state.raw),*hardware_names]
    parts={name:parts[name] for name in ordered}
    exploded=layout(parts,max(8,state.original.BoundingBox().DiagonalLength*.05))
    split_exploded=layout(state.raw,max(8,state.original.BoundingBox().DiagonalLength*.05))
    metadata=dict(schema_version=2,status="exporting",success=False,seed=seed,units="mm",
        request=request,source=parameters,settings=asdict(geometry),decomposition_settings=asdict(settings),
        assembly_status=state.assembly["status"],assembly_report=state.assembly,
        main_component_count=len(state.raw),cut_count=len(state.cuts),
        joints=renamed([j.metadata() for j in state.joints],names),
        graph=renamed(state.checks["graph"],names),cuts=state.cuts,
        stopping_conditions=renamed(state.stops,names),rejected_candidates=state.trials,
        checks=renamed(state.checks,names),assembly_sequence=renamed(state.sequence,names),
        counts=dict(main_components=len(state.raw),cuts=len(state.cuts),bolts=b,nuts=n,
                    grooves=sum(j.parameters["type"] in ("groove","combined") for j in state.joints),
                    protrusions=sum(j.parameters["type"] in ("groove","combined") for j in state.joints)),
        components=[],raw_components=[],component_id_map=names,
        note="Bounded heuristic decomposition; not all possible cuts. Finite trajectory samples "
             "do not prove continuous clearance. No thread or mechanical retention modeled.")
    if state.checks.get("method")=="constructive_operation_volumes":
        features=[f for j in state.joints for f in j.parameters.get("features",[])]
        grooves=sum(f["type"] in ("groove","cylindrical_fit") for f in features)
        metadata["counts"].update(grooves=grooves,protrusions=grooves,screws=screw_count,
            cylindrical_fits=sum(f["type"]=="cylindrical_fit" for f in features),
            constructive_components=len(state.raw))
    save_json(target/"metadata.json",metadata)

    def stl(shape,path):
        options=dict(tolerance=0.1,angularTolerance=0.15)
        cq.exporters.export(shape,str(path),**options)
        if path.stat().st_size>9_500_000:
            options=dict(tolerance=0.25,angularTolerance=0.25)
            cq.exporters.export(shape,str(path),**options)
        if path.stat().st_size>10_000_000:
            raise GeometryRejected(f"STL exceeds GitHub preview budget: {path.name}")
        mesh=trimesh.load(str(path),force="mesh")
        if not len(mesh.faces) or not np.isfinite(mesh.vertices).all() or mesh.volume<=0:
            raise GeometryRejected(f"Invalid STL export: {path.name}")
        return dict(bytes=path.stat().st_size,triangles=len(mesh.faces),**options)

    try:
        cq.exporters.export(state.original,str(target/"original.step"))
        metadata["stl_exports"]={"original.stl":stl(state.original,target/"original.stl")}
        if program:(target/"original.py").write_text(program,encoding="utf-8")
        assembly=cq.Assembly(name="assembly")
        exploded_assembly=cq.Assembly(name="parts_exploded")
        split_assembly=cq.Assembly(name="split_exploded")
        palette=[(0.2,.55,.9),(1.,.6,.15),(.3,.75,.4),(.7,.35,.85),(.85,.4,.4),(.25,.75,.8)]
        for index,(old,shape) in enumerate(parts.items()):
            name=names[old]
            center=np.array(shape.Center().toTuple())
            local=shape.translate(tuple(-center))
            cq.exporters.export(local,str(target/f"{name}.step"))
            metadata["stl_exports"][f"{name}.stl"]=stl(local,target/f"{name}.stl")
            color=cq.Color(*(palette[index%len(palette)] if old in state.raw else (.6,.62,.65)))
            assembly.add(local,name=name,loc=location(np.eye(3),center),color=color)
            exploded_assembly.add(local,name=name,loc=location(np.eye(3),center+exploded[old]),color=color)
            metadata["components"].append(dict(name=name,role="main" if old in state.raw else "bolt" if "_bolt_" in old else "screw" if "_screw_" in old else "nut",
                step=f"{name}.step",stl=f"{name}.stl",rotation_matrix=np.eye(3).tolist(),translation=center.tolist(),
                exploded_translation=(center+exploded[old]).tolist(),volume=shape.Volume()))
        for old,shape in sorted(state.raw.items()):
            name=names[old];center=np.array(shape.Center().toTuple());local=shape.translate(tuple(-center))
            cq.exporters.export(local,str(target/f"split_{name}.step"))
            metadata["stl_exports"][f"split_{name}.stl"]=stl(local,target/f"split_{name}.stl")
            split_assembly.add(local,name=name,loc=location(np.eye(3),center+split_exploded[old]))
            metadata["raw_components"].append(dict(name=name,step=f"split_{name}.step",stl=f"split_{name}.stl",
                rotation_matrix=np.eye(3).tolist(),translation=center.tolist(),
                exploded_translation=(center+split_exploded[old]).tolist(),volume=shape.Volume()))
        assembly.save(str(target/"assembly.step"),exportType="STEP")
        exploded_assembly.save(str(target/"exploded.step"),exportType="STEP")
        split_assembly.save(str(target/"split_exploded.step"),exportType="STEP")
        for filename,view in [("assembly.stl",assembly),("parts_exploded.stl",exploded_assembly),
                              ("split_exploded.stl",split_assembly)]:
            metadata["stl_exports"][filename]=stl(view.toCompound(),target/filename)
        loaded=cq.importers.importStep(str(target/"assembly.step"))
        if len(loaded.solids().vals())!=len(parts) or not all(s.isValid() for s in loaded.solids().vals()):
            raise GeometryRejected("STEP lost separate valid components")
        expected=cq.Compound.makeCompound(list(parts.values()))
        if difference_volume(expected,loaded.val())>geometry.volume_tolerance:
            raise GeometryRejected("STEP roundtrip geometry or placements changed")
        for filename,expected_count in (("exploded.step",len(parts)),("split_exploded.step",len(state.raw))):
            read=cq.importers.importStep(str(target/filename)).solids().vals()
            if len(read)!=expected_count or not all(s.isValid() for s in read):
                raise GeometryRejected(f"Invalid separated STEP view: {filename}")
        metadata["checks"].update(step_roundtrip_separate_solids=len(parts),step_placements_verified=True,
                                  all_stl_readable=True,exploded_layout_disjoint=True)
        metadata.update(status="success",success=True)
        save_json(target/"metadata.json",metadata)
        return metadata
    except Exception as error:
        metadata.update(status="export_failed",success=False,export_error=f"{type(error).__name__}: {error}")
        save_json(target/"metadata.json",metadata)
        raise


def export_examples(output,manifest,target):
    from .assembly_generator import save_json
    target=Path(target)
    if target.exists():raise FileExistsError("Examples directory already exists; preserving its contents")
    target.mkdir(parents=True)
    table=["# AIRI: результаты автоматической декомпозиции CADGen", "",
           "Реальные результаты алгоритма; не контрольные синтетические модели. "
           "Пути проверены дискретно, резьба и механическое удержание не моделируются.","",
           "| Модель | Seed | Частей | Разрезов | Пазов/выступов | Болтов/гаек | Соединения | Остановка | Проверка | Представления |",
           "|---|---:|---:|---:|---:|---|---|---|---|---|"]
    selected=[]
    for index,entry in enumerate(manifest["assemblies"][:10],1):
        name=f"model_{index:02d}"
        shutil.copytree(Path(output)/entry["folder"],target/name)
        meta=json.loads((target/name/"metadata.json").read_text())
        kinds=Counter(j["parameters"]["type"] for j in meta["joints"])
        grooves=sum(j["parameters"]["type"] in ("groove","combined") for j in meta["joints"])
        bolts=sum(c["role"]=="bolt" for c in meta["components"])
        stops=dict(Counter(v["reason"] for v in meta["stopping_conditions"].values()))
        views=" · ".join(f"[{label}]({name}/{file})" for label,file in [
            ("исходник","original.stl"),("разрезы","split_exploded.stl"),
            ("крепления","parts_exploded.stl"),("сборка","assembly.stl")])
        table.append(f"| [{index}]({name}/metadata.json) | {meta['seed']} | {meta['main_component_count']} | "
                     f"{meta['cut_count']} | {grooves}/{grooves} | {bolts}/{bolts} | {dict(kinds)} | {stops} | "
                     f"валидна, полный порядок найден | {views} |")
        selected.append(dict(model=name,**entry))
    table.extend(["",f"Seed серии: `{manifest['seed']}`. Успешных сборок: {manifest['successful_count']}/"
                  f"{manifest['requested_count']}; отклонено исходников: {len(manifest['failures'])}.","",
                  "Декомпозиция ограничена исследованным семейством сечений. `technical_limit_reached` "
                  "означает вычислительную остановку, а не отсутствие целесообразных разрезов.","",
                  "Число частей — результат геометрии и проверок, целевой диапазон не задавался.",""])
    (target/"README.md").write_text("\n".join(table),encoding="utf-8")
    save_json(target/"experiment.json",dict(manifest,assemblies=selected))


def generate_auto_batch(output,count=1,connection="auto",seed=None,profile="auto",source="cadgen",config=None,
                        max_attempts=8,geometry=None,settings=None,examples=None):
    from .assembly_generator import save_json
    geometry=geometry or AssemblySettings();settings=settings or DecompositionSettings()
    geometry.validate();settings.validate()
    if count<1 or max_attempts<1:raise ValueError("count and max_attempts must be positive")
    if connection not in ("auto","groove","bolted","combined"):raise ValueError("Unknown automatic connection mode")
    if profile=="random":raise ValueError("Use --profile auto for geometric profile selection in automatic mode")
    if examples and source!="cadgen":raise ValueError("Demonstration examples require real CADGen sources")
    if examples and Path(examples).exists():raise FileExistsError("Examples directory already exists")
    seed=random.SystemRandom().randrange(2**63) if seed is None else seed
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
    manifest=dict(schema_version=2,decomposition="auto",seed=seed,requested_count=count,successful_count=0,
        connection=connection,profile=profile,source=source,settings=asdict(geometry),
        decomposition_settings=asdict(settings),max_attempts_per_assembly=max_attempts,
        assemblies=[],failures=[],status="running")
    originals=[];start=time.monotonic()
    save_json(output/"manifest.json",manifest)
    for slot in range(count):
        stream=random.Random(f"auto-batch:{seed}:{slot}")
        for attempt in range(max_attempts):
            item_seed=seed if slot==0 and attempt==0 else stream.randrange(2**63)
            stage="source";state=None;parameters=None
            try:
                original,parameters,program=generate_source(item_seed,source,config,complexity="decomposition")
                if any(abs(s.Volume()-original.Volume())<geometry.volume_tolerance and
                       difference_volume(s,original)<=geometry.volume_tolerance for s in originals):
                    raise GeometryRejected("Duplicate source geometry")
                stage="decomposition"
                state=decompose_geometry(original,settings,history=decomposition_history(parameters))
                folder=f"assembly_{len(manifest['assemblies'])+1:04d}_slot_{slot+1:04d}_attempt_{attempt+1:02d}"
                geometry_folder=folder+"/geometry"
                stage="geometry_export"
                export_geometry(state,output/geometry_folder,settings,parameters,program)
                stage="assembly"
                assemble_partition(state,item_seed,geometry,settings,connection,profile)
                save_json(output/folder/"assembly_report.json",state.assembly)
                if len(state.raw)<2 or not state.assembly["success"]:
                    raise GeometryRejected(state.assembly.get("reason","Source has only one geometric constituent"))
                stage="export"
                meta=export_auto(state,item_seed,parameters,program,output/folder/"assembly",geometry,settings,
                                 dict(decomposition="auto",connection=connection,profile=profile,
                                      source=source,cad_config=str(config) if config else None))
                manifest["assemblies"].append(dict(folder=folder+"/assembly",geometry_folder=geometry_folder,seed=item_seed,
                    main_components=len(state.raw),cuts=len(state.cuts),
                    connection_types=dict(Counter(j.parameters["type"] for j in state.joints)),
                    decomposition_complete_within_search=state.checks["decomposition_complete_within_search"]))
                originals.append(original)
                manifest["successful_count"]=len(manifest["assemblies"])
                print(f"[{len(originals)}/{count}] {folder}: {len(state.raw)} main parts, {len(state.joints)} joints",flush=True)
                save_json(output/"manifest.json",manifest)
                break
            except Exception as error:
                failure=dict(slot=slot+1,attempt=attempt+1,seed=item_seed,stage=stage,
                             error_type=type(error).__name__,reason=str(error))
                if parameters:
                    failure["source_parameters"]={k:v for k,v in parameters.items() if k!="cad"}
                if state:
                    failure.update(stops=state.stops,assembly=state.assembly)
                    if stage in ("assembly","export"):
                        failure["geometry_folder"]=geometry_folder
                manifest["failures"].append(failure)
                print(f"Rejected slot {slot+1}/{count}, attempt {attempt+1}: {stage}: {error}",flush=True)
                save_json(output/"manifest.json",manifest)
    manifest.update(status="complete" if len(originals)==count else "incomplete",
                    elapsed_seconds=round(time.monotonic()-start,3),
                    failure_counts=dict(Counter(f["stage"]+":"+f["error_type"] for f in manifest["failures"])))
    save_json(output/"manifest.json",manifest)
    if examples:export_examples(output,manifest,examples)
    print(f"Successful automatic assemblies: {len(originals)}/{count}; {output}",flush=True)
    return manifest
