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
r=extrude(r, (0, 92, 0), 'ZX', "sketch().push([(-2, 0)]).circle(10).finalize()", -185)
r=extrude(r, (0, -6, -2), 'ZX', "sketch().push([(-2, 0)]).circle(12).finalize()", -39, False)
r=extrude(r, (0, 66, 8), 'XY', "sketch().push([(0, 66)]).circle(9).finalize()", 5)
r=extrude(r, (0, -39, 10), 'XY', "sketch().segment((-18, -46), (-12, -24)).segment((18, -32)).segment((12, -54)).close().assemble().finalize()", 2)
