from cadgen.cad import CADFactory
from cadgen.thread import ThreadFactory

# Isolated single-op preset that forces the THREAD factory, to test the
# `thread(...)` one-liner emission and threaded-cylinder/cone coverage.
cad_factory = CADFactory(
    factories=[dict(factory=ThreadFactory(), plane=0, probability=1.0)],
    world_size=200,
    max_string_length=2000,
)
