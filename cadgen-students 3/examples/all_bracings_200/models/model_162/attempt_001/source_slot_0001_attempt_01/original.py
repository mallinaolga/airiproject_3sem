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
r=extrude(r, (0, 110, 0), 'ZX', "sketch().push([(2, -7)]).circle(11).finalize()", -219)
r=extrude(r, (-7, 16, 2), 'ZX', "sketch().push([(2, -7)]).circle(13).finalize()", -23, False)
r=extrude(r, (-7, 14, -11), 'XY', "sketch().push([(-7, 14)]).circle(4).finalize()", -4)
r=extrude(r, (5, -45, 2), 'ZX', "sketch().segment((-4, 3), (-2, 10)).arc((-4, 14), (-2, 18)).arc((2, 20), (6, 18)).arc((8, 14), (6, 10)).segment((8, 3)).arc((2, 5), (-4, 3)).assemble().finalize()", 14)
