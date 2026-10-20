"""
Isolated acceptance preset for the three new sketch-level features:
corner fillet, corner chamfer, and periodic-spline outer profiles.

All three are sketch constructs rather than 3D operations, so they cost no
extra op -- which is what makes them affordable at the stage-3 budget of
<= 20 ops per part.

Why each exists (measured on the SFT run over CADENA-Bench + clean MCB):
  * fillet/chamfer -- 50.7% of ALL build failures on clean MCB are 3D edge
    fillet/chamfer via PointOnEdgeSelector; rounding in the sketch has no
    selector to get wrong.
  * spline -- truncated steps carry a median 356 `.segment()` calls and
    `unterminated string literal` is the top cause of zero-output parts
    (41.8%); the corpus contains 0 splines and tops out at 80 segments.

n_outer_probabilities=[1.0] keeps a single outer wire: `.vertices()` selects
every face's vertices, so the corner clamps are only sound for one face.
"""

from cadgen.cad import CADFactory
from cadgen.extrude import ExtrudeFactory
from cadgen.sketch import SketchFactory

factory_config = dict(
    factories=[
        dict(
            factory=ExtrudeFactory(
                sketch_factory=SketchFactory(
                    min_n_commands=1,
                    max_n_commands=3,
                    n_outer_probabilities=[1.0],
                    rotation_probability=0.3,
                    corner_fillet_probability=0.35,
                    corner_chamfer_probability=0.35,
                    spline_profile_probability=0.30,
                ),
            ),
            plane=0,
            probability=1.0,
        ),
    ],
    world_size=200,
    max_string_length=800,
)

cad_factory = CADFactory(
    factories=factory_config["factories"],
    world_size=factory_config["world_size"],
    max_string_length=factory_config["max_string_length"],
    # Match production (main_12_operations.yaml:459-460); the CADFactory
    # default n_extrude_retries=1 under-reports yield -- see TODO.md Step 8.
    n_retries=15,
    n_extrude_retries=15,
)
