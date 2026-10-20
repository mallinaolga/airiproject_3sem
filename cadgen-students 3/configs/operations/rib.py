from cadgen.cad import CADFactory
from cadgen.rib import RibFactory

# Isolated single-op preset that forces the RIB factory, to test the `rib(...)`
# one-liner emission and the ribbed-structure coverage in isolation.
cad_factory = CADFactory(
    factories=[dict(factory=RibFactory(), plane=0, probability=1.0)],
    world_size=200,
    max_string_length=2000,
)
