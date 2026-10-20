from cadgen.cad import CADFactory
from cadgen.spring import SpringFactory

# Isolated single-op preset that forces the SPRING (coil / helix) factory,
# so we can test the `spring(...)` one-liner emission in isolation.
factory_config = dict(
    factories=[
        dict(
            factory=SpringFactory(),
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
