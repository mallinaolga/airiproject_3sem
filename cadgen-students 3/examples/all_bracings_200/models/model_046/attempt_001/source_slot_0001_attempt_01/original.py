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
r=extrude(r, (0, 24, 0), 'ZX', "sketch().push([(-25, -68.5)]).rect(50, 9).finalize()", -105)
r=extrude(r, (-68, -6, -25), 'ZX', "sketch().push([(-25, -68)]).rect(82, 16).finalize()", -15, False)
r=extrude(r, (-57, 20, -21), 'YZ', "sketch().push([(20, -21)]).circle(50).finalize()", 6)
r=extrude(r, (-53, 20, 29), 'YZ', "sketch().segment((4, 25), (9, 48)).arc((4, 59), (9, 71)).arc((20, 75), (31, 71)).arc((36, 59), (31, 48)).segment((36, 25)).arc((20, 29), (4, 25)).assemble().finalize()", -8)
r=extrude(r, (-51, 1, 2), 'XY', "sketch().push([(-37.5, 1)]).rect(27, 194).finalize()", 64)
r=extrude(r, (-58, 16, -66), 'YZ', "sketch().push([(16, -66)]).circle(9).finalize()", -14)
r=extrude(r, (-51, -2, -43), 'XY', "sketch().segment((-51, -98), (-51, 94)).segment((-21, 39)).arc((19, 55), (60, 39)).arc((76, -2), (60, -43)).arc((19, -59), (-21, -43)).close().assemble().finalize()", -4)
