"""Interpretable B-rep section/transition search and recursive partitioning.

No component count is a target. Sampling defines the investigated plane family;
budgets are reported separately from geometric stopping conditions.
"""

from dataclasses import asdict, dataclass, field, replace
from itertools import combinations
import math

import cadquery as cq
import numpy as np

from .assembly_geometry import (AssemblySettings, GeometryRejected, Split, difference_volume,
                                frame, require_solid, split_model, contact_patch)
from .assembly_validation import overlap_volume, transform_part


@dataclass(frozen=True)
class DecompositionSettings:
    min_component_size: float = 6.0
    min_component_volume: float = 300.0
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


def directions(shape):
    # The three dominant planar-normal families define an explicit heuristic
    # sampling family. Inertia axes cover models with few/no planar faces.
    found = []
    faces = sorted(shape.Faces(), key=lambda f: f.Area(), reverse=True)
    options = [np.array(f.normalAt().toTuple()) for f in faces if f.geomType() == "PLANE"]
    _, inertia = np.linalg.eigh(np.array(cq.Shape.matrixOfInertia(shape)))
    options += list(inertia.T)
    for v in options:
        v = v/np.linalg.norm(v)
        if next((x for x in v if abs(x) > 1e-7), 1) < 0:
            v = -v
        if not any(abs(np.dot(v, old)) > 0.99999 for old in found):
            found.append(v)
        if len(found) == 3:
            break
    return found


def section(local, z):
    b = local.BoundingBox()
    size = b.DiagonalLength*3+1
    wire = cq.Workplane("XY", origin=(0, 0, z)).rect(2*size, 2*size).val()
    plane = cq.Face.makeFromWires(wire)
    return local.intersect(plane)


@dataclass
class CutCandidate:
    split: object
    score: float
    metrics: dict

    def metadata(self):
        return dict(score=self.score, metrics=self.metrics, plane=self.split.metadata())


def rank_cuts(shape, geometry, settings, budget):
    faces = shape.Faces()
    if len(faces) <= 3 or (len(faces) <= 6 and all(f.geomType() == "PLANE" for f in faces)):
        return [], dict(reason="simple_brep", sampled_candidates=0, truncated=False)
    center = np.array(shape.Center().toTuple())
    candidates, errors, sampled, truncated = [], [], 0, False
    complexity = len(faces)
    cut_settings = replace(geometry, min_part_fraction=0.025)
    for normal in directions(shape):
        rotation = frame(normal)
        local = transform_part(shape, rotation.T, -rotation.T@center)
        bb = local.BoundingBox()
        epsilon = max(bb.DiagonalLength*1e-5, 1e-5)
        # Parallel planar faces mark genuine steps/terminations. Projecting
        # every unrelated vertex creates many spurious transition proposals.
        levels = []
        for z in sorted(f.Center().z for f in local.Faces()
                        if f.geomType()=="PLANE" and abs(f.normalAt().z)>0.99999):
            # Keep an actual B-rep coordinate. Decimal rounding moves a cut
            # off its step and creates a thin platform/sliver in one child.
            if not levels or abs(z-levels[-1])>epsilon*.001:
                levels.append(z)
        interior = [z for z in levels if bb.zmin+settings.min_component_size < z < bb.zmax-settings.min_component_size]
        grid = np.linspace(bb.zmin+epsilon, bb.zmax-epsilon, 9).tolist()
        probes = sorted(set(grid + [z-epsilon for z in interior]+[z+epsilon for z in interior]))
        areas = []
        for z in probes:
            budget.use()
            try:
                areas.append(float(section(local, z).Area()))
            except Exception:
                areas.append(0.0)
        proposals = sorted(set(interior+[(a+b)/2 for a, b in zip(probes, probes[1:])]))
        for z in proposals:
            if min(z-bb.zmin, bb.zmax-z) < settings.min_component_size:
                continue
            if sampled >= settings.max_candidates:
                truncated = True
                break
            sampled += 1
            left = max((a for p, a in zip(probes, areas) if p < z), default=0)
            right = max((a for p, a in zip(probes, areas) if p > z), default=0)
            before = min(zip(probes, areas), key=lambda pair: abs(pair[0]-(z-epsilon)))[1]
            after = min(zip(probes, areas), key=lambda pair: abs(pair[0]-(z+epsilon)))[1]
            transition = abs(before-after)/max(before, after, 1e-9)
            near = min(zip(probes, areas), key=lambda pair: abs(pair[0]-z))[1]
            neck_hint = max(0., 1-near/max(min(left, right), 1e-9))
            # A uniform region without a B-rep transition cannot improve a
            # prismatic part just by slicing along its extrusion axis.
            if transition < 0.1 and neck_hint < 0.15 and z not in interior:
                continue
            budget.use(4)
            try:
                origin = center+normal*z
                split = split_model(shape, origin, normal, cut_settings)
                children = (split.upper, split.lower)
                if min(s.Volume() for s in children) < settings.min_component_volume:
                    continue
                if any(min(s.BoundingBox().xlen, s.BoundingBox().ylen, s.BoundingBox().zlen)
                       < settings.min_component_size for s in children):
                    continue
                patch = contact_patch(split.lower,split.upper)
                area = float(patch.Area())
                if area < 4*geometry.min_wall**2:
                    continue
                neck = max(0., 1-area/max(min(left, right), 1e-9))
                gain = (complexity-max(len(s.Faces()) for s in children))/max(complexity, 1)
                imbalance = abs(children[0].Volume()-children[1].Volume())/shape.Volume()
                score = (settings.neck_weight*neck+settings.transition_weight*transition
                         + settings.simplicity_weight*gain-settings.imbalance_weight*imbalance)
                if score < settings.min_score or (gain < settings.min_simplicity_gain and neck < 0.35):
                    continue
                candidates.append(CutCandidate(split, score, dict(
                    neck_contrast=neck, area_transition=transition, simplicity_gain=gain,
                    original_faces=complexity, child_faces=[len(s.Faces()) for s in children],
                    interface_area=area, imbalance=imbalance,
                    minimum_local_dimensions=[min(s.BoundingBox().xlen, s.BoundingBox().ylen,
                                                   s.BoundingBox().zlen) for s in children])))
            except Exception as error:
                errors.append(f"{type(error).__name__}: {error}")
        if truncated:
            break
    candidates.sort(key=lambda c: (-c.score, tuple(c.split.origin)))
    return candidates, dict(sampled_candidates=sampled, meaningful_candidates=len(candidates),
                            truncated=truncated, errors=errors,
                            plane_family="dominant B-rep normals/inertia; section transitions and valleys")


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


