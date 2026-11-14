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
r=extrude(r, (87, 0, 0), 'YZ', "sketch().push([(13, 9)]).circle(11).finalize()", -191)
r=extrude(r, (38, 13, 9), 'YZ', "sketch().push([(13, 9)]).circle(12).finalize()", -20, False)
r=extrude(r, (54, 3, 9), 'ZX', "sketch().push([(9, 54)]).rect(12, 14).finalize()", -28)
r=extrude(r, (87, 14, 8), 'YZ', "sketch().segment((9, 6), (18, 11)).segment((19, 10)).segment((10, 5)).close().assemble().finalize()", 19)
r=extrude(r, (50, -13, 2), 'XY', "sketch().push([(50, -13)]).circle(13).finalize()", -8)
r=extrude(r, (-102, 13, -2), 'XY', "sketch().push([(-102, 13)]).circle(4).finalize()", -19)
