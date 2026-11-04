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
r=extrude(r, (0, -101, 0), 'ZX', "sketch().push([(0, 0)]).rect(14, 22).finalize()", 201)
r=extrude(r, (0, -13, 0), 'ZX', "sketch().push([(0, 0)]).rect(24, 38).finalize()", 23, False)
r=extrude(r, (-1, 89, -7), 'XY', "sketch().push([(-1, 89)]).circle(5).finalize()", -5)
r=extrude(r, (-11, -65, -3), 'YZ', "sketch().push([(-65, -3)]).circle(2).finalize()", -4)
