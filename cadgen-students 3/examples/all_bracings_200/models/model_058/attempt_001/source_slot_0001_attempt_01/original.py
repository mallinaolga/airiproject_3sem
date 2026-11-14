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
r=extrude(r, (58, 0, 0), 'YZ', "sketch().push([(-41.5, 3)]).rect(13, 16).finalize()", -149)
r=extrude(r, (11, -41, 3), 'YZ', "sketch().push([(-41, 3)]).rect(18, 22).finalize()", -16, False)
r=extrude(r, (-49, -36, 11), 'ZX', "sketch().push([(-28.5, -49)]).rect(79, 78).finalize()", 62)
r=extrude(r, (-10, 14, -17), 'XY', "sketch().push([(37.5, 14)]).rect(95, 74).finalize()", -43)
r=extrude(r, (6, -47, -8), 'XY', "sketch().push([(6, -47)]).circle(1).finalize()", -16)
r=extrude(r, (7, -40, 14), 'XY', "sketch().push([(7, -40)]).circle(4).finalize()", 54)
