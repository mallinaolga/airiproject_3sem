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
r=extrude(r, (0, 0, -37), 'XY', "sketch().push([(-61, -73)]).rect(66, 36).finalize()", 57)
r=extrude(r, (-100, -62, 0), 'ZX', "sketch().segment((-83, -100), (-59, -41)).arc((-83, 17), (-59, 76)).arc((0, 100), (59, 76)).arc((83, 17), (59, -41)).segment((83, -100)).close().assemble().finalize()", 153)
