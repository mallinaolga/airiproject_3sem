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
r=extrude(r, (0, -16, 0), 'ZX', "sketch().push([(-32, -14)]).circle(31).finalize()", 128)
r=extrude(r, (-14, 71, -32), 'ZX', "sketch().push([(-32, -14)]).circle(48).finalize()", 21, False)
r=extrude(r, (17, 0, -32), 'ZX', "sketch().segment((-56, 5), (-47, 28)).arc((-53, 42), (-47, 57)).arc((-32, 63), (-17, 57)).arc((-11, 42), (-17, 28)).segment((-8, 5)).arc((-32, 17), (-56, 5)).assemble().finalize()", -36)
r=extrude(r, (-14, 79, 16), 'XY', "sketch().segment((-49, 63), (18, 100)).segment((21, 95)).segment((-46, 58)).close().assemble().finalize()", 24)
r=extrude(r, (-14, 46, -1), 'ZX', "sketch().arc((-13, -38), (-1, -14), (-13, 10)).segment((75, 10)).segment((75, -38)).close().assemble().finalize()", -26)
r=extrude(r, (-4, 21, 70), 'YZ', "sketch().push([(-43.5, 70)]).rect(129, 20).finalize()", 42)
r=extrude(r, (10, 25, 16), 'YZ', "sketch().push([(25, 16)]).circle(3).finalize()", 52)
