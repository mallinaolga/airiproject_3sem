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
r=extrude(r, (-105, 0, 0), 'YZ', "sketch().push([(16, 0)]).circle(16).finalize()", 192)
r=extrude(r, (32, 16, 0), 'YZ', "sketch().push([(16, 0)]).circle(24).finalize()", 87, False)
r=extrude(r, (92, -8, 0), 'ZX', "sketch().push([(0, 92)]).circle(1).finalize()", -25)
r=extrude(r, (76, -8, 0), 'ZX', "sketch().segment((-7, 80), (-6, 81)).segment((7, 72)).segment((6, 71)).close().assemble().finalize()", -18)
r=extrude(r, (-74, 0, 0), 'YZ', "sketch().arc((-29, -9), (-33, 0), (-29, 9)).arc((-20, 13), (-11, 9)).segment((7, 13)).arc((0, 0), (7, -13)).segment((-11, -9)).arc((-20, -13), (-29, -9)).assemble().finalize()", -45)
r=extrude(r, (73, -26, 4), 'ZX', "sketch().push([(4, 73)]).circle(1).finalize()", -13)
