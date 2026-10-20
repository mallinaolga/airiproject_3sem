import cadquery as cq
from cadgen.selectors import PointOnEdgeSelector, PointOnFaceSelector
from cadgen.extrude import extrude
from cadgen.shell import shell
from cadgen.hole import hole
from cadgen.revolve import revolve
from cadgen.orto_cut import orto_cut
from cadgen.sweep import sweep
from cadgen.sweep_adv import sweep_adv
from cadgen.spring import spring
from cadgen.loft import loft
from cadgen.gear import gear
from cadgen.rib import rib
from cadgen.thread import thread
r = None
r=extrude(r, (89, 0, 0), 'YZ', "sketch().arc((-56, -92), (-13, 91), (76, -74)).segment((76, -39)).segment((40, -39)).segment((40, -37)).segment((-20, -37)).segment((-20, -39)).segment((-56, -39)).close().assemble().reset().push([(-60, 21)]).rarray(5, 49, 8, 1).face(cq.Workplane('YZ').sketch().segment((-2, 0), (1, 2)).segment((2, 0)).segment((-1, -2)).close().assemble().wires(), mode='s').finalize()", -177)
