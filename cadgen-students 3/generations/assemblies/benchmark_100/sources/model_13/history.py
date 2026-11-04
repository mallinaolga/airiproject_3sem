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
r=extrude(r, (0, 0, -107), 'XY', "sketch().push([(0, 21)]).circle(9).finalize()", 162)
r=extrude(r, (0, 21, 11), 'XY', "sketch().push([(0, 21)]).circle(13).finalize()", 19, False)
r=extrude(r, (0, 13, -77), 'ZX', "sketch().segment((-85, -2), (-85, 2)).segment((-83, 2)).segment((-83, 3)).segment((-73, 3)).segment((-73, 2)).segment((-69, 2)).segment((-69, -2)).segment((-73, -2)).segment((-73, -3)).segment((-83, -3)).segment((-83, -2)).close().assemble().finalize()", -19)
r=extrude(r, (0, 13, 49), 'ZX', "sketch().segment((-9, -24), (46, 63)).segment((107, 24)).segment((52, -63)).close().assemble().finalize()", -26)
r=extrude(r, (1, -6, -76), 'ZX', "sketch().push([(-76, 1)]).rect(54, 54).finalize()", -28)
