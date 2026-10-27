"""Persist geometric constituents before any fastener or assembly attempt."""

from dataclasses import asdict
from pathlib import Path

import cadquery as cq
import numpy as np
import trimesh

from .assembly_geometry import GeometryRejected, difference_volume
from .assembly_validation import transform_part
from .decomposition import validate_raw_partition


def export_geometry(state, target, settings, source=None, program=None):
    from .auto_assembly import layout, renamed
    from .assembly_generator import location, save_json

    target = Path(target)
    target.mkdir(parents=True,exist_ok=False)
    names = {n:f"part_{i}" for i,n in enumerate(sorted(state.raw),1)}
    shifts = layout(state.raw,max(8,state.original.BoundingBox().DiagonalLength*.05))
    meta = dict(schema_version=3,stage="geometry",status="exporting",geometry_success=False,
                assembly_success=False,assembly_status=state.assembly["status"],
                source=source,decomposition_settings=asdict(settings),component_id_map=names,
                main_component_count=len(state.raw),cut_count=len(state.cuts),cuts=state.cuts,
                stopping_conditions=renamed(state.stops,names),checks=renamed(state.checks,names),
                raw_components=[],stl_exports={})
    save_json(target/"metadata.json",meta)

    def stl(shape,name):
        path = target/name
        cq.exporters.export(shape,str(path),tolerance=.1,angularTolerance=.15)
        mesh = trimesh.load(str(path),force="mesh")
        if not len(mesh.faces) or not np.isfinite(mesh.vertices).all() or mesh.volume<=0:
            raise GeometryRejected(f"Invalid geometric STL: {name}")
        meta["stl_exports"][name] = dict(bytes=path.stat().st_size,triangles=len(mesh.faces))

    try:
        cq.exporters.export(state.original,str(target/"original.step"))
        stl(state.original,"original.stl")
        if program:(target/"original.py").write_text(program,encoding="utf-8")
        placed = cq.Assembly(name="geometric_partition")
        exploded = cq.Assembly(name="geometric_constituents")
        loaded = {}
        for old,shape in sorted(state.raw.items()):
            name = names[old]
            center = np.array(shape.Center().toTuple())
            local = shape.translate(tuple(-center))
            cq.exporters.export(local,str(target/f"{name}.step"))
            stl(local,f"{name}.stl")
            placed.add(local,name=name,loc=location(np.eye(3),center))
            exploded.add(local,name=name,loc=location(np.eye(3),center+shifts[old]))
            record = dict(name=name,step=f"{name}.step",stl=f"{name}.stl",volume=shape.Volume(),
                          rotation_matrix=np.eye(3).tolist(),translation=center.tolist(),
                          exploded_translation=(center+shifts[old]).tolist())
            meta["raw_components"].append(record)
            read = cq.importers.importStep(str(target/record["step"])).val()
            loaded[old] = transform_part(read,np.eye(3),center)
            if difference_volume(shape,loaded[old])>1e-5:
                raise GeometryRejected(f"Geometric STEP changed: {name}")
        placed.save(str(target/"geometric_partition.step"),exportType="STEP")
        exploded.save(str(target/"split_exploded.step"),exportType="STEP")
        stl(placed.toCompound(),"geometric_partition.stl")
        stl(exploded.toCompound(),"split_exploded.stl")
        checks = validate_raw_partition(state.original,loaded)
        for filename in ("geometric_partition.step","split_exploded.step"):
            read = cq.importers.importStep(str(target/filename)).solids().vals()
            if len(read)!=len(state.raw) or not all(s.isValid() for s in read):
                raise GeometryRejected(f"Lost geometric constituents in {filename}")
        meta["checks"].update(checks,step_placements_verified=True,all_stl_readable=True)
        meta.update(status="geometry_exported",geometry_success=True)
        save_json(target/"metadata.json",meta)
        return meta
    except Exception as error:
        meta.update(status="geometry_export_failed",error=f"{type(error).__name__}: {error}")
        save_json(target/"metadata.json",meta)
        raise
