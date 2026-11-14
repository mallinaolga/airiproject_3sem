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
r=extrude(r, (0, 0, 98), 'XY', "sketch().push([(0, -22)]).circle(24).finalize()", -174)
r=extrude(r, (0, -22, 86), 'XY', "sketch().push([(0, -22)]).circle(36).finalize()", -46, False)
r=extrude(r, (-24, -22, -72), 'YZ', "sketch().segment((-49, -65), (-13, -46)).segment((5, -79)).segment((-31, -98)).close().assemble().finalize()", -12)
r=extrude(r, (0, 2, -19), 'ZX', "sketch().segment((-23, 6), (-22, 6)).segment((-22, 10)).segment((-16, 10)).segment((-16, -1)).segment((-15, -6)).segment((-16, -6)).segment((-16, -10)).segment((-22, -10)).segment((-22, 1)).close().assemble().finalize()", 55)
r=extrude(r, (29, -33, 40), 'XY', "sketch().segment((26, -38), (26, -37)).arc((30, -34), (26, -31)).segment((26, -28)).segment((32, -28)).segment((32, -38)).close().assemble().finalize()", -11)
r=extrude(r, (-30, -39, 40), 'XY', "sketch().segment((-34, -43), (-34, -37)).segment((-32, -37)).arc((-26, -37), (-31, -41)).segment((-31, -43)).close().assemble().finalize()", -19)
