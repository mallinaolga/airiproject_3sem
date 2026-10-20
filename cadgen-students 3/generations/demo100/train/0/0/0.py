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
r=extrude(r, (0, 0, -100), 'XY', "sketch().segment((-85, -35), (-85, 90)).segment((19, 90)).segment((19, 44)).segment((85, 44)).segment((85, -90)).segment((-50, -90)).segment((-50, -35)).close().assemble().finalize()", 200)
