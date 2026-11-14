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
r=extrude(r, (0, -92, 0), 'ZX', "sketch().push([(-7.5, -12)]).rect(19, 4).finalize()", 111)
r=extrude(r, (-12, 8, -8), 'ZX', "sketch().push([(-8, -12)]).rect(20, 4).finalize()", 26, False)
r=extrude(r, (-10, -80, -1), 'YZ', "sketch().push([(-80, -1)]).circle(2).finalize()", 33)
r=extrude(r, (-14, -65, 2), 'YZ', "sketch().segment((-70, 2), (-68, 4)).arc((-69, 7), (-68, 9)).arc((-65, 10), (-62, 9)).arc((-61, 7), (-62, 4)).segment((-60, 2)).close().assemble().finalize()", 21)
r=extrude(r, (-10, -41, 2), 'XY', "sketch().push([(-10, -41)]).circle(1).finalize()", 24)
r=extrude(r, (-14, 25, -7), 'YZ', "sketch().push([(25, -7)]).circle(19).finalize()", -10)
r=extrude(r, (-10, 0, -14), 'XY', "sketch().segment((-10, -106), (-10, 106)).segment((-3, 9)).arc((6, 13), (16, 9)).arc((19, 0), (16, -9)).arc((6, -13), (-3, -9)).close().assemble().finalize()", -8)
