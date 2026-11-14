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
r=extrude(r, (0, 0, -101), 'XY', "sketch().push([(4, 0)]).circle(19).finalize()", 206)
r=extrude(r, (4, 0, 62), 'XY', "sketch().push([(4, 0)]).circle(26).finalize()", 44, False)
r=extrude(r, (4, 26, 64), 'ZX', "sketch().push([(64, 4)]).circle(8).finalize()", 2)
r=extrude(r, (-15, 0, 3), 'YZ', "sketch().push([(0, 3)]).circle(42).finalize()", -5)
r=extrude(r, (-20, 14, -12), 'YZ', "sketch().push([(14, -12)]).rect(22, 162).finalize()", -3)
r=extrude(r, (-9, -12, -101), 'XY', "sketch().push([(-9, -12)]).circle(21).finalize()", -5)
