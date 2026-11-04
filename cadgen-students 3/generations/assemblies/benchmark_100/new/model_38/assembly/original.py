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
r=extrude(r, (0, 0, 103), 'XY', "sketch().push([(-3.5, 0)]).rect(19, 50).finalize()", -201)
r=extrude(r, (-3, 0, -85), 'XY', "sketch().push([(-3, 0)]).rect(30, 82).finalize()", -21, False)
r=extrude(r, (12, -9, -103), 'YZ', "sketch().push([(-9, -103)]).circle(1).finalize()", 18)
r=extrude(r, (-13, -17, 65), 'YZ', "sketch().push([(-17, 65)]).circle(15).finalize()", -15)
r=extrude(r, (-13, -9, 96), 'YZ', "sketch().arc((-18, 96), (-14, 99), (-13, 104)).segment((0, 96)).segment((-5, 88)).close().assemble().finalize()", -17)
