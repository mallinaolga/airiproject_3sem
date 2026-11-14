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
r=extrude(r, (0, -64, 0), 'ZX', "sketch().push([(14.5, -10)]).rect(29, 16).finalize()", 157)
r=extrude(r, (-10, 87, 15), 'ZX', "sketch().push([(15, -10)]).rect(46, 26).finalize()", 29, False)
r=extrude(r, (3, 87, 9), 'ZX', "sketch().push([(9, 3)]).rect(8, 34).finalize()", -66)
r=extrude(r, (-18, 10, 24), 'YZ', "sketch().push([(10, 24)]).rect(70, 76).finalize()", -7)
r=extrude(r, (4, 29, 5), 'XY', "sketch().push([(4, 29)]).circle(2).finalize()", -33)
r=extrude(r, (-2, 109, -7), 'XY', "sketch().push([(-2, 109)]).rect(2, 2).finalize()", -7)
r=extrude(r, (-22, -25, -10), 'YZ', "sketch().push([(-66, -10)]).rect(82, 108).finalize()", -17)
r=extrude(r, (-38, -59, 43), 'XY', "sketch().push([(-38, -59)]).circle(10).finalize()", 21)
r=extrude(r, (-22, -85, 17), 'XY', "sketch().segment((-22, -116), (-22, -54)).segment((-5, -63)).arc((17, -54), (39, -63)).arc((48, -85), (39, -107)).arc((17, -116), (-5, -107)).close().assemble().finalize()", -43)
