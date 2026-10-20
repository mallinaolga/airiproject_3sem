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
r=extrude(r, (-100, 0, 0), 'YZ', "sketch().segment((-30, -18), (-30, 18)).arc((3, 9), (35, 18)).segment((35, -18)).close().assemble().finalize()", 200)
r=extrude(r, (-41, -30, -11), 'ZX', "sketch().segment((-12, -44), (-12, -38)).segment((-10, -38)).arc((-8, -41), (-10, -44)).close().assemble().finalize()", -5)
