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
r=extrude(r, (0, 0, -85), 'XY', "sketch().push([(-25, -35)]).circle(16).finalize()", 168)
r=extrude(r, (-25, -35, -16), 'XY', "sketch().push([(-25, -35)]).circle(18).finalize()", 19, False)
r=extrude(r, (-41, -35, -79), 'YZ', "sketch().segment((-41, -97), (-38, -60)).segment((-29, -61)).segment((-32, -98)).close().assemble().finalize()", -41)
r=extrude(r, (-43, -35, -5), 'YZ', "sketch().push([(-35, -5)]).rect(58, 26).finalize()", -61)
r=extrude(r, (-63, -6, -3), 'ZX', "sketch().segment((-7, -60), (-5, -60)).segment((-5, -59)).segment((1, -66)).segment((0, -67)).close().assemble().finalize()", 77)
r=extrude(r, (-28, -32, 82), 'XY', "sketch().push([(-28, -32)]).rect(16, 78).finalize()", 15)
r=extrude(r, (-9, -35, 25), 'YZ', "sketch().push([(-35, 25)]).circle(1).finalize()", 114)
