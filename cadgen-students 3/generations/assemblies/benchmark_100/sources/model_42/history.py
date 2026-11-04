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
r=extrude(r, (81, 0, 0), 'YZ', "sketch().push([(0, -3)]).circle(28).finalize()", -179)
r=extrude(r, (26, 0, -3), 'YZ', "sketch().push([(0, -3)]).circle(34).finalize()", -41, False)
r=extrude(r, (77, 0, 26), 'XY', "sketch().push([(77, 0)]).rect(24, 150).finalize()", 11)
r=extrude(r, (78, 71, 37), 'XY', "sketch().push([(78, 71)]).rect(2, 4).finalize()", 21)
r=extrude(r, (5, 0, -38), 'XY', "sketch().push([(5, 0)]).circle(84).finalize()", -21)
r=extrude(r, (81, 6, 15), 'YZ', "sketch().segment((5, 16), (6, 16)).segment((7, 14)).segment((6, 14)).close().assemble().finalize()", 18)
