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
r=extrude(r, (0, 62, 0), 'ZX', "sketch().push([(-22, -8)]).circle(40).finalize()", -163)
r=extrude(r, (-8, -7, -22), 'ZX', "sketch().push([(-22, -8)]).circle(63).finalize()", -23, False)
r=extrude(r, (22, 62, -3), 'ZX', "sketch().segment((-38, 18), (19, 49)).segment((32, 26)).segment((-25, -5)).close().assemble().finalize()", 39)
r=extrude(r, (55, -26, -22), 'YZ', "sketch().segment((-37, -25), (-37, -19)).segment((-30, -19)).arc((-26, -17), (-22, -19)).segment((-15, -19)).segment((-15, -25)).segment((-22, -25)).arc((-26, -27), (-30, -25)).close().assemble().finalize()", 16)
r=extrude(r, (-8, -23, 41), 'ZX', "sketch().arc((38, -24), (41, -8), (38, 8)).segment((85, 8)).segment((85, -24)).close().assemble().finalize()", 76)
