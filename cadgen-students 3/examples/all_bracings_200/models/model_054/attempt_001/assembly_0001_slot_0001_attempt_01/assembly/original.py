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
r=extrude(r, (0, -5, 0), 'ZX', "sketch().push([(0, -1)]).circle(2).finalize()", 13)
r=extrude(r, (-1, 0, 0), 'ZX', "sketch().push([(0, -1)]).circle(3).finalize()", 2, False)
r=extrude(r, (-3, -2, 0), 'YZ', "sketch().push([(-2, 0)]).circle(48).finalize()", -45)
r=extrude(r, (-3, -31, -21), 'ZX', "sketch().segment((-31, -3), (-31, 4)).segment((-31, 44)).segment((-11, 44)).segment((-11, 4)).segment((-11, -3)).close().assemble().push([(-21, 24)]).circle(9, mode='s').finalize()", -13)
r=extrude(r, (24, -37, -30), 'ZX', "sketch().arc((-47, 19), (-49, 24), (-47, 29)).arc((-42, 31), (-37, 29)).segment((-25, 31)).arc((-30, 24), (-25, 17)).segment((-37, 19)).arc((-42, 17), (-47, 19)).assemble().finalize()", 62)
r=extrude(r, (-48, -22, -31), 'YZ', "sketch().push([(-22, -31)]).rect(2, 6).finalize()", -47)
r=extrude(r, (44, -35, -25), 'YZ', "sketch().push([(-35, -25)]).circle(1).finalize()", 50)
r=extrude(r, (-7, 46, 0), 'ZX', "sketch().segment((-51, 10), (25, 41)).segment((51, -24)).segment((-25, -55)).close().assemble().finalize()", 4)
