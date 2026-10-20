from cadgen.cad import CADFactory
from cadgen.extrude import ExtrudeFactory
from cadgen.hole import HoleFactory
from cadgen.selected_face_plane import SelectedFacePlaneFactory
from cadgen.sketch import SketchFactory

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
            ),
            plane=0,
            probability=1.0,
        ),
        dict(
            factory=SelectedFacePlaneFactory(top_p=1.0),
            probability=1.0,
        ),
        dict(
            factory=HoleFactory(
                hole_type_probabilities={
                    "blind": 0.2,
                    "through": 0.2,
                    "cut_thru_all": 0.2,
                    "multi_cbore": 0.2,
                    "cbore": 0.0,
                    "csk": 0.0,
                },
                sketch_factory=SketchFactory(
                    min_n_commands=1,
                    max_n_commands=4,
                    n_outer_probabilities=[1.0],
                    rotation_probability=0.3,
                    array_pattern_probability=0.0,
                ),
            ),
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
)
