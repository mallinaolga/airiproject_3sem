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
r=extrude(r, (0, -104, 0), 'ZX', "sketch().push([(0, 1)]).circle(12).finalize()", 208)
r=extrude(r, (1, -38, 0), 'ZX', "sketch().push([(0, 1)]).circle(15).finalize()", 40, False)
r=extrude(r, (-15, -11, 0), 'YZ', "sketch().segment((-51, 7), (-29, 37)).segment((29, -7)).segment((7, -37)).close().assemble().finalize()", -2)
r=extrude(r, (1, -14, -15), 'XY', "sketch().segment((0, -13), (1, -13)).segment((2, -15)).segment((1, -15)).close().assemble().finalize()", -3)
