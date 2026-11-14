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
r=extrude(r, (0, 71, 0), 'ZX', "sketch().push([(0.5, 3.5)]).rect(37, 47).finalize()", -172)
r=extrude(r, (4, 50, 0), 'ZX', "sketch().push([(0, 4)]).rect(58, 74).finalize()", -77, False)
r=extrude(r, (9, -8, 30), 'XY', "sketch().arc((4, -20), (5, 3), (19, -15)).arc((11, -16), (4, -20)).assemble().finalize()", 2)
r=extrude(r, (-33, 4, 10), 'YZ', "sketch().segment((-26, 26), (26, 35)).segment((34, -6)).segment((-18, -15)).close().assemble().finalize()", -17)
r=extrude(r, (8, 71, -11), 'ZX', "sketch().push([(-11, 8)]).rect(48, 84).finalize()", 30)
