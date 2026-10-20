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
r=extrude(r, (0, 25, 0), 'ZX', "sketch().segment((-74, -51), (-74, -29)).segment((-35, -29)).arc((-11, -21), (14, -29)).segment((74, -29)).segment((74, -51)).segment((28, -51)).arc((-11, -100), (-49, -51)).close().assemble().finalize()", -53)
r=extrude(r, (-29, 10, -57), 'YZ', "sketch().segment((-9, -55), (-9, -49)).segment((-3, -49)).arc((2, -45), (8, -49)).segment((12, -49)).segment((12, -53)).arc((28, -64), (10, -55)).segment((5, -55)).arc((2, -56), (0, -55)).close().assemble().push([(10, -51)]).circle(1, mode='s').finalize()", 129)
