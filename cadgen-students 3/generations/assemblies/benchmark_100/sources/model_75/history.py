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
r=extrude(r, (0, 38, 0), 'ZX', "sketch().push([(-15.5, -9.5)]).rect(67, 3).finalize()", -143)
r=extrude(r, (-9, -9, -15), 'ZX', "sketch().push([(-15, -9)]).rect(70, 2).finalize()", -16, False)
r=extrude(r, (-8, -46, -20), 'YZ', "sketch().push([(-46, -20)]).rect(42, 46).finalize()", 39)
r=extrude(r, (26, -25, -6), 'ZX', "sketch().push([(-6, 26)]).circle(4).finalize()", 98)
r=extrude(r, (31, -59, -3), 'YZ', "sketch().segment((-73, -7), (-68, 8)).segment((-45, 1)).segment((-50, -14)).close().assemble().finalize()", 31)
r=extrude(r, (-11, -87, 10), 'YZ', "sketch().push([(-87, 10)]).circle(1).finalize()", -48)
r=extrude(r, (-11, 26, 0), 'YZ', "sketch().push([(26, 0)]).circle(79).finalize()", -51)
r=extrude(r, (-9, -15, 20), 'XY', "sketch().push([(-9, -15)]).circle(1).finalize()", 29)
