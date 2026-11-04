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
r=extrude(r, (97, 0, 0), 'YZ', "sketch().push([(-2, 3)]).rect(22, 30).finalize()", -193)
r=extrude(r, (80, -2, 3), 'YZ', "sketch().push([(-2, 3)]).rect(34, 44).finalize()", -40, False)
r=extrude(r, (75, -18, 12), 'ZX', "sketch().push([(12, 75)]).circle(13).finalize()", -6)
r=extrude(r, (17, 9, -9), 'ZX', "sketch().segment((-22, 3), (-22, 4)).segment((-13, 35)).segment((-12, 35)).arc((-4, 35), (4, 31)).segment((4, 30)).segment((-5, -1)).segment((-6, -1)).arc((-14, -1), (-22, 3)).assemble().finalize()", 16)
r=extrude(r, (59, 1, -20), 'XY', "sketch().segment((40, -7), (40, -3)).arc((55, 19), (76, 3)).segment((78, 2)).segment((75, -13)).segment((70, -12)).arc((55, -17), (42, -7)).close().assemble().finalize()", -6)
r=extrude(r, (70, 15, -4), 'ZX', "sketch().push([(-4, 70)]).circle(4).finalize()", 4)
