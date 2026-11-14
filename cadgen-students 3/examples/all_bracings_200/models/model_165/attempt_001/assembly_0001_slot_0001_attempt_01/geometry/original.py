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
r=extrude(r, (91, 0, 0), 'YZ', "sketch().push([(-18, 0)]).circle(8).finalize()", -105)
r=extrude(r, (-10, -18, 0), 'YZ', "sketch().push([(-18, 0)]).circle(10).finalize()", -26, False)
r=extrude(r, (-16, -27, 0), 'ZX', "sketch().push([(0, -16)]).rect(192, 164).finalize()", -42)
r=extrude(r, (12, -27, -53), 'ZX', "sketch().push([(-53, 12)]).circle(18).finalize()", 6)
r=extrude(r, (-11, -18, -10), 'XY', "sketch().push([(-11, -18)]).rect(14, 18).finalize()", -17)
r=extrude(r, (69, -10, 0), 'YZ', "sketch().arc((-13, -5), (-10, 0), (-13, 5)).segment((71, 5)).segment((71, -5)).close().assemble().finalize()", 29)