def decompose(original, seed, geometry=None, settings=None, connection="auto", profile="auto"):
    from .joint_design import propose_joints, materialize
    from .assembly_planning import validate_partition, assembly_graph

    geometry = geometry or AssemblySettings()
    settings = settings or DecompositionSettings()
    geometry.validate(); settings.validate()
    original = require_solid(original, "original")
    state = Partition(original, {"p": original})
    budget = Budget(settings.max_operations)
    design_library = {}
    refinements = []

    def visit(node, depth):
        nonlocal state
        if depth >= settings.max_depth:
            state.stops[node] = dict(reason="technical_limit_reached", limit="max_depth")
            return
        try:
            candidates, analysis = rank_cuts(state.raw[node], geometry, settings, budget)
        except TechnicalLimit as error:
            state.stops[node] = dict(reason="technical_limit_reached", limit=str(error))
            return
        accepted = False
        for index, candidate in enumerate(candidates[:settings.max_connection_trials]):
            split = candidate.split
            children = (node+"u", node+"l")
            raw = {k: v for k, v in state.raw.items() if k != node}
            raw.update({children[0]: split.world(split.upper), children[1]: split.world(split.lower)})
            previous = []
            conflict = None
            for joint in state.joints:
                if node not in joint.owners:
                    previous.append(joint)
                    continue
                overlap = [overlap_volume(raw[n], joint.zone) for n in children]
                if min(overlap) <= geometry.volume_tolerance:
                    owner = children[int(overlap[1] > overlap[0])]
                    previous.append(replace(joint, owners=tuple(owner if n == node else n for n in joint.owners)))
                    continue
                # Try already validated alternative designs of the parent
                # interface rather than treating its first fastener as fixed.
                relocated=None
                for variant in design_library.get(joint.id,[]):
                    endpoints=[]
                    for ancestor in variant.owners:
                        hits=[n for n in raw if n.startswith(ancestor)
                              and overlap_volume(raw[n],variant.zone)>geometry.volume_tolerance]
                        if len(hits)!=1:break
                        endpoints.append(hits[0])
                    if len(endpoints)==2:
                        relocated=replace(variant,owners=tuple(endpoints));break
                if relocated is None:
                    conflict = "new cut crosses protected material and parent alternatives cannot be relocated"
                    break
                previous.append(relocated)
            if conflict:
                state.trials.append(dict(node=node, candidate=index, reason=conflict))
                continue
            try:
                options = propose_joints(split, children, f"j{len(state.joints)+1}", seed,
                                         geometry, connection, profile,excluded=[j.zone for j in previous])
                for joint in options:
                    try:
                        if any(overlap_volume(joint.zone, j.zone) > geometry.volume_tolerance for j in previous):
                            raise GeometryRejected("joint protected zones conflict")
                        proposed = previous+[joint]
                        if any(overlap_volume(a.zone,b.zone)>geometry.volume_tolerance
                               for a,b in combinations(proposed,2)):
                            raise GeometryRejected("joint protection envelopes conflict after redesign")
                        parts = materialize(raw, proposed, geometry)
                        if any(parts[n].Volume()<settings.min_component_volume for n in raw):
                            raise GeometryRejected("fasteners leave an insufficient-volume main component")
                        checks, sequence = validate_partition(original, raw, parts, proposed, geometry,
                                                               settings.max_sequence_states)
                        graph = assembly_graph(raw, proposed, geometry)
                        state = Partition(original, raw, proposed, dict(state.stops),
                                          state.cuts+[dict(node=node, children=list(children),
                                                           selected=candidate.metadata())],
                                          state.trials, checks, sequence)
                        state.checks["graph"] = graph
                        design_library[joint.id]=options
                        accepted = True
                        break
                    except Exception as error:
                        state.trials.append(dict(node=node, candidate=index, connection=joint.parameters["type"],
                                                 reason=f"{type(error).__name__}: {error}"))
                if accepted:
                    break
            except Exception as error:
                state.trials.append(dict(node=node, candidate=index, reason=f"{type(error).__name__}: {error}"))
        if accepted:
            for child in children:
                visit(child, depth+1)
        else:
            limited = (analysis.get("truncated") or len(candidates) > settings.max_connection_trials
                       or any(t.get("node")==node and "technical_limit_reached" in t.get("reason","")
                              for t in state.trials))
            reason = ("technical_limit_reached" if limited else
                      "no_feasible_connections" if candidates else "no_meaningful_splits")
            state.stops[node] = dict(reason=reason, analysis=analysis,
                                     considered_connections=min(len(candidates), settings.max_connection_trials))

    visit("p", 0)
    # A parent redesign may free a formerly blocked sibling. Revisit only
    # feasibility stops until a full pass accepts no new geometric split.
    while True:
        if not state.joints:break
        before=len(state.raw)
        # Descendants can expose bearing seats unavailable on an entire parent
        # subassembly. Re-evaluate the actual final neighbours, not just the
        # large provisional pair used when their ancestral cut was accepted.
        for index,old in enumerate(list(state.joints)):
            try:
                r=np.array(old.parameters["cut_to_world_rotation"])
                t=np.array(old.parameters["cut_origin"])
                upper,lower=[state.raw[n] for n in old.owners]
                local=lambda s:transform_part(s,r.T,-r.T@t)
                pair=Split(local(upper.fuse(lower)),local(lower),local(upper),r,t,
                           dict(final_neighbour_pair=True))
                others=[j for j in state.joints if j.id!=old.id]
                options=propose_joints(pair,old.owners,old.id,seed,geometry,connection,profile,
                                       excluded=[j.zone for j in others])
                for option in options:
                    if option.score<=old.score+.1:continue
                    proposed=state.joints[:index]+[option]+state.joints[index+1:]
                    try:
                        parts=materialize(state.raw,proposed,geometry)
                        checks,sequence=validate_partition(original,state.raw,parts,proposed,geometry,
                                                            settings.max_sequence_states)
                    except GeometryRejected:
                        continue
                    state.joints=proposed;state.checks=checks;state.sequence=sequence
                    design_library[old.id]=options
                    refinements.append(dict(joint=old.id,previous_type=old.parameters["type"],
                        selected_type=option.parameters["type"],reason="actual final neighbours expose a better feasible joint"))
                    break
            except GeometryRejected:
                pass  # The already validated design remains intact.
        blocked=[n for n,s in state.stops.items() if s["reason"]=="no_feasible_connections" and n in state.raw]
        for node in blocked:
            state.stops.pop(node,None)
            visit(node,len(node)-1)
        if len(state.raw)==before:break
    parts = materialize(state.raw, state.joints, geometry)
    state.checks, state.sequence = validate_partition(original, state.raw, parts, state.joints, geometry,
                                                      settings.max_sequence_states)
    state.checks["graph"] = assembly_graph(state.raw, state.joints, geometry)
    state.checks["budget"] = dict(cad_operations=budget.operations, maximum=settings.max_operations)
    state.checks["joint_refinements"] = refinements
    state.checks["decomposition_complete_within_search"] = not any(
        s["reason"] == "technical_limit_reached" for s in state.stops.values())
    state.checks["exhaustive_geometric_search"] = False
    return state
