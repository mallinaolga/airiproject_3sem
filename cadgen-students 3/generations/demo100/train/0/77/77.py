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
r=extrude(r, (0, 0, -63), 'XY', "sketch().segment((-22, -25), (-22, 75)).segment((100, 75)).arc((54, 34), (37, -25)).close().assemble().finalize()", 100)
r=extrude(r, (-22, -21, 34), 'YZ', "sketch().segment((-75, 13), (-71, 63)).segment((10, 57)).arc((10, 55), (12, 54)).segment((12, 52)).segment((16, 52)).segment((16, 54)).arc((17, 55), (17, 57)).segment((33, 55)).segment((29, 5)).close().assemble().finalize()", -15)
r=extrude(r, (-22, 14, -57), 'YZ', "sketch().arc((7, -59), (14, -55), (21, -59)).segment((18, -59)).arc((17, -58), (16, -58)).segment((16, -59)).segment((12, -59)).segment((12, -58)).arc((11, -58), (10, -59)).close().assemble().finalize()", -78)
