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
r=extrude(r, (0, -11, 0), 'ZX', "sketch().arc((-54, -84), (-100, 0), (-54, 84)).segment((-54, 66)).segment((54, 66)).segment((54, 84)).arc((100, 0), (54, -84)).segment((54, -66)).segment((-54, -66)).close().assemble().finalize()", 23)
