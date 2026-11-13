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
r=extrude(r, (0, -80, 0), 'ZX', "sketch().push([(7, -5)]).circle(9).finalize()", 178)
r=extrude(r, (-5, -71, 7), 'ZX', "sketch().push([(7, -5)]).circle(10).finalize()", 20, False)
r=extrude(r, (5, -79, 7), 'YZ', "sketch().push([(-79, 7)]).rect(8, 34).finalize()", 22)
r=extrude(r, (-16, -56, 7), 'YZ', "sketch().push([(-56, 7)]).circle(12).finalize()", -8)
r=extrude(r, (27, -82, -4), 'YZ', "sketch().push([(-82, -4)]).circle(15).finalize()", 6)
r=extrude(r, (27, -83, -17), 'XY', "sketch().push([(-2.5, -83)]).rect(59, 22).finalize()", -7)
r=extrude(r, (-23, -64, 6), 'YZ', "sketch().push([(-64, 6)]).rect(4, 2).finalize()", -7)
