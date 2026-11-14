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
r=extrude(r, (-97, 0, 0), 'YZ', "sketch().push([(0, -5)]).rect(22, 18).finalize()", 211)
r=extrude(r, (-69, 0, -5), 'YZ', "sketch().push([(0, -5)]).rect(36, 28).finalize()", 23, False)
r=extrude(r, (-4, -4, 4), 'ZX', "sketch().push([(-1, -4)]).rect(10, 216).finalize()", -4)
r=extrude(r, (-87, -5, 4), 'XY', "sketch().push([(-87, -5)]).circle(4).finalize()", 15)
r=extrude(r, (-108, -6, -7), 'XY', "sketch().segment((-115, -7), (-108, 1)).segment((-101, -5)).segment((-108, -13)).close().assemble().finalize()", -8)
r=extrude(r, (42, -11, 2), 'ZX', "sketch().push([(2, 42)]).circle(1).finalize()", -6)
