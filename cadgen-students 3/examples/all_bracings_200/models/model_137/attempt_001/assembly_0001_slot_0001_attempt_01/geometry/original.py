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
r=extrude(r, (0, 0, 85), 'XY', "sketch().push([(-0.5, -4)]).rect(21, 6).finalize()", -192)
r=extrude(r, (-1, -4, -5), 'XY', "sketch().push([(-1, -4)]).rect(26, 8).finalize()", -29, False)
r=extrude(r, (-11, -4, 84), 'ZX', "sketch().segment((61, -11), (78, -7)).arc((76, -1), (78, 5)).arc((84, 8), (90, 5)).arc((92, -1), (90, -7)).segment((107, -11)).close().assemble().push([(84, -1)]).circle(4, mode='s').finalize()", 5)
r=extrude(r, (2, 0, 16), 'ZX', "sketch().push([(16, 2)]).circle(12).finalize()", 7)
