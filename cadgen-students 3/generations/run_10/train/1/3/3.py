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
r=extrude(r, (-100, 0, 0), 'YZ', "sketch().segment((-45, -93), (-45, 43)).segment((31, 43)).segment((-1, -93)).close().assemble().finalize()", 200)
r=extrude(r, (75, 0, 43), 'XY', "sketch().segment((65, -4), (65, 4)).segment((71, 4)).segment((71, 98)).segment((79, 98)).segment((79, 4)).segment((85, 4)).segment((85, -4)).segment((79, -4)).segment((79, -98)).segment((71, -98)).segment((71, -4)).close().assemble().finalize()", 50)
