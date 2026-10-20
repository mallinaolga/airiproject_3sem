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
r=extrude(r, (0, -40, 0), 'ZX', "sketch().segment((-61, -83), (-61, -58)).segment((-22, -46)).segment((-25, -38)).segment((-61, -50)).segment((-61, -21)).segment((-37, -21)).arc((0, -4), (37, -21)).segment((61, -21)).segment((61, -83)).segment((37, -83)).arc((0, -100), (-37, -83)).close().assemble().finalize()", 87)
r=extrude(r, (-4, -27, 0), 'YZ', "sketch().segment((-47, -48), (-47, 48)).arc((-27, 47), (-7, 48)).segment((-7, -48)).close().assemble().finalize()", 104)
