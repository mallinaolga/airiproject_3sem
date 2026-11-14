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
r=extrude(r, (-37, 0, 0), 'YZ', "sketch().push([(-30.5, -2.5)]).rect(1, 7).finalize()", 57)
r=extrude(r, (-16, -30, -3), 'YZ', "sketch().push([(-30, -3)]).rect(2, 8).finalize()", 15, False)
r=extrude(r, (-16, -31, -5), 'ZX', "sketch().push([(-5, -7.5)]).rect(178, 17).finalize()", 57)
r=extrude(r, (-9, 27, 11), 'ZX', "sketch().push([(11, -9)]).rect(10, 10).finalize()", 37)
r=extrude(r, (-10, 13, 85), 'XY', "sketch().push([(-10, 13)]).circle(1).finalize()", 9)
r=extrude(r, (2, -25, 58), 'YZ', "sketch().push([(-25, 58)]).circle(34).finalize()", 41)
r=extrude(r, (-2, -31, -7), 'ZX', "sketch().push([(-24.5, -2)]).rect(35, 82).finalize()", -33)
