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
r=extrude(r, (0, 0, -24), 'XY', "sketch().push([(-1, 98)]).circle(8).finalize()", 39)
r=extrude(r, (-1, 98, -8), 'XY', "sketch().push([(-1, 98)]).circle(10).finalize()", 6, False)
r=extrude(r, (7, 98, -15), 'YZ', "sketch().segment((79, -21), (87, 1)).segment((87, -1)).segment((97, -1)).segment((97, 1)).segment((117, -6)).segment((108, -31)).close().assemble().finalize()", 86)
r=extrude(r, (41, 87, 0), 'YZ', "sketch().arc((-84, -63), (-110, 0), (-84, 63)).arc((-21, 89), (41, 63)).segment((87, 89)).segment((87, -89)).segment((41, -63)).arc((-21, -89), (-84, -63)).assemble().finalize()", 47)
r=extrude(r, (41, -78, -25), 'ZX', "sketch().segment((-29, 41), (-21, 41)).segment((-22, 35)).arc((-21, 32), (-22, 29)).arc((-25, 28), (-28, 29)).arc((-29, 32), (-28, 35)).close().assemble().finalize()", -29)
r=extrude(r, (41, -62, -7), 'YZ', "sketch().push([(-62, -7)]).rect(110, 120).finalize()", -134)
