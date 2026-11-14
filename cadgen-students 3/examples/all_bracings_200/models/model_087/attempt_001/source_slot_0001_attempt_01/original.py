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
r=extrude(r, (119, 0, 0), 'YZ', "sketch().push([(-7.5, -32.5)]).rect(67, 7).finalize()", -238)
r=extrude(r, (-90, -8, -32), 'YZ', "sketch().push([(-8, -32)]).rect(106, 12).finalize()", -25, False)
r=extrude(r, (-3, 1, -29), 'XY', "sketch().push([(-3, 1)]).rect(156, 120).finalize()", 24)
r=extrude(r, (65, 48, -5), 'XY', "sketch().push([(65, 48)]).circle(1).finalize()", 43)
r=extrude(r, (-10, -51, -5), 'XY', "sketch().push([(-10, -51)]).rect(2, 10).finalize()", 24)
r=extrude(r, (28, -42, -29), 'ZX', "sketch().segment((-29, 17), (-29, 39)).segment((-11, 36)).arc((-3, 39), (4, 36)).arc((8, 28), (4, 20)).arc((-3, 17), (-11, 20)).close().assemble().finalize()", -4)
