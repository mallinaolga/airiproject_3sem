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
r=extrude(r, (0, 11, 0), 'ZX', "sketch().segment((-100, -64), (-100, 19)).segment((-79, 19)).arc((-52, 73), (-14, 26)).arc((8, 27), (29, 19)).segment((100, 19)).segment((100, -64)).segment((29, -64)).arc((0, -73), (-29, -64)).close().assemble().finalize()", -23)
