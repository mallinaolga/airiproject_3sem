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
r=extrude(r, (0, 0, -56), 'XY', "sketch().push([(7, -30)]).circle(70).finalize()", 79)
r=extrude(r, (19, 26, -56), 'YZ', "sketch().segment((-42, -62), (-42, -56)).segment((94, -56)).segment((92, -63)).close().assemble().finalize()", -96)
r=extrude(r, (7, 40, 11), 'ZX', "sketch().segment((-41, -41), (-41, 55)).segment((-7, 55)).arc((11, 58), (29, 55)).segment((63, 55)).segment((63, -41)).segment((29, -41)).arc((11, -44), (-7, -41)).close().assemble().finalize()", 60)
