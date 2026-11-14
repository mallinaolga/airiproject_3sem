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
r=extrude(r, (0, 111, 0), 'ZX', "sketch().push([(-8, 0)]).rect(2, 20).finalize()", -202)
r=extrude(r, (0, -47, -8), 'ZX', "sketch().push([(-8, 0)]).rect(4, 30).finalize()", -64, False)
r=extrude(r, (8, 39, -9), 'YZ', "sketch().segment((-15, -9), (37, -8)).arc((36, -6), (37, -4)).arc((39, -3), (41, -4)).arc((42, -6), (41, -8)).segment((93, -9)).close().assemble().finalize()", 2)
r=extrude(r, (-2, -12, -7), 'XY', "sketch().push([(-2, -12)]).circle(10).finalize()", 11)
r=extrude(r, (2, -8, 3), 'XY', "sketch().push([(2, -8)]).rect(22, 10).finalize()", 7)
