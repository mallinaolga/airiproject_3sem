"""Bounded eight-type selection on the existing decomposition interfaces."""
import random

import numpy as np

from .assembly_geometry import GeometryRejected, Split
from .assembly_validation import transform_part, overlap_volume

JOINT_TYPES = ("mortise_tenon", "tongue_groove_stop", "dovetail", "pinned",
               "bolted", "bayonet", "threaded", "snap_fit")


def _frames(split, owners):
    """Both donor roles; existing material and world placement stay unchanged."""
    yield split, owners
    flip = np.diag([1., -1., -1.])
    local = lambda shape: transform_part(shape, flip, np.zeros(3))
    yield Split(local(split.original), local(split.upper), local(split.lower),
                split.rotation@flip, split.origin, split.checks), tuple(reversed(owners))


def propose_all_connections(split, owners, name, seed, geometry, *, preferred_types=(), excluded=()):
    from .joint_design import propose_joints, make_joint
    from .bayonet import BayonetSpec, build_bayonet
    from .snap_fit import SnapFitSpec, build_snap_fit
    from .threaded import build_threaded
    from .pin_joint import build_pin
    from .tongue_groove_stop import build_tongue_groove_stop

    if any(kind not in JOINT_TYPES for kind in preferred_types):
        raise ValueError("Unknown preferred joint type")
    order = list(dict.fromkeys([*preferred_types, *JOINT_TYPES]))
    report = dict(investigated_types=order, rejected_designs=[], bounded_search=True)
    options = []
    for kind in order:
        candidates = []
        if kind in ("mortise_tenon", "dovetail", "bolted"):
            try:
                try:
                    candidates = propose_joints(split, owners, name, seed, geometry, kind,
                                                excluded=excluded, adaptive=False)
                except (ValueError, RuntimeError):
                    candidates = propose_joints(split, owners, name, seed, geometry, kind, excluded=excluded)
                # Preserve one alternative direction/placement per type within the global budget.
                candidates = candidates[:2]
            except (ValueError, RuntimeError) as error:
                report["rejected_designs"].append(dict(joint_type=kind, reason=str(error),
                                                      details=getattr(error, "report", None)))
        else:
            for local, roles in _frames(split, owners):
                for scale in (1., .65):
                    try:
                        rng = random.Random(f"all:{seed}:{name}:{kind}:{scale}")
                        if kind == "bayonet":
                            spec = BayonetSpec(radius=6*scale, depth=10*scale,
                                lug_projection=2*scale, lug_height=2*scale)
                            result = build_bayonet(local, geometry, spec)
                        elif kind == "snap_fit":
                            spec = SnapFitSpec(length=12*scale, thickness=scale, width=4*scale,
                                hook_height=1.2*scale, max_deflection=2*scale, relief_depth=2.2*scale)
                            result = build_snap_fit(local, geometry, spec)
                        elif kind == "threaded":
                            result = build_threaded(local, rng, geometry, diameter=6*scale,
                                                    engagement_length=max(geometry.min_wall, 6*scale))
                        elif kind == "pinned":
                            result = build_pin(local, rng, geometry, diameter=4*scale)
                        else:
                            if scale != 1.: continue
                            result = build_tongue_groove_stop(local, rng, geometry)
                        joint = make_joint(local, result, roles, name, 5., dict(method="eight_type_material_fit"), geometry)
                        if any(overlap_volume(joint.zone, z) > geometry.volume_tolerance for z in excluded):
                            raise GeometryRejected("Protected joint zones overlap")
                        candidates.append(joint)
                        break
                    except (ValueError, RuntimeError) as error:
                        report["rejected_designs"].append(dict(joint_type=kind, owners=list(roles),
                                                              scale=scale, reason=str(error)))
                if candidates: break
        for joint in candidates:
            joint.parameters["joint_type"] = kind
            # Geometry, walls and accessibility already passed the real builder checks.
            # Priority only ranks feasible alternatives; it never overrides rejection.
            joint.score += (len(order)-order.index(kind))*10 if preferred_types else 0
            joint.selection["catalogue_search"] = report
            options.append(joint)
    if not options:
        error = GeometryRejected("No feasible connection among the eight AIRI types")
        error.report = report
        raise error
    # Round-robin keeps all feasible types available to the existing graph search.
    ordered = []
    for index in range(2):
        for kind in order:
            group = [j for j in options if j.parameters["joint_type"] == kind]
            if index < len(group): ordered.append(group[index])
    report["feasible_types"] = list(dict.fromkeys(j.parameters["joint_type"] for j in ordered))
    return ordered
