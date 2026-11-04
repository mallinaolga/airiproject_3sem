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
r=extrude(r, (103, 0, 0), 'YZ', "sketch().push([(2.5, -3)]).rect(21, 22).finalize()", -205)
r=extrude(r, (93, 2, -4), 'YZ', "sketch().push([(2, -4)]).rect(30, 28).finalize()", -28, False)
r=extrude(r, (73, -12, -3), 'ZX', "sketch().push([(-3, 73)]).circle(3).finalize()", -2)
r=extrude(r, (2, -4, -14), 'XY', "sketch().push([(2, -4)]).rect(2, 6).finalize()", -7)
r=extrude(r, (-23, -7, 8), 'XY', "sketch().push([(-23, -7)]).rect(40, 20).finalize()", 13)
