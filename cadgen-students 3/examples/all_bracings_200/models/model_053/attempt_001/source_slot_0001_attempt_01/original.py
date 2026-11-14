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
r=extrude(r, (92, 0, 0), 'YZ', "sketch().push([(0, -13)]).circle(11).finalize()", -184)
r=extrude(r, (52, 0, -13), 'YZ', "sketch().push([(0, -13)]).circle(16).finalize()", -34, False)
r=extrude(r, (-70, 11, -13), 'ZX', "sketch().segment((-21, -60), (-12, -58)).segment((-5, -80)).segment((-14, -82)).close().assemble().finalize()", 4)
r=extrude(r, (67, 0, -2), 'YZ', "sketch().segment((-7, -5), (-7, 29)).segment((7, 29)).segment((7, -5)).arc((0, -2), (-7, -5)).assemble().finalize()", 20)
r=extrude(r, (25, 0, 2), 'XY', "sketch().push([(25, 0)]).circle(21).finalize()", 9)
