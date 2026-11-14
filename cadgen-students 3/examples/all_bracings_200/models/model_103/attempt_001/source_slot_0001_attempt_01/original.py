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
r=extrude(r, (-117, 0, 0), 'YZ', "sketch().push([(0.5, -1)]).rect(25, 18).finalize()", 235)
r=extrude(r, (66, 0, -1), 'YZ', "sketch().push([(0, -1)]).rect(28, 20).finalize()", 31, False)
r=extrude(r, (-113, -12, 0), 'YZ', "sketch().segment((-12, -18), (-12, 18)).segment((-7, 8)).arc((1, 11), (9, 8)).arc((12, 0), (9, -8)).arc((1, -11), (-7, -8)).close().assemble().finalize()", 2)
r=extrude(r, (-36, -6, 8), 'YZ', "sketch().push([(-6, 1)]).rect(22, 14).finalize()", -71)
r=extrude(r, (-83, 13, -3), 'ZX', "sketch().push([(-3, -83)]).circle(7).finalize()", 4)
