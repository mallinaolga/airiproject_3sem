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
r=extrude(r, (0, -101, 0), 'ZX', "sketch().push([(0, -9.5)]).rect(18, 21).finalize()", 202)
r=extrude(r, (-10, 13, 0), 'ZX', "sketch().push([(0, -10)]).rect(20, 22).finalize()", 87, False)
r=extrude(r, (2, 91, -4), 'YZ', "sketch().push([(91, -4)]).circle(4).finalize()", 19)
r=extrude(r, (2, 57, 9), 'YZ', "sketch().push([(57, 9)]).circle(1).finalize()", 6)
