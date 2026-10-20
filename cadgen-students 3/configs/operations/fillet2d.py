"""
Isolated acceptance preset for the 2D sketch corner fillet.

Why this op exists: 50.7% of the SFT model's build failures on the clean MCB
non-overlap split are 3D edge fillet/chamfer (edge_chamfer 26.2% +
edge_fillet 24.5%), dying as `no_edges_for_fillet` (490) and
`BRep_API: command not done` (614) -- the model has to guess a 3D point that
lands on the edge it means.  Rounding in the SKETCH removes the selector
entirely, and costs no extra operation, which matters at the stage-3 budget of
<= 20 ops per part.

n_outer_probabilities=[1.0] keeps a single outer wire: `.vertices()` selects
every face's vertices, so the clamp is only sound for the single-face case.
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
                    corner_fillet_probability=1.0,
                    corner_fillet_min_rel=0.10,
                    corner_fillet_max_rel=0.90,
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
    # Match production (configs/cad_factory/main_12_operations.yaml:459-460).
    # The CADFactory default is n_extrude_retries=1, which makes an isolated
    # batch report a fraction of the real production yield -- see TODO.md Step 8.
    n_retries=15,
    n_extrude_retries=15,
)
