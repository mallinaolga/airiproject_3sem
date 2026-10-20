from cadgen.cad import CADFactory
from cadgen.loft import LoftFactory

factory_config = dict(
    factories=[
        dict(
            factory=LoftFactory(),
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
)
