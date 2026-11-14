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
r=extrude(r, (98, 0, 0), 'YZ', "sketch().push([(13, -1)]).circle(7).finalize()", -140)
r=extrude(r, (42, 13, -1), 'YZ', "sketch().push([(13, -1)]).circle(9).finalize()", -53, False)
r=extrude(r, (-9, 4, -1), 'ZX', "sketch().segment((-32, -98), (-32, 80)).arc((30, -9), (-32, -98)).assemble().finalize()", -20)
r=extrude(r, (-9, -9, 31), 'XY', "sketch().push([(-9, -9)]).rect(36, 26).finalize()", 2)
r=extrude(r, (5, 13, 8), 'XY', "sketch().segment((-1, 19), (10, 19)).segment((11, 7)).segment((0, 7)).close().assemble().finalize()", 21)
