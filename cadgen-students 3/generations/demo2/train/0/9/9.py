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
r=extrude(r, (0, 0, 56), 'XY', "sketch().push([(23, 27.5)]).rect(154, 81).push([(55, 34)]).circle(24, mode='s').finalize()", 19)
r=extrude(r, (3, -9, 56), 'YZ', "sketch().segment((-68, 56), (50, 56)).segment((33, 25)).arc((50, -16), (33, -58)).arc((-9, -75), (-51, -58)).arc((-68, -16), (-51, 25)).close().assemble().finalize()", -103)
