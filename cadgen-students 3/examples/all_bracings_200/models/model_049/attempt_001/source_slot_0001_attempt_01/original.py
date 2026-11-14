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
r=extrude(r, (98, 0, 0), 'YZ', "sketch().push([(0, -9)]).circle(13).finalize()", -157)
r=extrude(r, (-54, 0, -9), 'YZ', "sketch().push([(0, -9)]).circle(16).finalize()", -44, False)
r=extrude(r, (-63, 0, 7), 'YZ', "sketch().segment((-11, 2), (-11, 34)).segment((11, 34)).segment((11, 2)).arc((0, 7), (-11, 2)).assemble().finalize()", 37)
r=extrude(r, (-15, 0, -22), 'XY', "sketch().segment((-73, 32), (-46, 58)).segment((43, -32)).segment((16, -58)).close().assemble().finalize()", -13)
r=extrude(r, (84, 13, -9), 'YZ', "sketch().arc((8, -19), (13, -9), (8, 1)).segment((48, 1)).segment((48, -19)).close().assemble().finalize()", -4)
r=extrude(r, (-29, 11, 4), 'ZX', "sketch().push([(4, -29)]).rect(2, 2).finalize()", 5)
