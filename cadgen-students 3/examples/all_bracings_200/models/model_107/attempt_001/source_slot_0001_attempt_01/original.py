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
r=extrude(r, (0, -72, 0), 'ZX', "sketch().push([(0, -0.5)]).rect(12, 19).finalize()", 162)
r=extrude(r, (-1, -53, 0), 'ZX', "sketch().push([(0, -1)]).rect(22, 32).finalize()", 17, False)
r=extrude(r, (9, -70, -4), 'ZX', "sketch().push([(-4, -1)]).rect(6, 20).finalize()", -21)
r=extrude(r, (10, -53, -4), 'XY', "sketch().segment((5, -53), (15, -53)).segment((13, -56)).arc((15, -59), (13, -63)).arc((10, -64), (7, -63)).arc((5, -59), (7, -56)).close().assemble().finalize()", -4)
r=extrude(r, (14, -59, -4), 'YZ', "sketch().push([(-59, -4)]).circle(4).finalize()", 3)
