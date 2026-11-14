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
r=extrude(r, (0, -109, 0), 'ZX', "sketch().push([(-11.5, -1)]).rect(55, 20).finalize()", 217)
r=extrude(r, (-1, 43, -11), 'ZX', "sketch().push([(-11, -1)]).rect(82, 30).finalize()", 32, False)
r=extrude(r, (3, -61, 16), 'XY', "sketch().push([(3, -61)]).rect(6, 2).finalize()", 39)
r=extrude(r, (-16, 70, 10), 'YZ', "sketch().push([(70, 10)]).rect(2, 2).finalize()", -17)
r=extrude(r, (-11, -49, -34), 'XY', "sketch().segment((-11, -89), (-11, -9)).segment((-1, -35)).arc((13, -29), (27, -35)).arc((33, -49), (27, -63)).arc((13, -69), (-1, -63)).close().assemble().finalize()", -20)
r=extrude(r, (9, -59, -11), 'YZ', "sketch().push([(-59, -11)]).circle(1).finalize()", 4)
