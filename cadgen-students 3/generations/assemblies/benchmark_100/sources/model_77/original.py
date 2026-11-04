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
r=extrude(r, (-119, 0, 0), 'YZ', "sketch().push([(25, 18)]).circle(23).finalize()", 238)
r=extrude(r, (70, 25, 18), 'YZ', "sketch().push([(25, 18)]).circle(34).finalize()", 32, False)
r=extrude(r, (87, -10, 18), 'YZ', "sketch().segment((-21, -9), (-21, 45)).segment((5, 45)).arc((-10, 18), (5, -9)).close().assemble().finalize()", -162)
r=extrude(r, (-57, 25, -5), 'YZ', "sketch().arc((6, 6), (25, -5), (44, 6)).segment((38, -21)).arc((44, -35), (38, -48)).arc((25, -54), (12, -48)).arc((6, -35), (12, -21)).close().assemble().finalize()", 35)
r=extrude(r, (-22, 24, -22), 'YZ', "sketch().push([(24, -22)]).rect(22, 14).finalize()", 33)
r=extrude(r, (-15, -20, 40), 'ZX', "sketch().segment((37, -16), (39, -13)).segment((43, -14)).segment((41, -17)).close().assemble().finalize()", -39)
