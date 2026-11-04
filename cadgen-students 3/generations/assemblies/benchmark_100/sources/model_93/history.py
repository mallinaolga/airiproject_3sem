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
r=extrude(r, (96, 0, 0), 'YZ', "sketch().push([(-15, 6.5)]).rect(6, 19).finalize()", -171)
r=extrude(r, (-67, -15, 6), 'YZ', "sketch().push([(-15, 6)]).rect(10, 30).finalize()", -29, False)
r=extrude(r, (17, -12, 11), 'ZX', "sketch().push([(11, 17)]).circle(3).finalize()", 38)
r=extrude(r, (-4, -18, 0), 'ZX', "sketch().push([(0, -4)]).circle(21).finalize()", -3)
r=extrude(r, (11, -21, -11), 'ZX', "sketch().push([(-11, 11)]).circle(6).finalize()", -5)
