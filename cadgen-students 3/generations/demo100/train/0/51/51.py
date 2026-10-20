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
r=extrude(r, (2, 0, 0), 'YZ', "sketch().segment((-100, -71), (-71, -43)).arc((-58, 60), (45, 70)).segment((74, 98)).segment((100, 71)).segment((71, 43)).arc((58, -60), (-45, -70)).segment((-74, -98)).close().assemble().finalize()", -4)
