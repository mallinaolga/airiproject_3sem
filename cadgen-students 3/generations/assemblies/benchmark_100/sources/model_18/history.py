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
r=extrude(r, (0, -108, 0), 'ZX', "sketch().push([(-11, -2)]).rect(14, 26).finalize()", 215)
r=extrude(r, (-2, -102, -11), 'ZX', "sketch().push([(-11, -2)]).rect(20, 36).finalize()", 35, False)
r=extrude(r, (-15, -11, -17), 'YZ', "sketch().push([(-11, -17)]).circle(1).finalize()", -18)
r=extrude(r, (4, 82, -4), 'XY', "sketch().segment((1, 76), (1, 88)).arc((4, 87), (7, 88)).segment((7, 76)).close().assemble().finalize()", 40)
r=extrude(r, (11, -86, -21), 'XY', "sketch().push([(11, -86)]).rect(2, 4).finalize()", -23)
r=extrude(r, (16, -71, -19), 'YZ', "sketch().push([(-71, -19)]).circle(2).finalize()", 15)
r=extrude(r, (5, 81, 37), 'XY', "sketch().push([(5, 81)]).rect(56, 26).finalize()", 8)
