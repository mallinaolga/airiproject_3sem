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
r=extrude(r, (0, 0, -17), 'XY', "sketch().segment((-75, 66), (-16, 100)).segment((75, -60)).segment((59, -78)).segment((19, -100)).segment((-32, -9)).arc((-20, 27), (-57, 34)).close().assemble().finalize()", 34)
