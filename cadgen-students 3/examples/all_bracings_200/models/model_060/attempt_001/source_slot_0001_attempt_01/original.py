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
r=extrude(r, (0, 99, 0), 'ZX', "sketch().push([(-7, -0.5)]).rect(28, 3).finalize()", -192)
r=extrude(r, (0, -63, -6), 'ZX', "sketch().push([(-6, 0)]).rect(40, 4).finalize()", -26, False)
r=extrude(r, (-1, -85, 12), 'XY', "sketch().push([(-1, -85)]).rect(34, 28).finalize()", 5)
r=extrude(r, (1, 49, 1), 'YZ', "sketch().push([(49, 1)]).rect(48, 6).finalize()", 12)
r=extrude(r, (16, -74, 17), 'YZ', "sketch().segment((-76, 8), (-76, 19)).segment((-76, 26)).segment((-72, 26)).segment((-72, 8)).close().assemble().finalize()", 2)
r=extrude(r, (-2, -25, 3), 'YZ', "sketch().push([(-25, 3)]).rect(4, 6).finalize()", -9)
