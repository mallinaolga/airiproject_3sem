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
r=extrude(r, (0, -98, 0), 'ZX', "sketch().push([(10.5, 5.5)]).rect(5, 21).finalize()", 178)
r=extrude(r, (5, 20, 11), 'ZX', "sketch().push([(11, 5)]).rect(8, 34).finalize()", 81, False)
r=extrude(r, (-2, -62, 8), 'XY', "sketch().push([(-2, -62)]).circle(3).finalize()", -14)
r=extrude(r, (-9, 70, 7), 'XY', "sketch().push([(-9, 70)]).rect(26, 86).finalize()", -6)
r=extrude(r, (-2, -93, 8), 'ZX', "sketch().push([(-3, -2)]).rect(22, 6).finalize()", -21)
r=extrude(r, (-7, 71, 1), 'XY', "sketch().segment((-19, 76), (-9, 84)).segment((5, 66)).segment((-5, 58)).close().assemble().finalize()", -2)
r=extrude(r, (-13, 78, -1), 'XY', "sketch().push([(-13, 78)]).circle(9).finalize()", -10)
