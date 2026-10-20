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
r=extrude(r, (0, -100, 0), 'ZX', "sketch().segment((-87, 11), (77, 43)).segment((84, 4)).segment((84, 3)).segment((87, -11)).segment((84, -12)).segment((84, -43)).segment((-45, -43)).segment((-45, -37)).segment((-77, -43)).close().assemble().finalize()", 200)
