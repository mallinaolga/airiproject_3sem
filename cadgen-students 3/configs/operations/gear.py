from cadgen.cad import CADFactory
from cadgen.gear import GearFactory

factory_config = dict(
    factories=[
        dict(
            factory=GearFactory(
                hole_probability=0.8,
                outer_teeth_probability=1.0,
                inner_teeth_probability=0.6,
            ),
            plane=0,
            reuse_plane_probability=0.0,
            selected_plane_probability=0.0,
            probability=1.0,
        ),
    ],
    world_size=200,
    max_string_length=5000,
)

cad_factory = CADFactory(
    factories=factory_config["factories"],
    world_size=factory_config["world_size"],
    max_string_length=factory_config["max_string_length"],
)
