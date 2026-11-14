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
r=extrude(r, (0, -109, 0), 'ZX', "sketch().push([(-9, 3.5)]).rect(14, 25).finalize()", 219)
r=extrude(r, (4, 25, -9), 'ZX', "sketch().push([(-9, 4)]).rect(22, 40).finalize()", 30, False)
r=extrude(r, (17, -52, -9), 'YZ', "sketch().push([(-52, -9)]).circle(6).finalize()", 17)
r=extrude(r, (11, 75, -3), 'XY', "sketch().push([(11, 75)]).circle(4).finalize()", 32)
r=extrude(r, (-16, 32, -16), 'YZ', "sketch().push([(32, -16)]).circle(13).finalize()", -12)
r=extrude(r, (-25, 32, -2), 'YZ', "sketch().segment((26, -4), (28, 5)).arc((26, 9), (28, 14)).arc((32, 15), (36, 14)).arc((38, 9), (36, 5)).segment((38, -4)).arc((32, -2), (26, -4)).assemble().finalize()", -9)
