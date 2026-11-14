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
r=extrude(r, (0, 0, 102), 'XY', "sketch().push([(37, 6)]).rect(14, 62).finalize()", -204)
r=extrude(r, (37, 6, 18), 'XY', "sketch().push([(37, 6)]).rect(16, 74).finalize()", -101, False)
r=extrude(r, (32, 43, -30), 'ZX', "sketch().push([(-30, 32)]).circle(1).finalize()", 25)
r=extrude(r, (31, 43, -53), 'ZX', "sketch().push([(-53, 31)]).circle(1).finalize()", 32)
r=extrude(r, (29, -1, -56), 'YZ', "sketch().push([(-1, -56)]).circle(27).finalize()", -52)
r=extrude(r, (-12, -28, -56), 'YZ', "sketch().arc((-69, -70), (-75, -56), (-69, -42)).arc((-56, -37), (-42, -42)).segment((-19, -37)).arc((-28, -56), (-19, -75)).segment((-42, -70)).arc((-56, -75), (-69, -70)).assemble().finalize()", -33)
r=extrude(r, (44, 30, 56), 'ZX', "sketch().segment((55, -4), (55, 44)).segment((57, 44)).segment((57, -4)).segment((56, -4)).close().assemble().finalize()", 18)
