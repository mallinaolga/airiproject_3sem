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
r=extrude(r, (0, 0, 75), 'XY', "sketch().push([(-10.5, 6)]).rect(65, 4).finalize()", -178)
r=extrude(r, (-11, 6, -95), 'XY', "sketch().push([(-11, 6)]).rect(104, 8).finalize()", -18, False)
r=extrude(r, (4, 4, -4), 'YZ', "sketch().push([(20.5, -4)]).rect(33, 34).finalize()", 24)
r=extrude(r, (21, 4, -17), 'ZX', "sketch().segment((-32, 18), (-32, 24)).segment((-22, 24)).arc((-17, 27), (-12, 24)).segment((-2, 24)).segment((-2, 18)).segment((-12, 18)).arc((-17, 15), (-22, 18)).close().assemble().finalize()", -41)
r=extrude(r, (26, 13, 13), 'ZX', "sketch().push([(63.5, 26)]).rect(101, 26).finalize()", 24)
r=extrude(r, (4, 19, -8), 'YZ', "sketch().push([(19, -8)]).circle(2).finalize()", -62)
r=extrude(r, (3, 4, -6), 'ZX', "sketch().segment((-13, -3), (-13, 9)).segment((-11, 9)).segment((-11, 13)).segment((-1, 13)).segment((-1, 9)).segment((1, 9)).segment((1, -3)).segment((-1, -3)).segment((-1, -7)).segment((-11, -7)).segment((-11, -3)).close().assemble().finalize()", -21)
r=extrude(r, (40, 24, 85), 'YZ', "sketch().push([(24, 85)]).rect(12, 16).finalize()", 24)
