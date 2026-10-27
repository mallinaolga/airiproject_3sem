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
r=extrude(r, (0, -49, 0), 'ZX', "sketch().push([(-1, 30)]).circle(11).finalize()", 153)
r=extrude(r, (30, 15, -1), 'ZX', "sketch().push([(-1, 30)]).circle(14).finalize()", 18, False)
r=extrude(r, (19, -34, -1), 'ZX', "sketch().segment((-10, -58), (-10, 24)).arc((-1, 19), (8, 24)).segment((8, -58)).close().assemble().finalize()", -43)
r=extrude(r, (30, -40, -12), 'XY', "sketch().push([(30, -40)]).circle(1).finalize()", -56)
r=extrude(r, (-10, -36, 8), 'XY', "sketch().push([(-10, -36)]).rect(10, 4).finalize()", 54)
r=extrude(r, (0, -48, 8), 'XY', "sketch().segment((36, -58), (46, -75)).segment((52, -71)).arc((-54, -29), (55, -63)).segment((49, -51)).close().assemble().finalize()", 59)
