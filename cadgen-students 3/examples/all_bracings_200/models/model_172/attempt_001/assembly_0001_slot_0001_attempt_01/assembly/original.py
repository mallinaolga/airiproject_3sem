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
r=extrude(r, (18, 0, 0), 'YZ', "sketch().push([(42, 15)]).circle(20).finalize()", -76)
r=extrude(r, (-25, 42, 15), 'YZ', "sketch().push([(42, 15)]).circle(35).finalize()", -19, False)
r=extrude(r, (-58, 24, 9), 'YZ', "sketch().push([(24, 9)]).circle(39).finalize()", -43)
r=extrude(r, (18, 43, 12), 'YZ', "sketch().push([(43, 12)]).circle(7).finalize()", 41)
r=extrude(r, (-16, 42, -5), 'YZ', "sketch().segment((25, -50), (25, 5)).arc((42, -5), (59, 5)).segment((59, -50)).close().assemble().finalize()", 117)
r=extrude(r, (-12, 25, -22), 'ZX', "sketch().push([(-22, -12)]).circle(2).finalize()", -102)
