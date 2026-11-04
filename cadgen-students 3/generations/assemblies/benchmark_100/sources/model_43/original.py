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
r=extrude(r, (0, -91, 0), 'ZX', "sketch().push([(0, 3.5)]).rect(22, 3).finalize()", 181)
r=extrude(r, (3, 53, 0), 'ZX', "sketch().push([(0, 3)]).rect(36, 6).finalize()", 22, False)
r=extrude(r, (1, -18, -3), 'YZ', "sketch().push([(-18, -3)]).rect(4, 6).finalize()", -11)
r=extrude(r, (1, -51, 6), 'YZ', "sketch().push([(-51, 6)]).circle(4).finalize()", -2)
r=extrude(r, (6, 66, 6), 'YZ', "sketch().push([(66, 6)]).rect(10, 10).finalize()", 4)
