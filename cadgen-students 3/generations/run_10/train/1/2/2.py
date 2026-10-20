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
r=extrude(r, (0, 0, -100), 'XY', "sketch().segment((-44, 81), (3, 92)).segment((44, -81)).segment((-3, -92)).segment((-14, -46)).segment((-8, -46)).segment((-8, -19)).arc((-4, -8), (-8, 3)).segment((-8, 29)).segment((-32, 29)).close().assemble().finalize()", 200)
