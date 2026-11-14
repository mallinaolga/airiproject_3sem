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
r=extrude(r, (0, 0, 113), 'XY', "sketch().push([(-8, 0.5)]).rect(22, 7).finalize()", -221)
r=extrude(r, (-8, 1, -45), 'XY', "sketch().push([(-8, 1)]).rect(26, 8).finalize()", -68, False)
r=extrude(r, (-4, -3, 37), 'ZX', "sketch().push([(37, -4)]).circle(9).finalize()", -5)
r=extrude(r, (-12, 4, -111), 'ZX', "sketch().segment((-113, -14), (-112, -10)).segment((-109, -10)).segment((-110, -14)).close().assemble().finalize()", 3)
r=extrude(r, (-18, 4, -46), 'ZX', "sketch().push([(-46, -18)]).circle(1).finalize()", 3)
r=extrude(r, (4, 4, 3), 'ZX', "sketch().segment((-12, -2), (4, 20)).segment((18, 10)).segment((2, -12)).close().assemble().finalize()", 1)
