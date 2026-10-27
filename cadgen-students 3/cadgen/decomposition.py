"""Interpretable B-rep section/transition search and recursive partitioning.

No component count is a target. Sampling defines the investigated plane family;
budgets are reported separately from geometric stopping conditions.
"""

from dataclasses import asdict, dataclass, field
from collections import Counter
from itertools import combinations
import math

import cadquery as cq
import numpy as np

from .assembly_geometry import (AssemblySettings, GeometryRejected, Split, difference_volume,
                                require_solid, halfspace, frame, contact_patch)
from .assembly_validation import overlap_volume, transform_part
from .section_analysis import directions, section, recognize, outer_section, contour_difference


@dataclass(frozen=True)
class DecompositionSettings:
    min_component_size: float = 0.1
    min_component_volume: float = 0.001
    min_score: float = 0.8
    min_simplicity_gain: float = 0.08
    neck_weight: float = 2.0
    transition_weight: float = 2.0
    simplicity_weight: float = 3.0
    imbalance_weight: float = 0.35
    max_candidates: int = 160
    max_depth: int = 12
    max_operations: int = 5000
    max_connection_trials: int = 12
    max_sequence_states: int = 256

    def validate(self):
        for name, value in asdict(self).items():
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")


class TechnicalLimit(GeometryRejected):
    pass


@dataclass
class Budget:
    maximum: int
    operations: int = 0

    def use(self, count=1):
        if self.operations+count > self.maximum:
            raise TechnicalLimit("CAD operation budget exhausted")
        self.operations += count


def union(shapes):
    shapes = list(shapes)
    if not shapes:
        return cq.Compound.makeCompound([])
    result = shapes[0]
    for other in shapes[1:]:
        result = result.fuse(other)
    return result


@dataclass
class CutCandidate:
    split: object
    score: float
    metrics: dict

    def metadata(self):
        return dict(score=self.score, metrics=self.metrics, plane=self.split.metadata())


def geometric_split(shape, origin, normal, tolerance=1e-5):
    """Partition original material; no wall, fastener or part-fraction limits."""
    rotation = frame(normal)
    origin = np.asarray(origin, dtype=float)
    local = transform_part(shape, rotation.T, -rotation.T@origin)
    lower = local.intersect(halfspace(local,False)).clean()
    upper = local.intersect(halfspace(local,True)).clean()
    solids = lower.Solids()+upper.Solids()
    if not lower.Solids() or not upper.Solids() or any(not s.isValid() or s.Volume()<=1e-9 for s in solids):
        raise GeometryRejected("geometric cut must produce valid positive-volume solids on both sides")
    overlap = overlap_volume(lower,upper)
    error = difference_volume(local,lower.fuse(upper))
    if overlap>tolerance or error>tolerance:
        raise GeometryRejected("geometric cut does not reconstruct original material")
    return Split(local,lower,upper,rotation,origin,dict(reconstruction_error_volume=error,
        intersection_volume=overlap,geometric_only=True,solid_count=len(solids)))


