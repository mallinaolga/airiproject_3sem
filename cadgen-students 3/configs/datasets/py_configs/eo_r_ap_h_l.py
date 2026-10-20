from cadgen.cad import CADFactory
from cadgen.cli import build_default_factories
from cadgen.loft import LoftFactory

_factories = build_default_factories()
_factories.append(
    dict(
        factory=LoftFactory(
            n_sections_range=(2, 5),
            offset_range=(5.0, 40.0),
            profile_circle_radius_range=(4.0, 18.0),
            profile_rect_size_range=(4.0, 22.0),
            center_shift_range=(-12.0, 12.0),
        ),
        probability=0.15,
        plane=0,
    )
)

factory_config = dict(
    factories=_factories,
    world_size=200,
    max_string_length=800,
)

cad_factory = CADFactory(
    factories=factory_config["factories"],
    world_size=factory_config["world_size"],
    max_string_length=factory_config["max_string_length"],
)

__all__ = ["factory_config", "cad_factory"]
