"""Combined config for the NEW operations the dataset was missing: LOFT and the
advanced/freeform SWEEP (sweep_adv), placed as boss features on top of the base
extrude/fillet ops. Use this to generate the additional loft+sweep samples to
append to the colleague's existing dataset.

Note: the original simple sweep (cadgen/sweep.py, registry "sweep") is preserved
for his dataset; our freeform sweep here is sweep_adv (cadgen/sweep_adv.py).
"""
from cadgen.cad import CADFactory
from cadgen.cli import build_default_factories
from cadgen.loft import LoftFactory
from cadgen.sweep_adv import SweepAdvFactory

_factories = build_default_factories()
_factories.append(
    dict(
        factory=LoftFactory(
            n_sections_range=(2, 5),
            offset_range=(8.0, 36.0),
            profile_circle_radius_range=(4.0, 18.0),
            profile_rect_size_range=(6.0, 24.0),
            center_shift_range=(-10.0, 10.0),
        ),
        probability=0.15,
        plane=0,
    )
)
_factories.append(
    dict(
        factory=SweepAdvFactory(freeform_path_probability=1.0),
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
    n_extrude_retries=15,
)

__all__ = ["factory_config", "cad_factory"]
