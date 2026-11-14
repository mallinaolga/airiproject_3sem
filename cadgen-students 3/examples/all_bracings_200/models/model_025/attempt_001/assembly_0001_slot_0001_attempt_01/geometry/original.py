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
r=extrude(r, (0, 0, -101), 'XY', "sketch().push([(25, 4)]).rect(36, 52).finalize()", 203)
r=extrude(r, (25, 4, -99), 'XY', "sketch().push([(25, 4)]).rect(58, 84).finalize()", 68, False)
r=extrude(r, (5, -38, -32), 'YZ', "sketch().push([(6.5, -32)]).rect(89, 10).finalize()", -59)
r=extrude(r, (35, -38, -43), 'ZX', "sketch().push([(-43, 35)]).circle(3).finalize()", -13)
r=extrude(r, (-27, 34, -27), 'XY', "sketch().segment((-42, 40), (-32, 50)).segment((-26, 43)).segment((-34, 43)).segment((-34, 38)).segment((-21, 38)).segment((-12, 28)).segment((-22, 18)).close().assemble().finalize()", 2)
r=extrude(r, (-44, 23, -27), 'XY', "sketch().segment((-45, 23), (-44, 24)).segment((-43, 23)).segment((-44, 22)).close().assemble().finalize()", 5)
