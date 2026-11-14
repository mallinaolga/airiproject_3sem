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
r=extrude(r, (-91, 0, 0), 'YZ', "sketch().push([(-14, -11)]).circle(36).finalize()", 183)
r=extrude(r, (4, -14, -11), 'YZ', "sketch().push([(-14, -11)]).circle(63).finalize()", 21, False)
r=extrude(r, (9, -76, -11), 'ZX', "sketch().segment((-17, -8), (-17, 16)).segment((-11, 16)).segment((-11, 26)).segment((-9, 26)).segment((-9, 16)).segment((-5, 16)).segment((-5, -8)).close().assemble().finalize()", -19)
r=extrude(r, (18, 47, -11), 'ZX', "sketch().push([(-11, 18)]).circle(5).finalize()", 48)
r=extrude(r, (15, -14, 52), 'XY', "sketch().push([(15, -14)]).rect(2, 2).finalize()", 21)
r=extrude(r, (18, 72, -16), 'XY', "sketch().push([(18, 72)]).rect(2, 4).finalize()", -19)
