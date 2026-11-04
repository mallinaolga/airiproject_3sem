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
r=extrude(r, (0, 0, 98), 'XY', "sketch().push([(0, 5)]).rect(98, 42).finalize()", -196)
r=extrude(r, (0, 5, 15), 'XY', "sketch().push([(0, 5)]).rect(152, 64).finalize()", -26, False)
r=extrude(r, (49, 2, -16), 'YZ', "sketch().push([(2, -16)]).circle(3).finalize()", 3)
r=extrude(r, (35, -16, 80), 'ZX', "sketch().push([(80, 35)]).rect(10, 8).finalize()", -34)
r=extrude(r, (-32, 37, 1), 'ZX', "sketch().push([(1, -32)]).rect(36, 8).finalize()", 13)
