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
r=extrude(r, (0, 0, 92), 'XY', "sketch().push([(14, -6)]).circle(26).finalize()", -117)
r=extrude(r, (14, -6, -20), 'XY', "sketch().push([(14, -6)]).circle(30).finalize()", -16, False)
r=extrude(r, (40, -6, 66), 'YZ', "sketch().push([(-6, 66)]).rect(48, 20).finalize()", 16)
r=extrude(r, (-16, -6, -21), 'YZ', "sketch().push([(-6, -21)]).circle(71).finalize()", -31)
r=extrude(r, (-20, 65, -21), 'YZ', "sketch().arc((61, -40), (65, -21), (61, -2)).segment((68, -17)).arc((72, -15), (76, -17)).arc((78, -21), (76, -25)).arc((72, -27), (68, -25)).close().assemble().finalize()", 69)
r=extrude(r, (-47, -17, -64), 'YZ', "sketch().segment((-25, -60), (-13, -56)).segment((-9, -68)).segment((-21, -72)).close().assemble().finalize()", -9)
