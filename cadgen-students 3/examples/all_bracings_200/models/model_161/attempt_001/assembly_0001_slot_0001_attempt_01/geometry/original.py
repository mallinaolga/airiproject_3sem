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
r=extrude(r, (95, 0, 0), 'YZ', "sketch().push([(10, -5.5)]).rect(4, 21).finalize()", -190)
r=extrude(r, (18, 10, -6), 'YZ', "sketch().push([(10, -6)]).rect(8, 34).finalize()", -26, False)
r=extrude(r, (-84, 13, 2), 'YZ', "sketch().arc((-10, -6), (-13, 2), (-10, 10)).arc((-1, 14), (7, 10)).segment((13, 22)).segment((13, -18)).segment((7, -6)).arc((-1, -10), (-10, -6)).assemble().finalize()", 24)
r=extrude(r, (59, 8, -9), 'ZX', "sketch().push([(-9, 59)]).rect(20, 22).finalize()", -16)
