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
r=extrude(r, (-92, 0, 0), 'YZ', "sketch().push([(2, 8)]).rect(30, 16).finalize()", 196)
r=extrude(r, (-16, 2, 8), 'YZ', "sketch().push([(2, 8)]).rect(44, 24).finalize()", 21, False)
r=extrude(r, (-60, -13, 8), 'ZX', "sketch().segment((4, -60), (5, -59)).segment((12, -60)).segment((11, -61)).close().assemble().finalize()", -8)
r=extrude(r, (-15, -14, -3), 'ZX', "sketch().segment((-3, -68), (-3, 38)).segment((0, -10)).arc((5, -9), (9, -10)).arc((11, -15), (9, -20)).arc((5, -21), (0, -20)).close().assemble().finalize()", -10)
r=extrude(r, (77, 0, 0), 'XY', "sketch().push([(77, 0)]).circle(12).finalize()", -20)
r=extrude(r, (-92, 2, 11), 'YZ', "sketch().push([(2, 11)]).rect(4, 4).finalize()", -11)
