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
r=extrude(r, (0, 0, -103), 'XY', "sketch().push([(7, 0)]).circle(11).finalize()", 205)
r=extrude(r, (7, 0, -69), 'XY', "sketch().push([(7, 0)]).circle(14).finalize()", 65, False)
r=extrude(r, (-3, 0, 32), 'YZ', "sketch().push([(0, 32)]).rect(14, 52).finalize()", -10)
r=extrude(r, (-6, 0, -31), 'YZ', "sketch().segment((-21, -42), (-21, -14)).segment((-12, -14)).segment((-12, -39)).segment((19, -32)).segment((21, -40)).segment((-13, -48)).segment((-15, -42)).close().assemble().finalize()", -4)
r=extrude(r, (7, 13, -62), 'ZX', "sketch().push([(-62, 7)]).rect(8, 26).finalize()", 8)
r=extrude(r, (-3, 0, -81), 'YZ', "sketch().push([(0, -81)]).circle(1).finalize()", -18)
