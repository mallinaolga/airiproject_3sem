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
r=extrude(r, (0, 0, -34), 'XY', "sketch().push([(61, -10)]).circle(34).finalize()", 123)
r=extrude(r, (61, -10, 56), 'XY', "sketch().push([(61, -10)]).circle(48).finalize()", 16, False)
r=extrude(r, (67, -49, 73), 'XY', "sketch().push([(67, -49)]).circle(1).finalize()", 35)
r=extrude(r, (47, 14, -34), 'YZ', "sketch().push([(14, -50.5)]).rect(88, 33).finalize()", -155)
r=extrude(r, (94, -44, 57), 'XY', "sketch().push([(94, -44)]).circle(7).finalize()", -164)
r=extrude(r, (48, -18, 89), 'XY', "sketch().segment((38, -17), (54, -10)).segment((58, -19)).segment((42, -26)).close().assemble().finalize()", 14)
r=extrude(r, (47, 13, -59), 'YZ', "sketch().push([(13, -59)]).rect(64, 10).finalize()", 18)
r=extrude(r, (-95, 36, -34), 'XY', "sketch().push([(-95, 36)]).circle(13).finalize()", 32)
