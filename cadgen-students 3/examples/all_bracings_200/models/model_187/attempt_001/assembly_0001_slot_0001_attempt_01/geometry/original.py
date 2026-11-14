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
r=extrude(r, (0, 0, -119), 'XY', "sketch().push([(7, -3)]).circle(12).finalize()", 237)
r=extrude(r, (7, -3, -73), 'XY', "sketch().push([(7, -3)]).circle(20).finalize()", 45, False)
r=extrude(r, (-6, -3, 57), 'YZ', "sketch().push([(-3, 57)]).rect(54, 88).finalize()", -16)
r=extrude(r, (-17, 13, 14), 'XY', "sketch().push([(-17, 13)]).circle(9).finalize()", -85)
r=extrude(r, (-14, 24, 55), 'ZX', "sketch().push([(55, -14)]).rect(20, 2).finalize()", 6)
