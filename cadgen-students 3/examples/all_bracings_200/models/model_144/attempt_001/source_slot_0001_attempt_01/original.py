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
r=extrude(r, (-46, 0, 0), 'YZ', "sketch().push([(0, 11)]).circle(15).finalize()", 131)
r=extrude(r, (-45, 0, 11), 'YZ', "sketch().push([(0, 11)]).circle(24).finalize()", 40, False)
r=extrude(r, (-30, 0, -13), 'XY', "sketch().segment((-117, -26), (-15, 90)).segment((57, 26)).segment((-45, -90)).close().assemble().finalize()", -48)
r=extrude(r, (77, -15, 11), 'ZX', "sketch().push([(11, 77)]).circle(30).finalize()", -42)
r=extrude(r, (77, -47, 41), 'XY', "sketch().push([(77, -47)]).circle(40).finalize()", 48)
r=extrude(r, (1, 33, -60), 'XY', "sketch().segment((-9, 23), (-9, 43)).segment((11, 43)).segment((11, 23)).arc((5, 25), (-1, 23)).close().assemble().finalize()", -28)
