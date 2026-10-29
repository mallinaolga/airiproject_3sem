"""Try existing joint builders on a completed, immutable geometric partition."""

from itertools import combinations

import numpy as np

from .assembly_geometry import GeometryRejected, Split, contact_patch, frame
from .assembly_validation import overlap_volume, transform_part


def assemble_partition(state, seed, geometry, settings, connection="auto", profile="auto", *, edge_callback=None, joint_search=None, contact_function=None, incremental_validation=False):
    from .assembly_planning import assembly_graph, validate_partition
    from .joint_design import materialize, propose_joints

    contact_function=contact_function or contact_patch
    geometry.validate()
    state.joints, state.sequence = [], []
    trials, edges = [], []
    identifiers = tuple(state.raw)
    state.assembly = dict(status="searching",success=False,geometric_components=list(identifiers),
                          partition_modified=False,trials=trials)
    for a,b in combinations(identifiers,2):
        patch = contact_function(state.raw[a],state.raw[b])
        if patch.Area()<=1e-7:
            continue
        entry = dict(components=[a,b],interface_area=patch.Area())
        if len(trials)>=settings.max_candidates:
            state.assembly.update(status="technical_limit_reached",reason="assembly interface budget",trials=trials)
            return state
        try:
            if joint_search is not None:
                options=joint_search(a,b)
            else:
                face = max(patch.Faces(),key=lambda f:f.Area())
                normal = np.array(face.normalAt().toTuple())
                origin = np.array(face.Center().toTuple())
                r = frame(normal)
                local = lambda s:transform_part(s,r.T,-r.T@origin)
                # The normal points out of a, so a is the lower/receiver side.
                split = Split(local(state.raw[a].fuse(state.raw[b])),local(state.raw[a]),
                              local(state.raw[b]),r,origin,dict(final_geometric_neighbours=True))
                options = propose_joints(split,(b,a),f"e{len(trials)+1}",seed,geometry,connection,profile)
            entry.update(status="options_found",options=len(options),
                         joint_types=sorted(set(o.parameters["type"] for o in options)),
                         adaptive_search=options[0].selection.get("adaptive_search"),
                         constructive_search=options[0].selection.get("constructive_search"),
                         designs=[o.metadata() for o in options])
            if edge_callback:
                edge_callback(a,b,options)
            edges.append((a,b,options))
        except Exception as error:
            entry.update(status="rejected",reason=f"{type(error).__name__}: {error}",
                         adaptive_search=getattr(error,"report",None))
        trials.append(entry)
        if edge_callback:
            edge_callback(a,b,None,entry)

    reached = {identifiers[0]}
    while True:
        before = len(reached)
        for a,b,_ in edges:
            if a in reached or b in reached:
                reached.update((a,b))
        if len(reached)==before:
            break
    if len(reached)!=len(identifiers):
        state.assembly.update(status="failed",reason="No connected joint graph on the fixed geometric constituents",
                              unreachable_components=sorted(set(identifiers)-reached))
        return state

    visited, limited, failures = 0, False, []
    seen_joint_sets=set();rejected_joint_sets=set();compatibility={}
    def compatible(first,second):
        key=tuple(sorted((id(first),id(second))))
        if key not in compatibility:
            a=first.zone.BoundingBox();b=second.zone.BoundingBox()
            separate=(a.xmin>b.xmax or b.xmin>a.xmax or a.ymin>b.ymax or b.ymin>a.ymax or a.zmin>b.zmax or b.zmin>a.zmax)
            compatibility[key]=separate or overlap_volume(first.zone,second.zone)<=geometry.volume_tolerance
        return compatibility[key]

    def search(reached, joints):
        nonlocal visited, limited
        signature=frozenset(id(joint) for joint in joints)
        if signature in seen_joint_sets:
            return False
        if visited>=settings.max_sequence_states:
            limited = True
            return False
        seen_joint_sets.add(signature)
        visited += 1
        if incremental_validation and len(reached)<len(identifiers):
            possible=set(reached)
            viable=[(a,b) for a,b,options in edges if any(
                all(compatible(option,old) for old in joints) for option in options[:settings.max_connection_trials])]
            while True:
                before=len(possible)
                for left,right in viable:
                    if left in possible or right in possible:possible.update((left,right))
                if len(possible)==before:break
            if len(possible)<len(identifiers):
                failures.append(dict(reason="no remaining compatible joint graph",unreachable=sorted(set(identifiers)-possible)))
                return False
        if len(reached)==len(identifiers):
            try:
                parts = materialize(state.raw,joints,geometry)
                checks, sequence = validate_partition(state.original,state.raw,parts,joints,geometry,
                                                      settings.max_sequence_states)
                checks["graph"] = assembly_graph(state.raw,joints,geometry,contact_function)
                state.joints, state.sequence = joints, sequence
                state.checks.update(checks)
                return True
            except Exception as error:
                failures.append(dict(reason=f"{type(error).__name__}: {error}",
                                     joints=[dict(id=j.id,components=list(j.owners),
                                                  profile=j.parameters.get("profile",{}).get("kind")) for j in joints]))
                return False
        for a,b,options in edges:
            if (a in reached)==(b in reached):
                continue
            for option in options[:settings.max_connection_trials]:
                if any(not compatible(option,old) for old in joints):
                    failures.append(dict(edge=[a,b],reason="joint protected zones conflict"))
                    continue
                trial_signature=frozenset(id(j) for j in joints+[option])
                if incremental_validation and (trial_signature in rejected_joint_sets or trial_signature in seen_joint_sets):continue
                if incremental_validation:
                    try:
                        partial=materialize(state.raw,joints+[option],geometry)
                        changed={n for j in joints+[option] for n in (*j.owners,*(h[0] for h in j.hardware))}
                        collisions=[dict(components=[left,right],volume=overlap_volume(partial[left],partial[right]))
                                    for left,right in combinations(partial,2) if left in changed or right in changed]
                        if any(c['volume']>geometry.volume_tolerance for c in collisions):
                            rejected_joint_sets.add(trial_signature)
                            failures.append(dict(edge=[a,b],reason="incremental collision with another current component",
                                                 collisions=[c for c in collisions if c['volume']>geometry.volume_tolerance]))
                            continue
                    except Exception as error:
                        rejected_joint_sets.add(trial_signature)
                        failures.append(dict(edge=[a,b],reason=f"incremental materialization: {error}"))
                        continue
                if search(reached|{a,b},joints+[option]):
                    return True
                if limited:
                    return False
        return False

    success = search({identifiers[0]},[])
    state.assembly.update(status="success" if success else "technical_limit_reached" if limited else "failed",
                          success=success,search_states=visited,global_rejections=failures,
                          representative_options_per_edge=settings.max_connection_trials,
                          exhaustive_joint_search=False,
                          incremental_validation=incremental_validation,
                          incremental_pruning_can_exclude_future_joint_clearances=incremental_validation)
    if not success:
        state.assembly["reason"] = "No validated complete assembly of the fixed constituents within the search"
    assert tuple(state.raw)==identifiers
    return state
