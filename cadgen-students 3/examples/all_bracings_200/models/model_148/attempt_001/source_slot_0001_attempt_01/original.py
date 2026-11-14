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
r=extrude(r, (0, 0, 82), 'XY', "sketch().push([(36, 37)]).circle(45).finalize()", -163)
r=extrude(r, (36, 37, -22), 'XY', "sketch().push([(36, 37)]).circle(65).finalize()", -36, False)
r=extrude(r, (36, -8, 79), 'XY', "sketch().segment((7, -112), (7, 4)).arc((36, -8), (65, 4)).segment((65, -112)).close().assemble().finalize()", -24)
r=extrude(r, (-29, 37, -40), 'YZ', "sketch().push([(37, -40)]).rect(4, 4).finalize()", -70)
r=extrude(r, (36, 81, 69), 'ZX', "sketch().push([(69, 36)]).circle(1).finalize()", 31)
r=extrude(r, (-63, 35, -41), 'ZX', "sketch().push([(-41, -63)]).circle(39).finalize()", -140)
