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
r=extrude(r, (0, -73, 0), 'ZX', "sketch().segment((-83, -100), (-83, 100)).segment((-49, 100)).segment((49, 100)).segment((83, 100)).segment((83, -100)).segment((49, -100)).segment((-49, -100)).close().assemble().finalize()", 143)
r=extrude(r, (71, 70, -65), 'ZX', "sketch().segment((-76, 65), (-76, 81)).segment((-64, 81)).segment((-64, 76)).arc((-61, 76), (-59, 74)).segment((-56, 75)).segment((-54, 68)).segment((-56, 67)).arc((-61, 62), (-68, 63)).segment((-71, 62)).segment((-72, 65)).close().assemble().finalize()", 3)
