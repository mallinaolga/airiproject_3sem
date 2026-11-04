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
r=extrude(r, (0, 0, -107), 'XY', "sketch().push([(-13.5, 5)]).rect(11, 28).finalize()", 189)
r=extrude(r, (-14, 5, 19), 'XY', "sketch().push([(-14, 5)]).rect(12, 32).finalize()", 52, False)
r=extrude(r, (-8, 11, 61), 'YZ', "sketch().push([(11, 61)]).circle(3).finalize()", 5)
r=extrude(r, (-9, 5, -51), 'YZ', "sketch().arc((-6, -48), (0, -48), (-3, -43)).arc((14, -56), (-6, -48)).assemble().finalize()", 15)
r=extrude(r, (-16, -11, 53), 'ZX', "sketch().push([(53, -16)]).circle(3).finalize()", -2)
r=extrude(r, (-8, -7, 59), 'XY', "sketch().segment((-8, -21), (-8, 7)).segment((-6, -4)).arc((-3, -3), (0, -4)).arc((1, -7), (0, -10)).arc((-3, -11), (-6, -10)).close().assemble().finalize()", -47)
r=extrude(r, (-8, -20, 50), 'ZX', "sketch().push([(50, 6)]).rect(114, 28).finalize()", -1)
