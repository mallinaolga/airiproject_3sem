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
r=extrude(r, (0, -98, 0), 'ZX', "sketch().push([(0, -11)]).rect(24, 10).finalize()", 207)
r=extrude(r, (-11, -97, 0), 'ZX', "sketch().push([(0, -11)]).rect(36, 14).finalize()", 34, False)
r=extrude(r, (-18, -68, -13), 'YZ', "sketch().push([(-68, -13)]).circle(2).finalize()", -4)
r=extrude(r, (-16, 38, -1), 'YZ', "sketch().push([(38, -1)]).rect(34, 22).push([(38, -1)]).circle(8, mode='s').finalize()", -3)
r=extrude(r, (-6, 46, 2), 'ZX', "sketch().push([(2, 8)]).rect(26, 28).finalize()", -41)
r=extrude(r, (-4, -90, 7), 'XY', "sketch().segment((-4, -110), (-4, -70)).segment((1, -84)).arc((7, -81), (13, -84)).arc((16, -90), (13, -96)).arc((7, -99), (1, -96)).close().assemble().finalize()", -10)
