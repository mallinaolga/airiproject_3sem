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
r=extrude(r, (-109, 0, 0), 'YZ', "sketch().push([(0, 5.5)]).rect(26, 19).finalize()", 217)
r=extrude(r, (-4, 0, 6), 'YZ', "sketch().push([(0, 6)]).rect(40, 28).finalize()", 25, False)
r=extrude(r, (-76, 2, 15), 'ZX', "sketch().push([(-4.5, -76)]).rect(39, 16).finalize()", 13)
r=extrude(r, (63, -9, 15), 'XY', "sketch().push([(63, -9)]).rect(4, 6).finalize()", 10)
r=extrude(r, (-95, 8, 15), 'ZX', "sketch().push([(-1, -95)]).rect(32, 10).finalize()", -18)
r=extrude(r, (-68, 3, -25), 'YZ', "sketch().segment((-3, -25), (-1, -19)).arc((-3, -14), (-1, -10)).arc((3, -8), (7, -10)).arc((9, -14), (7, -19)).segment((9, -25)).close().assemble().finalize()", -11)
