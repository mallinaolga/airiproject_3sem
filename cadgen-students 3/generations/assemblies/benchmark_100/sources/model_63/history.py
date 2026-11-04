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
r=extrude(r, (0, -106, 0), 'ZX', "sketch().push([(2, 6)]).rect(46, 12).finalize()", 212)
r=extrude(r, (6, -38, 2), 'ZX', "sketch().push([(2, 6)]).rect(68, 18).finalize()", 38, False)
r=extrude(r, (-3, -37, -6), 'YZ', "sketch().segment((-70, -26), (-13, 24)).segment((-4, 14)).segment((-61, -36)).close().assemble().finalize()", -13)
r=extrude(r, (0, -87, 11), 'XY', "sketch().segment((0, -97), (0, -77)).segment((1, -86)).segment((10, -86)).segment((10, -88)).segment((1, -88)).close().assemble().finalize()", 25)
r=extrude(r, (0, 76, -16), 'YZ', "sketch().push([(76, -16)]).rect(4, 4).finalize()", -13)
r=extrude(r, (0, -84, 30), 'YZ', "sketch().push([(-84, 30)]).circle(2).finalize()", -14)
r=extrude(r, (8, -38, -27), 'ZX', "sketch().push([(-27, 8)]).circle(1).finalize()", -35)
