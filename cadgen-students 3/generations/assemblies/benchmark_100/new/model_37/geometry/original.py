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
r=extrude(r, (0, 0, 78), 'XY', "sketch().push([(9, 7)]).rect(36, 30).finalize()", -195)
r=extrude(r, (9, 7, 5), 'XY', "sketch().push([(9, 7)]).rect(52, 44).finalize()", -36, False)
r=extrude(r, (22, 22, 18), 'XY', "sketch().segment((17, 22), (27, 22)).segment((25, 18)).arc((27, 15), (25, 11)).arc((22, 10), (19, 11)).arc((17, 15), (19, 18)).close().assemble().finalize()", 4)
r=extrude(r, (-17, -14, -13), 'YZ', "sketch().push([(-14, -13)]).circle(15).finalize()", -18)
r=extrude(r, (12, 17, 78), 'ZX', "sketch().segment((78, -20), (78, 44)).segment((87, 24)).arc((99, 29), (111, 24)).arc((116, 12), (111, 0)).arc((99, -5), (87, 0)).close().assemble().finalize()", -23)
r=extrude(r, (-36, -12, -15), 'YZ', "sketch().push([(-12, -15)]).rect(4, 12).finalize()", -9)
