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
r=extrude(r, (99, 0, 0), 'YZ', "sketch().push([(-7, 3)]).circle(14).finalize()", -209)
r=extrude(r, (-44, -7, 3), 'YZ', "sketch().push([(-7, 3)]).circle(20).finalize()", -27, False)
r=extrude(r, (67, -7, -11), 'YZ', "sketch().arc((-11, -10), (-7, -11), (-3, -10)).segment((-4, -16)).arc((-3, -19), (-4, -22)).arc((-7, -23), (-10, -22)).arc((-11, -19), (-10, -16)).close().assemble().finalize()", 43)
r=extrude(r, (-56, 13, 3), 'ZX', "sketch().push([(3, -56)]).circle(1).finalize()", 14)
