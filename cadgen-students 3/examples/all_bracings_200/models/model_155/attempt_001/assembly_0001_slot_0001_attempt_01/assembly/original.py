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
r=extrude(r, (110, 0, 0), 'YZ', "sketch().push([(3.5, -2)]).rect(3, 54).finalize()", -221)
r=extrude(r, (50, 4, -2), 'YZ', "sketch().push([(4, -2)]).rect(2, 58).finalize()", -41, False)
r=extrude(r, (24, 2, -4), 'ZX', "sketch().segment((-7, 28), (-3, 29)).segment((-1, 20)).segment((-5, 19)).close().assemble().finalize()", -19)
r=extrude(r, (15, 4, 27), 'XY', "sketch().push([(15, 4)]).rect(62, 10).finalize()", 7)
r=extrude(r, (14, 5, -13), 'ZX', "sketch().segment((-17, 12), (-10, 18)).segment((-9, 16)).segment((-16, 10)).close().assemble().finalize()", 12)
r=extrude(r, (71, 5, -27), 'ZX', "sketch().arc((-27, 68), (-33, 71), (-27, 74)).arc((-21, 70), (-27, 68)).assemble().finalize()", 7)
