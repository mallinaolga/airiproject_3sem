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
r=extrude(r, (0, -108, 0), 'ZX', "sketch().push([(4, 6)]).circle(20).finalize()", 216)
r=extrude(r, (6, -25, 4), 'ZX', "sketch().push([(4, 6)]).circle(27).finalize()", 45, False)
r=extrude(r, (-20, -8, 4), 'YZ', "sketch().push([(-8, 4)]).circle(26).finalize()", -13)
r=extrude(r, (6, 4, -22), 'XY', "sketch().segment((-2, -18), (2, 0)).arc((0, 5), (4, 10)).segment((8, 28)).segment((14, 26)).segment((10, 8)).arc((12, 3), (8, -2)).segment((4, -20)).close().assemble().finalize()", -9)
