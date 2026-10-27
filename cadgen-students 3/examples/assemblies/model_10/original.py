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
r=extrude(r, (0, 0, -106), 'XY', "sketch().push([(-0.5, -4)]).rect(17, 24).finalize()", 220)
r=extrude(r, (-1, -4, 15), 'XY', "sketch().push([(-1, -4)]).rect(20, 28).finalize()", 77, False)
r=extrude(r, (7, 8, 105), 'ZX', "sketch().push([(105, 7)]).circle(5).finalize()", 1)
r=extrude(r, (-3, -16, -11), 'ZX', "sketch().push([(-11, -3)]).circle(20).finalize()", -7)
r=extrude(r, (-9, -1, -19), 'YZ', "sketch().push([(-1, -19)]).circle(8).finalize()", -11)
r=extrude(r, (8, 7, -5), 'YZ', "sketch().segment((-11, -19), (10, 17)).segment((25, 9)).segment((4, -27)).close().assemble().finalize()", 8)
r=extrude(r, (0, -2, -106), 'XY', "sketch().push([(0, -2)]).circle(22).finalize()", -8)
