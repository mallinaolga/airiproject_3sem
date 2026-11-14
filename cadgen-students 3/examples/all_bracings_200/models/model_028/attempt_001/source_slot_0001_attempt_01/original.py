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
r=extrude(r, (0, 0, -110), 'XY', "sketch().push([(-4, 13)]).circle(12).finalize()", 184)
r=extrude(r, (-4, 13, 40), 'XY', "sketch().push([(-4, 13)]).circle(15).finalize()", 70, False)
r=extrude(r, (12, 13, 44), 'YZ', "sketch().segment((7, 44), (11, 49)).segment((19, 44)).segment((15, 39)).close().assemble().finalize()", 7)
r=extrude(r, (-4, 1, -15), 'XY', "sketch().arc((-14, 7), (-4, 1), (6, 7)).segment((3, -5)).arc((6, -12), (3, -20)).arc((-4, -23), (-11, -20)).arc((-14, -12), (-11, -5)).close().assemble().finalize()", -18)
r=extrude(r, (-5, -15, -33), 'XY', "sketch().push([(-5, -15)]).rect(28, 26).push([(-5, -15)]).circle(1, mode='s').finalize()", -27)
