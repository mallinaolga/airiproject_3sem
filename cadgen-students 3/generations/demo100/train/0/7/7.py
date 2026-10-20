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
r=extrude(r, (0, -100, 0), 'ZX', "sketch().segment((-65, -35), (-23, 29)).segment((-23, 61)).segment((-1, 61)).segment((7, 74)).segment((65, 35)).segment((23, -29)).segment((23, -61)).segment((1, -61)).segment((-7, -74)).close().assemble().finalize()", 200)
