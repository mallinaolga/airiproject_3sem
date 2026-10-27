"""Undo collateral plane fragmentation only with an exact extrusion proof."""

from itertools import combinations

from .assembly_geometry import contact_patch
from .section_analysis import recognize


def coalesce_prisms(state, settings, history=None):
    from .decomposition import Budget, TechnicalLimit

    budget = Budget(settings.max_operations)
    merges = list(state.checks.get("geometry_merges",[]))
    cache, rejected = {}, []
    limited = False
    while True:
        contacts = []
        for a,b in combinations(sorted(state.raw),2):
            key = (a,b)
            if key in cache:
                if cache[key]>0:contacts.append((cache[key],a,b))
                continue
            aa,bb = state.raw[a].BoundingBox(),state.raw[b].BoundingBox()
            if any(getattr(aa,x+"max")<getattr(bb,x+"min")-1e-6 or
                   getattr(bb,x+"max")<getattr(aa,x+"min")-1e-6 for x in "xyz"):
                cache[key] = 0
                continue
            area = contact_patch(state.raw[a],state.raw[b]).Area()
            cache[key] = area if area>1e-7 else 0
            if area>1e-7:contacts.append((area,a,b))
        changed = False
        for area,a,b in sorted(contacts,key=lambda v:(-v[0],v[1],v[2])):
            key = (a,b)
            if cache[key]<0:
                continue
            try:
                budget.use(2)
                joined = state.raw[a].fuse(state.raw[b]).clean()
                if len(joined.Solids())!=1 or not joined.isValid():
                    cache[key] = -1
                    continue
                # Sequential complement avoids an intermediate boolean union
                # silently filling a genuine source cavity.
                if (joined.cut(state.raw[a]).cut(state.raw[b]).Volume()>1e-5 or
                    state.raw[a].cut(joined).Volume()+state.raw[b].cut(joined).Volume()>1e-5):
                    cache[key] = -1
                    rejected.append(dict(components=[a,b],reason="union does not preserve original material"))
                    continue
                info,_ = recognize(joined,budget,history)
                if not info["simple"]:
                    cache[key] = -1
                    rejected.append(dict(components=[a,b],reason="union is not a verified constant extrusion"))
                    continue
                name = f"m{len(merges)+1}"
                for old in (a,b):
                    state.raw.pop(old);state.stops.pop(old,None)
                state.raw[name] = joined.Solids()[0]
                state.stops[name] = dict(reason="no_meaningful_splits",analysis=dict(
                    reason="constant_outer_section",recognition=info,sampled_candidates=0))
                merges.append(dict(components=[a,b],result=name,contact_area=area,
                                   reason="exact union is one constant-section extrusion",recognition=info))
                changed = True
                break
            except TechnicalLimit:
                limited = True
                break
            except Exception as error:
                cache[key] = -1
                rejected.append(dict(components=[a,b],reason=f"{type(error).__name__}: {error}"))
        if limited or not changed:
            break
    state.checks.update(geometry_merges=merges,merge_rejections=rejected,
                       merge_budget=dict(operations=budget.operations,maximum=settings.max_operations,
                                         truncated=limited),geometric_merge_independent_of_assembly=True)
    return state
