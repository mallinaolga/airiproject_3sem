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
r=extrude(r, (0, 60, 0), 'ZX', "sketch().push([(0, 12)]).circle(22).finalize()", -168)
r=extrude(r, (12, -47, 0), 'ZX', "sketch().push([(0, 12)]).circle(33).finalize()", -32, False)
r=extrude(r, (-21, -53, 0), 'YZ', "sketch().push([(-53, 0)]).rect(8, 4).finalize()", -24)
r=extrude(r, (43, -48, 4), 'ZX', "sketch().push([(4, 43)]).rect(2, 4).finalize()", 62)
r=extrude(r, (3, 60, 1), 'ZX', "sketch().push([(1, 3)]).circle(5).finalize()", 37)
r=extrude(r, (43, -19, 5), 'XY', "sketch().push([(43, -19)]).circle(1).finalize()", 19)
r=extrude(r, (3, 84, -4), 'XY', "sketch().push([(3, 84)]).circle(25).finalize()", -8)
