from cadgen.cad import CADFactory
from cadgen.extrude import ExtrudeFactory
from cadgen.sketch import SketchFactory
from cadgen.sweep import SweepFactory

factory_config = dict(
    factories=[
        dict(
            factory=ExtrudeFactory(
                sketch_factory=SketchFactory(
                    min_n_commands=1,
                    max_n_commands=2,
                    n_outer_probabilities=[1.0],
                    rotation_probability=0.0,
                    array_pattern_probability=0.0,
                ),
                tangent_plane_prob=1.0,
                out_of_face_prob=0.0,
            ),
            plane=0,
            probability=1.0,
        ),
        dict(
            factory=SweepFactory(inclined_line_path_probability=1.0),
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
    n_extrude_retries=10,
)
