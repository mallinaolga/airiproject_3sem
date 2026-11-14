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
r=extrude(r, (0, 32, 0), 'ZX', "sketch().push([(-69, -26)]).circle(20).finalize()", -64)
r=extrude(r, (-26, 17, -69), 'ZX', "sketch().push([(-69, -26)]).circle(24).finalize()", -27, False)
r=extrude(r, (-1, -7, -69), 'ZX', "sketch().segment((-85, -9), (-80, 8)).arc((-85, 19), (-80, 31)).arc((-69, 35), (-58, 31)).arc((-53, 19), (-58, 8)).segment((-53, -9)).arc((-69, -1), (-85, -9)).assemble().finalize()", -13)
r=extrude(r, (35, -11, -69), 'YZ', "sketch().segment((-27, -80), (-7, -50)).segment((5, -58)).segment((-15, -88)).close().assemble().finalize()", 8)
r=extrude(r, (-26, 21, -49), 'ZX', "sketch().arc((-59, -42), (-49, -26), (-59, -10)).segment((94, -10)).segment((94, -42)).close().assemble().finalize()", -2)
r=extrude(r, (43, -2, -59), 'YZ', "sketch().push([(-2, -59)]).circle(29).finalize()", 7)
