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
r=extrude(r, (0, -22, 0), 'ZX', "sketch().push([(-35, 15)]).circle(23).finalize()", 91)
r=extrude(r, (15, 64, -35), 'ZX', "sketch().push([(-35, 15)]).circle(24).finalize()", 11, False)
r=extrude(r, (37, -18, -35), 'YZ', "sketch().push([(-18, -35)]).circle(35).finalize()", 42)
r=extrude(r, (15, 15, -13), 'XY', "sketch().segment((4, -5), (14, 38)).segment((26, 35)).segment((16, -8)).close().assemble().finalize()", 7)
r=extrude(r, (-8, 3, -35), 'ZX', "sketch().segment((-51, -95), (-51, 0)).arc((-35, -8), (-19, 0)).segment((-19, -95)).close().assemble().finalize()", 23)
r=extrude(r, (7, -22, -49), 'ZX', "sketch().push([(-49, 7)]).circle(5).finalize()", -53)
r=extrude(r, (80, -17, -66), 'YZ', "sketch().segment((-19, -65), (-16, -64)).segment((-15, -67)).segment((-18, -68)).close().assemble().push([(-17, -66)]).circle(1, mode='s').finalize()", 15)
r=extrude(r, (15, 66, -11), 'ZX', "sketch().arc((-18, -1), (-11, 15), (-18, 31)).segment((71, 31)).segment((71, -1)).close().assemble().finalize()", 5)
