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
r=extrude(r, (0, 3, 0), 'ZX', "sketch().segment((-100, 22), (-100, 78)).segment((-45, 78)).arc((23, 91), (63, 35)).segment((100, -21)).segment((-14, -95)).segment((-61, -22)).segment((-49, -14)).arc((-60, 3), (-66, 22)).close().assemble().push([(-58, 50)]).circle(5, mode='s').finalize()", -7)
