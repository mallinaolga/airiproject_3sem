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
r=extrude(r, (0, -89, 0), 'ZX', "sketch().push([(3.5, 1)]).rect(23, 12).finalize()", 182)
r=extrude(r, (1, -26, 3), 'ZX', "sketch().push([(3, 1)]).rect(38, 22).finalize()", 19, False)
r=extrude(r, (-2, -25, -16), 'XY', "sketch().segment((-3, -25), (-2, -24)).segment((-1, -25)).segment((-2, -26)).close().assemble().finalize()", -7)
r=extrude(r, (7, -37, 12), 'YZ', "sketch().push([(-37, 12)]).rect(16, 4).finalize()", 9)
r=extrude(r, (0, -89, 4), 'ZX', "sketch().push([(4, 0)]).circle(3).finalize()", -4)
r=extrude(r, (-5, 28, -6), 'YZ', "sketch().segment((27, -7), (27, -6)).segment((29, -5)).segment((29, -6)).close().assemble().finalize()", -11)
