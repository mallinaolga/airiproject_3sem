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
r=extrude(r, (90, 0, 0), 'YZ', "sketch().push([(-2, 3)]).circle(14).finalize()", -196)
r=extrude(r, (-23, -2, 3), 'YZ', "sketch().push([(-2, 3)]).circle(18).finalize()", -38, False)
r=extrude(r, (37, 12, 3), 'ZX', "sketch().push([(3, 37)]).circle(15).finalize()", 4)
r=extrude(r, (90, -10, -1), 'YZ', "sketch().push([(-10, -1)]).rect(12, 40).finalize()", 16)
r=extrude(r, (37, 12, -12), 'XY', "sketch().push([(37, 12)]).rect(10, 14).finalize()", -7)
