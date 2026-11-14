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
r=extrude(r, (0, 0, 55), 'XY', "sketch().push([(0, 10)]).circle(25).finalize()", -159)
r=extrude(r, (0, 10, -2), 'XY', "sketch().push([(0, 10)]).circle(31).finalize()", -20, False)
r=extrude(r, (0, -15, 44), 'XY', "sketch().arc((-10, -12), (0, -15), (10, -12)).segment((7, -20)).arc((10, -28), (7, -35)).arc((0, -38), (-7, -35)).arc((-10, -28), (-7, -20)).close().assemble().finalize()", 21)
r=extrude(r, (0, 35, 12), 'ZX', "sketch().push([(12, 0)]).rect(20, 78).finalize()", 1)
r=extrude(r, (0, -38, 59), 'XY', "sketch().segment((-6, -41), (-6, -35)).arc((0, -38), (6, -35)).segment((6, -41)).close().assemble().finalize()", 46)
r=extrude(r, (6, -40, 95), 'YZ', "sketch().push([(-40, 95)]).rect(2, 2).finalize()", 33)
