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
r=extrude(r, (0, 0, 31), 'XY', "sketch().push([(-2, 1)]).circle(4).finalize()", 11)
r=extrude(r, (-2, 1, 41), 'XY', "sketch().push([(-2, 1)]).circle(5).finalize()", 3, False)
r=extrude(r, (1, 1, 36), 'XY', "sketch().arc((-1, -2), (1, 1), (-1, 4)).segment((3, 4)).segment((3, -2)).close().assemble().finalize()", -108)
r=extrude(r, (0, 4, 41), 'XY', "sketch().segment((-95, -57), (-24, 114)).segment((95, 65)).segment((24, -106)).close().assemble().finalize()", -9)
r=extrude(r, (-42, 50, 42), 'XY', "sketch().push([(-42, 50)]).circle(33).finalize()", 60)
r=extrude(r, (2, 4, -24), 'XY', "sketch().segment((-58, 4), (62, 4)).segment((40, -23)).arc((55, -61), (40, -98)).arc((2, -114), (-36, -98)).arc((-51, -61), (-36, -23)).close().assemble().finalize()", -78)
