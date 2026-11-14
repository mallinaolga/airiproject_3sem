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
r=extrude(r, (0, 0, 87), 'XY', "sketch().push([(-21.5, 71)]).rect(65, 16).finalize()", -173)
r=extrude(r, (-21, 71, 32), 'XY', "sketch().push([(-21, 71)]).rect(106, 26).finalize()", -42, False)
r=extrude(r, (23, 66, -10), 'XY', "sketch().push([(23, 66)]).circle(3).finalize()", -23)
r=extrude(r, (-50, 61, -27), 'ZX', "sketch().segment((-51, -47), (-18, -28)).segment((-3, -53)).segment((-36, -72)).close().assemble().finalize()", -152)
r=extrude(r, (2, 84, 7), 'ZX', "sketch().push([(7, 2)]).circle(34).finalize()", 7)
r=extrude(r, (11, 66, 34), 'YZ', "sketch().push([(66, 34)]).circle(1).finalize()", 63)
r=extrude(r, (11, 65, -37), 'YZ', "sketch().push([(65, -37)]).circle(18).finalize()", 41)
