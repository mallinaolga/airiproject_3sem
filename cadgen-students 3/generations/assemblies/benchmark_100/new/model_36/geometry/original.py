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
r=extrude(r, (0, 0, -90), 'XY', "sketch().push([(5, -3)]).rect(20, 16).finalize()", 180)
r=extrude(r, (5, -4, -81), 'XY', "sketch().push([(5, -4)]).rect(30, 22).finalize()", 42, False)
r=extrude(r, (-10, -2, -40), 'XY', "sketch().segment((-10, -19), (-10, 15)).segment((0, 10)).arc((12, 15), (24, 10)).arc((29, -2), (24, -14)).arc((12, -19), (0, -14)).close().assemble().finalize()", -30)
r=extrude(r, (0, 5, 37), 'ZX', "sketch().push([(37, 0)]).rect(88, 72).finalize()", 14)
r=extrude(r, (9, 8, -6), 'XY', "sketch().push([(9, 8)]).circle(2).finalize()", -13)