def rank_cuts(shape, geometry, settings, budget, history=None):
    # The compatibility argument is intentionally unused: assembly settings
    # must never affect geometric boundaries, acceptance or stopping.

    recognition, axes = recognize(shape, budget, history)
    if recognition["simple"]:
        return [], dict(reason="constant_outer_section", recognition=recognition,
                        sampled_candidates=0, truncated=False)
    candidates, errors, sampled, truncated = [], [], 0, False
    rejections = Counter()
    complexity = len(shape.Faces())
    proposals_log = []
    child_cache = {}
    history_axes = []
    if history and history.get("operations") and not history.get("unsupported"):
        history_axes = [axis for axis in axes if len(axis["levels"])>2 and any(
            abs(np.dot(axis["normal"],n))>.999999 for n in history.get("directions",[]))]
    ordered_axes = history_axes+[axis for axis in axes if not any(axis is item for item in history_axes)]
    used_history = False
    for axis in ordered_axes:
        # Construction directions get first refusal. Every proposed plane is
        # still verified against B-rep. If none works, inspect other normals.
        if history_axes and not any(axis is item for item in history_axes) and candidates:
            used_history = True
            break
        normal, center = axis["normal"], axis["center"]
        local, epsilon = axis["local"], axis["epsilon"]
        low, high = axis["extent"]
        proposals = [(z, "brep_face_boundary") for z in axis["levels"]]
        # History is a candidate source, never a compatibility certificate.
        for boundary in (history or {}).get("boundaries", []):
            n = np.array(boundary["normal"])
            if abs(np.dot(n, normal)) > .999999:
                z = np.dot(np.array(boundary["point"])-center, normal)
                if not any(abs(z-p[0]) < epsilon for p in proposals):
                    proposals.append((z, "cadgen_history_boundary"))
        for z, source in sorted(proposals):
            record = dict(origin=(center+normal*z).tolist(),normal=normal.tolist(),source=source)
            proposals_log.append(record)
            if min(z-low, high-z) < settings.min_component_size:
                rejections["insufficient_axial_size"] += 1
                record.update(status="rejected",reason="geometric_minimum_size",
                              axial_depths=[z-low,high-z])
                continue
            if sampled >= settings.max_candidates:
                record.update(status="not_checked",reason="max_candidates")
                truncated = True
                break
            sampled += 1
            # Stay inside the adjacent geometric intervals, even for a thin
            # feature. Compare bounded contours, not just their areas.
            neighbour = min([abs(z-p[0]) for p in proposals if abs(z-p[0])>epsilon*.001]
                            + [z-low,high-z])
            delta = min(epsilon, neighbour*.1)
            budget.use(2)
            try:
                before, after = outer_section(local,z-delta), outer_section(local,z+delta)
                transition = abs(before.Area()-after.Area())/max(before.Area(),after.Area(),1e-9)
                contour = contour_difference(before,after)
                record["contour_transition"] = contour
                if contour < .001:
                    rejections["no_resolved_external_contour_jump"] += 1
                    record.update(status="rejected",reason="no_resolved_external_contour_jump")
                    continue
                budget.use(4)
                split = geometric_split(shape, center+normal*z, normal)
                children = split.upper.Solids()+split.lower.Solids()
                if min(s.Volume() for s in children) < settings.min_component_volume:
                    rejections["insufficient_component_volume"] += 1
                    record.update(status="rejected",reason="geometric_minimum_volume")
                    continue
                # Numerical size filter in the cut frame, unrelated to fastener walls.
                dimensions = [min(s.BoundingBox().xlen,s.BoundingBox().ylen,s.BoundingBox().zlen)
                              for s in children]
                if min(dimensions) < settings.min_component_size:
                    rejections["insufficient_local_dimensions"] += 1
                    record.update(status="rejected",reason="geometric_minimum_size",dimensions=dimensions)
                    continue
                patch = contact_patch(split.lower,split.upper)
                area = float(patch.Area())
                if area < 1e-7:
                    rejections["insufficient_actual_contact_area"] += 1
                    record.update(status="rejected",reason="no_positive_area_interface")
                    continue
                child_info = []
                for child in children:
                    key = child.hashCode()
                    if key not in child_cache:
                        child_cache[key] = recognize(child,budget)[0]
                    child_info.append(child_cache[key])
                gain = sum(info["simple"] for info in child_info)/len(children)
                face_gain = (complexity-max(len(s.Faces()) for s in children))/max(complexity,1)
                neck = max(0.,1-area/max(before.Area(),after.Area(),1e-9))
                imbalance = (max(s.Volume() for s in children)-min(s.Volume() for s in children))/shape.Volume()
                score = (settings.neck_weight*neck+settings.transition_weight*contour
                         + settings.simplicity_weight*gain-settings.imbalance_weight*imbalance)
                if score < settings.min_score or (gain < settings.min_simplicity_gain and contour < .1):
                    rejections["insufficient_section_improvement_score"] += 1
                    record.update(status="rejected",reason="insufficient_section_improvement_score",score=score)
                    continue
                record.update(status="eligible",score=score,child_count=len(children))
                candidates.append(CutCandidate(split,score,dict(
                    neck_contrast=neck,area_transition=transition,contour_transition=contour,
                    simplicity_gain=gain,face_count_gain_auxiliary=face_gain,
                    child_recognition=child_info,candidate_source=source,
                    original_faces=complexity,child_faces=[len(s.Faces()) for s in children],
                    interface_area=area,imbalance=imbalance,minimum_local_dimensions=dimensions)))
            except TechnicalLimit:
                raise
            except Exception as error:
                rejections["invalid_geometric_split"] += 1
                record.update(status="rejected",reason=f"{type(error).__name__}: {error}")
                errors.append(f"{type(error).__name__}: {error}")
        if truncated:
            break
    candidates.sort(key=lambda c:(-c.score,tuple(c.split.origin)))
    return candidates,dict(reason="section_boundaries" if candidates else "unresolved_geometry",
        recognition=recognition,sampled_candidates=sampled,meaningful_candidates=len(candidates),
        truncated=truncated,errors=errors,rejected_geometric_candidates=dict(rejections),
        proposed_planes=proposals_log,
        plane_family="verified construction-axis boundaries with B-rep fallback",
        construction_axis_priority_used=used_history)


@dataclass
class Partition:
    original: cq.Shape
    raw: dict
    joints: list = field(default_factory=list)
    stops: dict = field(default_factory=dict)
    cuts: list = field(default_factory=list)
    trials: list = field(default_factory=list)
    checks: dict = field(default_factory=dict)
    sequence: list = field(default_factory=list)
    assembly: dict = field(default_factory=lambda:dict(status="not_attempted",success=False))


def validate_raw_partition(original, raw, tolerance=1e-5):
    for name, shape in raw.items():
        require_solid(shape,name)
    overlaps = {f"{a}/{b}":overlap_volume(raw[a],raw[b]) for a,b in combinations(raw,2)}
    if any(v>tolerance for v in overlaps.values()):
        raise GeometryRejected("Geometric constituents overlap")
    reconstruction = difference_volume(original,union(raw.values()))
    if reconstruction>tolerance:
        raise GeometryRejected("Geometric constituents do not reconstruct source")
    return dict(raw_reconstruction_error_volume=reconstruction,raw_intersection_volumes=overlaps,
                geometric_partition_valid=True)


