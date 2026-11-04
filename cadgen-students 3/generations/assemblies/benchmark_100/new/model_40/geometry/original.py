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
r=extrude(r, (99, 0, 0), 'YZ', "sketch().push([(-11.5, 9.5)]).rect(23, 17).finalize()", -164)
r=extrude(r, (-41, -12, 10), 'YZ', "sketch().push([(-12, 10)]).rect(28, 22).finalize()", -59, False)
r=extrude(r, (-65, -13, 21), 'YZ', "sketch().segment((-22, 21), (-4, 21)).segment((-7, 16)).arc((-4, 10), (-7, 4)).arc((-13, 1), (-19, 4)).arc((-22, 10), (-19, 16)).close().assemble().finalize()", 35)
r=extrude(r, (-72, 2, 5), 'ZX', "sketch().push([(5, -72)]).circle(14).finalize()", 14)
r=extrude(r, (-47, -21, 21), 'XY', "sketch().segment((-49, -22), (-47, -20)).segment((-47, -19)).segment((-45, -19)).segment((-45, -21)).segment((-47, -21)).segment((-48, -23)).close().assemble().finalize()", 7)
r=extrude(r, (-61, 16, -1), 'ZX', "sketch().push([(-1, -61)]).circle(27).push([(4, -54)]).circle(15, mode='s').finalize()", 10)
