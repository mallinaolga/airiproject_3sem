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
r=extrude(r, (0, 106, 0), 'ZX', "sketch().push([(1, -1.5)]).rect(4, 25).finalize()", -212)
r=extrude(r, (-2, -12, 1), 'ZX', "sketch().push([(1, -2)]).rect(6, 34).finalize()", -25, False)
r=extrude(r, (-5, -35, 4), 'XY', "sketch().push([(-5, -35)]).circle(1).finalize()", 7)
r=extrude(r, (-12, 48, -1), 'XY', "sketch().push([(-12, 48)]).circle(9).finalize()", -11)
r=extrude(r, (0, -62, 3), 'XY', "sketch().push([(0, -62)]).circle(28).finalize()", 15)
r=extrude(r, (11, 43, 0), 'YZ', "sketch().push([(43, 0)]).rect(18, 54).finalize()", 2)
