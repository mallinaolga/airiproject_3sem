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
r=extrude(r, (-119, 0, 0), 'YZ', "sketch().push([(0, 9)]).rect(34, 44).finalize()", 204)
r=extrude(r, (31, 0, 10), 'YZ', "sketch().push([(0, 10)]).rect(60, 76).finalize()", 28, False)
r=extrude(r, (44, 18, -29), 'XY', "sketch().push([(44, 18)]).circle(4).finalize()", -3)
r=extrude(r, (59, -6, 31), 'ZX', "sketch().push([(30.5, 59)]).rect(1, 120).finalize()", -5)
r=extrude(r, (-12, -1, -13), 'XY', "sketch().push([(-12, -1)]).rect(26, 20).finalize()", -35)
