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
r=extrude(r, (-92, 0, 0), 'YZ', "sketch().push([(1.5, -9)]).rect(27, 6).finalize()", 184)
r=extrude(r, (46, 1, -9), 'YZ', "sketch().push([(1, -9)]).rect(30, 6).finalize()", 26, False)
r=extrude(r, (10, 14, -6), 'ZX', "sketch().push([(-6.5, 10)]).rect(1, 86).finalize()", -36)
r=extrude(r, (88, 2, -6), 'XY', "sketch().push([(88, 2)]).rect(4, 2).finalize()", 8)
r=extrude(r, (87, -1, -6), 'XY', "sketch().push([(87, -1)]).rect(10, 2).finalize()", 43)
r=extrude(r, (-35, 8, -12), 'XY', "sketch().push([(-35, 8)]).circle(3).finalize()", -25)
r=extrude(r, (62, 15, -8), 'ZX', "sketch().push([(-8, 62)]).rect(24, 32).finalize()", 5)
