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
r=extrude(r, (0, 97, 0), 'ZX', "sketch().push([(0, -10)]).rect(22, 2).finalize()", -113)
r=extrude(r, (-10, -4, 0), 'ZX', "sketch().push([(0, -10)]).rect(26, 2).finalize()", -25, False)
r=extrude(r, (-11, 88, 0), 'ZX', "sketch().segment((-5, -11), (2, 11)).segment((5, 11)).segment((5, -11)).close().assemble().finalize()", 13)
r=extrude(r, (-9, -19, 10), 'XY', "sketch().push([(-9.5, -19)]).rect(1, 164).finalize()", -18)
r=extrude(r, (-9, 52, 3), 'YZ', "sketch().push([(52, 3)]).circle(3).finalize()", 2)
r=extrude(r, (-9, 81, -4), 'YZ', "sketch().push([(81, -4)]).rect(8, 12).finalize()", 3)
