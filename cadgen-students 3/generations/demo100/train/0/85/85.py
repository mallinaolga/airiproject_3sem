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
r=extrude(r, (0, 0, -7), 'XY', "sketch().arc((12, -13), (-100, 6), (14, 3)).arc((24, 21), (41, 32)).segment((41, 39)).segment((71, 39)).segment((71, 32)).arc((100, -9), (71, -50)).segment((71, -58)).segment((41, -58)).segment((41, -50)).arc((21, -36), (12, -13)).assemble().finalize()", 14)
