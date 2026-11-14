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
r=extrude(r, (0, 0, 68), 'XY', "sketch().push([(-3.5, 10)]).rect(27, 10).finalize()", -162)
r=extrude(r, (-4, 10, -45), 'XY', "sketch().push([(-4, 10)]).rect(34, 12).finalize()", -19, False)
r=extrude(r, (-15, 5, 57), 'ZX', "sketch().push([(57, -15)]).circle(9).finalize()", -15)
r=extrude(r, (-4, 15, 49), 'ZX', "sketch().segment((45, -13), (45, 5)).segment((53, -4)).close().assemble().finalize()", 5)
r=extrude(r, (-18, 5, 62), 'YZ', "sketch().push([(-8.5, 62)]).rect(27, 64).finalize()", -3)
r=extrude(r, (10, 14, 3), 'YZ', "sketch().arc((6, -2), (21, 9), (7, -3)).segment((7, -2)).close().assemble().finalize()", 14)
r=extrude(r, (0, 5, 50), 'ZX', "sketch().push([(50, 0)]).circle(6).finalize()", -22)
