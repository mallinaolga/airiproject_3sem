"""Seeded source solids from the existing CADGen factory, without batch files."""

from contextlib import contextmanager
import random
import runpy

import cadquery as cq
import numpy as np


def decomposition_history(parameters):
    """Read extrusion directions/end-plane hints without replaying CADGen.

    Placed extrusions may snap to a different surface in the final program.
    Consequently these planes are proposals only; decomposition verifies their
    actual external-contour transition in the final B-rep before using them.
    Unknown operations/placements are reported and fall back to geometry.
    """
    cad = parameters.get("cad", parameters) if parameters else {}
    result = dict(directions=[], boundaries=[], operations=[], unsupported=[])
    planes = cad.get("planes", [])
    vectors = {"X": [1,0,0], "Y": [0,1,0], "Z": [0,0,1],
               "-X": [-1,0,0], "-Y": [0,-1,0], "-Z": [0,0,-1]}
    for index, entry in enumerate(cad.get("cs", [])):
        op, placement = entry.get("op", {}), entry.get("plane")
        try:
            if isinstance(placement, int):
                plane = planes[placement]
                normal = np.eye(3)[plane["axis"]]
                point = normal*plane["origin"]
            elif isinstance(placement, dict) and placement.get("type") == "AxisWorkplane":
                normal = np.array(vectors[placement["normal"]], dtype=float)
                point = np.array(placement["point"], dtype=float)
            else:
                raise ValueError("unsupported workplane")
            result["directions"].append(normal.tolist())
            segments = [(point,op)]
            if op.get("type") == "TwoExtrudes":
                # Only the normal coordinate matters for plane proposals.
                segments = [(point,op["first"]),
                            (point+normal*op["second_normal_offset"],op["second"])]
            elif op.get("type") != "Extrude":
                raise ValueError("not a supported extrusion operation")
            for start, segment in segments:
                end = start+normal*segment["extent"]
                result["operations"].append(dict(index=index,type=op["type"],
                    normal=normal.tolist(),start=start.tolist(),end=end.tolist()))
                for p in (start,end):
                    result["boundaries"].append(dict(normal=normal.tolist(),point=p.tolist(),operation=index))
        except (KeyError, IndexError, TypeError, ValueError) as error:
            result["unsupported"].append(dict(index=index,type=op.get("type"),reason=str(error)))
    return result


@contextmanager
def seeded_generators(seed):
    python_state, numpy_state = random.getstate(), np.random.get_state()
    random.seed(seed)
    np.random.seed(seed % 2**32)
    try:
        yield
    finally:
        random.setstate(python_state)
        np.random.set_state(numpy_state)


def generate_source(seed, source="cadgen", config=None, *, complexity="legacy"):
    """Return the solid, its parameters and a reproducible source program.

    CADGen's own procedural sketches/extrusions construct the default source.
    A box is an explicitly selected debugging mode, never a hidden fallback.
    """
    rng = random.Random(f"source:{seed}")
    if source == "box":
        dimensions = [round(rng.uniform(40, 75), 3) for _ in range(3)]
        return (cq.Workplane("XY").box(*dimensions).val(),
                dict(generator="debug_box", dimensions=dimensions),
                f"import cadquery as cq\nr = cq.Workplane('XY').box(*{dimensions!r})\n")
    if source != "cadgen":
        raise ValueError(f"Unknown source: {source}")
    from .cad import CADFactory
    from .extrude import ExtrudeFactory
    from .sketch import SketchFactory

    with seeded_generators(seed):
        if config:
            factory = runpy.run_path(str(config))["cad_factory"]
            requested_operations = None
        else:
            automatic = complexity == "decomposition"
            requested_operations = rng.randint(5, 8) if automatic else rng.randint(1, 3)
            sketch = SketchFactory(min_n_commands=1, max_n_commands=2 if automatic else 3,
                                   n_outer_probabilities=[1.0], rotation_probability=0.35,
                                   from_sketchgraph=False, from_sketchgraph_probability=0.0)
            entries = [dict(factory=ExtrudeFactory(sketch), plane=0, probability=1.0,
                            n_times=requested_operations)]
            if automatic:
                from .extrude import TwoExtrudesFactory
                base_sketch=SketchFactory(1,1,[1.0],0.0,from_sketchgraph=False,from_sketchgraph_probability=0.0)
                entries = [dict(factory=TwoExtrudesFactory(base_sketch, second_new_sketch_probability=0.0),
                                plane=0, probability=1.0),
                           dict(factory=ExtrudeFactory(sketch), plane=0, probability=1.0,
                                n_times=requested_operations-1)]
            factory = CADFactory(
                factories=entries,
                world_size=rng.uniform(180, 240) if automatic else rng.uniform(65, 100), max_string_length=12000 if automatic else 6000,
                n_retries=3, n_extrude_retries=3)
        cad = factory.generate()
        cad.finalize(skip_fix=getattr(factory, "skip_fix", False))
        program = cad.to_string()
        namespace = {}
        # The program comes from our local CADGen, never from an input data file.
        exec(compile(program, "<CADGen generated source>", "exec"), namespace)
        shape = namespace["r"].val()
        parameters = dict(generator="CADFactory", config=str(config) if config else None,
                          world_size=factory.world_size,
                          requested_operations=requested_operations,
                          actual_operations=len(cad.cs), cad=cad.to_dict())
        parameters["complexity"] = complexity
    return shape, parameters, program
