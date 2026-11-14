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
r=extrude(r, (-36, 0, 0), 'YZ', "sketch().push([(9, -8)]).circle(15).finalize()", 90)
r=extrude(r, (13, 9, -8), 'YZ', "sketch().push([(9, -8)]).circle(25).finalize()", 13, False)
r=extrude(r, (13, 9, -33), 'XY', "sketch().push([(13, 9)]).circle(94).finalize()", -14)
r=extrude(r, (13, 103, -41), 'ZX', "sketch().segment((-107, -12), (-107, 38)).segment((-58, 38)).segment((-58, 62)).segment((-24, 62)).segment((-24, 38)).segment((25, 38)).segment((25, -12)).segment((-24, -12)).segment((-24, -36)).segment((-58, -36)).segment((-58, -12)).close().assemble().finalize()", 10)
r=extrude(r, (-8, -26, -47), 'XY', "sketch().segment((-16, -34), (-14, -16)).segment((0, -18)).segment((-2, -36)).close().assemble().finalize()", -52)
r=extrude(r, (22, 9, 16), 'YZ', "sketch().segment((-6, 10), (-6, 107)).segment((24, 107)).segment((24, 10)).arc((9, 16), (-6, 10)).assemble().finalize()", 41)
r=extrude(r, (-21, -6, -8), 'YZ', "sketch().segment((-113, -19), (-113, 3)).segment((0, 3)).arc((-6, -8), (0, -19)).close().assemble().finalize()", -86)
