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
r=extrude(r, (-101, 0, 0), 'YZ', "sketch().push([(0, 5)]).circle(10).finalize()", 155)
r=extrude(r, (9, 0, 5), 'YZ', "sketch().push([(0, 5)]).circle(16).finalize()", 62, False)
r=extrude(r, (-97, 10, 5), 'ZX', "sketch().segment((-1, -107), (7, -85)).segment((11, -87)).segment((3, -109)).close().assemble().finalize()", 17)
r=extrude(r, (-101, 1, 0), 'YZ', "sketch().push([(1, 0)]).circle(7).finalize()", -2)
r=extrude(r, (67, 0, -11), 'XY', "sketch().push([(67, 0)]).rect(82, 68).finalize()", -10)
r=extrude(r, (-16, 10, 5), 'YZ', "sketch().arc((8, -1), (10, 5), (8, 11)).segment((28, 11)).segment((28, -1)).close().assemble().finalize()", -3)
r=extrude(r, (9, 13, -3), 'YZ', "sketch().push([(13, -3)]).circle(2).finalize()", -38)