def finish_leaf_recognition(raw, stops, settings, history=None):
    """Classify leaves skipped by a cut-search limit using a separate budget.

    Does not propose cuts or change solids. A search limit remains recorded even
    when the fixed resulting constituent can subsequently be proved prismatic.
    """
    budget = Budget(settings.max_operations)
    for name,stop in stops.items():
        if stop["reason"]!="technical_limit_reached" or stop.get("final_recognition_checked"):
            continue
        try:
            info,_ = recognize(raw[name],budget,history)
        except TechnicalLimit:
            break
        stop["analysis"] = dict(reason=info["reason"],recognition=info,sampled_candidates=0)
        stop["final_recognition_checked"] = True
    return dict(operations=budget.operations,maximum=settings.max_operations,
                scope="classification only; geometric leaves unchanged")


def decompose_geometry(original, settings=None, *, history=None):
    """Finish geometric recognition/partitioning before importing joint search."""
    settings = settings or DecompositionSettings()
    settings.validate()
    original = require_solid(original,"original")
    state = Partition(original,{"p":original})
    budget = Budget(settings.max_operations)
    analyses = {}

    def visit(node,depth):
        if depth>=settings.max_depth:
            state.stops[node] = dict(reason="technical_limit_reached",limit="max_depth")
            return
        try:
            candidates, analysis = rank_cuts(state.raw[node],None,settings,budget,history)
        except TechnicalLimit as error:
            state.stops[node] = dict(reason="technical_limit_reached",limit=str(error))
            return
        analyses[node] = analysis
        if not candidates:
            reason = ("technical_limit_reached" if analysis.get("truncated") else
                      "no_meaningful_splits" if analysis.get("recognition",{}).get("simple") else
                      "unresolved_geometry")
            state.stops[node] = dict(reason=reason,analysis=analysis)
            return
        chosen = candidates[0]
        children = {}
        for side,shape in (("u",chosen.split.upper),("l",chosen.split.lower)):
            solids = shape.Solids()
            for i,solid in enumerate(solids):
                name = node+side+(str(i+1) if len(solids)>1 else "")
                children[name] = chosen.split.world(solid)
        state.raw.pop(node)
        state.raw.update(children)
        state.cuts.append(dict(node=node,children=list(children),selected=chosen.metadata(),
                               selection_reason="highest geometric score; fasteners not considered"))
        for child in children:
            visit(child,depth+1)

    visit("p",0)
    state.checks.update(geometric_analyses=analyses,
                        budget=dict(cad_operations=budget.operations,maximum=settings.max_operations))
    return finalize_geometry(state,settings,history)


def finalize_geometry(state, settings, history=None):
    """Complete leaf classification and merge only proved prismatic unions."""
    from .decomposition_merge import coalesce_prisms
    classification_budget = finish_leaf_recognition(state.raw,state.stops,settings,history)
    analyses = state.checks.get("geometric_analyses",{})
    limits = list(state.checks.get("geometry_limits",[]))
    limits += [dict(node=n,limit="max_candidates") for n,a in analyses.items() if a.get("truncated")]
    limits += [dict(node=n,limit=s.get("limit","analysis limit")) for n,s in state.stops.items()
               if s["reason"]=="technical_limit_reached"]
    coalesce_prisms(state,settings,history)
    if state.checks["merge_budget"]["truncated"]:
        limits.append(dict(limit="geometric merge budget"))
    state.checks.update(validate_raw_partition(state.original,state.raw))
    state.checks.update(classification_budget=classification_budget,
        geometry_independent_of_fasteners=True,
        all_leaves_constant_section=all(s.get("analysis",{}).get("recognition",{}).get("simple",False)
                                       for s in state.stops.values()),
        unresolved_geometry_components=[n for n,s in state.stops.items()
            if not s.get("analysis",{}).get("recognition",{}).get("simple",False)],
        geometry_limits=limits,decomposition_complete_within_search=not limits,
        exhaustive_geometric_search=False,
        history_analysis=dict(operations=len((history or {}).get("operations",[])),
                              unsupported=(history or {}).get("unsupported",[]),trusted_without_brep_verification=False))
    return state


def decompose(original,seed,geometry=None,settings=None,connection="auto",profile="auto",*,history=None):
    """Compatibility workflow: geometric stage, then assembly of fixed leaves."""
    from .decomposition_assembly import assemble_partition
    settings = settings or DecompositionSettings()
    state = decompose_geometry(original,settings,history=history)
    try:
        return assemble_partition(state,seed,geometry or AssemblySettings(),settings,connection,profile)
    except Exception as error:
        state.assembly=dict(status="failed",success=False,partition_modified=False,
                            reason=f"{type(error).__name__}: {error}")
        return state
