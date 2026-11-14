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
r=extrude(r, (0, -109, 0), 'ZX', "sketch().push([(-3.5, -17.5)]).rect(39, 19).finalize()", 218)
r=extrude(r, (-17, -17, -4), 'ZX', "sketch().push([(-4, -17)]).rect(66, 32).finalize()", 22, False)
r=extrude(r, (-2, -13, -7), 'YZ', "sketch().push([(-13, -7)]).rect(2, 2).finalize()", 2)
r=extrude(r, (-10, 98, -23), 'ZX', "sketch().push([(7, -10)]).rect(60, 56).finalize()", -12)
r=extrude(r, (-13, 34, 16), 'XY', "sketch().push([(-13, 34)]).rect(2, 2).finalize()", 20)
r=extrude(r, (-8, 34, 9), 'YZ', "sketch().segment((28, 11), (33, 15)).segment((40, 7)).segment((35, 3)).close().assemble().finalize()", 46)
r=extrude(r, (-8, 60, 6), 'YZ', "sketch().push([(60, 6)]).circle(18).finalize()", 9)
r=extrude(r, (-17, -16, 30), 'XY', "sketch().segment((-38, -14), (-10, 4)).segment((4, -18)).segment((-24, -36)).close().assemble().finalize()", 1)
