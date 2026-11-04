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
r=extrude(r, (0, 0, -60), 'XY', "sketch().push([(-1.5, -2)]).rect(7, 2).finalize()", 52)
r=extrude(r, (-2, -2, -12), 'XY', "sketch().push([(-2, -2)]).rect(10, 2).finalize()", 7, False)
r=extrude(r, (2, -3, -6), 'YZ', "sketch().push([(4.5, -6)]).rect(15, 190).finalize()", 13)
r=extrude(r, (2, 5, -101), 'YZ', "sketch().segment((-6, -101), (-2, -90)).arc((-6, -83), (-2, -75)).arc((5, -72), (12, -75)).arc((16, -83), (12, -90)).segment((16, -101)).close().assemble().finalize()", 17)
r=extrude(r, (2, 8, 83), 'YZ', "sketch().push([(8, 83)]).circle(26).finalize()", -20)
r=extrude(r, (2, -3, -78), 'YZ', "sketch().push([(-3, -78)]).circle(31).finalize()", -20)
