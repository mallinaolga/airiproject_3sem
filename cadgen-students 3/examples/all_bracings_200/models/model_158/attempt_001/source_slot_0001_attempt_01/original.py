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
r=extrude(r, (0, 0, -53), 'XY', "sketch().push([(3, 3)]).circle(6).finalize()", 84)
r=extrude(r, (3, 3, -42), 'XY', "sketch().push([(3, 3)]).circle(8).finalize()", 32, False)
r=extrude(r, (3, 12, -37), 'XY', "sketch().segment((-3, 8), (-3, 92)).segment((9, 92)).segment((9, 8)).arc((3, 12), (-3, 8)).assemble().finalize()", 21)
r=extrude(r, (0, 0, 31), 'XY', "sketch().push([(0, 0)]).circle(115).finalize()", 22)
r=extrude(r, (7, 76, -16), 'XY', "sketch().push([(7, 76)]).circle(1).finalize()", 40)
