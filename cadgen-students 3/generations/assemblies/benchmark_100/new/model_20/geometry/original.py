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
r=extrude(r, (4, 0, 0), 'YZ', "sketch().push([(-10, -36)]).circle(10).finalize()", 82)
r=extrude(r, (19, -10, -36), 'YZ', "sketch().push([(-10, -36)]).circle(14).finalize()", 8, False)
r=extrude(r, (63, 0, -36), 'ZX', "sketch().push([(-36, 63)]).circle(1).finalize()", 93)
r=extrude(r, (86, -6, -36), 'YZ', "sketch().segment((-9, -33), (-4, -32)).segment((-3, -39)).segment((-8, -40)).close().assemble().finalize()", 9)
r=extrude(r, (15, -10, -26), 'XY', "sketch().push([(15, -10)]).circle(29).finalize()", 38)
r=extrude(r, (0, 0, 13), 'XY', "sketch().push([(0, 0)]).circle(115).finalize()", 37)
r=extrude(r, (24, 4, -36), 'ZX', "sketch().push([(-36, 24)]).rect(4, 28).finalize()", 17)
