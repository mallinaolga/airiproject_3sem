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
r=extrude(r, (33, 0, 0), 'YZ', "sketch().segment((-100, -79), (-100, 79)).segment((-87, 79)).segment((-87, 81)).segment((-56, 81)).segment((-56, 79)).segment((-43, 79)).segment((-43, -36)).segment((100, -36)).segment((100, -41)).segment((-43, -41)).segment((-43, -79)).segment((-56, -79)).segment((-56, -81)).segment((-87, -81)).segment((-87, -79)).close().assemble().finalize()", -67)
