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
r=extrude(r, (-93, 0, 0), 'YZ', "sketch().push([(11.5, 38)]).rect(45, 22).finalize()", 136)
r=extrude(r, (-82, 11, 38), 'YZ', "sketch().push([(11, 38)]).rect(66, 32).finalize()", 49, False)
r=extrude(r, (-88, 18, 49), 'YZ', "sketch().push([(18, -2.5)]).rect(2, 103).finalize()", 22)
r=extrude(r, (40, 0, 27), 'XY', "sketch().push([(40, 0)]).circle(53).finalize()", -44)
r=extrude(r, (-13, 0, -5), 'YZ', "sketch().segment((-12, 7), (-3, 12)).segment((12, -17)).segment((3, -22)).close().assemble().finalize()", -25)
