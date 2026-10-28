"""Try existing joint builders on a completed, immutable geometric partition."""

from itertools import combinations

import numpy as np

from .assembly_geometry import GeometryRejected, Split, contact_patch, frame
from .assembly_validation import overlap_volume, transform_part


def assemble_partition(state, seed, geometry, settings, connection="auto", profile="auto", *, edge_callback=None):
    from .assembly_planning import assembly_graph, validate_partition
    from .joint_design import materialize, propose_joints

    geometry.validate()
    state.joints, state.sequence = [], []
    trials, edges = [], []
    identifiers = tuple(state.raw)
    state.assembly = dict(status="searching",success=False,geometric_components=list(identifiers),
                          partition_modified=False,trials=trials)
    for a,b in combinations(identifiers,2):
        patch = contact_patch(state.raw[a],state.raw[b])
        if patch.Area()<=1e-7:
            continue
        entry = dict(components=[a,b],interface_area=patch.Area())
        if len(trials)>=settings.max_candidates:
            state.assembly.update(status="technical_limit_reached",reason="assembly interface budget",trials=trials)
            return state
        try:
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
    seen_joint_sets=set()

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
        if len(reached)==len(identifiers):
            try:
                parts = materialize(state.raw,joints,geometry)
                checks, sequence = validate_partition(state.original,state.raw,parts,joints,geometry,
                                                      settings.max_sequence_states)
                checks["graph"] = assembly_graph(state.raw,joints,geometry)
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
                if any(overlap_volume(option.zone,old.zone)>geometry.volume_tolerance for old in joints):
                    failures.append(dict(edge=[a,b],reason="joint protected zones conflict"))
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
                          exhaustive_joint_search=False)
    if not success:
        state.assembly["reason"] = "No validated complete assembly of the fixed constituents within the search"
    assert tuple(state.raw)==identifiers
    return state
