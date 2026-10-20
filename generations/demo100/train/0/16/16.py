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
r=extrude(r, (0, -10, 0), 'ZX', "sketch().segment((-18, -71), (-8, -50)).arc((6, 83), (3, -51)).arc((12, -54), (21, -55)).segment((8, -83)).close().assemble().finalize()", -90)
r=extrude(r, (55, -10, 0), 'YZ', "sketch().segment((-10, -78), (-10, 78)).segment((16, 35)).arc((51, 50), (86, 35)).arc((100, 0), (86, -35)).arc((51, -50), (16, -35)).close().assemble().finalize()", -68)
