from cadgen.cad import CADFactory
from cadgen.sweep_adv import SweepAdvFactory

# Isolated preset for the GENERAL (freeform) ADVANCED sweep = sweep_adv. The
# original simple sweep lives in cadgen/sweep.py (kept untouched for the
# colleague's dataset compatibility); our freeform sweep is sweep_adv.
# SweepAdvFactory as the first (only) factory triggers the standalone base-op
# path (_append_initial_sweep -> SweepAdvFactory.generate). freeform_path_
# probability=1.0 forces the freeform path (never a single line/arc/helix =
# extrude/revolve/spring).
factory_config = dict(
    factories=[
        dict(
            factory=SweepAdvFactory(freeform_path_probability=1.0),
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
    n_extrude_retries=15,
)
