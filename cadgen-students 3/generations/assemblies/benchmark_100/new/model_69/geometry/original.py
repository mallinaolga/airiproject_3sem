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
r=extrude(r, (0, 0, 97), 'XY', "sketch().push([(3.5, -1)]).rect(9, 20).finalize()", -195)
r=extrude(r, (4, -1, 95), 'XY', "sketch().push([(4, -1)]).rect(12, 26).finalize()", -37, False)
r=extrude(r, (8, 9, 37), 'ZX', "sketch().push([(37, 8)]).circle(17).finalize()", 5)
r=extrude(r, (8, 7, -65), 'YZ', "sketch().push([(7, -65)]).circle(1).finalize()", 13)
r=extrude(r, (-1, -7, 15), 'YZ', "sketch().push([(-7, 15)]).circle(2).finalize()", -24)
