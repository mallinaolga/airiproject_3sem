from cadgen.cad import CADFactory
from cadgen.cli import build_default_factories
from cadgen.sweep_init import SweepInitFactory

_factories = build_default_factories()
_factories.append(
    dict(
        factory=SweepInitFactory(
            pitch_range=(5.0, 30.0),
            height_range=(25.0, 120.0),
            base_radius_range=(8.0, 35.0),
            cone_angle_range_deg=(0.0, 15.0),
            profile_circle_radius_range=(1.5, 6.0),
            profile_rect_size_range=(2.5, 9.0),
            helix_angle_probability=0.75,
        ),
        probability=0.12,
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
