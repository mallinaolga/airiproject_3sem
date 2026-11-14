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
r=extrude(r, (0, 0, 67), 'XY', "sketch().push([(0, 11)]).circle(11).finalize()", -171)
r=extrude(r, (0, 11, -2), 'XY', "sketch().push([(0, 11)]).circle(19).finalize()", -17, False)
r=extrude(r, (17, 9, -1), 'XY', "sketch().push([(17, 9)]).rect(2, 2).finalize()", 10)
r=extrude(r, (0, -8, -14), 'ZX', "sketch().push([(-14, 0)]).circle(1).finalize()", -22)
r=extrude(r, (9, -2, -1), 'XY', "sketch().push([(9, -2)]).circle(2).finalize()", 85)
r=extrude(r, (0, 8, 67), 'XY', "sketch().push([(0, 8)]).rect(2, 2).finalize()", 36)
